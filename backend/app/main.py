from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.api.routes import auth, domain_map, evidence, exports, gmail, health, scans, services, settings
from app.core.config import settings as app_settings
from app.core.logging import setup_logging

load_dotenv()
setup_logging()

app = FastAPI(
    title=app_settings.project_name,
    openapi_url=f"{app_settings.api_prefix}/openapi.json",
)

origins = [origin.strip() for origin in app_settings.cors_origins.split(",") if origin]
if origins == ["*"]:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(health.router, prefix=app_settings.api_prefix, tags=["health"])
app.include_router(auth.router, prefix=app_settings.api_prefix, tags=["auth"])
app.include_router(gmail.router, prefix=app_settings.api_prefix, tags=["gmail"])
app.include_router(scans.router, prefix=app_settings.api_prefix, tags=["scans"])
app.include_router(services.router, prefix=app_settings.api_prefix, tags=["services"])
app.include_router(evidence.router, prefix=app_settings.api_prefix, tags=["evidence"])
app.include_router(exports.router, prefix=app_settings.api_prefix, tags=["exports"])
app.include_router(settings.router, prefix=app_settings.api_prefix, tags=["settings"])
app.include_router(domain_map.router, prefix=app_settings.api_prefix, tags=["domain-map"])
