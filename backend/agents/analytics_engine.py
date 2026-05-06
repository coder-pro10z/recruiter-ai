"""
Analytics Engine — computes funnel metrics and conversion rates.
"""
import logging
from collections import defaultdict
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.application import Application
from models.job import Job
from models.outreach import OutreachMessage

logger = logging.getLogger(__name__)


class AnalyticsEngine:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_funnel(self) -> dict:
        result = await self.db.execute(
            select(Application.status, func.count(Application.id))
            .group_by(Application.status)
        )
        counts = dict(result.all())
        stages = ["detected", "matched", "outreach_sent", "applied", "interviewing", "offer", "rejected", "ghosted"]
        return {stage: counts.get(stage, 0) for stage in stages}

    async def get_weekly_activity(self, weeks: int = 8) -> list[dict]:
        cutoff = datetime.utcnow() - timedelta(weeks=weeks)
        result = await self.db.execute(
            select(Application).where(Application.created_at >= cutoff)
        )
        apps = result.scalars().all()
        weekly: dict[str, int] = defaultdict(int)
        for app in apps:
            week_key = app.created_at.strftime("%Y-W%W")
            weekly[week_key] += 1
        return [{"week": k, "applications": v} for k, v in sorted(weekly.items())]

    async def get_response_rate(self) -> dict:
        total_result = await self.db.execute(
            select(func.count(Application.id)).where(Application.status == "applied")
        )
        total_applied = total_result.scalar() or 0

        responded_result = await self.db.execute(
            select(func.count(Application.id)).where(
                Application.status.in_(["interviewing", "offer"])
            )
        )
        responded = responded_result.scalar() or 0

        email_open_result = await self.db.execute(
            select(func.count(OutreachMessage.id)).where(OutreachMessage.opened == True)
        )
        emails_opened = email_open_result.scalar() or 0

        total_sent_result = await self.db.execute(
            select(func.count(OutreachMessage.id)).where(OutreachMessage.sent == True)
        )
        emails_sent = total_sent_result.scalar() or 0

        return {
            "total_applied": total_applied,
            "total_responded": responded,
            "response_rate": round(responded / total_applied, 3) if total_applied else 0,
            "emails_sent": emails_sent,
            "emails_opened": emails_opened,
            "email_open_rate": round(emails_opened / emails_sent, 3) if emails_sent else 0,
        }

    async def get_top_matched_companies(self, limit: int = 10) -> list[dict]:
        result = await self.db.execute(
            select(Job.company, func.avg(Job.match_score).label("avg_score"), func.count(Job.id).label("count"))
            .where(Job.is_match == True)
            .group_by(Job.company)
            .order_by(func.avg(Job.match_score).desc())
            .limit(limit)
        )
        return [{"company": row[0], "avg_score": round(row[1], 3), "job_count": row[2]} for row in result.all()]

    async def get_summary(self) -> dict:
        funnel = await self.get_funnel()
        rates = await self.get_response_rate()
        top_cos = await self.get_top_matched_companies(5)
        return {
            "funnel": funnel,
            "rates": rates,
            "top_matched_companies": top_cos,
            "generated_at": datetime.utcnow().isoformat(),
        }
