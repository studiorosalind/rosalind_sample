# SAHUR Core

The core library for the SAHUR (Smart AI-powered Help for Understanding and Resolving) system. This package contains the shared logic and components used by all other SAHUR modules.

## Features

- LangGraph workflows for issue analysis and resolution
- LLM orchestration and agent logic
- Context management (CauseContext and HistoryContext)
- Common data models and utilities
- MCP (Model Context Protocol) integration

## Installation

For development, install this package in editable mode:

```bash
pip install -e .
```

Other SAHUR components should include this as a dependency with:

```bash
pip install -e ../sahur-core
```

## Module Structure

- `agents/`: Agent definitions and behaviors
- `workflows/`: LangGraph workflow definitions
- `models/`: Pydantic data models
- `utils/`: Utility functions and helpers
- `context/`: Context management for issue analysis

## Usage

```python
from sahur_core.workflows import create_analysis_workflow
from sahur_core.models import IssueContext

# Create a workflow for issue analysis
workflow = create_analysis_workflow()

# Run the workflow with an issue context
result = workflow.invoke({
    "issue_id": "ISSUE-123",
    "description": "Service is returning 500 errors after deployment",
    "context": IssueContext(...)
})
