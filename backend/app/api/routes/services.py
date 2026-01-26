from datetime import datetime, timezone

from fastapi import APIRouter, Query
from pydantic import BaseModel

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
) -> ServiceListResponse:
    now = datetime.now(timezone.utc)
    item = ServiceListItem(
        id="svc-0001",
        display_name="Netflix",
        primary_domain="netflix.com",
        category="streaming",
        confidence="high",
        confidence_reason="welcome + receipts from official domain",
        first_seen_at=now,
        last_seen_at=now,
        evidence_count=5,
    )
    return ServiceListResponse(items=[item])


@router.get("/services/{service_id}", response_model=ServiceDetailResponse)
def get_service(service_id: str) -> ServiceDetailResponse:
    now = datetime.now(timezone.utc)
    return ServiceDetailResponse(
        id=service_id,
        display_name="Netflix",
        primary_domain="netflix.com",
        category="streaming",
        confidence="high",
        confidence_reason="welcome + receipts from official domain",
        first_seen_at=now,
        last_seen_at=now,
        evidence=[
            ServiceEvidenceItem(
                id="ev-0001",
                from_address="info@netflix.com",
                subject="Welcome to Netflix",
                sent_at=now,
                evidence_type="welcome",
                match_reason="domain_match",
            )
        ],
    )
