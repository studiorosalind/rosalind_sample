# SAHUR Development Guide

This document provides instructions for setting up a development environment, managing dependencies, and building/deploying the SAHUR project.

## Development Environment Setup

### Prerequisites

- **Python 3.9+**: Required for sahur-core, sahur-server, sahur-batch, and sahur-mcp
- **Node.js 18+**: Required for sahur-web
- **Docker and Docker Compose**: Required for running the full system
- **PostgreSQL 14+**: Required for local development (or use Docker)
- **Git**: Required for version control

### Initial Setup

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

3. Install development tools:

```bash
# Install Python development tools
pip install black isort flake8 mypy pytest

# Install Node.js development tools
npm install -g eslint prettier
```

### Component Setup

#### sahur-core

```bash
cd sahur-core
pip install -e .
cd ..
```

#### sahur-server

```bash
cd sahur-server
pip install -e ../sahur-core
pip install -e .
cd ..
```

#### sahur-batch

```bash
cd sahur-batch
pip install -e ../sahur-core
pip install -e .
cd ..
```

#### sahur-mcp

```bash
cd sahur-mcp
pip install -e ../sahur-core
pip install -e .
cd ..
```

#### sahur-web

```bash
cd sahur-web
npm install
cd ..
```

## Development Workflow

### Running Components Locally

#### Database

You can run PostgreSQL locally or use Docker:

```bash
# Using Docker
docker run -d --name sahur-postgres -p 5432:5432 \
  -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=sahur \
  ankane/pgvector:latest
```

#### sahur-server

```bash
cd sahur-server
uvicorn sahur_server.main:app --reload --port 8000
```

#### sahur-mcp

```bash
cd sahur-mcp
uvicorn sahur_mcp.main:app --reload --port 8002
```

#### sahur-web

```bash
cd sahur-web
npm run dev
```

#### sahur-batch

The batch component is typically started by the server, but you can run it manually for testing:

```bash
cd sahur-batch
python -m sahur_batch.main --tracking-id <tracking_id>
```

### Running with Docker Compose

To run the entire system with Docker Compose:

```bash
docker-compose up
```

To rebuild containers after making changes:

```bash
docker-compose up --build
```

To run specific services:

```bash
docker-compose up sahur-server sahur-mcp
```

## Dependency Management

### Python Dependencies

Python dependencies are managed using `pyproject.toml` files in each component. To add a new dependency:

1. Add the dependency to the appropriate `pyproject.toml` file
2. Update the component's `requirements.txt` file if it exists
3. Reinstall the component in development mode

```bash
cd <component-directory>
pip install -e .
```

### JavaScript Dependencies

JavaScript dependencies are managed using `package.json` in the sahur-web component. To add a new dependency:

```bash
cd sahur-web
npm install <package-name>
# or for dev dependencies
npm install --save-dev <package-name>
```

## Testing

### Python Tests

```bash
# Run tests for a specific component
cd <component-directory>
pytest

# Run tests with coverage
pytest --cov=<component-name>

# Run specific tests
pytest tests/test_specific.py
```

### JavaScript Tests

```bash
cd sahur-web
npm test

# Run tests in watch mode
npm test -- --watch

# Run specific tests
npm test -- <test-pattern>
```

## Code Quality

### Python Code Quality

```bash
# Format code with Black
black <component-directory>

# Sort imports with isort
isort <component-directory>

# Lint code with flake8
flake8 <component-directory>

# Type check with mypy
mypy <component-directory>
```

### JavaScript Code Quality

```bash
cd sahur-web

# Format code with Prettier
npm run format

# Lint code with ESLint
npm run lint

# Type check with TypeScript
npm run type-check
```

## Database Management

### Migrations

Database migrations are managed using Alembic:

```bash
cd sahur-server

# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1
```

### Database Reset

To reset the database during development:

```bash
# Using Docker
docker-compose down -v
docker-compose up postgres

# Using local PostgreSQL
dropdb sahur
createdb sahur
cd sahur-server
alembic upgrade head
```

## Debugging

### Python Debugging

You can use the Python debugger (pdb) or an IDE like VS Code for debugging:

```python
import pdb; pdb.set_trace()  # Add this line where you want to break
```

### JavaScript Debugging

For frontend debugging:

1. Use browser developer tools (F12)
2. Use `console.log()` statements
3. Use the React Developer Tools browser extension
4. Use the Redux DevTools browser extension (if using Redux)

## Deployment

### Production Deployment

For production deployment:

1. Build Docker images:

```bash
docker-compose build
```

2. Push Docker images to a registry:

```bash
docker tag sahur-server:latest your-registry/sahur-server:latest
docker push your-registry/sahur-server:latest
# Repeat for other components
```

3. Deploy using Kubernetes, Docker Swarm, or your preferred orchestration tool

### Environment Variables

The following environment variables should be set in production:

#### Common

- `ENVIRONMENT`: Set to `production`
- `LOG_LEVEL`: Set to `INFO` or `WARNING`

#### sahur-server

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Secret key for JWT tokens
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins for CORS
- `MCP_SERVER_URL`: URL of the MCP server

#### sahur-mcp

- `GITHUB_TOKEN`: GitHub API token
- `SLACK_BOT_TOKEN`: Slack Bot token
- `SENTRY_TOKEN`: Sentry API token

#### sahur-web

- `NEXT_PUBLIC_API_URL`: URL of the API server
- `NEXT_PUBLIC_WS_URL`: WebSocket URL of the API server

### Monitoring

For production monitoring:

1. Set up logging to a centralized logging service
2. Set up metrics collection using Prometheus
3. Set up alerting for critical errors
4. Set up uptime monitoring

## Troubleshooting

### Common Issues

#### Database Connection Issues

- Check that PostgreSQL is running
- Check the `DATABASE_URL` environment variable
- Check that the database exists
- Check that the user has the correct permissions

#### API Connection Issues

- Check that the API server is running
- Check the `NEXT_PUBLIC_API_URL` environment variable
- Check CORS configuration

#### WebSocket Connection Issues

- Check that the API server is running
- Check the `NEXT_PUBLIC_WS_URL` environment variable
- Check WebSocket configuration

#### Docker Issues

- Check that Docker and Docker Compose are installed
- Check that Docker daemon is running
- Check Docker logs: `docker-compose logs <service-name>`

### Getting Help

If you encounter issues not covered here:

1. Check the issue tracker for similar issues
2. Ask for help in the project's communication channels
3. Create a new issue with detailed information about the problem
