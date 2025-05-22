import os
import sys
import logging
import argparse
import asyncio
from contextlib import asynccontextmanager

from sqlalchemy.orm import Session
from dotenv import load_dotenv

from sahur_batch.database import get_db
from sahur_batch.processor import IssueProcessor

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


async def process_issue(tracking_id: str) -> bool:
    """
    Process an issue.
    
    Args:
        tracking_id: The ID of the issue tracking record
        
    Returns:
        True if processing was successful, False otherwise
    """
    # Get database session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Initialize processor
        processor = IssueProcessor(tracking_id, db)
        
        # Initialize processor
        if not await processor.initialize():
            logger.error(f"Failed to initialize processor for tracking ID: {tracking_id}")
            return False
        
        # Process issue
        success = await processor.process()
        
        if success:
            logger.info(f"Successfully processed issue for tracking ID: {tracking_id}")
        else:
            logger.error(f"Failed to process issue for tracking ID: {tracking_id}")
        
        return success
    
    except Exception as e:
        logger.exception(f"Error processing issue: {e}")
        return False
    
    finally:
        # Close database session
        db_gen.close()


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description="SAHUR Batch Process")
    parser.add_argument(
        "--tracking-id",
        required=True,
        help="The ID of the issue tracking record to process",
    )
    
    return parser.parse_args()


def main() -> int:
    """
    Main entry point.
    
    Returns:
        Exit code
    """
    try:
        # Parse arguments
        args = parse_args()
        
        # Get tracking ID
        tracking_id = args.tracking_id
        
        # Process issue
        success = asyncio.run(process_issue(tracking_id))
        
        return 0 if success else 1
    
    except Exception as e:
        logger.exception(f"Unhandled error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
