"""Top-level API router."""

from fastapi import APIRouter

from app.api.routes.config import router as config_router
from app.api.routes.health import router as health_router

api_router = APIRouter()
api_router.include_router(config_router, tags=["config"])
api_router.include_router(health_router, tags=["health"])
