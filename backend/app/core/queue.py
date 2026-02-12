from rq import Queue
from rq.job import Job
from redis import Redis

from app.core.config import settings


def get_queue() -> Queue:
    connection = Redis.from_url(settings.redis_url)
    return Queue("scans", connection=connection)


def enqueue_scan(func, *args, **kwargs) -> Job:
    queue = get_queue()
    return queue.enqueue(func, *args, **kwargs)


def queue_depth() -> int:
    queue = get_queue()
    return len(queue)


def queue_health() -> dict:
    try:
        queue = get_queue()
        queue.connection.ping()
        return {"healthy": True, "queue_depth": len(queue)}
    except Exception as exc:  # noqa: BLE001
        return {"healthy": False, "queue_depth": 0, "error": str(exc)}
