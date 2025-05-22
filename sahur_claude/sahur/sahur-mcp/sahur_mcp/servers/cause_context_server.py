import os
import json
import logging
from typing import Dict, Any, List, Optional
import asyncio
from datetime import datetime

from sahur_core.mcp_server import MCPServer, Tool, Resource, Schema

logger = logging.getLogger(__name__)


class CauseContextServer(MCPServer):
    """
    MCP server for cause context information.
    
    This server provides tools and resources for retrieving and analyzing
    cause context information for issues.
    """
    
    def __init__(self):
        """Initialize the cause context server."""
        super().__init__(name="sahur-mcp")
        
        # Register tools
        self.register_tool(
            Tool(
                name="getCauseContext",
                description="Get cause context for an event transaction",
                input_schema=Schema({
                    "type": "object",
                    "properties": {
                        "eventTransactionId": {
                            "type": "string",
                            "description": "The transaction ID of the event"
                        }
                    },
                    "required": ["eventTransactionId"]
                }),
                output_schema=Schema({
                    "type": "object",
                    "description": "Cause context information"
                }),
                handler=self.get_cause_context
            )
        )
    
    async def get_cause_context(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get cause context for an event transaction.
        
        Args:
            arguments: The arguments for the tool
            
        Returns:
            The cause context information
        """
        event_transaction_id = arguments.get("eventTransactionId")
        
        logger.info(f"Getting cause context for transaction ID: {event_transaction_id}")
        
        # In a real implementation, this would retrieve actual data
        # For now, we'll return dummy data
        
        # Generate a stack trace based on the transaction ID
        if event_transaction_id.startswith("java"):
            return self._get_java_stack_trace()
        elif event_transaction_id.startswith("python"):
            return self._get_python_stack_trace()
        elif event_transaction_id.startswith("node"):
            return self._get_node_stack_trace()
        else:
            return self._get_generic_cause_context()
    
    def _get_java_stack_trace(self) -> Dict[str, Any]:
        """
        Get a dummy Java stack trace.
        
        Returns:
            A dummy cause context with a Java stack trace
        """
        return {
            "stack_trace": {
                "exception_type": "java.lang.NullPointerException",
                "exception_message": "Cannot invoke method getUser() on null object",
                "frames": [
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
                    },
                    {
                        "file_path": "com/example/api/ApiHandler.java",
                        "line_number": 15,
                        "method_name": "handleApiRequest",
                        "code_line": "return userController.handleRequest(request);"
                    }
                ]
            },
            "http_requests": [
                {
                    "method": "POST",
                    "url": "https://api.example.com/users",
                    "headers": {"Content-Type": "application/json", "Authorization": "Bearer ..."},
                    "body": {"action": "getUser", "params": {}},
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "http_responses": [
                {
                    "status_code": 500,
                    "headers": {"Content-Type": "application/json"},
                    "body": {"error": "Internal Server Error", "message": "An unexpected error occurred"},
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "logs": [
                "2025-05-22T15:20:30.123Z ERROR [UserService] - Exception while processing user request",
                "2025-05-22T15:20:30.124Z ERROR [UserService] - java.lang.NullPointerException: Cannot invoke method getUser() on null object",
                "2025-05-22T15:20:30.125Z ERROR [UserService] - at com.example.service.UserService.processUserRequest(UserService.java:42)",
                "2025-05-22T15:20:30.126Z ERROR [UserService] - at com.example.controller.UserController.handleRequest(UserController.java:28)",
                "2025-05-22T15:20:30.127Z ERROR [UserService] - at com.example.api.ApiHandler.handleApiRequest(ApiHandler.java:15)"
            ]
        }
    
    def _get_python_stack_trace(self) -> Dict[str, Any]:
        """
        Get a dummy Python stack trace.
        
        Returns:
            A dummy cause context with a Python stack trace
        """
        return {
            "stack_trace": {
                "exception_type": "AttributeError",
                "exception_message": "'NoneType' object has no attribute 'get_user'",
                "frames": [
                    {
                        "file_path": "app/services/user_service.py",
                        "line_number": 25,
                        "method_name": "process_user_request",
                        "code_line": "return user_request.get_user().id"
                    },
                    {
                        "file_path": "app/controllers/user_controller.py",
                        "line_number": 18,
                        "method_name": "handle_request",
                        "code_line": "user = user_service.process_user_request(request)"
                    },
                    {
                        "file_path": "app/api/api_handler.py",
                        "line_number": 10,
                        "method_name": "handle_api_request",
                        "code_line": "return user_controller.handle_request(request)"
                    }
                ]
            },
            "http_requests": [
                {
                    "method": "POST",
                    "url": "https://api.example.com/users",
                    "headers": {"Content-Type": "application/json", "Authorization": "Bearer ..."},
                    "body": {"action": "get_user", "params": {}},
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "http_responses": [
                {
                    "status_code": 500,
                    "headers": {"Content-Type": "application/json"},
                    "body": {"error": "Internal Server Error", "message": "An unexpected error occurred"},
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "logs": [
                "2025-05-22 15:20:30,123 - ERROR - [user_service] - Exception while processing user request",
                "2025-05-22 15:20:30,124 - ERROR - [user_service] - AttributeError: 'NoneType' object has no attribute 'get_user'",
                "2025-05-22 15:20:30,125 - ERROR - [user_service] - File \"app/services/user_service.py\", line 25, in process_user_request",
                "2025-05-22 15:20:30,126 - ERROR - [user_service] - return user_request.get_user().id",
                "2025-05-22 15:20:30,127 - ERROR - [user_service] - File \"app/controllers/user_controller.py\", line 18, in handle_request",
                "2025-05-22 15:20:30,128 - ERROR - [user_service] - user = user_service.process_user_request(request)",
                "2025-05-22 15:20:30,129 - ERROR - [user_service] - File \"app/api/api_handler.py\", line 10, in handle_api_request",
                "2025-05-22 15:20:30,130 - ERROR - [user_service] - return user_controller.handle_request(request)"
            ]
        }
    
    def _get_node_stack_trace(self) -> Dict[str, Any]:
        """
        Get a dummy Node.js stack trace.
        
        Returns:
            A dummy cause context with a Node.js stack trace
        """
        return {
            "stack_trace": {
                "exception_type": "TypeError",
                "exception_message": "Cannot read property 'getUser' of null",
                "frames": [
                    {
                        "file_path": "src/services/userService.js",
                        "line_number": 15,
                        "method_name": "processUserRequest",
                        "code_line": "return userRequest.getUser().getId();"
                    },
                    {
                        "file_path": "src/controllers/userController.js",
                        "line_number": 10,
                        "method_name": "handleRequest",
                        "code_line": "const user = userService.processUserRequest(request);"
                    },
                    {
                        "file_path": "src/api/apiHandler.js",
                        "line_number": 8,
                        "method_name": "handleApiRequest",
                        "code_line": "return userController.handleRequest(request);"
                    }
                ]
            },
            "http_requests": [
                {
                    "method": "POST",
                    "url": "https://api.example.com/users",
                    "headers": {"Content-Type": "application/json", "Authorization": "Bearer ..."},
                    "body": {"action": "getUser", "params": {}},
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "http_responses": [
                {
                    "status_code": 500,
                    "headers": {"Content-Type": "application/json"},
                    "body": {"error": "Internal Server Error", "message": "An unexpected error occurred"},
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "logs": [
                "2025-05-22T15:20:30.123Z ERROR [userService] - Exception while processing user request",
                "2025-05-22T15:20:30.124Z ERROR [userService] - TypeError: Cannot read property 'getUser' of null",
                "2025-05-22T15:20:30.125Z ERROR [userService] - at processUserRequest (/app/src/services/userService.js:15:28)",
                "2025-05-22T15:20:30.126Z ERROR [userService] - at handleRequest (/app/src/controllers/userController.js:10:22)",
                "2025-05-22T15:20:30.127Z ERROR [userService] - at handleApiRequest (/app/src/api/apiHandler.js:8:16)"
            ]
        }
    
    def _get_generic_cause_context(self) -> Dict[str, Any]:
        """
        Get a generic cause context without a stack trace.
        
        Returns:
            A generic cause context
        """
        return {
            "http_requests": [
                {
                    "method": "POST",
                    "url": "https://api.example.com/data",
                    "headers": {"Content-Type": "application/json", "Authorization": "Bearer ..."},
                    "body": {"action": "getData", "params": {"id": "123"}},
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "http_responses": [
                {
                    "status_code": 500,
                    "headers": {"Content-Type": "application/json"},
                    "body": {"error": "Internal Server Error", "message": "An unexpected error occurred"},
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "logs": [
                "2025-05-22T15:20:30.123Z ERROR [DataService] - Failed to process request",
                "2025-05-22T15:20:30.124Z ERROR [DataService] - Error details: Connection timeout",
                "2025-05-22T15:20:30.125Z ERROR [DataService] - Request ID: REQ-123456"
            ],
            "kafka_messages": [
                {
                    "topic": "data-events",
                    "partition": 0,
                    "offset": 12345,
                    "key": "user-123",
                    "value": {"event": "data-request", "userId": "123", "timestamp": "2025-05-22T15:20:25Z"},
                    "timestamp": datetime.now().isoformat(),
                    "headers": {"source": "web-api", "version": "1.0"}
                }
            ],
            "database_errors": [
                {
                    "error_code": "ER_LOCK_WAIT_TIMEOUT",
                    "error_message": "Lock wait timeout exceeded; try restarting transaction",
                    "query": "SELECT * FROM users WHERE id = ?",
                    "parameters": {"id": "123"},
                    "timestamp": datetime.now().isoformat()
                }
            ]
        }


# Create an instance of the server
cause_context_server = CauseContextServer()
