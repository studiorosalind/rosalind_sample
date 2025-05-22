# SAHUR Server

The API server and issue tracking manager for the SAHUR (Smart AI-powered Help for Understanding and Resolving) system.

## Features

- REST API endpoints for issue management
- WebSocket gateway for real-time communication
- Slack webhook integration for receiving issue reports
- PostgreSQL database integration for issue tracking
- Dynamic creation of sahur-batch instances for issue processing

## Installation

First, install the sahur-core package in development mode:

```bash
cd ../sahur-core
pip install -e .
```

Then, install this package in development mode:

```bash
cd ../sahur-server
pip install -e .
```

## Configuration

Create a `.env` file in the root directory with the following variables:

```
DATABASE_URL=postgresql://user:password@localhost:5432/sahur
SLACK_SIGNING_SECRET=your_slack_signing_secret
SLACK_BOT_TOKEN=your_slack_bot_token
MCP_SERVER_URL=http://localhost:8002
BATCH_COMMAND=python -m sahur_batch.main
```

## Running the Server

```bash
uvicorn sahur_server.main:app --reload --port 8000
```

## API Endpoints

- `POST /api/issues`: Create a new issue
- `GET /api/issues`: List all issues
- `GET /api/issues/{issue_id}`: Get issue details
- `PUT /api/issues/{issue_id}`: Update issue
- `DELETE /api/issues/{issue_id}`: Delete issue
- `POST /api/slack/events`: Slack events webhook
- `GET /api/health`: Health check endpoint

## WebSocket Endpoints

- `/ws/issues/{issue_id}`: Real-time updates for a specific issue

## Database Schema

The server uses PostgreSQL with the following main tables:

- `issues`: Stores issue metadata
- `issue_tracking`: Tracks the status of issue analysis
- `issue_messages`: Stores messages related to issue analysis
- `users`: Stores user information
