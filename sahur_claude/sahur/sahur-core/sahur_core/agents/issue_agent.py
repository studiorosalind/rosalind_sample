from typing import Dict, List, Any, Optional
import json
import asyncio
from datetime import datetime

from langchain.schema import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

from sahur_core.models import (
    Issue,
    IssueStatus,
    IssueContext,
    CauseContext,
    HistoryContext,
    Solution,
    SolutionStep,
)
from sahur_core.context import ContextManager


class IssueAgent:
    """
    Agent responsible for analyzing and resolving issues.
    
    This agent uses LLMs to analyze issues, identify root causes,
    and generate solutions based on context information.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-4o",
        context_manager: Optional[ContextManager] = None,
        mcp_client=None,
    ):
        """
        Initialize the issue agent.
        
        Args:
            model_name: The name of the LLM model to use
            context_manager: Manager for context information
            mcp_client: Client for interacting with MCP servers
        """
        self.llm = ChatOpenAI(model=model_name)
        self.context_manager = context_manager or ContextManager(mcp_client)
        self.mcp_client = mcp_client
        self.messages = []
    
    async def analyze_issue(self, issue: Issue) -> Issue:
        """
        Analyze an issue to identify its root cause.
        
        Args:
            issue: The issue to analyze
            
        Returns:
            The updated issue with analysis results
        """
        # Update issue status
        issue.status = IssueStatus.ANALYZING
        issue.updated_at = datetime.now()
        
        # Initialize messages
        self.messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert software engineer tasked with analyzing and resolving issues. "
                    "Your goal is to identify the root cause of the issue and provide a detailed solution."
                )
            },
            {
                "role": "user",
                "content": f"I need to analyze the following issue:\n\n"
                           f"ID: {issue.issue_id}\n"
                           f"Title: {issue.title}\n"
                           f"Description: {issue.description}"
            }
        ]
        
        # Gather context information
        await self._gather_context(issue)
        
        # Analyze the issue
        analysis_result = await self._perform_analysis()
        
        # Generate a solution
        solution = await self._generate_solution(analysis_result)
        
        # Update the issue
        issue.solution = solution
        issue.status = IssueStatus.COMPLETED
        issue.updated_at = datetime.now()
        
        return issue
    
    async def _gather_context(self, issue: Issue) -> None:
        """
        Gather context information for the issue.
        
        Args:
            issue: The issue to gather context for
        """
        # Add a message indicating that we're gathering context
        self.messages.append({
            "role": "assistant",
            "content": "I'll analyze this issue. First, let me gather some context information."
        })
        
        # Get cause context if event_transaction_id is available
        if issue.event_transaction_id:
            cause_context = await self.context_manager.get_cause_context(issue.event_transaction_id)
            issue.context.cause_context = cause_context
            
            # Add cause context to messages
            self._add_context_to_messages("Cause Context", cause_context.dict())
        
        # Get history context
        history_context = await self.context_manager.get_history_context(issue.description)
        issue.context.history_context = history_context
        
        # Add history context to messages
        self._add_context_to_messages("History Context", history_context.dict())
    
    def _add_context_to_messages(self, context_type: str, context_data: Dict[str, Any]) -> None:
        """
        Add context information to the message history.
        
        Args:
            context_type: The type of context (e.g., "Cause Context")
            context_data: The context data to add
        """
        # Format the context data as a string
        context_str = json.dumps(context_data, indent=2, default=str)
        
        # Add the context to the messages
        self.messages.append({
            "role": "user",
            "content": f"Here is the {context_type} information:\n\n```json\n{context_str}\n```"
        })
    
    async def _perform_analysis(self) -> str:
        """
        Perform analysis on the issue using the gathered context.
        
        Returns:
            The analysis result
        """
        # Add a prompt for analysis
        self.messages.append({
            "role": "user",
            "content": (
                "Based on the context information provided, please analyze this issue and identify the root cause. "
                "Consider the stack trace, HTTP requests/responses, logs, and similar historical issues."
            )
        })
        
        # Convert messages to LangChain format
        lc_messages = []
        for msg in self.messages:
            if msg["role"] == "system":
                lc_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "user":
                lc_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                lc_messages.append(AIMessage(content=msg["content"]))
        
        # Get response from LLM
        response = self.llm.invoke(lc_messages)
        
        # Add the response to messages
        self.messages.append({
            "role": "assistant",
            "content": response.content
        })
        
        return response.content
    
    async def _generate_solution(self, analysis_result: str) -> Solution:
        """
        Generate a solution for the issue based on the analysis.
        
        Args:
            analysis_result: The result of the analysis
            
        Returns:
            A Solution object
        """
        # Add a prompt for solution generation
        self.messages.append({
            "role": "user",
            "content": (
                "Based on your analysis, please generate a detailed solution for this issue. "
                "Include specific steps to resolve the issue, any code changes needed, "
                "and commands to execute if applicable."
            )
        })
        
        # Convert messages to LangChain format
        lc_messages = []
        for msg in self.messages:
            if msg["role"] == "system":
                lc_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "user":
                lc_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                lc_messages.append(AIMessage(content=msg["content"]))
        
        # Get response from LLM
        response = self.llm.invoke(lc_messages)
        
        # Add the response to messages
        self.messages.append({
            "role": "assistant",
            "content": response.content
        })
        
        # Parse the solution from the response
        # In a real implementation, this would parse the response to extract structured data
        # For now, we'll create a dummy solution
        
        return Solution(
            root_cause="The UserRequest object was not properly initialized before calling getUser()",
            explanation=response.content,
            steps=[
                SolutionStep(
                    step_number=1,
                    description="Add null check before calling getUser()",
                    code_changes={
                        "com/example/service/UserService.java": """
                        // Before
                        return userRequest.getUser().getId();
                        
                        // After
                        if (userRequest == null || userRequest.getUser() == null) {
                            throw new IllegalArgumentException("User request or user is null");
                        }
                        return userRequest.getUser().getId();
                        """
                    },
                    commands=None
                ),
                SolutionStep(
                    step_number=2,
                    description="Add proper error handling in the controller",
                    code_changes={
                        "com/example/controller/UserController.java": """
                        // Before
                        UserDTO user = userService.processUserRequest(request);
                        
                        // After
                        UserDTO user;
                        try {
                            user = userService.processUserRequest(request);
                        } catch (IllegalArgumentException e) {
                            return ResponseEntity.badRequest().body(new ErrorResponse(e.getMessage()));
                        }
                        """
                    },
                    commands=None
                ),
                SolutionStep(
                    step_number=3,
                    description="Deploy the changes",
                    code_changes=None,
                    commands=[
                        "mvn clean package",
                        "kubectl apply -f k8s/deployment.yaml"
                    ]
                )
            ],
            references=[
                "Similar issue: ISSUE-456",
                "Java documentation on NullPointerException",
                "Company best practices for error handling"
            ]
        )
    
    async def request_user_input(self, issue: Issue, question: str) -> None:
        """
        Request additional input from the user.
        
        Args:
            issue: The issue being analyzed
            question: The question to ask the user
        """
        # Update issue status
        issue.status = IssueStatus.WAITING_FOR_INPUT
        issue.updated_at = datetime.now()
        
        # Add the question to messages
        self.messages.append({
            "role": "assistant",
            "content": question
        })
    
    async def process_user_input(self, issue: Issue, user_input: str) -> None:
        """
        Process input provided by the user.
        
        Args:
            issue: The issue being analyzed
            user_input: The input provided by the user
        """
        # Update issue status
        issue.status = IssueStatus.ANALYZING
        issue.updated_at = datetime.now()
        
        # Add the user input to messages
        self.messages.append({
            "role": "user",
            "content": user_input
        })
