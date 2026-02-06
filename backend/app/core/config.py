import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    project_name: str = os.getenv("PROJECT_NAME", "Email Footprint Audit API")
    api_prefix: str = os.getenv("API_PREFIX", "/api")
    cors_origins: str = os.getenv("CORS_ORIGINS", "*")
    google_client_id: str = os.getenv("GOOGLE_CLIENT_ID", "")
    google_client_secret: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    google_redirect_url: str = os.getenv(
        "OAUTH_REDIRECT_URL", "http://localhost:8000/api/auth/gmail/callback"
    )
    google_scopes: str = os.getenv(
        "GOOGLE_SCOPES", "https://www.googleapis.com/auth/gmail.readonly"
    )
    token_encryption_key: str = os.getenv("TOKEN_ENCRYPTION_KEY", "")
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    use_rq: bool = os.getenv("USE_RQ", "false").lower() in {"1", "true", "yes"}
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")


settings = Settings()
