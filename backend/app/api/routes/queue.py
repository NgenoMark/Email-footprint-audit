from fastapi import APIRouter

from app.core.config import settings
from app.core.queue import queue_health

router = APIRouter()


@router.get("/queue/health")
def get_queue_health() -> dict:
    if not settings.use_rq:
        return {"use_rq": False, "healthy": True, "queue_depth": 0}
    status = queue_health()
    status["use_rq"] = True
    return status
