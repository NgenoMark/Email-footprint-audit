from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models.connected_account import ConnectedAccount
from app.db.models.evidence_email import EvidenceEmail
from app.db.models.scan_run import ScanRun
from app.db.models.service import Service
from app.db.models.service_evidence_link import ServiceEvidenceLink
from app.db.models.user import User

router = APIRouter()


class DeleteDataResponse(BaseModel):
    deleted: bool


@router.post("/settings/delete-data", response_model=DeleteDataResponse)
def delete_data(db: Session = Depends(get_db)) -> DeleteDataResponse:
    user = db.query(User).order_by(User.created_at.asc()).first()
    if not user:
        return DeleteDataResponse(deleted=False)

    service_ids = [
        row[0] for row in db.query(Service.id).filter(Service.user_id == user.id).all()
    ]
    if service_ids:
        db.execute(
            delete(ServiceEvidenceLink).where(
                ServiceEvidenceLink.service_id.in_(service_ids)
            )
        )
    db.execute(delete(Service).where(Service.user_id == user.id))
    db.execute(delete(EvidenceEmail).where(EvidenceEmail.user_id == user.id))
    db.execute(delete(ScanRun).where(ScanRun.user_id == user.id))
    db.execute(delete(ConnectedAccount).where(ConnectedAccount.user_id == user.id))
    db.execute(delete(User).where(User.id == user.id))
    db.commit()
    return DeleteDataResponse(deleted=True)
