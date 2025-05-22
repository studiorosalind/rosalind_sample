from typing import Dict, List, Any, Annotated, TypedDict, Literal
import json
from datetime import datetime

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
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


class WorkflowState(TypedDict):
    """State maintained throughout the workflow execution."""
    issue: Issue
    messages: List[Dict[str, Any]]
    current_step: str
    cause_context_complete: bool
    history_context_complete: bool
    requires_user_input: bool
    user_input: str
    solution: Solution


def create_analysis_workflow(model_name: str = "gpt-4o") -> StateGraph:
    """
    Create a LangGraph workflow for issue analysis.
    
    Args:
        model_name: The name of the LLM model to use
        
    Returns:
        A LangGraph StateGraph instance
    """
    # Initialize the LLM
    llm = ChatOpenAI(model=model_name)
    
    # Define the workflow graph
    workflow = StateGraph(WorkflowState)
    
    # Define workflow nodes
    
    # 1. Initialize analysis
    def initialize_analysis(state: WorkflowState) -> WorkflowState:
        """Initialize the analysis process."""
        issue = state["issue"]
        issue.status = IssueStatus.ANALYZING
        issue.updated_at = datetime.now()
        
        return {
            **state,
            "issue": issue,
            "current_step": "initialize",
            "messages": [
                {
                    "role": "system",
                    "content": f"You are analyzing issue {issue.issue_id}: {issue.title}. "
                    f"Description: {issue.description}"
                }
            ],
            "cause_context_complete": False,
            "history_context_complete": False,
            "requires_user_input": False,
            "user_input": "",
            "solution": None,
        }
    
    # 2. Gather cause context
    def gather_cause_context(state: WorkflowState) -> WorkflowState:
        """Gather context information about the cause of the issue."""
        # In a real implementation, this would call external services via MCP
        # For now, we'll just update the state
        issue = state["issue"]
        messages = state["messages"]
        
        messages.append({
            "role": "system",
            "content": "Gathering cause context information..."
        })
        
        return {
            **state,
            "current_step": "gather_cause_context",
            "messages": messages,
            "cause_context_complete": True,
        }
    
    # 3. Gather history context
    def gather_history_context(state: WorkflowState) -> WorkflowState:
        """Gather context information about similar historical issues."""
        # In a real implementation, this would call external services via MCP
        # For now, we'll just update the state
        issue = state["issue"]
        messages = state["messages"]
        
        messages.append({
            "role": "system",
            "content": "Gathering historical context information..."
        })
        
        return {
            **state,
            "current_step": "gather_history_context",
            "messages": messages,
            "history_context_complete": True,
        }
    
    # 4. Analyze issue
    def analyze_issue(state: WorkflowState) -> WorkflowState:
        """Analyze the issue using the gathered context."""
        issue = state["issue"]
        messages = state["messages"]
        
        # Convert messages to LangChain format
        lc_messages = []
        for msg in messages:
            if msg["role"] == "system":
                lc_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "user":
                lc_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                lc_messages.append(AIMessage(content=msg["content"]))
        
        # Add analysis prompt
        lc_messages.append(HumanMessage(
            content="Based on the context information, analyze this issue and identify the root cause."
        ))
        
        # Get response from LLM
        response = llm.invoke(lc_messages)
        
        # Update messages
        messages.append({
            "role": "system",
            "content": "Analyzing issue..."
        })
        messages.append({
            "role": "assistant",
            "content": response.content
        })
        
        return {
            **state,
            "current_step": "analyze_issue",
            "messages": messages,
        }
    
    # 5. Check if user input is needed
    def check_user_input_needed(state: WorkflowState) -> Literal["generate_solution", "request_user_input"]:
        """Check if additional user input is needed to proceed."""
        # For demo purposes, we'll randomly decide if user input is needed
        # In a real implementation, this would be based on the analysis
        import random
        needs_input = random.choice([True, False])
        
        if needs_input:
            return "request_user_input"
        else:
            return "generate_solution"
    
    # 6. Request user input
    def request_user_input(state: WorkflowState) -> WorkflowState:
        """Request additional input from the user."""
        issue = state["issue"]
        messages = state["messages"]
        
        issue.status = IssueStatus.WAITING_FOR_INPUT
        issue.updated_at = datetime.now()
        
        messages.append({
            "role": "system",
            "content": "Additional information is needed to proceed with the analysis."
        })
        messages.append({
            "role": "assistant",
            "content": "Could you please provide more details about the issue? "
                      "Specifically, any error messages or logs would be helpful."
        })
        
        return {
            **state,
            "current_step": "request_user_input",
            "messages": messages,
            "requires_user_input": True,
            "issue": issue,
        }
    
    # 7. Process user input
    def process_user_input(state: WorkflowState) -> WorkflowState:
        """Process the input provided by the user."""
        issue = state["issue"]
        messages = state["messages"]
        user_input = state["user_input"]
        
        issue.status = IssueStatus.ANALYZING
        issue.updated_at = datetime.now()
        
        messages.append({
            "role": "user",
            "content": user_input
        })
        
        return {
            **state,
            "current_step": "process_user_input",
            "messages": messages,
            "requires_user_input": False,
            "issue": issue,
        }
    
    # 8. Generate solution
    def generate_solution(state: WorkflowState) -> WorkflowState:
        """Generate a solution for the issue."""
        issue = state["issue"]
        messages = state["messages"]
        
        issue.status = IssueStatus.GENERATING_SOLUTION
        issue.updated_at = datetime.now()
        
        # Convert messages to LangChain format
        lc_messages = []
        for msg in messages:
            if msg["role"] == "system":
                lc_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "user":
                lc_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                lc_messages.append(AIMessage(content=msg["content"]))
        
        # Add solution generation prompt
        lc_messages.append(HumanMessage(
            content="Based on your analysis, please generate a detailed solution for this issue."
        ))
        
        # Get response from LLM
        response = llm.invoke(lc_messages)
        
        # Create a solution object
        solution = Solution(
            root_cause="Identified root cause based on analysis",
            explanation=response.content,
            steps=[
                SolutionStep(
                    step_number=1,
                    description="First step of the solution",
                    code_changes=None,
                    commands=["command1", "command2"]
                ),
                SolutionStep(
                    step_number=2,
                    description="Second step of the solution",
                    code_changes={"file.py": "updated code here"},
                    commands=None
                )
            ],
            references=["Reference 1", "Reference 2"]
        )
        
        # Update issue
        issue.solution = solution
        issue.status = IssueStatus.COMPLETED
        issue.updated_at = datetime.now()
        
        # Update messages
        messages.append({
            "role": "system",
            "content": "Generating solution..."
        })
        messages.append({
            "role": "assistant",
            "content": response.content
        })
        
        return {
            **state,
            "current_step": "generate_solution",
            "messages": messages,
            "solution": solution,
            "issue": issue,
        }
    
    # Add nodes to the graph
    workflow.add_node("initialize", initialize_analysis)
    workflow.add_node("gather_cause_context", gather_cause_context)
    workflow.add_node("gather_history_context", gather_history_context)
    workflow.add_node("analyze_issue", analyze_issue)
    workflow.add_node("check_user_input", check_user_input_needed)
    workflow.add_node("request_user_input", request_user_input)
    workflow.add_node("process_user_input", process_user_input)
    workflow.add_node("generate_solution", generate_solution)
    
    # Define the edges
    workflow.add_edge("initialize", "gather_cause_context")
    workflow.add_edge("gather_cause_context", "gather_history_context")
    workflow.add_edge("gather_history_context", "analyze_issue")
    workflow.add_edge("analyze_issue", "check_user_input")
    workflow.add_edge("check_user_input", "request_user_input")
    workflow.add_edge("check_user_input", "generate_solution")
    workflow.add_edge("request_user_input", "process_user_input")
    workflow.add_edge("process_user_input", "analyze_issue")
    workflow.add_edge("generate_solution", END)
    
    # Set the entry point
    workflow.set_entry_point("initialize")
    
    return workflow


def run_analysis_workflow(issue: Issue) -> Issue:
    """
    Run the analysis workflow for an issue.
    
    Args:
        issue: The issue to analyze
        
    Returns:
        The updated issue with analysis results
    """
    workflow = create_analysis_workflow()
    
    # Initialize the state
    initial_state = {
        "issue": issue,
        "messages": [],
        "current_step": "",
        "cause_context_complete": False,
        "history_context_complete": False,
        "requires_user_input": False,
        "user_input": "",
        "solution": None,
    }
    
    # Run the workflow
    result = workflow.invoke(initial_state)
    
    # Return the updated issue
    return result["issue"]
