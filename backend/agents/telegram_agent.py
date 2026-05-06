"""
Telegram Agent — sends strike packages with job details and one-click actions.
"""
import logging
import httpx
from config.settings import get_settings

logger = logging.getLogger(__name__)

STRIKE_TEMPLATE = """\
🎯 *New Job Match* — Score: {score:.0%}

*{title}* at *{company}*
📍 {location} | {employment_type}
🔗 [View Job]({url})

*Skills matched:* {matched_skills}
*Gaps:* {missing_skills}

*Recruiter:* {recruiter_name} — {recruiter_email}

*Outreach subject:*
_{email_subject}_

*Cover angle:*
_{cover_angle}_

*Match reasons:*
{reasons}

⚡️ [Apply Now]({url}) | [Send Email](mailto:{recruiter_email}?subject={email_subject_encoded})
"""


class TelegramAgent:
    def __init__(self):
        self.settings = get_settings()
        self.base_url = f"https://api.telegram.org/bot{self.settings.telegram_bot_token}"

    async def send_strike_package(
        self,
        title: str,
        company: str,
        location: str,
        employment_type: str,
        url: str,
        score: float,
        matched_skills: list[str],
        missing_skills: list[str],
        recruiter_name: str | None,
        recruiter_email: str | None,
        email_subject: str,
        cover_angle: str,
        reasons: list[str],
    ) -> bool:
        if not self.settings.telegram_bot_token or not self.settings.telegram_chat_id:
            logger.warning("Telegram not configured — skipping notification")
            return False

        import urllib.parse
        message = STRIKE_TEMPLATE.format(
            title=title,
            company=company,
            location=location or "Remote",
            employment_type=employment_type or "Full-time",
            url=url,
            score=score,
            matched_skills=", ".join(matched_skills[:5]) or "—",
            missing_skills=", ".join(missing_skills[:3]) or "None",
            recruiter_name=recruiter_name or "Unknown",
            recruiter_email=recruiter_email or "N/A",
            email_subject=email_subject,
            cover_angle=cover_angle,
            reasons="\n".join(f"• {r}" for r in reasons) or "—",
            email_subject_encoded=urllib.parse.quote(email_subject),
        )
        return await self._send_message(message)

    async def send_followup_reminder(self, title: str, company: str, days_since: int) -> bool:
        message = (
            f"⏰ *Follow-up Reminder*\n\n"
            f"*{title}* at *{company}*\n"
            f"Applied {days_since} days ago — time to follow up!\n"
        )
        return await self._send_message(message)

    async def _send_message(self, text: str) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(
                    f"{self.base_url}/sendMessage",
                    json={
                        "chat_id": self.settings.telegram_chat_id,
                        "text": text,
                        "parse_mode": "Markdown",
                        "disable_web_page_preview": True,
                    },
                )
                resp.raise_for_status()
            return True
        except Exception as e:
            logger.error("Telegram send failed: %s", e)
            return False
