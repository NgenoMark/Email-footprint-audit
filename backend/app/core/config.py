import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    project_name: str = os.getenv("PROJECT_NAME", "Email Footprint Audit API")
    api_prefix: str = os.getenv("API_PREFIX", "/api")
    cors_origins: str = os.getenv("CORS_ORIGINS", "*")


settings = Settings()
