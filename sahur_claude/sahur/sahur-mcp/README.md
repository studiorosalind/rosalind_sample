# SAHUR MCP

The MCP (Model Context Protocol) proxy server for the SAHUR (Smart AI-powered Help for Understanding and Resolving) system.

## Features

- Integration with external MCP servers (GitHub, Slack, Sentry, etc.)
- Custom MCP server for internal data and functionality
- Unified interface for sahur-core agents to access tools and resources
- Proxy functionality to route requests to appropriate MCP servers

## Installation

First, install the sahur-core package in development mode:

```bash
cd ../sahur-core
pip install -e .
```

Then, install this package in development mode:

```bash
cd ../sahur-mcp
pip install -e .
```

## Configuration

Create a `.env` file in the root directory with the following variables:

```
GITHUB_TOKEN=your_github_token
SLACK_BOT_TOKEN=your_slack_bot_token
SENTRY_TOKEN=your_sentry_token
```

## Running the Server

```bash
uvicorn sahur_mcp.main:app --reload --port 8002
```

## MCP Servers

The SAHUR MCP proxy integrates with the following MCP servers:

### External MCP Servers

- **GitHub**: Access to repositories, issues, pull requests, etc.
- **Slack**: Integration with Slack channels, messages, users, etc.
- **Sentry**: Access to error tracking and monitoring data

### Internal MCP Servers

- **CauseContext**: Tools for retrieving and analyzing cause context
- **HistoryContext**: Tools for retrieving and analyzing historical context

## API Endpoints

- `POST /tools/{server_name}/{tool_name}`: Call an MCP tool
- `GET /resources/{server_name}/{uri}`: Access an MCP resource
- `GET /servers`: List available MCP servers
- `GET /tools/{server_name}`: List available tools for a server
- `GET /resources/{server_name}`: List available resources for a server
- `GET /health`: Health check endpoint

## Tool Examples

### CauseContext Tools

- `getCauseContext(eventTransactionId)`: Get cause context for an event transaction

### HistoryContext Tools

- `getHistoryContext(issueDescription)`: Get historical context for an issue description

### GitHub Tools

- `getFileContent(repo, path, ref)`: Get the content of a file from a GitHub repository
- `getIssue(repo, issueNumber)`: Get details of a GitHub issue
