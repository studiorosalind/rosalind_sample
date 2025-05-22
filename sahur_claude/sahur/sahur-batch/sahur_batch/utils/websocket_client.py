import os
import json
import asyncio
import logging
from typing import Dict, Any, Optional, Callable
import websockets
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Get server URL from environment variable or use a default
SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8000")


class WebSocketClient:
    """
    WebSocket client for communicating with the server.
    
    This class is responsible for sending real-time updates to the server
    about the progress of issue analysis.
    """
    
    def __init__(self, issue_id: str):
        """
        Initialize the WebSocket client.
        
        Args:
            issue_id: The ID of the issue being analyzed
        """
        self.issue_id = issue_id
        self.ws_url = f"{SERVER_URL.replace('http://', 'ws://').replace('https://', 'wss://')}/api/issues/ws/{issue_id}"
        self.websocket = None
        self.connected = False
        self.message_handler: Optional[Callable[[Dict[str, Any]], None]] = None
    
    async def connect(self) -> bool:
        """
        Connect to the WebSocket server.
        
        Returns:
            True if the connection was successful, False otherwise
        """
        try:
            self.websocket = await websockets.connect(self.ws_url)
            self.connected = True
            logger.info(f"Connected to WebSocket server: {self.ws_url}")
            return True
        except Exception as e:
            logger.exception(f"Error connecting to WebSocket server: {e}")
            self.connected = False
            return False
    
    async def disconnect(self) -> None:
        """Disconnect from the WebSocket server."""
        if self.websocket and self.connected:
            await self.websocket.close()
            self.connected = False
            logger.info("Disconnected from WebSocket server")
    
    async def send_message(self, role: str, content: str) -> bool:
        """
        Send a message to the server.
        
        Args:
            role: The role of the message sender (system, user, assistant)
            content: The content of the message
            
        Returns:
            True if the message was sent successfully, False otherwise
        """
        if not self.websocket or not self.connected:
            logger.warning("Cannot send message: not connected to WebSocket server")
            return False
        
        try:
            message = {
                "type": "message",
                "role": role,
                "content": content,
            }
            
            await self.websocket.send(json.dumps(message))
            logger.debug(f"Sent message: {message}")
            return True
        except Exception as e:
            logger.exception(f"Error sending message: {e}")
            return False
    
    async def send_status(self, status: str) -> bool:
        """
        Send a status update to the server.
        
        Args:
            status: The new status
            
        Returns:
            True if the status was sent successfully, False otherwise
        """
        if not self.websocket or not self.connected:
            logger.warning("Cannot send status: not connected to WebSocket server")
            return False
        
        try:
            message = {
                "type": "status",
                "status": status,
            }
            
            await self.websocket.send(json.dumps(message))
            logger.debug(f"Sent status: {status}")
            return True
        except Exception as e:
            logger.exception(f"Error sending status: {e}")
            return False
    
    async def send_context(self, context_type: str, context: Dict[str, Any]) -> bool:
        """
        Send context information to the server.
        
        Args:
            context_type: The type of context (cause_context or history_context)
            context: The context information
            
        Returns:
            True if the context was sent successfully, False otherwise
        """
        if not self.websocket or not self.connected:
            logger.warning("Cannot send context: not connected to WebSocket server")
            return False
        
        try:
            message = {
                "type": "context",
                "context_type": context_type,
                "context": context,
            }
            
            await self.websocket.send(json.dumps(message))
            logger.debug(f"Sent {context_type}")
            return True
        except Exception as e:
            logger.exception(f"Error sending context: {e}")
            return False
    
    async def send_solution(self, solution: Dict[str, Any]) -> bool:
        """
        Send a solution to the server.
        
        Args:
            solution: The solution
            
        Returns:
            True if the solution was sent successfully, False otherwise
        """
        if not self.websocket or not self.connected:
            logger.warning("Cannot send solution: not connected to WebSocket server")
            return False
        
        try:
            message = {
                "type": "solution",
                "solution": solution,
            }
            
            await self.websocket.send(json.dumps(message))
            logger.debug("Sent solution")
            return True
        except Exception as e:
            logger.exception(f"Error sending solution: {e}")
            return False
    
    async def listen(self) -> None:
        """
        Listen for messages from the server.
        
        This method runs in a loop, receiving messages from the server
        and calling the message handler if one is set.
        """
        if not self.websocket or not self.connected:
            logger.warning("Cannot listen: not connected to WebSocket server")
            return
        
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    logger.debug(f"Received message: {data}")
                    
                    if self.message_handler:
                        self.message_handler(data)
                except json.JSONDecodeError:
                    logger.warning(f"Received invalid JSON: {message}")
        except Exception as e:
            logger.exception(f"Error listening for messages: {e}")
    
    def set_message_handler(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """
        Set the message handler.
        
        Args:
            handler: The function to call when a message is received
        """
        self.message_handler = handler
