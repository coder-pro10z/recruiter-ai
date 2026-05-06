"""
Follow-up Engine — schedules and sends follow-up messages based on application timeline.
"""
import logging
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.application import Application
from models.job import Job
from models.outreach import OutreachMessage
from agents.apply_engine import ApplyEngine
from agents.telegram_agent import TelegramAgent

logger = logging.getLogger(__name__)

FOLLOWUP_SCHEDULE_DAYS = [3, 7, 14]

FOLLOWUP_TEMPLATE = """\
Hi {recruiter_name},

I wanted to follow up on my application for the {job_title} position at {company}.

I'm still very interested in the role and would love to learn more about the team's timeline.

Is there any update on the hiring process?

Best,
{my_name}
"""


class FollowupEngine:
    def __init__(self, db: AsyncSession, my_name: str = "Your Name"):
        self.db = db
        self.my_name = my_name
        self.apply_engine = ApplyEngine()
        self.telegram = TelegramAgent()

    async def run(self) -> list[str]:
        due_applications = await self._get_due_followups()
        sent_ids = []
        for app in due_applications:
            job = await self.db.get(Job, app.job_id)
            if not job:
                continue
            days_since = (datetime.utcnow() - (app.applied_at or app.created_at)).days
            outreach = await self._get_latest_outreach(app.job_id)
            recruiter_email = outreach.recruiter_id if outreach else None
            success = await self._send_followup(app, job, outreach, days_since)
            if success:
                app.last_followup_at = datetime.utcnow()
                app.followup_count += 1
                app.next_followup_at = self._next_followup_date(app.followup_count)
                timeline_entry = {
                    "event": f"followup_{app.followup_count}",
                    "at": datetime.utcnow().isoformat(),
                }
                app.timeline = (app.timeline or []) + [timeline_entry]
                await self.db.commit()
                sent_ids.append(app.id)
                await self.telegram.send_followup_reminder(job.title, job.company, days_since)
        logger.info("Sent %d follow-ups", len(sent_ids))
        return sent_ids

    async def _get_due_followups(self) -> list[Application]:
        now = datetime.utcnow()
        result = await self.db.execute(
            select(Application).where(
                Application.status.in_(["applied", "outreach_sent"]),
                Application.next_followup_at <= now,
                Application.followup_count < len(FOLLOWUP_SCHEDULE_DAYS),
            )
        )
        return result.scalars().all()

    async def _get_latest_outreach(self, job_id: str) -> OutreachMessage | None:
        result = await self.db.execute(
            select(OutreachMessage)
            .where(OutreachMessage.job_id == job_id, OutreachMessage.sent == True)
            .order_by(OutreachMessage.sent_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def _send_followup(
        self, app: Application, job: Job, outreach: OutreachMessage | None, days_since: int
    ) -> bool:
        if not outreach or not outreach.tracking_data.get("to_email"):
            return False
        body = FOLLOWUP_TEMPLATE.format(
            recruiter_name=outreach.tracking_data.get("recruiter_name", "Hiring Team"),
            job_title=job.title,
            company=job.company,
            my_name=self.my_name,
        )
        msg_id = await self.apply_engine.send_application_email(
            to_email=outreach.tracking_data["to_email"],
            subject=f"Re: {outreach.subject}",
            body=body,
        )
        return msg_id is not None

    def _next_followup_date(self, followup_count: int) -> datetime | None:
        if followup_count >= len(FOLLOWUP_SCHEDULE_DAYS):
            return None
        return datetime.utcnow() + timedelta(days=FOLLOWUP_SCHEDULE_DAYS[followup_count])
