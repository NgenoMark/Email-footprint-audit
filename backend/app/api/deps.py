from collections.abc import Generator

from app.db.session import get_db as get_db_session


def get_db() -> Generator:
    yield from get_db_session()
