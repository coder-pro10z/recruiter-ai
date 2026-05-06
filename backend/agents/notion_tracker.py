"""
Notion Tracker — syncs application state to a Notion database.
"""
import logging
from datetime import datetime
from config.settings import get_settings

logger = logging.getLogger(__name__)

STATUS_COLORS = {
    "detected": "gray",
    "matched": "blue",
    "outreach_sent": "yellow",
    "applied": "orange",
    "interviewing": "purple",
    "offer": "green",
    "rejected": "red",
    "ghosted": "default",
}


class NotionTracker:
    def __init__(self):
        self.settings = get_settings()
        self._client = None

    def _get_client(self):
        if not self._client and self.settings.notion_api_key:
            from notion_client import AsyncClient
            self._client = AsyncClient(auth=self.settings.notion_api_key)
        return self._client

    async def create_page(
        self,
        job_title: str,
        company: str,
        url: str,
        location: str,
        status: str,
        match_score: float,
        recruiter_email: str | None,
        applied_at: datetime | None,
        notes: str = "",
    ) -> str | None:
        client = self._get_client()
        if not client or not self.settings.notion_database_id:
            logger.warning("Notion not configured — skipping")
            return None
        try:
            page = await client.pages.create(
                parent={"database_id": self.settings.notion_database_id},
                properties={
                    "Name": {"title": [{"text": {"content": f"{job_title} @ {company}"}}]},
                    "Company": {"rich_text": [{"text": {"content": company}}]},
                    "URL": {"url": url},
                    "Location": {"rich_text": [{"text": {"content": location or ""}}]},
                    "Status": {"select": {"name": status, "color": STATUS_COLORS.get(status, "default")}},
                    "Match Score": {"number": round(match_score * 100)},
                    "Recruiter Email": {"email": recruiter_email} if recruiter_email else {"email": None},
                    "Applied Date": {"date": {"start": applied_at.isoformat()}} if applied_at else {"date": None},
                    "Notes": {"rich_text": [{"text": {"content": notes}}]},
                },
            )
            return page["id"]
        except Exception as e:
            logger.error("Notion create_page failed: %s", e)
            return None

    async def update_status(self, page_id: str, status: str, notes: str = "") -> bool:
        client = self._get_client()
        if not client:
            return False
        try:
            props: dict = {"Status": {"select": {"name": status, "color": STATUS_COLORS.get(status, "default")}}}
            if notes:
                props["Notes"] = {"rich_text": [{"text": {"content": notes}}]}
            await client.pages.update(page_id=page_id, properties=props)
            return True
        except Exception as e:
            logger.error("Notion update_status failed: %s", e)
            return False
