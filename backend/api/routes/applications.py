from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Any
from datetime import datetime
from sqlalchemy import select, desc
from models.application import Application
from api.dependencies import DBDep

router = APIRouter(prefix="/applications", tags=["applications"])

VALID_STATUSES = ["detected", "matched", "outreach_sent", "applied", "interviewing", "offer", "rejected", "ghosted"]


class ApplicationResponse(BaseModel):
    id: str
    job_id: str
    status: str
    applied_at: datetime | None
    last_followup_at: datetime | None
    next_followup_at: datetime | None
    followup_count: int
    notion_page_id: str | None
    notes: str | None
    timeline: list
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UpdateStatusRequest(BaseModel):
    status: str
    notes: str | None = None


@router.get("/", response_model=dict[str, Any])
async def list_applications(
    db: DBDep,
    status: str | None = Query(None),
    limit: int = Query(50, le=200),
    offset: int = Query(0),
):
    q = select(Application).order_by(desc(Application.created_at)).offset(offset).limit(limit)
    if status:
        q = q.where(Application.status == status)
    result = await db.execute(q)
    apps = result.scalars().all()
    return {"success": True, "data": [ApplicationResponse.model_validate(a) for a in apps], "error": None}


@router.get("/{app_id}", response_model=dict[str, Any])
async def get_application(app_id: str, db: DBDep):
    app = await db.get(Application, app_id)
    if not app:
        raise HTTPException(404, "Application not found")
    return {"success": True, "data": ApplicationResponse.model_validate(app), "error": None}


@router.patch("/{app_id}/status", response_model=dict[str, Any])
async def update_status(app_id: str, body: UpdateStatusRequest, db: DBDep):
    if body.status not in VALID_STATUSES:
        raise HTTPException(400, f"Invalid status. Must be one of: {VALID_STATUSES}")
    app = await db.get(Application, app_id)
    if not app:
        raise HTTPException(404, "Application not found")
    old_status = app.status
    app.status = body.status
    if body.notes:
        app.notes = body.notes
    if body.status == "applied" and not app.applied_at:
        app.applied_at = datetime.utcnow()
    timeline_entry = {"event": f"status_{old_status}_to_{body.status}", "at": datetime.utcnow().isoformat()}
    app.timeline = (app.timeline or []) + [timeline_entry]
    await db.commit()
    return {"success": True, "data": ApplicationResponse.model_validate(app), "error": None}


@router.post("/trigger-followups", response_model=dict[str, Any])
async def trigger_followups(db: DBDep):
    from agents.followup_engine import FollowupEngine
    engine = FollowupEngine(db)
    sent_ids = await engine.run()
    return {"success": True, "data": {"sent_count": len(sent_ids), "application_ids": sent_ids}, "error": None}
