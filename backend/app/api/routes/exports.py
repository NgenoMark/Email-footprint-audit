from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ExportRequest(BaseModel):
    format: str


class ExportResponse(BaseModel):
    url: str


@router.post("/exports", response_model=ExportResponse)
def create_export(payload: ExportRequest) -> ExportResponse:
    return ExportResponse(url="/exports/2024-01-01/services.csv")
