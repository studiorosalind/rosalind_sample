# SAHUR Batch

The dynamic issue processing instance for the SAHUR (Smart AI-powered Help for Understanding and Resolving) system.

## Features

- Independent processing instance for each issue
- Real-time streaming of analysis progress via WebSocket
- Integration with sahur-core for issue analysis
- Integration with sahur-mcp for context gathering
- Automatic termination after issue resolution

## Installation

First, install the sahur-core package in development mode:

```bash
cd ../sahur-core
pip install -e .
```

Then, install this package in development mode:

```bash
cd ../sahur-batch
pip install -e .
```

## Configuration

Create a `.env` file in the root directory with the following variables:

```
DATABASE_URL=postgresql://user:password@localhost:5432/sahur
MCP_SERVER_URL=http://localhost:8002
SERVER_URL=http://localhost:8000
```

## Running the Batch Process

The batch process is typically started by the sahur-server component, but you can also run it manually:

```bash
python -m sahur_batch.main --tracking-id <tracking_id>
```

## Process Flow

1. The batch process is started with a tracking ID
2. It connects to the database to get issue information
3. It establishes a WebSocket connection to stream progress
4. It initializes the issue agent from sahur-core
5. It gathers context information from sahur-mcp
6. It analyzes the issue and generates a solution
7. It updates the database with the solution
8. It terminates automatically

## WebSocket Communication

The batch process communicates with the frontend via WebSocket messages:

- `message`: Updates on the analysis progress
- `status`: Status changes of the issue
- `context`: Context information gathered
- `solution`: The final solution

## Dependencies

- sahur-core: Core agent logic and common library
- sahur-mcp: MCP proxy server for external integrations
