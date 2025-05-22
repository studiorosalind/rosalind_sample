# SAHUR Architecture

This document describes the architecture of the SAHUR system, including its components, their interactions, and data flow.

## System Overview

SAHUR is a monorepo project consisting of five main components:

1. **sahur-core**: Common library used by all components
2. **sahur-server**: API server and issue tracking manager
3. **sahur-batch**: Dynamic issue processing instance
4. **sahur-web**: Frontend UI
5. **sahur-mcp**: MCP (Model Context Protocol) proxy server

The system is designed to be modular, scalable, and maintainable, with clear separation of concerns between components.

## Component Architecture

### sahur-core

The core library provides common functionality used by all other components, including:

- Issue models and data structures
- LangGraph workflows for issue analysis
- LLM orchestration and integration
- Context management utilities
- Common utilities and helpers

All other components depend on sahur-core, which is installed as an editable dependency (`pip install -e ../sahur-core`).

### sahur-server

The server component is the central API server and issue tracking manager:

- Receives requests from Slack via webhooks
- Manages issue tracking state in PostgreSQL
- Dynamically creates sahur-batch instances for issue processing
- Provides REST API endpoints for the frontend
- Manages WebSocket connections for real-time updates

Key modules:
- `api/`: REST API endpoints
- `database/`: Database models and connection management
- `services/`: Business logic and service layer
- `websockets/`: WebSocket management for real-time communication
- `models/`: API request/response models

### sahur-batch

The batch component is a dynamic instance created for each issue:

- One instance per issue, created by sahur-server
- Processes a single issue and terminates when complete
- Streams analysis progress via WebSocket
- Integrates with sahur-mcp for context gathering
- Uses sahur-core for issue analysis

Key modules:
- `processor/`: Issue processing logic
- `database/`: Database models and connection management
- `utils/`: Utility functions and helpers

### sahur-web

The web component provides the frontend UI:

- Built with Next.js, TypeScript, and TailwindCSS
- Provides real-time monitoring of issue analysis
- Allows interaction with the analysis process
- Displays issue tracking information and solutions
- Responsive design for desktop and mobile

Key modules:
- `pages/`: Next.js pages and routing
- `components/`: Reusable UI components
- `hooks/`: React hooks for state management and API calls
- `styles/`: TailwindCSS styles and theme configuration
- `utils/`: Utility functions and helpers

### sahur-mcp

The MCP component is a proxy server for Model Context Protocol:

- Integrates with external MCP servers (GitHub, Slack, Sentry)
- Provides custom MCP servers for internal functionality
- Unified interface for sahur-core agents to access tools and resources
- Proxy functionality to route requests to appropriate MCP servers

Key modules:
- `servers/`: Custom MCP server implementations
- `proxy/`: MCP proxy functionality
- `utils/`: Utility functions and helpers

## Communication Patterns

The components communicate with each other using the following patterns:

1. **sahur-server ↔ sahur-core**: Internal function calls
   - The server uses core functionality directly through the library

2. **sahur-batch ↔ sahur-mcp**: HTTP API communication
   - The batch process calls MCP tools and accesses resources via HTTP

3. **sahur-batch ↔ sahur-web**: WebSocket real-time communication
   - The batch process streams updates to the web UI via WebSocket
   - The web UI sends user input back to the batch process

4. **sahur-server ↔ sahur-batch**: Process creation and management
   - The server creates and manages batch processes
   - Communication happens through the database and WebSocket

## Data Flow

1. **Issue Creation**:
   - User submits an issue via Slack
   - sahur-server receives the webhook and creates an issue in the database
   - sahur-server creates a sahur-batch instance for the issue

2. **Issue Analysis**:
   - sahur-batch connects to the database and retrieves issue information
   - sahur-batch establishes a WebSocket connection for real-time updates
   - sahur-batch uses sahur-mcp to gather context information
   - sahur-batch uses sahur-core to analyze the issue and generate a solution
   - sahur-batch streams updates to the web UI via WebSocket

3. **User Interaction**:
   - User views the analysis in the web UI
   - User can interact with the analysis process via the web UI
   - User input is sent to sahur-batch via WebSocket
   - sahur-batch incorporates user input into the analysis

4. **Solution Generation**:
   - sahur-batch generates a solution based on the analysis
   - sahur-batch updates the database with the solution
   - sahur-batch streams the solution to the web UI
   - sahur-batch terminates after the solution is generated

## Deployment Architecture

The system is deployed using Docker and Docker Compose:

- Each component has its own Dockerfile
- PostgreSQL is used as the database
- All components are connected via a Docker network
- sahur-batch instances are created dynamically by sahur-server

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   sahur-web     │◄────┤   sahur-server  │◄────┤   sahur-batch   │
│   (Next.js)     │     │   (FastAPI)     │     │   (Python)      │
│                 │     │                 │     │                 │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         │                       │                       │
         │                       ▼                       │
         │              ┌─────────────────┐              │
         │              │                 │              │
         └──────────────┤   PostgreSQL    │◄─────────────┘
                        │                 │
                        └────────┬────────┘
                                 │
                                 │
                                 ▼
                        ┌─────────────────┐
                        │                 │
                        │   sahur-mcp     │
                        │   (FastAPI)     │
                        │                 │
                        └─────────────────┘
```

## Security Considerations

- Authentication and authorization for API endpoints
- Secure storage of sensitive information (tokens, credentials)
- Input validation and sanitization
- Rate limiting and throttling
- CORS configuration for web UI
- Secure WebSocket connections

## Scalability Considerations

- Horizontal scaling of sahur-server instances
- Dynamic creation of sahur-batch instances
- Database connection pooling and optimization
- Caching of frequently accessed data
- Asynchronous processing of requests
