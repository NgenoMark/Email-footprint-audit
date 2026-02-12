from collections.abc import Generator

from fastapi import Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models.user import User
from app.db.session import get_db as get_db_session


def get_db() -> Generator:
    yield from get_db_session()


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    x_user_email: str | None = Header(default=None),
) -> User:
    email = (x_user_email or request.cookies.get(settings.session_cookie_name) or "").strip().lower()

    if email:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(email=email, display_name=email)
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    if settings.allow_legacy_single_user_fallback:
        # Server-rendered frontend calls may not forward browser session context.
        # Fall back to the latest local user to keep local single-operator UX working.
        fallback_user = db.query(User).order_by(User.updated_at.desc()).first()
        if fallback_user:
            return fallback_user

    raise HTTPException(
        status_code=401,
        detail="No active user session. Provide X-User-Email header or connect Gmail first.",
    )
