from sqlalchemy import String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from db.session import Base
import uuid


class OutreachMessage(Base):
    __tablename__ = "outreach_messages"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id"), nullable=False)
    recruiter_id: Mapped[str] = mapped_column(String(36), ForeignKey("recruiters.id"), nullable=True)

    channel: Mapped[str] = mapped_column(String(50), nullable=False)  # email, linkedin, telegram
    subject: Mapped[str] = mapped_column(String(500), nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)

    sent: Mapped[bool] = mapped_column(Boolean, default=False)
    sent_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    opened: Mapped[bool] = mapped_column(Boolean, default=False)
    opened_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    clicked: Mapped[bool] = mapped_column(Boolean, default=False)

    gmail_message_id: Mapped[str] = mapped_column(String(255), nullable=True)
    tracking_data: Mapped[dict] = mapped_column(JSON, default=dict)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
