from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models.connected_account import ConnectedAccount
from app.db.models.scan_run import ScanRun
from app.db.session import SessionLocal
from app.db.models.scan_run import ScanRun
from app.services.scan_engine import run_gmail_scan_by_id

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


@router.post("/scans", response_model=ScanCreateResponse)
def create_scan(
    payload: ScanCreateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> ScanCreateResponse:
    if payload.provider != "gmail":
        raise HTTPException(status_code=400, detail="Unsupported provider")
    connected = db.query(ConnectedAccount).filter_by(provider="gmail").first()
    if not connected:
        raise HTTPException(status_code=400, detail="No Gmail account connected")
    scan = ScanRun(
        user_id=connected.user_id,
        connected_account_id=connected.id,
        status="queued",
        query=payload.query,
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)

    def _run_scan():
        db_session = SessionLocal()
        try:
            run_gmail_scan_by_id(
                db_session, scan.id, connected.id, payload.query
            )
        finally:
            db_session.close()

    background_tasks.add_task(_run_scan)
    return ScanCreateResponse(scan_id=str(scan.id), status="queued")


@router.get("/scans", response_model=ScanListResponse)
def list_scans(db: Session = Depends(get_db)) -> ScanListResponse:
    scans = (
        db.query(ScanRun)
        .order_by(ScanRun.created_at.desc())
        .limit(20)
        .all()
    )
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
    return ScanListResponse(items=items)


@router.post("/scans/{scan_id}/resume", response_model=ScanCreateResponse)
def resume_scan(
    scan_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> ScanCreateResponse:
    scan = db.query(ScanRun).filter_by(id=scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if not scan.next_page_token:
        raise HTTPException(status_code=400, detail="Scan is not resumable")
    connected = db.query(ConnectedAccount).filter_by(id=scan.connected_account_id).first()
    if not connected:
        raise HTTPException(status_code=400, detail="No Gmail account connected")

    def _resume_scan():
        db_session = SessionLocal()
        try:
            run_gmail_scan_by_id(
                db_session, scan.id, connected.id, scan.query
            )
        finally:
            db_session.close()

    background_tasks.add_task(_resume_scan)
    return ScanCreateResponse(scan_id=str(scan.id), status="queued")
