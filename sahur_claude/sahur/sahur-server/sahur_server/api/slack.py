import os
import hmac
import hashlib
import time
import logging
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Request, status, Header
from sqlalchemy.orm import Session

from sahur_server.database import get_db
from sahur_server.models import SlackEventRequest
from sahur_server.services import process_slack_event

router = APIRouter()
logger = logging.getLogger(__name__)

# Get Slack signing secret from environment variable
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET", "")


async def verify_slack_request(
    request: Request,
    x_slack_request_timestamp: str = Header(...),
    x_slack_signature: str = Header(...),
):
    """
    Verify that the request is coming from Slack.
    
    Args:
        request: The request object
        x_slack_request_timestamp: The X-Slack-Request-Timestamp header
        x_slack_signature: The X-Slack-Signature header
        
    Raises:
        HTTPException: If the request is invalid
    """
    if not SLACK_SIGNING_SECRET:
        logger.warning("SLACK_SIGNING_SECRET is not set, skipping verification")
        return
    
    # Check if the timestamp is recent
    timestamp = int(x_slack_request_timestamp)
    current_timestamp = int(time.time())
    
    if abs(current_timestamp - timestamp) > 60 * 5:
        # The request is older than 5 minutes
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Slack request timestamp is too old",
        )
    
    # Get the request body
    body = await request.body()
    
    # Create the signature base string
    sig_basestring = f"v0:{timestamp}:{body.decode('utf-8')}"
    
    # Create the signature
    signature = (
        "v0="
        + hmac.new(
            SLACK_SIGNING_SECRET.encode("utf-8"),
            sig_basestring.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
    )
    
    # Compare the signatures
    if not hmac.compare_digest(signature, x_slack_signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Slack signature",
        )


@router.post("/events")
async def slack_events(
    request: Request,
    event_request: SlackEventRequest,
    db: Session = Depends(get_db),
):
    """
    Handle Slack events.
    
    This endpoint is called by Slack when an event occurs.
    """
    # Verify the request
    await verify_slack_request(request)
    
    # Handle URL verification
    if event_request.type == "url_verification":
        return {"challenge": event_request.challenge}
    
    # Handle events
    if event_request.type == "event_callback":
        event_data = event_request.event
        
        # Process the event
        issue = process_slack_event(db, event_data)
        
        if issue:
            return {
                "status": "success",
                "message": f"Issue created: {issue.id}",
                "issue_id": issue.id,
            }
    
    return {"status": "success"}
