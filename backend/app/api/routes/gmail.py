from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models.connected_account import ConnectedAccount
from app.db.models.user import User

router = APIRouter()


@router.get("/gmail/status")
def gmail_status(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    connected = db.query(ConnectedAccount).filter_by(provider="gmail", user_id=user.id).first()
    return {"connected": connected is not None}
