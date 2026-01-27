from collections import defaultdict
from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models.evidence_email import EvidenceEmail
from app.db.models.service import Service
from app.db.models.service_evidence_link import ServiceEvidenceLink
from app.services.confidence_scoring import score_confidence
from app.utils.domain_map import load_domain_map, resolve_service


def detect_and_upsert_services(db: Session, user_id) -> list[Service]:
    mapping = load_domain_map()
    evidence_rows = (
        db.query(EvidenceEmail)
        .filter(EvidenceEmail.user_id == user_id)
        .order_by(EvidenceEmail.sent_at.asc())
        .all()
    )

    grouped: dict[str, list[EvidenceEmail]] = defaultdict(list)
    for evidence in evidence_rows:
        if not evidence.from_domain:
            continue
        grouped[evidence.from_domain].append(evidence)

    services: list[Service] = []
    for from_domain, items in grouped.items():
        match = resolve_service(from_domain, mapping)
        primary_domain = match.matched_domain
        official = match.match_type in {"exact", "subdomain"}

        evidence_types = [item.evidence_type for item in items]
        confidence, reason = score_confidence(evidence_types, official)
        first_seen = min((item.sent_at for item in items), default=None)
        last_seen = max((item.sent_at for item in items), default=None)

        service = (
            db.query(Service)
            .filter_by(user_id=user_id, primary_domain=primary_domain)
            .first()
        )
        if not service:
            service = Service(
                user_id=user_id,
                display_name=match.display_name,
                primary_domain=primary_domain,
                category=match.category,
                confidence=confidence,
                confidence_reason=reason,
                first_seen_at=first_seen,
                last_seen_at=last_seen,
            )
            db.add(service)
            db.flush()
        else:
            service.display_name = match.display_name
            service.category = match.category
            service.confidence = confidence
            service.confidence_reason = reason
            service.first_seen_at = _min_datetime(service.first_seen_at, first_seen)
            service.last_seen_at = _max_datetime(service.last_seen_at, last_seen)

        for evidence in items:
            existing_link = (
                db.query(ServiceEvidenceLink)
                .filter_by(service_id=service.id, evidence_email_id=evidence.id)
                .first()
            )
            if existing_link:
                continue
            link = ServiceEvidenceLink(
                service_id=service.id,
                evidence_email_id=evidence.id,
                match_reason="domain_match" if official else "domain_guess",
            )
            db.add(link)

        services.append(service)

    return services


def _min_datetime(current: datetime | None, candidate: datetime | None) -> datetime | None:
    if current is None:
        return candidate
    if candidate is None:
        return current
    return min(current, candidate)


def _max_datetime(current: datetime | None, candidate: datetime | None) -> datetime | None:
    if current is None:
        return candidate
    if candidate is None:
        return current
    return max(current, candidate)
