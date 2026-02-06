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
