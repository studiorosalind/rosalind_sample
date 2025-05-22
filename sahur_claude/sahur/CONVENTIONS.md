# SAHUR Code Conventions

This document outlines the coding conventions, naming rules, and style guides for the SAHUR project. Following these conventions ensures consistency across the codebase and makes it easier for developers to understand and maintain the code.

## General Conventions

### Project Structure

- Each component is a separate package with its own directory
- All components follow a similar structure for consistency
- Common code is placed in the sahur-core component
- Each component has its own README.md file

### Git Workflow

- Use feature branches for new features and bug fixes
- Branch naming: `feature/feature-name` or `bugfix/issue-number-description`
- Commit messages should be clear and descriptive
- Pull requests should be reviewed by at least one other developer
- Squash commits before merging

### Documentation

- All public APIs should be documented
- Use docstrings for functions, classes, and modules
- Keep documentation up-to-date with code changes
- Use Markdown for documentation files

## Language-Specific Conventions

### Python (sahur-core, sahur-server, sahur-batch, sahur-mcp)

#### Code Style

- Follow PEP 8 style guide
- Use Black for code formatting
- Use isort for import sorting
- Use flake8 for linting
- Maximum line length: 88 characters (Black default)

#### Naming Conventions

- Classes: `PascalCase`
- Functions and methods: `snake_case`
- Variables and attributes: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private attributes and methods: `_leading_underscore`
- Module names: `snake_case`
- Package names: `snake_case`

#### Type Hints

- Use type hints for all function parameters and return values
- Use `Optional` for parameters that can be `None`
- Use `Union` for parameters that can be multiple types
- Use `List`, `Dict`, `Set`, etc. for container types
- Use `Any` sparingly and only when necessary

#### Imports

- Group imports in the following order:
  1. Standard library imports
  2. Third-party library imports
  3. Local application imports
- Use absolute imports for external modules
- Use relative imports for internal modules

#### Error Handling

- Use specific exception types
- Handle exceptions at the appropriate level
- Log exceptions with context information
- Provide meaningful error messages

#### Testing

- Write unit tests for all public APIs
- Use pytest for testing
- Aim for high test coverage
- Use fixtures for test setup
- Use mocks for external dependencies

### TypeScript/JavaScript (sahur-web)

#### Code Style

- Use ESLint for linting
- Use Prettier for code formatting
- Maximum line length: 100 characters

#### Naming Conventions

- Classes and interfaces: `PascalCase`
- Functions and methods: `camelCase`
- Variables: `camelCase`
- Constants: `UPPER_SNAKE_CASE`
- Private properties and methods: `_leadingUnderscore`
- File names: `kebab-case.ts` or `kebab-case.tsx`
- Component files: `PascalCase.tsx`

#### TypeScript

- Use strict type checking
- Define interfaces for all data structures
- Use type annotations for function parameters and return values
- Use generics where appropriate
- Avoid using `any` type

#### React

- Use functional components with hooks
- Use TypeScript for component props
- Use CSS modules or TailwindCSS for styling
- Use context API for global state
- Use custom hooks for reusable logic

#### Imports

- Group imports in the following order:
  1. React and related libraries
  2. Third-party libraries
  3. Local components and utilities
- Sort imports alphabetically within each group

#### Error Handling

- Use error boundaries for React components
- Handle API errors gracefully
- Provide user-friendly error messages
- Log errors to the console in development

#### Testing

- Use Jest for unit testing
- Use React Testing Library for component testing
- Write tests for all components and utilities
- Use mocks for external dependencies

## Component-Specific Conventions

### sahur-core

- Models should be defined using Pydantic
- Use dataclasses for internal data structures
- Workflows should be defined using LangGraph
- Utility functions should be grouped by functionality

### sahur-server

- API endpoints should be organized by resource
- Use dependency injection for services
- Database models should be defined using SQLAlchemy
- Use Pydantic for request and response models
- WebSocket handlers should be in the websockets module

### sahur-batch

- Processor logic should be in the processor module
- Use async/await for I/O operations
- Use logging for tracking progress
- Handle errors gracefully and report them

### sahur-web

- Use Next.js pages for routing
- Use components for reusable UI elements
- Use hooks for state management and side effects
- Use TailwindCSS for styling
- Use TypeScript for type safety

### sahur-mcp

- MCP servers should be in the servers module
- Proxy logic should be in the proxy module
- Use async/await for I/O operations
- Handle errors gracefully and report them

## Database Conventions

### Table Naming

- Table names should be plural and snake_case
- Junction tables should be named after both tables they connect
- Use descriptive names for tables and columns

### Column Naming

- Primary keys: `id`
- Foreign keys: `table_name_id`
- Timestamps: `created_at`, `updated_at`
- Boolean columns: `is_active`, `has_feature`
- Use descriptive names for columns

### Indexes

- Add indexes for frequently queried columns
- Add indexes for foreign keys
- Use unique indexes for unique constraints

## API Conventions

### Endpoints

- Use RESTful conventions for API endpoints
- Use plural nouns for resources
- Use nested routes for related resources
- Use query parameters for filtering and pagination

### HTTP Methods

- GET: Retrieve resources
- POST: Create resources
- PUT: Update resources (full update)
- PATCH: Update resources (partial update)
- DELETE: Delete resources

### Response Formats

- Use JSON for all responses
- Use consistent response structure
- Include status code in the response
- Include error messages for failed requests

### Error Handling

- Use appropriate HTTP status codes
- Provide detailed error messages
- Include error codes for client-side handling
- Log errors on the server side

## WebSocket Conventions

### Message Format

- Use JSON for all messages
- Include message type in the message
- Include timestamp in the message
- Use consistent message structure

### Message Types

- `message`: Chat messages
- `status`: Status updates
- `context`: Context information
- `solution`: Solution information

### Error Handling

- Send error messages to the client
- Log errors on the server side
- Reconnect automatically on connection loss
