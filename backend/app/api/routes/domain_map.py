from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models.user import User
from app.utils.domain_map import list_overrides, upsert_override

router = APIRouter()


class DomainMapRequest(BaseModel):
    domain: str
    service_name: str
    category: str | None = None


@router.get("/domain-map")
def get_domain_overrides(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    _ = user
    return {"items": list_overrides(db)}


@router.post("/domain-map")
def upsert_domain_override(
    payload: DomainMapRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    _ = user
    try:
        upsert_override(db, payload.domain, payload.service_name, payload.category)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"updated": True}
