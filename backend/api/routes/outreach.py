from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any
from datetime import datetime
from sqlalchemy import select
from models.outreach import OutreachMessage
from models.job import Job
from models.recruiter import Recruiter
from agents.outreach_generator import OutreachGenerator
from agents.resume_matcher import ResumeMatcher
from agents.apply_engine import ApplyEngine
from agents.notion_tracker import NotionTracker
from api.dependencies import DBDep

router = APIRouter(prefix="/outreach", tags=["outreach"])
generator = OutreachGenerator()
matcher = ResumeMatcher()
apply_engine = ApplyEngine()
notion = NotionTracker()


class GenerateRequest(BaseModel):
    job_id: str
    recruiter_id: str | None = None
    my_name: str = "Your Name"
    experience_years: int = 5
    highlight: str = "scalable distributed systems"


class SendRequest(BaseModel):
    outreach_id: str


class OutreachResponse(BaseModel):
    id: str
    job_id: str
    recruiter_id: str | None
    channel: str
    subject: str | None
    body: str
    sent: bool
    sent_at: datetime | None
    opened: bool
    opened_at: datetime | None

    model_config = {"from_attributes": True}


@router.post("/generate", response_model=dict[str, Any])
async def generate_outreach(body: GenerateRequest, db: DBDep):
    job = await db.get(Job, body.job_id)
    if not job:
        raise HTTPException(404, "Job not found")

    recruiter = None
    if body.recruiter_id:
        recruiter = await db.get(Recruiter, body.recruiter_id)

    resume_match = matcher.match(
        job_title=job.title,
        company=job.company,
        required_skills=job.required_skills or [],
        preferred_skills=job.preferred_skills or [],
        experience_level=job.experience_level or "mid",
    )

    outreach_content = await generator.generate(
        job_title=job.title,
        company=job.company,
        recruiter_name=recruiter.name if recruiter else None,
        cover_angle=resume_match.cover_angle,
        matched_skills=resume_match.matched_skills,
        experience_years=body.experience_years,
        highlight=body.highlight,
        my_name=body.my_name,
    )

    msg = OutreachMessage(
        job_id=body.job_id,
        recruiter_id=body.recruiter_id,
        channel="email",
        subject=outreach_content["email_subject"],
        body=outreach_content["email_body"],
        tracking_data={
            "to_email": recruiter.email if recruiter else None,
            "recruiter_name": recruiter.name if recruiter else None,
            "linkedin_note": outreach_content.get("linkedin_note"),
        },
    )
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return {"success": True, "data": OutreachResponse.model_validate(msg), "error": None}


@router.post("/send/{outreach_id}", response_model=dict[str, Any])
async def send_outreach(outreach_id: str, db: DBDep):
    msg = await db.get(OutreachMessage, outreach_id)
    if not msg:
        raise HTTPException(404, "Outreach message not found")
    if msg.sent:
        raise HTTPException(400, "Already sent")

    to_email = msg.tracking_data.get("to_email")
    if not to_email:
        raise HTTPException(400, "No recipient email — scrape recruiter first")

    gmail_id = await apply_engine.send_application_email(
        to_email=to_email,
        subject=msg.subject or "",
        body=msg.body,
    )
    msg.sent = True
    msg.sent_at = datetime.utcnow()
    msg.gmail_message_id = gmail_id
    await db.commit()
    return {"success": True, "data": {"sent": True, "gmail_message_id": gmail_id}, "error": None}


@router.get("/", response_model=dict[str, Any])
async def list_outreach(db: DBDep, job_id: str | None = None):
    q = select(OutreachMessage)
    if job_id:
        q = q.where(OutreachMessage.job_id == job_id)
    result = await db.execute(q)
    messages = result.scalars().all()
    return {"success": True, "data": [OutreachResponse.model_validate(m) for m in messages], "error": None}
