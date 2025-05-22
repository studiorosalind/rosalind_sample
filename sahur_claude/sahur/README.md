# SAHUR

**S**mart **A**I-powered **H**elp for **U**nderstanding and **R**esolving issues

SAHUR is an interactive issue analysis and resolution system that uses AI to significantly reduce the resources development organizations spend on issue response.

## Overview

SAHUR is designed to help development teams quickly analyze and resolve issues by leveraging AI to understand the context, identify root causes, and suggest solutions. The system integrates with existing tools and workflows to provide a seamless experience for developers.

## Architecture

SAHUR is built as a monorepo with five main components:

1. **sahur-core**: Common library used by all components
2. **sahur-server**: API server and issue tracking manager
3. **sahur-batch**: Dynamic issue processing instance
4. **sahur-web**: Frontend UI
5. **sahur-mcp**: MCP (Model Context Protocol) proxy server

For more details, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Features

- **Slack Integration**: Receive and process issue reports directly from Slack
- **Real-time Analysis**: Watch the AI's thought process in real-time
- **Interactive UI**: Interact with the analysis process through a web interface
- **Context Gathering**: Automatically gather relevant context from various sources
- **Solution Generation**: Generate detailed solutions with step-by-step instructions
- **MCP Integration**: Leverage the Model Context Protocol for external integrations

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.9+ (for local development)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your-org/sahur.git
cd sahur
```

2. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the services:

```bash
docker-compose up
```

4. Access the web interface at http://localhost:3000

### Development

For local development, see [DEVELOPMENT.md](DEVELOPMENT.md).

## Usage

### Analyzing an Issue

1. In Slack, use the `/sahur analyze` command with a description of the issue
2. SAHUR will create a new issue tracking record and provide a link to the real-time analysis page
3. Watch the AI analyze the issue and interact with it if needed
4. Review the solution and implement the suggested fixes

### Monitoring Issues

1. Access the web interface at http://localhost:3000
2. View all active and resolved issues
3. Filter and search for specific issues
4. Access detailed analysis and solution reports

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md): Detailed architecture overview
- [CONVENTIONS.md](CONVENTIONS.md): Code conventions and style guide
- [DEVELOPMENT.md](DEVELOPMENT.md): Development setup and workflow
- [COMPONENT_TEMPLATE.md](COMPONENT_TEMPLATE.md): Template for new components

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
