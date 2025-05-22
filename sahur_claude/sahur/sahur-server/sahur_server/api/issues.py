from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from sahur_server.database import get_db
from sahur_server.models import (
    IssueCreate,
    IssueUpdate,
    IssueResponse,
    IssueTrackingCreate,
    IssueTrackingUpdate,
    IssueTrackingResponse,
    IssueMessageCreate,
    IssueMessageResponse,
)
from sahur_server.services import (
    create_issue,
    get_issue,
    get_issues,
    update_issue,
    delete_issue,
    create_issue_tracking,
    get_issue_tracking,
    get_issue_tracking_by_issue_id,
    update_issue_tracking,
    create_issue_message,
    get_issue_messages,
    start_batch_process,
)
from sahur_server.websockets import manager

router = APIRouter()


@router.post("/", response_model=IssueResponse, status_code=status.HTTP_201_CREATED)
def create_issue_endpoint(issue_create: IssueCreate, db: Session = Depends(get_db)):
    """
    Create a new issue.
    """
    db_issue = create_issue(db, issue_create)
    
    # Create issue tracking
    tracking_create = IssueTrackingCreate(issue_id=db_issue.id)
    db_tracking = create_issue_tracking(db, tracking_create)
    
    # Start batch process
    batch_process_id = start_batch_process(db_tracking.id)
    
    # Update tracking with batch process ID
    tracking_update = IssueTrackingUpdate(batch_process_id=batch_process_id)
    update_issue_tracking(db, db_tracking.id, tracking_update)
    
    # Create response with tracking ID
    response = IssueResponse.model_validate(db_issue)
    response.tracking_id = db_tracking.id
    
    return response


@router.get("/{issue_id}", response_model=IssueResponse)
def get_issue_endpoint(issue_id: str, db: Session = Depends(get_db)):
    """
    Get an issue by ID.
    """
    db_issue = get_issue(db, issue_id)
    
    # Get tracking ID if available
    try:
        db_tracking = get_issue_tracking_by_issue_id(db, issue_id)
        tracking_id = db_tracking.id
    except HTTPException:
        tracking_id = None
    
    # Create response with tracking ID
    response = IssueResponse.model_validate(db_issue)
    response.tracking_id = tracking_id
    
    return response


@router.get("/", response_model=List[IssueResponse])
def get_issues_endpoint(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    source: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Get a list of issues.
    """
    db_issues = get_issues(db, skip, limit, status, source)
    
    # Create responses with tracking IDs
    responses = []
    for db_issue in db_issues:
        response = IssueResponse.model_validate(db_issue)
        
        # Get tracking ID if available
        try:
            db_tracking = get_issue_tracking_by_issue_id(db, db_issue.id)
            response.tracking_id = db_tracking.id
        except HTTPException:
            response.tracking_id = None
        
        responses.append(response)
    
    return responses


@router.put("/{issue_id}", response_model=IssueResponse)
def update_issue_endpoint(issue_id: str, issue_update: IssueUpdate, db: Session = Depends(get_db)):
    """
    Update an issue.
    """
    db_issue = update_issue(db, issue_id, issue_update)
    
    # Get tracking ID if available
    try:
        db_tracking = get_issue_tracking_by_issue_id(db, issue_id)
        tracking_id = db_tracking.id
    except HTTPException:
        tracking_id = None
    
    # Create response with tracking ID
    response = IssueResponse.model_validate(db_issue)
    response.tracking_id = tracking_id
    
    return response


@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issue_endpoint(issue_id: str, db: Session = Depends(get_db)):
    """
    Delete an issue.
    """
    delete_issue(db, issue_id)
    return None


@router.get("/{issue_id}/tracking", response_model=IssueTrackingResponse)
def get_issue_tracking_endpoint(issue_id: str, db: Session = Depends(get_db)):
    """
    Get tracking information for an issue.
    """
    db_tracking = get_issue_tracking_by_issue_id(db, issue_id)
    return IssueTrackingResponse.model_validate(db_tracking)


@router.put("/{issue_id}/tracking", response_model=IssueTrackingResponse)
def update_issue_tracking_endpoint(
    issue_id: str, tracking_update: IssueTrackingUpdate, db: Session = Depends(get_db)
):
    """
    Update tracking information for an issue.
    """
    db_tracking = get_issue_tracking_by_issue_id(db, issue_id)
    db_tracking = update_issue_tracking(db, db_tracking.id, tracking_update)
    return IssueTrackingResponse.model_validate(db_tracking)


@router.get("/{issue_id}/messages", response_model=List[IssueMessageResponse])
def get_issue_messages_endpoint(issue_id: str, db: Session = Depends(get_db)):
    """
    Get all messages for an issue.
    """
    db_messages = get_issue_messages(db, issue_id)
    return [IssueMessageResponse.model_validate(msg) for msg in db_messages]


@router.post("/{issue_id}/messages", response_model=IssueMessageResponse)
async def create_issue_message_endpoint(
    issue_id: str, message_create: IssueMessageCreate, db: Session = Depends(get_db)
):
    """
    Create a new message for an issue.
    """
    # Override issue_id from path
    message_create.issue_id = issue_id
    
    # Create the message
    db_message = create_issue_message(db, message_create)
    
    # Broadcast the message to WebSocket clients
    await manager.broadcast_message(
        db_message.role, db_message.content, issue_id, db_message.id
    )
    
    return IssueMessageResponse.model_validate(db_message)


@router.websocket("/ws/{issue_id}")
async def websocket_endpoint(websocket: WebSocket, issue_id: str, db: Session = Depends(get_db)):
    """
    WebSocket endpoint for real-time updates.
    """
    # Check if the issue exists
    get_issue(db, issue_id)
    
    # Connect the WebSocket
    await manager.connect(websocket, issue_id)
    
    try:
        # Send initial messages
        db_messages = get_issue_messages(db, issue_id)
        for msg in db_messages:
            await manager.send_personal_message(
                {
                    "type": "message",
                    "role": msg.role,
                    "content": msg.content,
                    "issue_id": issue_id,
                    "message_id": msg.id,
                },
                websocket,
            )
        
        # Send tracking information if available
        try:
            db_tracking = get_issue_tracking_by_issue_id(db, issue_id)
            await manager.send_personal_message(
                {
                    "type": "status",
                    "status": db_tracking.status,
                    "issue_id": issue_id,
                },
                websocket,
            )
            
            if db_tracking.cause_context:
                await manager.send_personal_message(
                    {
                        "type": "context",
                        "context_type": "cause_context",
                        "context": db_tracking.cause_context,
                        "issue_id": issue_id,
                    },
                    websocket,
                )
            
            if db_tracking.history_context:
                await manager.send_personal_message(
                    {
                        "type": "context",
                        "context_type": "history_context",
                        "context": db_tracking.history_context,
                        "issue_id": issue_id,
                    },
                    websocket,
                )
            
            if db_tracking.solution:
                await manager.send_personal_message(
                    {
                        "type": "solution",
                        "solution": db_tracking.solution,
                        "issue_id": issue_id,
                    },
                    websocket,
                )
        except HTTPException:
            pass
        
        # Listen for messages from the client
        while True:
            data = await websocket.receive_json()
            
            # Handle user messages
            if data.get("type") == "message":
                content = data.get("content", "")
                
                # Create a new message
                message_create = IssueMessageCreate(
                    issue_id=issue_id,
                    role="user",
                    content=content,
                )
                
                db_message = create_issue_message(db, message_create)
                
                # Broadcast the message to all clients
                await manager.broadcast_message(
                    db_message.role, db_message.content, issue_id, db_message.id
                )
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, issue_id)
