from fastapi import FastAPI
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from .dummy_github import get_github_file

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.warning("DATABASE_URL environment variable not set. Using default connection.")

# Get vector database URL from environment variables
VECTORDATABASE_URL = os.getenv("VECTORDATABASE_URL")
if not VECTORDATABASE_URL:
    logger.warning("VECTORDATABASE_URL environment variable not set. Using default connection.")

app = FastAPI()

@app.get("/github/file")
async def github_file(filename: str):
    logger.info(f"Fetching GitHub file: {filename}")
    return get_github_file(filename)
