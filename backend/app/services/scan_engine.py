from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import decrypt_token
from app.db.models.connected_account import ConnectedAccount
from app.db.models.evidence_email import EvidenceEmail
from app.db.models.scan_run import ScanRun
from app.services.gmail_client import GmailClient
from app.utils.parsing import classify_evidence_type, extract_domain


def _parse_headers(headers: list[dict]) -> dict:
    parsed = {}
    for header in headers:
        name = header.get("name", "").lower()
        value = header.get("value", "")
        parsed[name] = value
    return parsed


def _parse_sent_date(value: str) -> datetime:
    if not value:
        return datetime.now(timezone.utc)
    try:
        parsed = parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed
    except (TypeError, ValueError):
        return datetime.now(timezone.utc)


def run_gmail_scan(
    db: Session,
    connected_account: ConnectedAccount,
    query: str,
    max_results: int = 50,
) -> ScanRun:
    scan = ScanRun(
        user_id=connected_account.user_id,
        connected_account_id=connected_account.id,
        status="running",
        query=query,
        started_at=datetime.now(timezone.utc),
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)

    try:
        client = GmailClient(
            access_token=decrypt_token(connected_account.access_token_enc),
            refresh_token=decrypt_token(connected_account.refresh_token_enc),
            client_id=settings.google_client_id,
            client_secret=settings.google_client_secret,
            token_uri="https://oauth2.googleapis.com/token",
            scopes=connected_account.scopes,
        )

        messages = client.list_messages(query=query, max_results=max_results)
        for message in messages:
            message_id = message.get("id")
            if not message_id:
                continue
            existing = (
                db.query(EvidenceEmail)
                .filter_by(provider="gmail", provider_message_id=message_id)
                .first()
            )
            if existing:
                continue
            data = client.get_message(message_id)
            headers = _parse_headers(data.get("payload", {}).get("headers", []))
            from_address = headers.get("from", "")
            subject = headers.get("subject", "")
            sent_at = _parse_sent_date(headers.get("date", ""))
            evidence = EvidenceEmail(
                user_id=connected_account.user_id,
                provider="gmail",
                provider_message_id=message_id,
                from_address=from_address,
                from_domain=extract_domain(from_address),
                subject=subject,
                snippet=data.get("snippet"),
                sent_at=sent_at,
                received_at=datetime.now(timezone.utc),
                evidence_type=classify_evidence_type(subject),
                raw_headers=headers,
            )
            db.add(evidence)

        scan.status = "success"
    except Exception as exc:  # noqa: BLE001
        scan.status = "failed"
        scan.error_message = str(exc)
    finally:
        scan.finished_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(scan)
    return scan
