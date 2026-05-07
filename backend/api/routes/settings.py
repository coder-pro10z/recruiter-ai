from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any
from sqlalchemy import select, update
from api.dependencies import DBDep
from agents.rule_engine import DEFAULT_RULES
from agents.resume_matcher import DEFAULT_RESUME
from agents.job_detector import DEFAULT_RSS_FEEDS
from models.settings import SearchProfile, RssFeed

router = APIRouter(prefix="/settings", tags=["settings"])

_runtime_resume: dict = dict(DEFAULT_RESUME)

class ProfileCreateUpdate(BaseModel):
    name: str
    required_skills: list[str] | None = None
    preferred_skills: list[str] | None = None
    blocked_companies: list[str] | None = None
    blocked_keywords: list[str] | None = None
    min_match_score: float | None = None
    target_levels: list[str] | None = None
    target_employment: list[str] | None = None
    is_active: bool = False

class FeedsUpdate(BaseModel):
    feeds: list[str]

# ===============================
# PROFILES & RULES
# ===============================

@router.get("/profiles", response_model=dict[str, Any])
async def get_profiles(db: DBDep):
    result = await db.execute(select(SearchProfile).order_by(SearchProfile.created_at.desc()))
    profiles = result.scalars().all()
    return {"success": True, "data": [{"id": p.id, "name": p.profile_name, "is_active": p.is_active} for p in profiles], "error": None}

@router.get("/rules", response_model=dict[str, Any])
async def get_active_rules(db: DBDep):
    result = await db.execute(select(SearchProfile).where(SearchProfile.is_active == True))
    profile = result.scalars().first()
    if profile:
        return {"success": True, "data": {
            "required_skills": profile.required_skills,
            "preferred_skills": profile.preferred_skills,
            "blocked_companies": profile.blocked_companies,
            "blocked_keywords": profile.blocked_keywords,
            "min_match_score": profile.min_match_score,
            "target_levels": profile.target_levels,
            "target_employment": profile.target_employment,
        }, "error": None}
    return {"success": True, "data": DEFAULT_RULES, "error": None}

@router.post("/profiles", response_model=dict[str, Any])
async def create_profile(body: ProfileCreateUpdate, db: DBDep):
    if body.is_active:
        await db.execute(update(SearchProfile).values(is_active=False))
        
    profile = SearchProfile(
        profile_name=body.name,
        required_skills=body.required_skills or [],
        preferred_skills=body.preferred_skills or [],
        blocked_companies=body.blocked_companies or [],
        blocked_keywords=body.blocked_keywords or [],
        min_match_score=body.min_match_score or 0.4,
        target_levels=body.target_levels or [],
        target_employment=body.target_employment or [],
        is_active=body.is_active
    )
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return {"success": True, "data": {"id": profile.id, "name": profile.profile_name}, "error": None}

@router.put("/profiles/{profile_id}/activate", response_model=dict[str, Any])
async def activate_profile(profile_id: str, db: DBDep):
    await db.execute(update(SearchProfile).values(is_active=False))
    profile = await db.get(SearchProfile, profile_id)
    if not profile:
        raise HTTPException(404, "Profile not found")
    profile.is_active = True
    await db.commit()
    return {"success": True, "data": {"active_profile_id": profile.id}, "error": None}

@router.patch("/rules", response_model=dict[str, Any])
async def update_rules_legacy(body: dict, db: DBDep):
    # For backward compatibility with current frontend (which just sends a PATCH to /rules)
    result = await db.execute(select(SearchProfile).where(SearchProfile.is_active == True))
    profile = result.scalars().first()
    
    if not profile:
        # Create a default active profile
        profile = SearchProfile(profile_name="Default Profile", is_active=True)
        db.add(profile)
        await db.flush()

    if "required_skills" in body: profile.required_skills = body["required_skills"]
    if "preferred_skills" in body: profile.preferred_skills = body["preferred_skills"]
    if "blocked_companies" in body: profile.blocked_companies = body["blocked_companies"]
    if "blocked_keywords" in body: profile.blocked_keywords = body["blocked_keywords"]
    if "min_match_score" in body: profile.min_match_score = body["min_match_score"]
    if "target_levels" in body: profile.target_levels = body["target_levels"]
    if "target_employment" in body: profile.target_employment = body["target_employment"]

    await db.commit()
    return {"success": True, "data": {"status": "updated"}, "error": None}

# ===============================
# FEEDS
# ===============================

@router.get("/feeds", response_model=dict[str, Any])
async def get_feeds(db: DBDep):
    result = await db.execute(select(RssFeed).where(RssFeed.is_active == True))
    feeds = result.scalars().all()
    feed_urls = [f.url for f in feeds] if feeds else DEFAULT_RSS_FEEDS
    return {"success": True, "data": {"feeds": feed_urls}, "error": None}

@router.put("/feeds", response_model=dict[str, Any])
async def update_feeds_legacy(body: FeedsUpdate, db: DBDep):
    # Deactivate all existing
    await db.execute(update(RssFeed).values(is_active=False))
    
    # Upsert new feeds
    for url in body.feeds:
        result = await db.execute(select(RssFeed).where(RssFeed.url == url))
        existing = result.scalars().first()
        if existing:
            existing.is_active = True
        else:
            db.add(RssFeed(url=url, is_active=True))
            
    await db.commit()
    return {"success": True, "data": {"feeds": body.feeds}, "error": None}

# ===============================
# RESUME (unchanged)
# ===============================

@router.get("/resume", response_model=dict[str, Any])
async def get_resume():
    return {"success": True, "data": _runtime_resume, "error": None}

@router.put("/resume", response_model=dict[str, Any])
async def update_resume(resume: dict):
    _runtime_resume.update(resume)
    return {"success": True, "data": _runtime_resume, "error": None}
