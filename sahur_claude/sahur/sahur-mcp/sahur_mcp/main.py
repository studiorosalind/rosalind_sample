import os
import sys
import logging
import argparse
from typing import Dict, Any, List
import asyncio
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from sahur_mcp.proxy import proxy
from sahur_mcp.servers import cause_context_server, history_context_server

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="SAHUR MCP",
    description="MCP proxy server for SAHUR",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, this should be restricted
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define request and response models
class ToolRequest(BaseModel):
    """Request model for calling a tool."""
    arguments: Dict[str, Any]


class ResourceResponse(BaseModel):
    """Response model for accessing a resource."""
    data: Dict[str, Any]


class ServerInfo(BaseModel):
    """Information about an MCP server."""
    name: str
    type: str
    description: str = ""
    url: str = ""


class ToolInfo(BaseModel):
    """Information about an MCP tool."""
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]


class ResourceInfo(BaseModel):
    """Information about an MCP resource."""
    uri: str
    description: str
    schema: Dict[str, Any]


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    version: str


@app.on_event("startup")
async def startup_event():
    """
    Startup event handler.
    
    This function is called when the application starts up.
    """
    logger.info("Starting SAHUR MCP")
    
    # Register local servers
    proxy.register_server(cause_context_server)
    proxy.register_server(history_context_server)
    
    # Register external servers
    github_url = os.getenv("GITHUB_MCP_URL")
    if github_url:
        proxy.register_external_server("github", github_url)
    
    slack_url = os.getenv("SLACK_MCP_URL")
    if slack_url:
        proxy.register_external_server("slack", slack_url)
    
    sentry_url = os.getenv("SENTRY_MCP_URL")
    if sentry_url:
        proxy.register_external_server("sentry", sentry_url)
    
    logger.info("SAHUR MCP started")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event handler.
    
    This function is called when the application shuts down.
    """
    logger.info("Shutting down SAHUR MCP")
    await proxy.close()


@app.get("/servers", response_model=List[ServerInfo])
async def get_servers():
    """
    Get a list of available servers.
    
    Returns:
        A list of server information
    """
    return proxy.get_servers()


@app.get("/tools/{server_name}", response_model=List[ToolInfo])
async def get_tools(server_name: str):
    """
    Get a list of available tools for a server.
    
    Args:
        server_name: The name of the server
        
    Returns:
        A list of tool information
    """
    try:
        return proxy.get_tools(server_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/resources/{server_name}", response_model=List[ResourceInfo])
async def get_resources(server_name: str):
    """
    Get a list of available resources for a server.
    
    Args:
        server_name: The name of the server
        
    Returns:
        A list of resource information
    """
    try:
        return proxy.get_resources(server_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/tools/{server_name}/{tool_name}")
async def call_tool(server_name: str, tool_name: str, request: ToolRequest):
    """
    Call a tool on an MCP server.
    
    Args:
        server_name: The name of the server
        tool_name: The name of the tool
        request: The request containing the arguments
        
    Returns:
        The result of the tool call
    """
    try:
        return await proxy.call_tool(server_name, tool_name, request.arguments)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception(f"Error calling tool: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/resources/{server_name}/{uri:path}", response_model=ResourceResponse)
async def access_resource(server_name: str, uri: str):
    """
    Access a resource on an MCP server.
    
    Args:
        server_name: The name of the server
        uri: The URI of the resource
        
    Returns:
        The resource data
    """
    try:
        data = await proxy.access_resource(server_name, uri)
        return {"data": data}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception(f"Error accessing resource: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Health check response
    """
    return {
        "status": "ok",
        "version": "0.1.0",
    }


def main():
    """
    Main entry point.
    
    Returns:
        Exit code
    """
    import uvicorn
    
    parser = argparse.ArgumentParser(description="SAHUR MCP Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8002, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    
    args = parser.parse_args()
    
    uvicorn.run(
        "sahur_mcp.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
    )
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
