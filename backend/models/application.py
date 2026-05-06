from sqlalchemy import String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from db.session import Base
import uuid


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id: Mapped[str] = mapped_column(String(36), ForeignKey("jobs.id"), nullable=False)

    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="detected"
    )
    # detected → matched → outreach_sent → applied → interviewing → offer → rejected → ghosted

    applied_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    last_followup_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    next_followup_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    followup_count: Mapped[int] = mapped_column(default=0)

    notion_page_id: Mapped[str] = mapped_column(String(255), nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    timeline: Mapped[list] = mapped_column(JSON, default=list)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
