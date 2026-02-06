from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models.user import User
from app.utils.domain_map import list_overrides, upsert_override

router = APIRouter()


class DomainMapRequest(BaseModel):
    domain: str
    service_name: str
    category: str | None = None


@router.get("/domain-map")
def get_domain_overrides(db: Session = Depends(get_db)) -> dict:
    user = db.query(User).order_by(User.created_at.asc()).first()
    if not user:
        return {"items": []}
    return {"items": list_overrides(db)}


@router.post("/domain-map")
def upsert_domain_override(
    payload: DomainMapRequest, db: Session = Depends(get_db)
) -> dict:
    try:
        upsert_override(db, payload.domain, payload.service_name, payload.category)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"updated": True}
