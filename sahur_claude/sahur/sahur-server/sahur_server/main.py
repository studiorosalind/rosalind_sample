import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sahur_server.api import api_router
from sahur_server.database import create_tables

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Create the FastAPI application
app = FastAPI(
    title="SAHUR Server",
    description="API server and issue tracking manager for SAHUR",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, this should be restricted
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """
    Startup event handler.
    
    This function is called when the application starts up.
    """
    logger.info("Starting SAHUR Server")
    
    # Create database tables
    create_tables()
    
    logger.info("SAHUR Server started")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event handler.
    
    This function is called when the application shuts down.
    """
    logger.info("Shutting down SAHUR Server")


if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable or use default
    port = int(os.getenv("PORT", "8000"))
    
    # Run the application
    uvicorn.run(
        "sahur_server.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
    )
