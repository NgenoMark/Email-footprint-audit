import csv
import io
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models.evidence_email import EvidenceEmail
from app.db.models.export_history import ExportHistory
from app.db.models.service import Service
from app.db.models.service_evidence_link import ServiceEvidenceLink
from app.db.models.user import User

router = APIRouter()


class ExportRequest(BaseModel):
    format: str


class ExportResponse(BaseModel):
    url: str
    export_id: str


@router.post("/exports", response_model=ExportResponse)
def create_export(payload: ExportRequest) -> ExportResponse:
    export_id = str(uuid.uuid4())
    fmt = payload.format.lower()
    if fmt not in {"csv", "json"}:
        raise HTTPException(status_code=400, detail="Unsupported format")
    return ExportResponse(url=f"/exports/{export_id}.{fmt}", export_id=export_id)


@router.get("/exports/{export_id}.csv")
def download_export_csv(export_id: str, db: Session = Depends(get_db)) -> StreamingResponse:
    user = db.query(User).order_by(User.created_at.asc()).first()
    if not user:
        raise HTTPException(status_code=404, detail="No user found")

    services = db.query(Service).filter(Service.user_id == user.id).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "service_id",
            "display_name",
            "primary_domain",
            "category",
            "confidence",
            "confidence_reason",
            "first_seen_at",
            "last_seen_at",
            "evidence_count",
        ]
    )
    for service in services:
        evidence_count = (
            db.query(ServiceEvidenceLink).filter_by(service_id=service.id).count()
        )
        writer.writerow(
            [
                str(service.id),
                service.display_name,
                service.primary_domain,
                service.category or "",
                service.confidence,
                service.confidence_reason,
                service.first_seen_at.isoformat() if service.first_seen_at else "",
                service.last_seen_at.isoformat() if service.last_seen_at else "",
                evidence_count,
            ]
        )
    output.seek(0)
    filename = f"services-{datetime.now(timezone.utc).date()}.csv"
    db.add(
        ExportHistory(
            user_id=user.id,
            format="csv",
            status="ready",
            download_url=f"/exports/{export_id}.csv",
        )
    )
    db.commit()
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/exports/{export_id}.json")
def download_export_json(
    export_id: str, db: Session = Depends(get_db)
) -> JSONResponse:
    user = db.query(User).order_by(User.created_at.asc()).first()
    if not user:
        raise HTTPException(status_code=404, detail="No user found")

    services = db.query(Service).filter(Service.user_id == user.id).all()
    payload = []
    for service in services:
        evidence_count = (
            db.query(ServiceEvidenceLink).filter_by(service_id=service.id).count()
        )
        payload.append(
            {
                "id": str(service.id),
                "display_name": service.display_name,
                "primary_domain": service.primary_domain,
                "category": service.category,
                "confidence": service.confidence,
                "confidence_reason": service.confidence_reason,
                "first_seen_at": service.first_seen_at.isoformat()
                if service.first_seen_at
                else None,
                "last_seen_at": service.last_seen_at.isoformat() if service.last_seen_at else None,
                "evidence_count": evidence_count,
            }
        )
    db.add(
        ExportHistory(
            user_id=user.id,
            format="json",
            status="ready",
            download_url=f"/exports/{export_id}.json",
        )
    )
    db.commit()
    return JSONResponse(payload)


@router.get("/exports/history")
def export_history(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> dict:
    user = db.query(User).order_by(User.created_at.asc()).first()
    if not user:
        return {"items": [], "total": 0, "page": page, "page_size": page_size}
    query = db.query(ExportHistory).filter(ExportHistory.user_id == user.id)
    total = query.count()
    rows = (
        query.order_by(ExportHistory.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    items = [
        {
            "id": str(row.id),
            "format": row.format,
            "status": row.status,
            "download_url": row.download_url,
            "created_at": row.created_at.isoformat(),
        }
        for row in rows
    ]
    return {"items": items, "total": total, "page": page, "page_size": page_size}
