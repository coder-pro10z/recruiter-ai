from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Any
from datetime import datetime
from sqlalchemy import select
from models.recruiter import Recruiter
from agents.recruiter_scraper import RecruiterScraper
from api.dependencies import DBDep

router = APIRouter(prefix="/recruiters", tags=["recruiters"])
scraper = RecruiterScraper()


class RecruiterResponse(BaseModel):
    id: str
    job_id: str | None
    name: str | None
    title: str | None
    company: str
    email: str | None
    linkedin_url: str | None
    email_verified: bool
    email_confidence: float
    source: str | None

    model_config = {"from_attributes": True}


class ScrapeRequest(BaseModel):
    job_id: str
    company: str
    job_title: str


@router.get("/", response_model=dict[str, Any])
async def list_recruiters(
    db: DBDep,
    job_id: str | None = Query(None),
    limit: int = Query(50, le=200),
):
    q = select(Recruiter).limit(limit)
    if job_id:
        q = q.where(Recruiter.job_id == job_id)
    result = await db.execute(q)
    recruiters = result.scalars().all()
    return {"success": True, "data": [RecruiterResponse.model_validate(r) for r in recruiters], "error": None}


@router.post("/scrape", response_model=dict[str, Any])
async def scrape_recruiters(body: ScrapeRequest, db: DBDep):
    results = await scraper.find_recruiters(body.company, body.job_title)
    saved = []
    for r in results:
        recruiter = Recruiter(
            job_id=body.job_id,
            name=r.get("name"),
            title=r.get("title"),
            company=r.get("company", body.company),
            email=r.get("email"),
            linkedin_url=r.get("linkedin_url"),
            email_confidence=r.get("email_confidence", 0.0),
            source=r.get("source"),
        )
        db.add(recruiter)
        saved.append(recruiter)
    await db.commit()
    return {"success": True, "data": {"found": len(saved)}, "error": None}
