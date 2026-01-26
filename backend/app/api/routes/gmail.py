from fastapi import APIRouter

router = APIRouter()


@router.get("/gmail/status")
def gmail_status() -> dict:
    return {"connected": False}
