from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models.import_run import ImportRun
from app.db.models.service import Service
from app.db.models.user import User
from app.services.confidence_scoring import score_confidence
from app.services.import_parsers import parse_password_manager_csv
from app.utils.domain_map import load_domain_map, resolve_service

router = APIRouter()

@router.post("/imports/password-manager")
def import_password_manager(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> dict:
    user = db.query(User).order_by(User.created_at.asc()).first()
    if not user:
        raise HTTPException(status_code=400, detail="No user found")

    content = file.file.read()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        text = content.decode("latin-1")

    domains = parse_password_manager_csv(text)
    mapping = load_domain_map(db)
    imported = 0
    for domain in domains:
        if not domain:
            continue

        match = resolve_service(domain, mapping)
        primary_domain = match.matched_domain
        service = (
            db.query(Service)
            .filter_by(user_id=user.id, primary_domain=primary_domain)
            .first()
        )
        if not service:
            confidence, reason = score_confidence([], match.match_type != "unknown")
            service = Service(
                user_id=user.id,
                display_name=match.display_name,
                primary_domain=primary_domain,
                category=match.category,
                confidence=confidence,
                confidence_reason="password manager import",
            )
            db.add(service)
            imported += 1
        else:
            service.category = service.category or match.category
        db.commit()

    db.add(
        ImportRun(
            user_id=user.id,
            source="password_manager",
            status="success",
            imported_count=imported,
        )
    )
    db.commit()
    return {"imported": imported}
