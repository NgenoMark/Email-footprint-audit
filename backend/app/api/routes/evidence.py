from datetime import datetime, timezone

from fastapi import APIRouter, Query
from pydantic import BaseModel

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


@router.get("/evidence", response_model=EvidenceListResponse)
def list_evidence(
    service_id: str | None = Query(default=None),
    evidence_type: str | None = Query(default=None, alias="type"),
) -> EvidenceListResponse:
    now = datetime.now(timezone.utc)
    return EvidenceListResponse(
        items=[
            EvidenceItem(
                id="ev-0001",
                from_address="no-reply@substack.com",
                from_domain="substack.com",
                subject="Confirm your email",
                sent_at=now,
                evidence_type="verify",
                snippet="Click the button to confirm...",
            )
        ]
    )
