from sqlalchemy import String, Text, Float, Boolean, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from db.session import Base
import uuid


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    company: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=True)
    url: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False)  # rss, linkedin, manual

    description: Mapped[str] = mapped_column(Text, nullable=True)
    required_skills: Mapped[list] = mapped_column(JSON, default=list)
    preferred_skills: Mapped[list] = mapped_column(JSON, default=list)
    experience_level: Mapped[str] = mapped_column(String(50), nullable=True)
    employment_type: Mapped[str] = mapped_column(String(50), nullable=True)
    salary_range: Mapped[dict] = mapped_column(JSON, nullable=True)

    match_score: Mapped[float] = mapped_column(Float, nullable=True)
    match_reasons: Mapped[list] = mapped_column(JSON, default=list)
    is_match: Mapped[bool] = mapped_column(Boolean, default=False)

    detected_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
