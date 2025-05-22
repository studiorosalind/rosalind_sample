# SAHUR Web

The frontend web interface for the SAHUR (Smart AI-powered Help for Understanding and Resolving) system.

## Features

- Modern React-based UI built with Next.js
- Real-time updates via WebSocket communication
- Issue tracking and management interface
- Analysis progress visualization
- Solution display with code snippets

## Installation

First, install dependencies:

```bash
npm install
```

## Configuration

Create a `.env.local` file in the root directory with the following variables:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
```

## Development

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Production Build

Build the application for production:

```bash
npm run build
```

Then start the production server:

```bash
npm start
```

## Docker

You can also run the application using Docker:

```bash
docker build -t sahur-web .
docker run -p 3000:3000 sahur-web
```

## Pages

- `/` - Home page with system overview
- `/issues` - List of all issues
- `/issues/[id]` - Details of a specific issue with real-time updates
- `/new-issue` - Form to create a new issue

## Dependencies

- Next.js - React framework
- React Query - Data fetching and caching
- Socket.io-client - WebSocket communication
- Chakra UI - UI component library
- React Syntax Highlighter - Code highlighting 