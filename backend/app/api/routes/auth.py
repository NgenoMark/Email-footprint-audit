from fastapi import APIRouter

router = APIRouter()


@router.get("/auth/gmail/start")
def gmail_oauth_start() -> dict:
    return {"url": "https://accounts.google.com/o/oauth2/v2/auth?..."}


@router.get("/auth/gmail/callback")
def gmail_oauth_callback() -> dict:
    return {"connected": True}
