from google_auth_oauthlib.flow import Flow

from app.core.config import settings


def _client_config() -> dict:
    if not settings.google_client_id or not settings.google_client_secret:
        raise ValueError("GOOGLE_CLIENT_ID/GOOGLE_CLIENT_SECRET not set")
    return {
        "web": {
            "client_id": settings.google_client_id,
            "client_secret": settings.google_client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [settings.google_redirect_url],
        }
    }


def build_auth_url() -> str:
    scopes = settings.google_scopes.replace(",", " ").split()
    flow = Flow.from_client_config(
        _client_config(),
        scopes=scopes,
        redirect_uri=settings.google_redirect_url,
    )
    auth_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    return auth_url


def exchange_code_for_tokens(code: str) -> dict:
    scopes = settings.google_scopes.replace(",", " ").split()
    flow = Flow.from_client_config(
        _client_config(),
        scopes=scopes,
        redirect_uri=settings.google_redirect_url,
    )
    flow.fetch_token(code=code)
    credentials = flow.credentials
    return {
        "access_token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "scopes": list(credentials.scopes or []),
        "expires_at": credentials.expiry,
    }
