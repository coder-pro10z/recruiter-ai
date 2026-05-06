"""
Mailtrack Monitor — detects email opens and link clicks using Gmail label monitoring.
Mailtrack appends a tracking pixel and uses Gmail labels to mark opened emails.
"""
import logging
from datetime import datetime
from config.settings import get_settings

logger = logging.getLogger(__name__)


class MailtrackMonitor:
    def __init__(self):
        self.settings = get_settings()
        self._service = None

    def _get_service(self):
        if self._service:
            return self._service
        if not all([
            self.settings.gmail_client_id,
            self.settings.gmail_client_secret,
            self.settings.gmail_refresh_token,
        ]):
            return None
        try:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            creds = Credentials(
                token=None,
                refresh_token=self.settings.gmail_refresh_token,
                client_id=self.settings.gmail_client_id,
                client_secret=self.settings.gmail_client_secret,
                token_uri="https://oauth2.googleapis.com/token",
            )
            self._service = build("gmail", "v1", credentials=creds)
            return self._service
        except Exception as e:
            logger.error("Gmail service init failed: %s", e)
            return None

    async def check_opens(self, gmail_message_ids: list[str]) -> dict[str, dict]:
        """Returns {message_id: {opened: bool, opened_at: datetime | None}}"""
        service = self._get_service()
        if not service:
            return {}
        results = {}
        for msg_id in gmail_message_ids:
            try:
                msg = service.users().messages().get(userId="me", id=msg_id).execute()
                labels = msg.get("labelIds", [])
                # Mailtrack marks opened emails with a custom label
                opened = any("mailtrack" in label.lower() or "opened" in label.lower() for label in labels)
                # Use internal date as a proxy for open time
                opened_at = None
                if opened:
                    ts_ms = int(msg.get("internalDate", 0))
                    opened_at = datetime.utcfromtimestamp(ts_ms / 1000) if ts_ms else None
                results[msg_id] = {"opened": opened, "opened_at": opened_at}
            except Exception as e:
                logger.warning("Failed to check message %s: %s", msg_id, e)
                results[msg_id] = {"opened": False, "opened_at": None}
        return results

    async def list_opened_sent(self, days: int = 7) -> list[dict]:
        """Returns recently sent emails that have been opened."""
        service = self._get_service()
        if not service:
            return []
        try:
            result = service.users().messages().list(
                userId="me",
                q=f"in:sent newer_than:{days}d",
                maxResults=50,
            ).execute()
            messages = result.get("messages", [])
            opened = []
            for m in messages:
                msg = service.users().messages().get(userId="me", id=m["id"]).execute()
                labels = msg.get("labelIds", [])
                if any("mailtrack" in l.lower() or "opened" in l.lower() for l in labels):
                    headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
                    opened.append({
                        "id": m["id"],
                        "to": headers.get("To"),
                        "subject": headers.get("Subject"),
                    })
            return opened
        except Exception as e:
            logger.error("list_opened_sent failed: %s", e)
            return []
