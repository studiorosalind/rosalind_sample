# SAHUR Manual Demo Guide

This guide provides step-by-step instructions for testing the SAHUR system components.

## Prerequisites

- Docker and Docker Compose installed
- Basic knowledge of command line tools

## Step 1: Set up environment

Copy the example environment file:

```bash
cp .env.example .env
```

## Step 2: Start the services

Start all services using Docker Compose:

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database
- sahur-server (API server)
- sahur-mcp (MCP proxy server)
- sahur-batch-builder (Batch image builder)

The system is designed to automatically install sahur-core in each component's Docker container using the install_core.sh script.

## Step 3: Verify services are running

Check if all services are running:

```bash
docker-compose ps
```

You should see all services in the "Up" state.

## Step 4: Test the API server

Test the health endpoint of the API server:

```bash
curl http://localhost:8000/api/health
```

You should receive a JSON response with status "ok".

## Step 5: Simulate a Slack event

Send a simulated Slack event to the server:

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "type": "event_callback",
  "event": {
    "type": "app_mention",
    "text": "@sahur analyze NullPointerException in UserService.processUserRequest",
    "user": "U12345678",
    "channel": "C12345678",
    "event_ts": "1621234567.123456",
    "ts": "1621234567.123456"
  },
  "team_id": "T12345678",
  "api_app_id": "A12345678",
  "event_id": "Ev12345678",
  "event_time": 1621234567
}' http://localhost:8000/api/slack/events
```

This should return a JSON response with an issue ID.

## Step 6: Check the issue status

Using the issue ID from the previous step:

```bash
curl http://localhost:8000/api/issues/[ISSUE_ID]
```

Replace `[ISSUE_ID]` with the actual issue ID from the previous step.

## Step 7: Access the web UI

Open your browser and navigate to:

```
http://localhost:3000/issue/tracking/[ISSUE_ID]
```

Replace `[ISSUE_ID]` with the actual issue ID.

## Step 8: Clean up

When you're done testing, stop all services:

```bash
docker-compose down
```

## Troubleshooting

### Docker issues

If you encounter Docker-related issues:

1. Make sure Docker and Docker Compose are installed and running
2. Check Docker logs: `docker-compose logs [service-name]`
3. Try rebuilding the services: `docker-compose up -d --build`

### API issues

If the API server is not responding:

1. Check if the service is running: `docker-compose ps sahur-server`
2. Check the logs: `docker-compose logs sahur-server`
3. Make sure the database is running: `docker-compose ps postgres`

### sahur-core installation issues

If there are issues with sahur-core installation:

1. Check the logs: `docker-compose logs sahur-server` (or other component)
2. Make sure the volume mounts are correct in docker-compose.yml
3. Check if the install_core.sh script is executable

### Database issues

If there are database connection issues:

1. Check if the database is running: `docker-compose ps postgres`
2. Check the logs: `docker-compose logs postgres`
3. Make sure the DATABASE_URL in .env is correct

## Understanding the Docker Setup

The SAHUR system uses Docker Compose to manage multiple services:

1. **PostgreSQL**: Database for storing issue tracking information
2. **sahur-server**: API server that handles requests and manages issue tracking
3. **sahur-mcp**: MCP proxy server that provides tools and resources for the AI
4. **sahur-batch-builder**: Builds the sahur-batch image for dynamic issue processing

Each component has its own Dockerfile and install_core.sh script to handle the installation of sahur-core as a dependency.

The docker-compose.yml file defines the services, their dependencies, and volume mounts. The volume mounts are used to share the sahur-core directory with each component's container.
