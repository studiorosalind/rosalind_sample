from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union, Any

from pydantic import BaseModel, Field


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


class StackTraceFrame(BaseModel):
    """Represents a single frame in a stack trace."""
    file_path: str
    line_number: int
    method_name: str
    code_line: Optional[str] = None


class StackTrace(BaseModel):
    """Represents a stack trace from an error."""
    exception_type: str
    exception_message: str
    frames: List[StackTraceFrame]


class HttpRequest(BaseModel):
    """Represents an HTTP request associated with an issue."""
    method: str
    url: str
    headers: Dict[str, str]
    body: Optional[Any] = None
    timestamp: datetime


class HttpResponse(BaseModel):
    """Represents an HTTP response associated with an issue."""
    status_code: int
    headers: Dict[str, str]
    body: Optional[Any] = None
    timestamp: datetime


class KafkaMessage(BaseModel):
    """Represents a Kafka message associated with an issue."""
    topic: str
    partition: int
    offset: int
    key: Optional[str] = None
    value: Any
    timestamp: datetime
    headers: Optional[Dict[str, str]] = None


class DatabaseError(BaseModel):
    """Represents a database error associated with an issue."""
    error_code: str
    error_message: str
    query: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    timestamp: datetime


class CauseContext(BaseModel):
    """Context information about the cause of an issue."""
    stack_trace: Optional[StackTrace] = None
    http_requests: List[HttpRequest] = Field(default_factory=list)
    http_responses: List[HttpResponse] = Field(default_factory=list)
    kafka_messages: List[KafkaMessage] = Field(default_factory=list)
    database_errors: List[DatabaseError] = Field(default_factory=list)
    logs: List[str] = Field(default_factory=list)
    additional_context: Dict[str, Any] = Field(default_factory=dict)


class HistoricalIssue(BaseModel):
    """Represents a historical issue for reference."""
    issue_id: str
    title: str
    description: str
    root_cause: str
    solution: str
    similarity_score: float
    resolved_at: datetime


class HistoryContext(BaseModel):
    """Context information about similar historical issues."""
    similar_issues: List[HistoricalIssue] = Field(default_factory=list)
    relevant_code_changes: Dict[str, str] = Field(default_factory=dict)
    deployment_events: List[Dict[str, Any]] = Field(default_factory=list)


class IssueContext(BaseModel):
    """Complete context for an issue being analyzed."""
    cause_context: CauseContext = Field(default_factory=CauseContext)
    history_context: HistoryContext = Field(default_factory=HistoryContext)


class SolutionStep(BaseModel):
    """A step in the solution to an issue."""
    step_number: int
    description: str
    code_changes: Optional[Dict[str, str]] = None
    commands: Optional[List[str]] = None


class Solution(BaseModel):
    """A complete solution to an issue."""
    root_cause: str
    explanation: str
    steps: List[SolutionStep] = Field(default_factory=list)
    references: List[str] = Field(default_factory=list)


class Issue(BaseModel):
    """Represents an issue in the SAHUR system."""
    issue_id: str
    tracking_id: str
    title: str
    description: str
    status: IssueStatus
    source: IssueSource
    created_at: datetime
    updated_at: datetime
    event_transaction_id: Optional[str] = None
    additional_metadata: Dict[str, Any] = Field(default_factory=dict)
    context: IssueContext = Field(default_factory=IssueContext)
    solution: Optional[Solution] = None
