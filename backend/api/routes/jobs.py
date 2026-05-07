from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Any
from sqlalchemy import select, desc
from models.job import Job
from agents.jd_parser import JDParser
from agents.rule_engine import RuleEngine
from api.dependencies import DBDep

router = APIRouter(prefix="/jobs", tags=["jobs"])
jd_parser = JDParser()
rule_engine = RuleEngine()


class JobResponse(BaseModel):
    id: str
    title: str
    company: str
    location: str | None
    url: str
    source: str
    match_score: float | None
    is_match: bool
    experience_level: str | None
    employment_type: str | None
    required_skills: list
    preferred_skills: list
    match_reasons: list

    model_config = {"from_attributes": True}


@router.get("", response_model=dict[str, Any])
async def list_jobs(
    db: DBDep,
    is_match: bool | None = Query(None),
    limit: int = Query(50, le=200),
    offset: int = Query(0),
):
    q = select(Job).order_by(desc(Job.detected_at)).offset(offset).limit(limit)
    if is_match is not None:
        q = q.where(Job.is_match == is_match)
    result = await db.execute(q)
    jobs = result.scalars().all()
    return {"success": True, "data": [JobResponse.model_validate(j) for j in jobs], "error": None}


@router.get("/{job_id}", response_model=dict[str, Any])
async def get_job(job_id: str, db: DBDep):
    job = await db.get(Job, job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return {"success": True, "data": JobResponse.model_validate(job), "error": None}


@router.post("/detect", response_model=dict[str, Any])
async def trigger_detection(db: DBDep):
    from agents.job_detector import JobDetector, DEFAULT_RSS_FEEDS
    from agents.rule_engine import RuleEngine
    from models.settings import SearchProfile, RssFeed
    from sqlalchemy import select
    
    feeds_res = await db.execute(select(RssFeed).where(RssFeed.is_active == True))
    active_feeds = [f.url for f in feeds_res.scalars().all()] or DEFAULT_RSS_FEEDS

    profile_res = await db.execute(select(SearchProfile).where(SearchProfile.is_active == True))
    profile = profile_res.scalars().first()
    active_rules = None
    if profile:
        active_rules = {
            "required_skills": profile.required_skills,
            "preferred_skills": profile.preferred_skills,
            "blocked_companies": profile.blocked_companies,
            "blocked_keywords": profile.blocked_keywords,
            "min_match_score": profile.min_match_score,
            "target_levels": profile.target_levels,
            "target_employment": profile.target_employment,
        }
    
    detector = JobDetector(db, rss_feeds=active_feeds)
    dynamic_rule_engine = RuleEngine(rules=active_rules)
    
    jobs = await detector.run()
    for job in jobs:
        parsed = jd_parser.parse(job.description or "")
        result = dynamic_rule_engine.evaluate(
            title=job.title,
            company=job.company,
            description=job.description or "",
            required_skills=parsed.required_skills,
            preferred_skills=parsed.preferred_skills,
            experience_level=parsed.experience_level,
            employment_type=parsed.employment_type,
        )
        job.required_skills = parsed.required_skills
        job.preferred_skills = parsed.preferred_skills
        job.experience_level = parsed.experience_level
        job.employment_type = parsed.employment_type
        job.salary_range = parsed.salary_range
        job.match_score = result.score
        job.is_match = result.is_match
        job.match_reasons = result.reasons
    await db.commit()
    return {"success": True, "data": {"detected": len(jobs)}, "error": None}


@router.delete("/{job_id}", response_model=dict[str, Any])
async def delete_job(job_id: str, db: DBDep):
    job = await db.get(Job, job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    await db.delete(job)
    await db.commit()
    return {"success": True, "data": {"deleted": job_id}, "error": None}
