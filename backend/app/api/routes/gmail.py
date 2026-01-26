from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models.connected_account import ConnectedAccount

router = APIRouter()


@router.get("/gmail/status")
def gmail_status(db: Session = Depends(get_db)) -> dict:
    connected = db.query(ConnectedAccount).filter_by(provider="gmail").first()
    return {"connected": connected is not None}
