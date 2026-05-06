from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any
from agents.rule_engine import DEFAULT_RULES
from agents.resume_matcher import DEFAULT_RESUME
from agents.job_detector import DEFAULT_RSS_FEEDS

router = APIRouter(prefix="/settings", tags=["settings"])

_runtime_rules: dict = dict(DEFAULT_RULES)
_runtime_resume: dict = dict(DEFAULT_RESUME)
_runtime_feeds: list[str] = list(DEFAULT_RSS_FEEDS)


class RulesUpdate(BaseModel):
    required_skills: list[str] | None = None
    preferred_skills: list[str] | None = None
    blocked_companies: list[str] | None = None
    blocked_keywords: list[str] | None = None
    min_match_score: float | None = None
    target_levels: list[str] | None = None
    target_employment: list[str] | None = None


class FeedsUpdate(BaseModel):
    feeds: list[str]


@router.get("/rules", response_model=dict[str, Any])
async def get_rules():
    return {"success": True, "data": _runtime_rules, "error": None}


@router.patch("/rules", response_model=dict[str, Any])
async def update_rules(body: RulesUpdate):
    updates = body.model_dump(exclude_none=True)
    _runtime_rules.update(updates)
    return {"success": True, "data": _runtime_rules, "error": None}


@router.get("/resume", response_model=dict[str, Any])
async def get_resume():
    return {"success": True, "data": _runtime_resume, "error": None}


@router.put("/resume", response_model=dict[str, Any])
async def update_resume(resume: dict):
    _runtime_resume.update(resume)
    return {"success": True, "data": _runtime_resume, "error": None}


@router.get("/feeds", response_model=dict[str, Any])
async def get_feeds():
    return {"success": True, "data": {"feeds": _runtime_feeds}, "error": None}


@router.put("/feeds", response_model=dict[str, Any])
async def update_feeds(body: FeedsUpdate):
    _runtime_feeds.clear()
    _runtime_feeds.extend(body.feeds)
    return {"success": True, "data": {"feeds": _runtime_feeds}, "error": None}
