from fastapi import APIRouter, Depends, File, UploadFile
from fastapi import Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
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
    user: User = Depends(get_current_user),
) -> dict:
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
            confidence, _reason = score_confidence([], match.match_type != "unknown")
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


@router.get("/imports/history")
def import_history(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    query = db.query(ImportRun).filter(ImportRun.user_id == user.id)
    total = query.count()
    rows = (
        query.order_by(ImportRun.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    items = [
        {
            "id": str(row.id),
            "source": row.source,
            "status": row.status,
            "imported_count": row.imported_count,
            "notes": row.notes,
            "created_at": row.created_at.isoformat(),
        }
        for row in rows
    ]
    return {"items": items, "total": total, "page": page, "page_size": page_size}
