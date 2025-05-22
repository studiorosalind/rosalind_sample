"""
SAHUR Core - The core library for the SAHUR system.

This package contains the shared logic and components used by all other SAHUR modules.
"""

from sahur_core.agents import IssueAgent
from sahur_core.context import ContextManager
from sahur_core.models import (
    Issue,
    IssueStatus,
    IssueSource,
    IssueContext,
    CauseContext,
    HistoryContext,
    Solution,
    SolutionStep,
)
from sahur_core.utils import MCPClient
from sahur_core.workflows import create_analysis_workflow, run_analysis_workflow

__version__ = "0.1.0"

__all__ = [
    "IssueAgent",
    "ContextManager",
    "Issue",
    "IssueStatus",
    "IssueSource",
    "IssueContext",
    "CauseContext",
    "HistoryContext",
    "Solution",
    "SolutionStep",
    "MCPClient",
    "create_analysis_workflow",
    "run_analysis_workflow",
]
