from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models.connected_account import ConnectedAccount
from app.db.models.scan_run import ScanRun
from app.db.models.user import User
from app.core.config import settings
from app.core.queue import enqueue_scan
from app.services.scan_jobs import perform_scan_job

router = APIRouter()


class ScanCreateRequest(BaseModel):
    provider: str
    query: str


class ScanCreateResponse(BaseModel):
    scan_id: str
    status: str


class ScanItem(BaseModel):
    id: str
    status: str
    query: str
    started_at: datetime | None
    finished_at: datetime | None
    processed_count: int
    total_estimated: int | None
    progress_pct: float | None


class ScanListResponse(BaseModel):
    items: list[ScanItem]
    total: int
    page: int
    page_size: int


@router.post("/scans", response_model=ScanCreateResponse)
def create_scan(
    payload: ScanCreateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ScanCreateResponse:
    if payload.provider != "gmail":
        raise HTTPException(status_code=400, detail="Unsupported provider")
    connected = (
        db.query(ConnectedAccount)
        .filter_by(provider="gmail", user_id=user.id)
        .first()
    )
    if not connected:
        raise HTTPException(status_code=400, detail="No Gmail account connected")
    scan = ScanRun(
        user_id=user.id,
        connected_account_id=connected.id,
        status="queued",
        query=payload.query,
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)

    if settings.use_rq:
        enqueue_scan(
            perform_scan_job,
            str(scan.id),
            str(connected.id),
            payload.query,
        )
    else:
        background_tasks.add_task(
            perform_scan_job,
            str(scan.id),
            str(connected.id),
            payload.query,
        )
    return ScanCreateResponse(scan_id=str(scan.id), status="queued")


@router.get("/scans", response_model=ScanListResponse)
def list_scans(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ScanListResponse:
    scans = (
        db.query(ScanRun)
        .filter(ScanRun.user_id == user.id)
        .order_by(ScanRun.created_at.desc())
    )
    total = scans.count()
    scans = scans.offset((page - 1) * page_size).limit(page_size).all()
    items = [
        ScanItem(
            id=str(scan.id),
            status=scan.status,
            query=scan.query,
            started_at=scan.started_at,
            finished_at=scan.finished_at,
            processed_count=scan.processed_count or 0,
            total_estimated=scan.total_estimated,
            progress_pct=scan.progress_pct,
        )
        for scan in scans
    ]
    return ScanListResponse(items=items, total=total, page=page, page_size=page_size)


@router.post("/scans/{scan_id}/resume", response_model=ScanCreateResponse)
def resume_scan(
    scan_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ScanCreateResponse:
    scan = db.query(ScanRun).filter_by(id=scan_id, user_id=user.id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if not scan.next_page_token and not scan.cursor_before_sent_at:
        raise HTTPException(status_code=400, detail="Scan is not resumable")
    connected = db.query(ConnectedAccount).filter_by(id=scan.connected_account_id).first()
    if not connected:
        raise HTTPException(status_code=400, detail="No Gmail account connected")

    if settings.use_rq:
        enqueue_scan(
            perform_scan_job,
            str(scan.id),
            str(connected.id),
            scan.query,
        )
    else:
        background_tasks.add_task(
            perform_scan_job,
            str(scan.id),
            str(connected.id),
            scan.query,
        )
    return ScanCreateResponse(scan_id=str(scan.id), status="queued")
