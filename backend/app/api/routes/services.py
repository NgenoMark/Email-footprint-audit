from datetime import datetime

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models.service import Service
from app.db.models.service_evidence_link import ServiceEvidenceLink
from app.db.models.evidence_email import EvidenceEmail
from app.db.models.user import User

router = APIRouter()


class ServiceListItem(BaseModel):
    id: str
    display_name: str
    primary_domain: str
    category: str | None
    confidence: str
    confidence_reason: str
    first_seen_at: datetime | None
    last_seen_at: datetime | None
    evidence_count: int


class ServiceListResponse(BaseModel):
    items: list[ServiceListItem]


class ServiceEvidenceItem(BaseModel):
    id: str
    from_address: str
    subject: str
    sent_at: datetime
    evidence_type: str
    match_reason: str


class ServiceDetailResponse(BaseModel):
    id: str
    display_name: str
    primary_domain: str
    category: str | None
    confidence: str
    confidence_reason: str
    first_seen_at: datetime | None
    last_seen_at: datetime | None
    evidence: list[ServiceEvidenceItem]


@router.get("/services", response_model=ServiceListResponse)
def list_services(
    q: str | None = Query(default=None),
    confidence: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> ServiceListResponse:
    user = db.query(User).order_by(User.created_at.asc()).first()
    if not user:
        return ServiceListResponse(items=[])
    query = db.query(Service).filter(Service.user_id == user.id)
    if q:
        like = f"%{q}%"
        query = query.filter(Service.display_name.ilike(like))
    if confidence:
        query = query.filter(Service.confidence == confidence)
    services = query.order_by(Service.last_seen_at.desc().nullslast()).all()
    items = []
    for service in services:
        evidence_count = (
            db.query(ServiceEvidenceLink)
            .filter_by(service_id=service.id)
            .count()
        )
        items.append(
            ServiceListItem(
                id=str(service.id),
                display_name=service.display_name,
                primary_domain=service.primary_domain,
                category=service.category,
                confidence=service.confidence,
                confidence_reason=service.confidence_reason,
                first_seen_at=service.first_seen_at,
                last_seen_at=service.last_seen_at,
                evidence_count=evidence_count,
            )
        )
    return ServiceListResponse(items=items)


@router.get("/services/{service_id}", response_model=ServiceDetailResponse)
def get_service(service_id: str, db: Session = Depends(get_db)) -> ServiceDetailResponse:
    service = db.query(Service).filter_by(id=service_id).first()
    if not service:
        return ServiceDetailResponse(
            id=service_id,
            display_name="unknown",
            primary_domain="unknown",
            category=None,
            confidence="low",
            confidence_reason="service not found",
            first_seen_at=None,
            last_seen_at=None,
            evidence=[],
        )
    links = (
        db.query(ServiceEvidenceLink, EvidenceEmail)
        .join(EvidenceEmail, EvidenceEmail.id == ServiceEvidenceLink.evidence_email_id)
        .filter(ServiceEvidenceLink.service_id == service.id)
        .order_by(EvidenceEmail.sent_at.desc())
        .limit(50)
        .all()
    )
    evidence_items = [
        ServiceEvidenceItem(
            id=str(ev.id),
            from_address=ev.from_address,
            subject=ev.subject,
            sent_at=ev.sent_at,
            evidence_type=ev.evidence_type,
            match_reason=link.match_reason,
        )
        for link, ev in links
    ]
    return ServiceDetailResponse(
        id=str(service.id),
        display_name=service.display_name,
        primary_domain=service.primary_domain,
        category=service.category,
        confidence=service.confidence,
        confidence_reason=service.confidence_reason,
        first_seen_at=service.first_seen_at,
        last_seen_at=service.last_seen_at,
        evidence=evidence_items,
    )
