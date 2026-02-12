from datetime import datetime

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models.evidence_email import EvidenceEmail
from app.db.models.service_evidence_link import ServiceEvidenceLink
from app.db.models.user import User

router = APIRouter()


class EvidenceItem(BaseModel):
    id: str
    from_address: str
    from_domain: str
    subject: str
    sent_at: datetime
    evidence_type: str
    snippet: str | None


class EvidenceListResponse(BaseModel):
    items: list[EvidenceItem]
    total: int
    page: int
    page_size: int


@router.get("/evidence", response_model=EvidenceListResponse)
def list_evidence(
    service_id: str | None = Query(default=None),
    evidence_type: str | None = Query(default=None, alias="type"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> EvidenceListResponse:
    query = db.query(EvidenceEmail).filter(EvidenceEmail.user_id == user.id)
    if service_id:
        query = (
            query.join(
                ServiceEvidenceLink,
                ServiceEvidenceLink.evidence_email_id == EvidenceEmail.id,
            )
            .filter(ServiceEvidenceLink.service_id == service_id)
        )
    if evidence_type:
        query = query.filter(EvidenceEmail.evidence_type == evidence_type)
    total = query.count()
    rows = (
        query.order_by(EvidenceEmail.sent_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    items = [
        EvidenceItem(
            id=str(row.id),
            from_address=row.from_address,
            from_domain=row.from_domain,
            subject=row.subject,
            sent_at=row.sent_at,
            evidence_type=row.evidence_type,
            snippet=row.snippet,
        )
        for row in rows
    ]
    return EvidenceListResponse(items=items, total=total, page=page, page_size=page_size)
