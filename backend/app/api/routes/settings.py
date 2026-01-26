from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class DeleteDataResponse(BaseModel):
    deleted: bool


@router.post("/settings/delete-data", response_model=DeleteDataResponse)
def delete_data() -> DeleteDataResponse:
    return DeleteDataResponse(deleted=True)
