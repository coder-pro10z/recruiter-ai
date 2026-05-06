"""
Apply Engine — sends application emails via Gmail API.
"""
import base64
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import get_settings

logger = logging.getLogger(__name__)


class ApplyEngine:
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

    async def send_application_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        cc: str | None = None,
    ) -> str | None:
        service = self._get_service()
        if not service:
            logger.warning("Gmail not configured — skipping email send")
            return None
        try:
            msg = MIMEMultipart("alternative")
            msg["From"] = self.settings.gmail_from_address
            msg["To"] = to_email
            msg["Subject"] = subject
            if cc:
                msg["Cc"] = cc
            msg.attach(MIMEText(body, "plain"))
            raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
            sent = service.users().messages().send(
                userId="me", body={"raw": raw}
            ).execute()
            logger.info("Email sent, message_id=%s", sent.get("id"))
            return sent.get("id")
        except Exception as e:
            logger.error("Email send failed: %s", e)
            return None

    async def list_inbox(self, query: str = "is:unread", max_results: int = 10) -> list[dict]:
        service = self._get_service()
        if not service:
            return []
        try:
            result = service.users().messages().list(
                userId="me", q=query, maxResults=max_results
            ).execute()
            messages = result.get("messages", [])
            details = []
            for m in messages:
                msg = service.users().messages().get(userId="me", id=m["id"]).execute()
                headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
                details.append({
                    "id": m["id"],
                    "from": headers.get("From"),
                    "subject": headers.get("Subject"),
                    "date": headers.get("Date"),
                    "snippet": msg.get("snippet"),
                })
            return details
        except Exception as e:
            logger.error("Gmail list_inbox failed: %s", e)
            return []
