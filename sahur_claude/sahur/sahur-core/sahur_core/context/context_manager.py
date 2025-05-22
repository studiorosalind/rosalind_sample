from typing import Dict, List, Optional, Any
import json
from datetime import datetime

from sahur_core.models import (
    CauseContext,
    HistoryContext,
    HistoricalIssue,
    StackTrace,
    HttpRequest,
    HttpResponse,
    KafkaMessage,
    DatabaseError,
)


class ContextManager:
    """
    Manages context information for issue analysis.
    
    This class is responsible for gathering, organizing, and providing
    context information needed for issue analysis, including:
    - Cause context (stack traces, HTTP requests/responses, etc.)
    - History context (similar historical issues)
    """
    
    def __init__(self, mcp_client=None):
        """
        Initialize the context manager.
        
        Args:
            mcp_client: Client for interacting with MCP servers
        """
        self.mcp_client = mcp_client
    
    async def get_cause_context(self, event_transaction_id: str) -> CauseContext:
        """
        Get cause context information for an issue based on its transaction ID.
        
        Args:
            event_transaction_id: The transaction ID associated with the issue
            
        Returns:
            A CauseContext object containing information about the cause
        """
        if self.mcp_client:
            # In a real implementation, this would call the MCP client
            # For now, we'll return a dummy context
            pass
        
        # Create a dummy cause context for demonstration
        return CauseContext(
            stack_trace=StackTrace(
                exception_type="java.lang.NullPointerException",
                exception_message="Cannot invoke method getUser() on null object",
                frames=[
                    {
                        "file_path": "com/example/service/UserService.java",
                        "line_number": 42,
                        "method_name": "processUserRequest",
                        "code_line": "return userRequest.getUser().getId();"
                    },
                    {
                        "file_path": "com/example/controller/UserController.java",
                        "line_number": 28,
                        "method_name": "handleRequest",
                        "code_line": "UserDTO user = userService.processUserRequest(request);"
                    }
                ]
            ),
            http_requests=[
                HttpRequest(
                    method="POST",
                    url="https://api.example.com/users",
                    headers={"Content-Type": "application/json", "Authorization": "Bearer ..."},
                    body={"action": "getUser", "params": {}},
                    timestamp=datetime.now()
                )
            ],
            http_responses=[
                HttpResponse(
                    status_code=500,
                    headers={"Content-Type": "application/json"},
                    body={"error": "Internal Server Error", "message": "An unexpected error occurred"},
                    timestamp=datetime.now()
                )
            ],
            logs=[
                "2025-05-22T15:20:30.123Z ERROR [UserService] - Exception while processing user request",
                "2025-05-22T15:20:30.124Z ERROR [UserService] - java.lang.NullPointerException: Cannot invoke method getUser() on null object",
                "2025-05-22T15:20:30.125Z ERROR [UserService] - at com.example.service.UserService.processUserRequest(UserService.java:42)"
            ]
        )
    
    async def get_history_context(self, issue_description: str) -> HistoryContext:
        """
        Get historical context information for an issue based on its description.
        
        Args:
            issue_description: The description of the issue
            
        Returns:
            A HistoryContext object containing information about similar historical issues
        """
        if self.mcp_client:
            # In a real implementation, this would call the MCP client
            # For now, we'll return a dummy context
            pass
        
        # Create a dummy history context for demonstration
        return HistoryContext(
            similar_issues=[
                HistoricalIssue(
                    issue_id="ISSUE-456",
                    title="NullPointerException in UserService.processUserRequest",
                    description="Users are getting 500 errors when trying to access their profile",
                    root_cause="The UserRequest object was not properly initialized before calling getUser()",
                    solution="Added null check before calling getUser() and proper error handling",
                    similarity_score=0.92,
                    resolved_at=datetime(2025, 4, 15, 10, 30)
                ),
                HistoricalIssue(
                    issue_id="ISSUE-789",
                    title="500 error on user profile page",
                    description="After the latest deployment, users are unable to view their profiles",
                    root_cause="Database connection timeout due to increased load",
                    solution="Increased connection pool size and added retry mechanism",
                    similarity_score=0.78,
                    resolved_at=datetime(2025, 5, 1, 14, 45)
                )
            ],
            relevant_code_changes={
                "com/example/service/UserService.java": "Commit abc123: Refactored user request handling",
                "com/example/controller/UserController.java": "Commit def456: Updated API endpoint parameters"
            },
            deployment_events=[
                {
                    "id": "DEPLOY-123",
                    "timestamp": datetime(2025, 5, 21, 18, 0),
                    "version": "v2.3.4",
                    "changes": ["Updated user service", "Fixed authentication bug"]
                }
            ]
        )
    
    async def enrich_context(self, cause_context: CauseContext) -> CauseContext:
        """
        Enrich the cause context with additional information.
        
        Args:
            cause_context: The initial cause context
            
        Returns:
            An enriched cause context
        """
        if not cause_context.stack_trace:
            return cause_context
        
        # In a real implementation, this would call external services via MCP
        # to get additional information about the code, such as:
        # - File contents
        # - Recent changes
        # - Related issues
        
        return cause_context
