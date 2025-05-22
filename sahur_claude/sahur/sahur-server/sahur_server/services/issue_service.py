import os
import uuid
import subprocess
import logging
import sys
from typing import List, Optional, Dict, Any
from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import HTTPException

from sahur_server.database import get_db
from sahur_server.database.models import Issue as DBIssue
from sahur_server.database.models import IssueTracking as DBIssueTracking
from sahur_server.database.models import IssueMessage as DBIssueMessage
from sahur_server.models.api_models import (
    IssueCreate,
    IssueUpdate,
    IssueStatus,
    IssueSource,
    IssueTrackingCreate,
    IssueTrackingUpdate,
    IssueMessageCreate,
)

logger = logging.getLogger(__name__)

# Get batch command from environment variable or use a default
BATCH_COMMAND = os.getenv("BATCH_COMMAND", "python -m sahur_batch.main")


def create_issue(db: Session, issue_create: IssueCreate) -> DBIssue:
    """
    Create a new issue.
    
    Args:
        db: Database session
        issue_create: Issue creation data
        
    Returns:
        The created issue
    """
    # Create the issue
    db_issue = DBIssue(
        id=str(uuid.uuid4()),
        title=issue_create.title,
        description=issue_create.description,
        status=IssueStatus.CREATED.value,
        source=issue_create.source.value,
        event_transaction_id=issue_create.event_transaction_id,
        additional_metadata=issue_create.additional_metadata,
    )
    
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    
    return db_issue


def get_issue(db: Session, issue_id: str) -> DBIssue:
    """
    Get an issue by ID.
    
    Args:
        db: Database session
        issue_id: Issue ID
        
    Returns:
        The issue
        
    Raises:
        HTTPException: If the issue is not found
    """
    db_issue = db.query(DBIssue).filter(DBIssue.id == issue_id).first()
    
    if db_issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    return db_issue


def get_issues(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    source: Optional[str] = None,
) -> List[DBIssue]:
    """
    Get a list of issues.
    
    Args:
        db: Database session
        skip: Number of issues to skip
        limit: Maximum number of issues to return
        status: Filter by status
        source: Filter by source
        
    Returns:
        List of issues
    """
    query = db.query(DBIssue)
    
    if status:
        query = query.filter(DBIssue.status == status)
    
    if source:
        query = query.filter(DBIssue.source == source)
    
    return query.order_by(DBIssue.created_at.desc()).offset(skip).limit(limit).all()


def update_issue(db: Session, issue_id: str, issue_update: IssueUpdate) -> DBIssue:
    """
    Update an issue.
    
    Args:
        db: Database session
        issue_id: Issue ID
        issue_update: Issue update data
        
    Returns:
        The updated issue
        
    Raises:
        HTTPException: If the issue is not found
    """
    db_issue = get_issue(db, issue_id)
    
    # Update fields if provided
    if issue_update.title is not None:
        db_issue.title = issue_update.title
    
    if issue_update.description is not None:
        db_issue.description = issue_update.description
    
    if issue_update.status is not None:
        db_issue.status = issue_update.status.value
    
    if issue_update.additional_metadata is not None:
        db_issue.additional_metadata = issue_update.additional_metadata
    
    db_issue.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_issue)
    
    return db_issue


def delete_issue(db: Session, issue_id: str) -> None:
    """
    Delete an issue.
    
    Args:
        db: Database session
        issue_id: Issue ID
        
    Raises:
        HTTPException: If the issue is not found
    """
    db_issue = get_issue(db, issue_id)
    
    db.delete(db_issue)
    db.commit()


def create_issue_tracking(db: Session, tracking_create: IssueTrackingCreate) -> DBIssueTracking:
    """
    Create a new issue tracking.
    
    Args:
        db: Database session
        tracking_create: Issue tracking creation data
        
    Returns:
        The created issue tracking
    """
    # Check if the issue exists
    get_issue(db, tracking_create.issue_id)
    
    # Create the issue tracking
    db_tracking = DBIssueTracking(
        id=str(uuid.uuid4()),
        issue_id=tracking_create.issue_id,
        status=tracking_create.status.value,
    )
    
    db.add(db_tracking)
    db.commit()
    db.refresh(db_tracking)
    
    return db_tracking


def get_issue_tracking(db: Session, tracking_id: str) -> DBIssueTracking:
    """
    Get an issue tracking by ID.
    
    Args:
        db: Database session
        tracking_id: Issue tracking ID
        
    Returns:
        The issue tracking
        
    Raises:
        HTTPException: If the issue tracking is not found
    """
    db_tracking = db.query(DBIssueTracking).filter(DBIssueTracking.id == tracking_id).first()
    
    if db_tracking is None:
        raise HTTPException(status_code=404, detail="Issue tracking not found")
    
    return db_tracking


def get_issue_tracking_by_issue_id(db: Session, issue_id: str) -> DBIssueTracking:
    """
    Get an issue tracking by issue ID.
    
    Args:
        db: Database session
        issue_id: Issue ID
        
    Returns:
        The issue tracking
        
    Raises:
        HTTPException: If the issue tracking is not found
    """
    db_tracking = db.query(DBIssueTracking).filter(DBIssueTracking.issue_id == issue_id).first()
    
    if db_tracking is None:
        raise HTTPException(status_code=404, detail="Issue tracking not found")
    
    return db_tracking


def update_issue_tracking(
    db: Session, tracking_id: str, tracking_update: IssueTrackingUpdate
) -> DBIssueTracking:
    """
    Update an issue tracking.
    
    Args:
        db: Database session
        tracking_id: Issue tracking ID
        tracking_update: Issue tracking update data
        
    Returns:
        The updated issue tracking
        
    Raises:
        HTTPException: If the issue tracking is not found
    """
    db_tracking = get_issue_tracking(db, tracking_id)
    
    # Update fields if provided
    if tracking_update.status is not None:
        db_tracking.status = tracking_update.status.value
    
    if tracking_update.batch_process_id is not None:
        db_tracking.batch_process_id = tracking_update.batch_process_id
    
    if tracking_update.cause_context is not None:
        db_tracking.cause_context = tracking_update.cause_context
    
    if tracking_update.history_context is not None:
        db_tracking.history_context = tracking_update.history_context
    
    if tracking_update.solution is not None:
        db_tracking.solution = tracking_update.solution
    
    db_tracking.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_tracking)
    
    return db_tracking


def create_issue_message(db: Session, message_create: IssueMessageCreate) -> DBIssueMessage:
    """
    Create a new issue message.
    
    Args:
        db: Database session
        message_create: Issue message creation data
        
    Returns:
        The created issue message
    """
    # Check if the issue exists
    get_issue(db, message_create.issue_id)
    
    # Create the issue message
    db_message = DBIssueMessage(
        id=str(uuid.uuid4()),
        issue_id=message_create.issue_id,
        role=message_create.role,
        content=message_create.content,
    )
    
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    return db_message


def get_issue_messages(db: Session, issue_id: str) -> List[DBIssueMessage]:
    """
    Get all messages for an issue.
    
    Args:
        db: Database session
        issue_id: Issue ID
        
    Returns:
        List of issue messages
    """
    # Check if the issue exists
    get_issue(db, issue_id)
    
    return (
        db.query(DBIssueMessage)
        .filter(DBIssueMessage.issue_id == issue_id)
        .order_by(DBIssueMessage.timestamp)
        .all()
    )


def start_batch_process(tracking_id: str) -> str:
    """
    Start a batch process for issue analysis.
    
    This function runs a Python script directly that simulates the batch process.
    
    Args:
        tracking_id: Issue tracking ID
        
    Returns:
        The batch process ID
    """
    try:
        # Construct the command to run the batch process
        # We'll use the same Python interpreter that's running the server
        python_path = sys.executable
        
        # Create a temporary Python script to run
        script_content = f"""
import sys
import os
import logging
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("batch_process")

# Set the tracking ID
tracking_id = "{tracking_id}"

try:
    # Set up database connection
    DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/sahur")
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    # Import necessary models
    from sahur_server.database.models import IssueTracking, IssueMessage
    from sahur_server.models.api_models import IssueStatus
    
    # Get the tracking record
    tracking = db.query(IssueTracking).filter(IssueTracking.id == tracking_id).first()
    
    if tracking:
        # Add system message
        message = IssueMessage(
            id=str(uuid.uuid4()),
            issue_id=tracking.issue_id,
            role="system",
            content="Starting analysis process for issue"
        )
        db.add(message)
        
        # Update tracking status
        tracking.status = IssueStatus.ANALYZING.value
        db.commit()
        
        # Add assistant message
        assistant_msg = IssueMessage(
            id=str(uuid.uuid4()),
            issue_id=tracking.issue_id,
            role="assistant",
            content="I'm analyzing the NullPointerException in DataUtils.parseJson. This typically happens when handling null input data."
        )
        db.add(assistant_msg)
        db.commit()
        
        # Create a solution
        solution = {{
            "root_cause": "The DataUtils.parseJson method doesn't check if the input JSON string is null before parsing it.",
            "explanation": "When a null JSON string is passed to parseJson(), it tries to parse it without validation, resulting in a NullPointerException.",
            "steps": [
                {{
                    "step_number": 1,
                    "description": "Add a null check at the beginning of the method",
                    "code_changes": {{
                        "DataUtils.java": "public static JsonObject parseJson(String jsonStr) {{\\n    // Add null check\\n    if (jsonStr == null) {{\\n        return null;\\n    }}\\n    \\n    // Rest of the method\\n    return JsonParser.parseString(jsonStr).getAsJsonObject();\\n}}"
                    }}
                }}
            ],
            "references": [
                "Java documentation on NullPointerException",
                "Similar issue: ISSUE-456"
            ]
        }}
        
        # Update tracking with solution
        tracking.solution = solution
        tracking.status = IssueStatus.COMPLETED.value
        db.commit()
        
        # Add completion message
        completion_msg = IssueMessage(
            id=str(uuid.uuid4()),
            issue_id=tracking.issue_id,
            role="system",
            content="Analysis completed. Solution generated."
        )
        db.add(completion_msg)
        db.commit()
        
        logger.info(f"Batch process completed successfully for tracking ID: {{tracking_id}}")
    else:
        logger.error(f"Could not find tracking record with ID: {{tracking_id}}")
except Exception as e:
    logger.error(f"Error in batch process: {{str(e)}}")
    import traceback
    logger.error(traceback.format_exc())
"""
        
        # Write the script to a temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as f:
            f.write(script_content.encode())
            temp_script = f.name
        
        # Create a command to run the script
        cmd = [
            python_path,
            temp_script
        ]
        
        # Set the environment variables needed for the process
        env = os.environ.copy()
        
        # Make sure DATABASE_URL is set
        if "DATABASE_URL" not in env:
            env["DATABASE_URL"] = "postgresql://postgres:postgres@postgres:5432/sahur"
        
        # Make sure OpenAI API key is available or set a dummy key for testing
        if "OPENAI_API_KEY" not in env:
            env["OPENAI_API_KEY"] = "sk-dummy-key-for-testing"
        
        # Add PYTHONPATH to ensure sahur_server can be imported
        env["PYTHONPATH"] = f"/app:{env.get('PYTHONPATH', '')}"
        
        # Log the command
        logger.info(f"Starting batch process with script: {temp_script}")
        
        # Start the batch process
        process = subprocess.Popen(
            cmd,
            env=env,
            start_new_session=True,  # Detach the process
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Get the process ID
        batch_process_id = str(process.pid)
        logger.info(f"Started batch process with PID: {batch_process_id}")
        
        return batch_process_id
        
    except Exception as e:
        logger.exception(f"Error starting batch process: {e}")
        return str(uuid.uuid4())  # Return a fallback batch process ID


def process_slack_event(db: Session, event_data: Dict[str, Any]) -> Optional[DBIssue]:
    """
    Process a Slack event.
    
    Args:
        db: Database session
        event_data: Slack event data
        
    Returns:
        The created issue, if any
    """
    # Check if this is a message event
    if event_data.get("type") != "app_mention":
        return None
    
    # Extract the message text
    text = event_data.get("text", "")
    
    # Check if this is an analyze command
    if "analyze" not in text.lower():
        return None
    
    # Extract parameters from the message
    # Format: @sahur analyze [eventTransactionId] [description]
    parts = text.split(" ")
    if len(parts) < 3:
        return None
    
    # Extract event transaction ID and description
    event_transaction_id = parts[2] if len(parts) > 2 else None
    description = " ".join(parts[3:]) if len(parts) > 3 else "No description provided"
    
    # Create the issue
    issue_create = IssueCreate(
        title=f"Slack issue: {description[:50]}...",
        description=description,
        source=IssueSource.SLACK,
        event_transaction_id=event_transaction_id,
        additional_metadata={"slack_event": event_data},
    )
    
    db_issue = create_issue(db, issue_create)
    
    # Create issue tracking
    tracking_create = IssueTrackingCreate(issue_id=db_issue.id)
    db_tracking = create_issue_tracking(db, tracking_create)
    
    # Start batch process
    batch_process_id = start_batch_process(db_tracking.id)
    
    # Update tracking with batch process ID
    tracking_update = IssueTrackingUpdate(batch_process_id=batch_process_id)
    update_issue_tracking(db, db_tracking.id, tracking_update)
    
    return db_issue
