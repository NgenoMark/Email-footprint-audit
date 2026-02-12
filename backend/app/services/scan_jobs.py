from app.db.session import SessionLocal
from app.services.scan_engine import run_gmail_scan_by_id


def perform_scan_job(scan_id: str, connected_account_id: str, query: str) -> None:
    db = SessionLocal()
    try:
        run_gmail_scan_by_id(db, scan_id, connected_account_id, query)
    finally:
        db.close()
