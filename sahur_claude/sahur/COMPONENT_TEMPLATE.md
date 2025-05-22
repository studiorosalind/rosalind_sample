# SAHUR Component Template

This document provides a template for creating new components in the SAHUR project. It outlines the recommended file structure, development patterns, and best practices to ensure consistency across the codebase.

## Component Structure

A typical SAHUR component should follow this structure:

```
sahur-{component}/
├── Dockerfile                 # Docker configuration
├── README.md                  # Component documentation
├── pyproject.toml             # Python package configuration (for Python components)
├── requirements.txt           # Dependencies for Docker build
├── sahur_{component}/         # Main package directory
│   ├── __init__.py            # Package initialization
│   ├── main.py                # Entry point
│   ├── api/                   # API endpoints (if applicable)
│   │   ├── __init__.py
│   │   └── ...
│   ├── models/                # Data models
│   │   ├── __init__.py
│   │   └── ...
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   └── ...
│   └── utils/                 # Utility functions
│       ├── __init__.py
│       └── ...
└── tests/                     # Unit tests
    ├── __init__.py
    ├── conftest.py            # Test fixtures
    └── ...
```

For JavaScript/TypeScript components (e.g., sahur-web), the structure should be:

```
sahur-{component}/
├── Dockerfile                 # Docker configuration
├── README.md                  # Component documentation
├── package.json               # Node.js package configuration
├── tsconfig.json              # TypeScript configuration
├── .eslintrc.js               # ESLint configuration
├── .prettierrc                # Prettier configuration
├── next.config.js             # Next.js configuration (if applicable)
├── src/                       # Source code
│   ├── pages/                 # Next.js pages (if applicable)
│   │   ├── _app.tsx
│   │   ├── index.tsx
│   │   └── ...
│   ├── components/            # React components
│   │   ├── common/
│   │   └── ...
│   ├── hooks/                 # React hooks
│   │   └── ...
│   ├── services/              # API services
│   │   └── ...
│   ├── utils/                 # Utility functions
│   │   └── ...
│   ├── styles/                # CSS/SCSS styles
│   │   └── ...
│   └── types/                 # TypeScript type definitions
│       └── ...
└── tests/                     # Unit tests
    └── ...
```

## Python Component Template

### pyproject.toml

```toml
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "sahur-{component}"
version = "0.1.0"
description = "{Component description}"
readme = "README.md"
authors = [
    {name = "SAHUR Team"}
]
requires-python = ">=3.9"
dependencies = [
    # List your dependencies here
    "sahur-core @ file://../sahur-core",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "mypy>=1.0.0",
]

[tool.setuptools]
packages = ["sahur_{component}"]

[project.scripts]
sahur-{component} = "sahur_{component}.main:main"
```

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install sahur-core
COPY ../sahur-core /app/sahur-core
RUN pip install -e /app/sahur-core

# Copy the application
COPY . .

# Expose the port (if needed)
EXPOSE 8000

# Run the application
CMD ["python", "-m", "sahur_{component}.main"]
```

### requirements.txt

```
# List your dependencies here
fastapi>=0.100.0
uvicorn>=0.22.0
pydantic>=2.0.0
python-dotenv>=1.0.0
```

### __init__.py

```python
"""
sahur-{component} package.

{Component description}
"""

__version__ = "0.1.0"
```

### main.py

```python
import os
import sys
import logging
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def main() -> int:
    """
    Main entry point.
    
    Returns:
        Exit code
    """
    parser = argparse.ArgumentParser(description="SAHUR {Component}")
    # Add your command-line arguments here
    
    args = parser.parse_args()
    
    # Your main logic here
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## JavaScript/TypeScript Component Template

### package.json

```json
{
  "name": "sahur-{component}",
  "version": "0.1.0",
  "description": "{Component description}",
  "main": "index.js",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
    "format": "prettier --write .",
    "type-check": "tsc --noEmit",
    "test": "jest"
  },
  "dependencies": {
    // List your dependencies here
  },
  "devDependencies": {
    // List your dev dependencies here
  }
}
```

### Dockerfile

```dockerfile
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000

CMD ["npm", "start"]
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules"]
}
```

## Development Patterns

### Python Components

1. **Dependency Injection**: Use dependency injection for services and repositories
2. **Type Hints**: Use type hints for all function parameters and return values
3. **Error Handling**: Use try-except blocks for error handling
4. **Logging**: Use the logging module for logging
5. **Configuration**: Use environment variables for configuration
6. **Testing**: Write unit tests for all public APIs

Example:

```python
from typing import Optional, List
import logging
from sqlalchemy.orm import Session

from sahur_core.models import Issue

logger = logging.getLogger(__name__)


class IssueService:
    """Service for managing issues."""
    
    def __init__(self, db: Session):
        """
        Initialize the issue service.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def get_issue(self, issue_id: str) -> Optional[Issue]:
        """
        Get an issue by ID.
        
        Args:
            issue_id: The ID of the issue
            
        Returns:
            The issue, or None if not found
        """
        try:
            return self.db.query(Issue).filter(Issue.id == issue_id).first()
        except Exception as e:
            logger.exception(f"Error getting issue {issue_id}: {e}")
            return None
    
    def get_issues(self) -> List[Issue]:
        """
        Get all issues.
        
        Returns:
            A list of issues
        """
        try:
            return self.db.query(Issue).all()
        except Exception as e:
            logger.exception(f"Error getting issues: {e}")
            return []
```

### JavaScript/TypeScript Components

1. **Functional Components**: Use functional components with hooks
2. **Type Safety**: Use TypeScript for type safety
3. **Custom Hooks**: Use custom hooks for reusable logic
4. **API Services**: Use services for API calls
5. **Error Handling**: Use try-catch blocks for error handling
6. **Testing**: Write unit tests for all components and utilities

Example:

```tsx
import React, { useState, useEffect } from 'react';
import { Issue } from '@/types';
import { issueService } from '@/services';

interface IssueListProps {
  status?: string;
}

export const IssueList: React.FC<IssueListProps> = ({ status }) => {
  const [issues, setIssues] = useState<Issue[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    const fetchIssues = async () => {
      try {
        setLoading(true);
        const data = await issueService.getIssues(status);
        setIssues(data);
        setError(null);
      } catch (err) {
        setError('Failed to fetch issues');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchIssues();
  }, [status]);
  
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  
  return (
    <div>
      <h2>Issues</h2>
      <ul>
        {issues.map((issue) => (
          <li key={issue.id}>
            <a href={`/issues/${issue.id}`}>{issue.title}</a>
          </li>
        ))}
      </ul>
    </div>
  );
};
```

## Best Practices

### General

1. **Documentation**: Document all public APIs
2. **Error Handling**: Handle errors gracefully
3. **Logging**: Log important events and errors
4. **Configuration**: Use environment variables for configuration
5. **Testing**: Write unit tests for all components
6. **Code Style**: Follow the project's code style guidelines

### Python

1. **Type Hints**: Use type hints for all function parameters and return values
2. **Docstrings**: Use docstrings for all functions, classes, and modules
3. **Exception Handling**: Use specific exception types
4. **Context Managers**: Use context managers for resource management
5. **Dependency Injection**: Use dependency injection for services and repositories

### JavaScript/TypeScript

1. **TypeScript**: Use TypeScript for type safety
2. **Functional Components**: Use functional components with hooks
3. **Custom Hooks**: Use custom hooks for reusable logic
4. **Error Boundaries**: Use error boundaries for error handling
5. **Memoization**: Use memoization for expensive calculations

## Integration with sahur-core

All components should integrate with sahur-core for common functionality:

1. **Models**: Use sahur-core models for data structures
2. **Workflows**: Use sahur-core workflows for issue analysis
3. **Utilities**: Use sahur-core utilities for common tasks

Example:

```python
from sahur_core.models import Issue, IssueStatus
from sahur_core.workflows import analyze_issue
from sahur_core.utils import format_issue

# Use sahur-core models
issue = Issue(
    id="issue-123",
    title="Example Issue",
    description="This is an example issue",
    status=IssueStatus.OPEN,
)

# Use sahur-core workflows
analyzed_issue = analyze_issue(issue)

# Use sahur-core utilities
formatted_issue = format_issue(analyzed_issue)
```

## Conclusion

Following this template will ensure consistency across the SAHUR project and make it easier for developers to understand and maintain the codebase. If you have any questions or suggestions, please refer to the project documentation or contact the project maintainers.
