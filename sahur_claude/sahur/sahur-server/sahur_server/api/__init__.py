from fastapi import APIRouter

from sahur_server.api.issues import router as issues_router
from sahur_server.api.slack import router as slack_router
from sahur_server.api.health import router as health_router

# Create the main API router
api_router = APIRouter()

# Include the routers
api_router.include_router(issues_router, prefix="/issues", tags=["issues"])
api_router.include_router(slack_router, prefix="/slack", tags=["slack"])
api_router.include_router(health_router, prefix="/health", tags=["health"])

__all__ = ["api_router"]
