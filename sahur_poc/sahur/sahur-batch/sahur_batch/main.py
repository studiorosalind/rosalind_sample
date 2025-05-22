import asyncio
from fastapi import FastAPI, WebSocket
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from .agent_runner import run_agent_analysis

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.warning("DATABASE_URL environment variable not set. Using default connection.")

# Get vector database URL from environment variables
VECTORDATABASE_URL = os.getenv("VECTORDATABASE_URL")
if not VECTORDATABASE_URL:
    logger.warning("VECTORDATABASE_URL environment variable not set. Using default connection.")

app = FastAPI()

@app.websocket("/ws/issue/{issueTrackingId}")
async def websocket_endpoint(websocket: WebSocket, issueTrackingId: str):
    await websocket.accept()
    logger.info(f"WebSocket connection established for issue: {issueTrackingId}")
    # 실제 환경에서는 이슈 분석 결과를 실시간으로 스트림
    async for update in run_agent_analysis(issueTrackingId):
        await websocket.send_json(update)
