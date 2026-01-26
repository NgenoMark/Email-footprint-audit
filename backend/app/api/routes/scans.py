from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

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


class ScanListResponse(BaseModel):
    items: list[ScanItem]


@router.post("/scans", response_model=ScanCreateResponse)
def create_scan(payload: ScanCreateRequest) -> ScanCreateResponse:
    return ScanCreateResponse(scan_id="scan-0001", status="queued")


@router.get("/scans", response_model=ScanListResponse)
def list_scans() -> ScanListResponse:
    now = datetime.now(timezone.utc)
    return ScanListResponse(
        items=[
            ScanItem(
                id="scan-0001",
                status="running",
                query="subject:(welcome OR verify OR \"confirm your email\")",
                started_at=now,
                finished_at=None,
            )
        ]
    )
