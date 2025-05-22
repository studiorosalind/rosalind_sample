import os
import json
import logging
import asyncio
import uuid
from typing import Dict, Any, Optional
from datetime import datetime
import traceback

from sqlalchemy.orm import Session

from sahur_core.agents import IssueAgent
from sahur_core.models import (
    Issue as CoreIssue,
    IssueStatus,
    IssueSource,
    IssueContext,
    CauseContext,
    HistoryContext,
    Solution,
)

from sahur_batch.database.models import Issue, IssueTracking, IssueMessage
from sahur_batch.utils import WebSocketClient, MCPClient

logger = logging.getLogger(__name__)


class IssueProcessor:
    """
    Processor for analyzing and resolving issues.
    
    This class is responsible for processing an issue, gathering context,
    analyzing the issue, and generating a solution.
    """
    
    def __init__(self, tracking_id: str, db: Session):
        """
        Initialize the issue processor.
        
        Args:
            tracking_id: The ID of the issue tracking record
            db: Database session
        """
        self.tracking_id = tracking_id
        self.db = db
        self.tracking = None
        self.issue = None
        self.ws_client = None
        self.mcp_client = None
        self.agent = None
    
    async def initialize(self) -> bool:
        """
        Initialize the processor.
        
        Returns:
            True if initialization was successful, False otherwise
        """
        try:
            # Get the tracking record
            self.tracking = (
                self.db.query(IssueTracking)
                .filter(IssueTracking.id == self.tracking_id)
                .first()
            )
            
            if not self.tracking:
                logger.error(f"Tracking record not found: {self.tracking_id}")
                return False
            
            # Get the issue
            self.issue = (
                self.db.query(Issue)
                .filter(Issue.id == self.tracking.issue_id)
                .first()
            )
            
            if not self.issue:
                logger.error(f"Issue not found: {self.tracking.issue_id}")
                return False
            
            # Initialize WebSocket client
            self.ws_client = WebSocketClient(self.issue.id)
            if not await self.ws_client.connect():
                logger.warning("Failed to connect to WebSocket server")
            
            # Initialize MCP client
            self.mcp_client = MCPClient()
            
            # Initialize issue agent
            self.agent = IssueAgent(mcp_client=self.mcp_client)
            
            # Update tracking status
            self.tracking.status = IssueStatus.ANALYZING.value
            self.tracking.batch_process_id = str(os.getpid())
            self.db.commit()
            
            # Send status update
            if self.ws_client.connected:
                await self.ws_client.send_status(IssueStatus.ANALYZING.value)
            
            # Log initialization
            logger.info(f"Initialized processor for issue {self.issue.id}")
            
            return True
        
        except Exception as e:
            logger.exception(f"Error initializing processor: {e}")
            return False
    
    async def process(self) -> bool:
        """
        Process the issue.
        
        Returns:
            True if processing was successful, False otherwise
        """
        try:
            # Send initial message
            await self._send_message(
                "system",
                f"Starting analysis of issue: {self.issue.title}"
            )
            
            # Convert DB issue to Core issue
            core_issue = self._convert_to_core_issue()
            
            # Gather context
            await self._gather_context(core_issue)
            
            # Analyze issue
            await self._analyze_issue(core_issue)
            
            # Update tracking status
            self.tracking.status = IssueStatus.COMPLETED.value
            self.db.commit()
            
            # Send status update
            if self.ws_client.connected:
                await self.ws_client.send_status(IssueStatus.COMPLETED.value)
            
            # Send completion message
            await self._send_message(
                "system",
                "Analysis completed. Solution generated."
            )
            
            return True
        
        except Exception as e:
            logger.exception(f"Error processing issue: {e}")
            
            # Update tracking status
            self.tracking.status = IssueStatus.FAILED.value
            self.db.commit()
            
            # Send status update
            if self.ws_client.connected:
                await self.ws_client.send_status(IssueStatus.FAILED.value)
            
            # Send error message
            await self._send_message(
                "system",
                f"Error processing issue: {str(e)}\n\n{traceback.format_exc()}"
            )
            
            return False
        
        finally:
            # Disconnect WebSocket client
            if self.ws_client and self.ws_client.connected:
                await self.ws_client.disconnect()
    
    def _convert_to_core_issue(self) -> CoreIssue:
        """
        Convert a database issue to a core issue.
        
        Returns:
            A core issue
        """
        return CoreIssue(
            issue_id=self.issue.id,
            tracking_id=self.tracking.id,
            title=self.issue.title,
            description=self.issue.description,
            status=IssueStatus(self.issue.status),
            source=IssueSource(self.issue.source),
            created_at=self.issue.created_at,
            updated_at=self.issue.updated_at,
            event_transaction_id=self.issue.event_transaction_id,
            additional_metadata=self.issue.additional_metadata or {},
            context=IssueContext(),
            solution=None,
        )
    
    async def _gather_context(self, core_issue: CoreIssue) -> None:
        """
        Gather context information for the issue.
        
        Args:
            core_issue: The core issue
        """
        await self._send_message(
            "system",
            "Gathering context information..."
        )
        
        # Get cause context if event_transaction_id is available
        if core_issue.event_transaction_id:
            await self._send_message(
                "system",
                f"Getting cause context for transaction ID: {core_issue.event_transaction_id}"
            )
            
            try:
                cause_context_data = await self.mcp_client.get_cause_context(
                    core_issue.event_transaction_id
                )
                
                # Convert to CauseContext
                cause_context = CauseContext.model_validate(cause_context_data)
                core_issue.context.cause_context = cause_context
                
                # Update tracking record
                self.tracking.cause_context = cause_context_data
                self.db.commit()
                
                # Send context to WebSocket
                if self.ws_client.connected:
                    await self.ws_client.send_context("cause_context", cause_context_data)
                
                await self._send_message(
                    "system",
                    "Cause context gathered successfully."
                )
            
            except Exception as e:
                logger.exception(f"Error getting cause context: {e}")
                await self._send_message(
                    "system",
                    f"Error getting cause context: {str(e)}"
                )
        
        # Get history context
        await self._send_message(
            "system",
            "Getting history context..."
        )
        
        try:
            history_context_data = await self.mcp_client.get_history_context(
                core_issue.description
            )
            
            # Convert to HistoryContext
            history_context = HistoryContext.model_validate(history_context_data)
            core_issue.context.history_context = history_context
            
            # Update tracking record
            self.tracking.history_context = history_context_data
            self.db.commit()
            
            # Send context to WebSocket
            if self.ws_client.connected:
                await self.ws_client.send_context("history_context", history_context_data)
            
            await self._send_message(
                "system",
                "History context gathered successfully."
            )
        
        except Exception as e:
            logger.exception(f"Error getting history context: {e}")
            await self._send_message(
                "system",
                f"Error getting history context: {str(e)}"
            )
    
    async def _analyze_issue(self, core_issue: CoreIssue) -> None:
        """
        Analyze the issue and generate a solution.
        
        Args:
            core_issue: The core issue
        """
        await self._send_message(
            "system",
            "Analyzing issue..."
        )
        
        # Set up message handler
        def message_handler(message: Dict[str, Any]) -> None:
            if message.get("type") == "message" and message.get("role") == "user":
                # Handle user message
                content = message.get("content", "")
                asyncio.create_task(self.agent.process_user_input(core_issue, content))
        
        if self.ws_client.connected:
            self.ws_client.set_message_handler(message_handler)
            asyncio.create_task(self.ws_client.listen())
        
        # Analyze the issue
        analyzed_issue = await self.agent.analyze_issue(core_issue)
        
        # Update the solution
        if analyzed_issue.solution:
            solution_data = analyzed_issue.solution.model_dump()
            
            # Update tracking record
            self.tracking.solution = solution_data
            self.db.commit()
            
            # Send solution to WebSocket
            if self.ws_client.connected:
                await self.ws_client.send_solution(solution_data)
            
            await self._send_message(
                "assistant",
                f"# Solution\n\n"
                f"## Root Cause\n\n{analyzed_issue.solution.root_cause}\n\n"
                f"## Explanation\n\n{analyzed_issue.solution.explanation}\n\n"
                f"## Steps\n\n"
                + "\n\n".join([
                    f"### Step {step.step_number}: {step.description}\n\n"
                    + (f"```\n{step.code_changes}\n```\n\n" if step.code_changes else "")
                    + (f"Commands:\n```\n{chr(10).join(step.commands)}\n```" if step.commands else "")
                    for step in analyzed_issue.solution.steps
                ])
                + "\n\n## References\n\n"
                + "\n".join([f"- {ref}" for ref in analyzed_issue.solution.references])
            )
    
    async def _send_message(self, role: str, content: str) -> None:
        """
        Send a message.
        
        Args:
            role: The role of the message sender (system, user, assistant)
            content: The content of the message
        """
        # Create message in database
        message = IssueMessage(
            id=str(uuid.uuid4()),
            issue_id=self.issue.id,
            role=role,
            content=content,
        )
        
        self.db.add(message)
        self.db.commit()
        
        # Send message to WebSocket
        if self.ws_client and self.ws_client.connected:
            await self.ws_client.send_message(role, content)
        
        logger.debug(f"Sent message: {role} - {content[:100]}...")
