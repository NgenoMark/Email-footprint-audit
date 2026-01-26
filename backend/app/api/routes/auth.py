from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import encrypt_token
from app.db.models.connected_account import ConnectedAccount
from app.db.models.user import User
from app.services.gmail_client import GmailClient
from app.services.gmail_oauth import build_auth_url, exchange_code_for_tokens
from app.core.config import settings

router = APIRouter()


@router.get("/auth/gmail/start")
def gmail_oauth_start() -> dict:
    try:
        return {"url": build_auth_url()}
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/auth/gmail/callback")
def gmail_oauth_callback(
    code: str = Query(default=""),
    db: Session = Depends(get_db),
) -> dict:
    if not code:
        raise HTTPException(status_code=400, detail="Missing code")
    tokens = exchange_code_for_tokens(code)
    try:
        client = GmailClient(
            access_token=tokens["access_token"],
            refresh_token=tokens.get("refresh_token") or "",
            client_id=settings.google_client_id,
            client_secret=settings.google_client_secret,
            token_uri=tokens["token_uri"],
            scopes=tokens["scopes"],
        )
        email = client.get_profile_email()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Failed to resolve Gmail profile") from exc
    if not email:
        raise HTTPException(status_code=500, detail="Could not resolve Gmail address")

    user = db.query(User).filter_by(email=email).first()
    if not user:
        user = User(email=email, display_name=email)
        db.add(user)
        db.commit()
        db.refresh(user)

    connected = (
        db.query(ConnectedAccount)
        .filter_by(provider="gmail", provider_account_id=email)
        .first()
    )
    if not connected:
        try:
            connected = ConnectedAccount(
                user_id=user.id,
                provider="gmail",
                provider_account_id=email,
                access_token_enc=encrypt_token(tokens["access_token"]),
                refresh_token_enc=encrypt_token(tokens.get("refresh_token") or ""),
                scopes=tokens["scopes"],
            )
        except ValueError as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
        db.add(connected)
    else:
        try:
            connected.access_token_enc = encrypt_token(tokens["access_token"])
            if tokens.get("refresh_token"):
                connected.refresh_token_enc = encrypt_token(tokens["refresh_token"])
        except ValueError as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc
        connected.scopes = tokens["scopes"]
    db.commit()

    return {"connected": True, "email": email}
