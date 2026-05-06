from fastapi import APIRouter
from typing import Any
from agents.analytics_engine import AnalyticsEngine
from api.dependencies import DBDep

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary", response_model=dict[str, Any])
async def get_summary(db: DBDep):
    engine = AnalyticsEngine(db)
    data = await engine.get_summary()
    return {"success": True, "data": data, "error": None}


@router.get("/funnel", response_model=dict[str, Any])
async def get_funnel(db: DBDep):
    engine = AnalyticsEngine(db)
    data = await engine.get_funnel()
    return {"success": True, "data": data, "error": None}


@router.get("/weekly", response_model=dict[str, Any])
async def get_weekly(db: DBDep, weeks: int = 8):
    engine = AnalyticsEngine(db)
    data = await engine.get_weekly_activity(weeks)
    return {"success": True, "data": data, "error": None}


@router.get("/response-rate", response_model=dict[str, Any])
async def get_response_rate(db: DBDep):
    engine = AnalyticsEngine(db)
    data = await engine.get_response_rate()
    return {"success": True, "data": data, "error": None}


@router.get("/top-companies", response_model=dict[str, Any])
async def get_top_companies(db: DBDep, limit: int = 10):
    engine = AnalyticsEngine(db)
    data = await engine.get_top_matched_companies(limit)
    return {"success": True, "data": data, "error": None}
