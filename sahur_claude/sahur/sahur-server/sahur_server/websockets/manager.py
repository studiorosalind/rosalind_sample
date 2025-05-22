import json
import logging
from typing import Dict, Set, Any, Optional
import asyncio

from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    Manager for WebSocket connections.
    
    This class is responsible for managing WebSocket connections
    and broadcasting messages to connected clients.
    """
    
    def __init__(self):
        """Initialize the connection manager."""
        # Map of issue ID to set of connected WebSockets
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, issue_id: str) -> None:
        """
        Connect a WebSocket to an issue.
        
        Args:
            websocket: The WebSocket connection
            issue_id: The ID of the issue to connect to
        """
        await websocket.accept()
        
        if issue_id not in self.active_connections:
            self.active_connections[issue_id] = set()
        
        self.active_connections[issue_id].add(websocket)
        
        logger.info(f"WebSocket connected to issue {issue_id}")
    
    def disconnect(self, websocket: WebSocket, issue_id: str) -> None:
        """
        Disconnect a WebSocket from an issue.
        
        Args:
            websocket: The WebSocket connection
            issue_id: The ID of the issue to disconnect from
        """
        if issue_id in self.active_connections:
            self.active_connections[issue_id].discard(websocket)
            
            # Remove the issue if there are no more connections
            if not self.active_connections[issue_id]:
                del self.active_connections[issue_id]
        
        logger.info(f"WebSocket disconnected from issue {issue_id}")
    
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket) -> None:
        """
        Send a message to a specific WebSocket.
        
        Args:
            message: The message to send
            websocket: The WebSocket to send to
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.exception(f"Error sending personal message: {e}")
    
    async def broadcast(self, message: Dict[str, Any], issue_id: str) -> None:
        """
        Broadcast a message to all WebSockets connected to an issue.
        
        Args:
            message: The message to broadcast
            issue_id: The ID of the issue to broadcast to
        """
        if issue_id not in self.active_connections:
            return
        
        disconnected = set()
        
        for websocket in self.active_connections[issue_id]:
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.exception(f"Error broadcasting message: {e}")
                disconnected.add(websocket)
        
        # Remove disconnected WebSockets
        for websocket in disconnected:
            self.disconnect(websocket, issue_id)
    
    async def broadcast_message(
        self, role: str, content: str, issue_id: str, message_id: Optional[str] = None
    ) -> None:
        """
        Broadcast a message to all WebSockets connected to an issue.
        
        Args:
            role: The role of the message sender (system, user, assistant)
            content: The content of the message
            issue_id: The ID of the issue to broadcast to
            message_id: The ID of the message, if available
        """
        message = {
            "type": "message",
            "role": role,
            "content": content,
            "issue_id": issue_id,
            "message_id": message_id,
        }
        
        await self.broadcast(message, issue_id)
    
    async def broadcast_status(self, status: str, issue_id: str) -> None:
        """
        Broadcast a status update to all WebSockets connected to an issue.
        
        Args:
            status: The new status
            issue_id: The ID of the issue to broadcast to
        """
        message = {
            "type": "status",
            "status": status,
            "issue_id": issue_id,
        }
        
        await self.broadcast(message, issue_id)
    
    async def broadcast_solution(self, solution: Dict[str, Any], issue_id: str) -> None:
        """
        Broadcast a solution to all WebSockets connected to an issue.
        
        Args:
            solution: The solution
            issue_id: The ID of the issue to broadcast to
        """
        message = {
            "type": "solution",
            "solution": solution,
            "issue_id": issue_id,
        }
        
        await self.broadcast(message, issue_id)
    
    async def broadcast_context(
        self, context_type: str, context: Dict[str, Any], issue_id: str
    ) -> None:
        """
        Broadcast context information to all WebSockets connected to an issue.
        
        Args:
            context_type: The type of context (cause_context or history_context)
            context: The context information
            issue_id: The ID of the issue to broadcast to
        """
        message = {
            "type": "context",
            "context_type": context_type,
            "context": context,
            "issue_id": issue_id,
        }
        
        await self.broadcast(message, issue_id)


# Create a global connection manager
manager = ConnectionManager()
