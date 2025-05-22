from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr


class IssueStatus(str, Enum):
    """Status of an issue in the SAHUR system."""
    CREATED = "created"
    ANALYZING = "analyzing"
    WAITING_FOR_INPUT = "waiting_for_input"
    GENERATING_SOLUTION = "generating_solution"
    COMPLETED = "completed"
    FAILED = "failed"


class IssueSource(str, Enum):
    """Source of an issue in the SAHUR system."""
    SLACK = "slack"
    API = "api"
    WEB = "web"
    AUTOMATED = "automated"


class IssueCreate(BaseModel):
    """Model for creating a new issue."""
    title: str
    description: str
    source: IssueSource = IssueSource.API
    event_transaction_id: Optional[str] = None
    additional_metadata: Optional[Dict[str, Any]] = None


class IssueUpdate(BaseModel):
    """Model for updating an existing issue."""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[IssueStatus] = None
    additional_metadata: Optional[Dict[str, Any]] = None


class IssueResponse(BaseModel):
    """Model for issue response."""
    id: str
    title: str
    description: str
    status: IssueStatus
    source: IssueSource
    created_at: datetime
    updated_at: datetime
    event_transaction_id: Optional[str] = None
    additional_metadata: Optional[Dict[str, Any]] = None
    tracking_id: Optional[str] = None

    class Config:
        from_attributes = True


class IssueTrackingCreate(BaseModel):
    """Model for creating a new issue tracking."""
    issue_id: str
    status: IssueStatus = IssueStatus.CREATED


class IssueTrackingUpdate(BaseModel):
    """Model for updating an existing issue tracking."""
    status: Optional[IssueStatus] = None
    batch_process_id: Optional[str] = None
    cause_context: Optional[Dict[str, Any]] = None
    history_context: Optional[Dict[str, Any]] = None
    solution: Optional[Dict[str, Any]] = None


class IssueTrackingResponse(BaseModel):
    """Model for issue tracking response."""
    id: str
    issue_id: str
    status: IssueStatus
    batch_process_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    cause_context: Optional[Dict[str, Any]] = None
    history_context: Optional[Dict[str, Any]] = None
    solution: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


class IssueMessageCreate(BaseModel):
    """Model for creating a new issue message."""
    issue_id: str
    role: str  # system, user, assistant
    content: str


class IssueMessageResponse(BaseModel):
    """Model for issue message response."""
    id: str
    issue_id: str
    role: str
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    """Model for creating a new user."""
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Model for user response."""
    id: str
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Model for authentication token."""
    access_token: str
    token_type: str


class SlackEventRequest(BaseModel):
    """Model for Slack event request."""
    token: Optional[str] = ""
    team_id: str
    api_app_id: str
    event: Dict[str, Any]
    type: str
    event_id: str
    event_time: int
    authed_users: Optional[List[str]] = Field(default_factory=list)
    challenge: Optional[str] = None


class HealthResponse(BaseModel):
    """Model for health check response."""
    status: str
    version: str
    timestamp: datetime
