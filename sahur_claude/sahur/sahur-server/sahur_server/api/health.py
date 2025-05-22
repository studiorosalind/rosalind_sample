from datetime import datetime
from fastapi import APIRouter

from sahur_server.models import HealthResponse

router = APIRouter()


@router.get("/", response_model=HealthResponse)
def health_check():
    """
    Health check endpoint.
    
    This endpoint is used to check if the server is running.
    """
    return HealthResponse(
        status="ok",
        version="0.1.0",
        timestamp=datetime.utcnow(),
    )
