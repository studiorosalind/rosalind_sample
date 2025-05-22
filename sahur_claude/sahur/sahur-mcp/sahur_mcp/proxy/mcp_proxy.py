import os
import json
import logging
from typing import Dict, Any, List, Optional
import aiohttp

from sahur_core.mcp_server import MCPServer, Tool, Resource, Schema

logger = logging.getLogger(__name__)


class MCPProxy:
    """
    Proxy for MCP servers.
    
    This class is responsible for routing requests to the appropriate MCP server.
    """
    
    def __init__(self):
        """Initialize the MCP proxy."""
        self.servers: Dict[str, MCPServer] = {}
        self.external_servers: Dict[str, str] = {}
        self.session: Optional[aiohttp.ClientSession] = None
    
    def register_server(self, server: MCPServer) -> None:
        """
        Register an MCP server.
        
        Args:
            server: The MCP server to register
        """
        self.servers[server.name] = server
        logger.info(f"Registered MCP server: {server.name}")
    
    def register_external_server(self, name: str, url: str) -> None:
        """
        Register an external MCP server.
        
        Args:
            name: The name of the external server
            url: The URL of the external server
        """
        self.external_servers[name] = url
        logger.info(f"Registered external MCP server: {name} at {url}")
    
    async def get_session(self) -> aiohttp.ClientSession:
        """
        Get the HTTP session.
        
        Returns:
            The HTTP session
        """
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        
        return self.session
    
    async def close(self) -> None:
        """Close the HTTP session."""
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None
    
    def get_servers(self) -> List[Dict[str, Any]]:
        """
        Get a list of available servers.
        
        Returns:
            A list of server information
        """
        servers = []
        
        # Add local servers
        for name, server in self.servers.items():
            servers.append({
                "name": name,
                "type": "local",
                "description": server.__class__.__doc__ or "",
            })
        
        # Add external servers
        for name, url in self.external_servers.items():
            servers.append({
                "name": name,
                "type": "external",
                "url": url,
            })
        
        return servers
    
    def get_tools(self, server_name: str) -> List[Dict[str, Any]]:
        """
        Get a list of available tools for a server.
        
        Args:
            server_name: The name of the server
            
        Returns:
            A list of tool information
        """
        if server_name in self.servers:
            server = self.servers[server_name]
            return [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.input_schema.schema,
                    "output_schema": tool.output_schema.schema,
                }
                for tool in server.tools.values()
            ]
        
        # For external servers, we would need to fetch this information
        # For now, return an empty list
        return []
    
    def get_resources(self, server_name: str) -> List[Dict[str, Any]]:
        """
        Get a list of available resources for a server.
        
        Args:
            server_name: The name of the server
            
        Returns:
            A list of resource information
        """
        if server_name in self.servers:
            server = self.servers[server_name]
            return [
                {
                    "uri": resource.uri,
                    "description": resource.description,
                    "schema": resource.schema.schema,
                }
                for resource in server.resources.values()
            ]
        
        # For external servers, we would need to fetch this information
        # For now, return an empty list
        return []
    
    async def call_tool(
        self, server_name: str, tool_name: str, arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Call a tool on an MCP server.
        
        Args:
            server_name: The name of the server
            tool_name: The name of the tool
            arguments: The arguments for the tool
            
        Returns:
            The result of the tool call
        """
        # Check if this is a local server
        if server_name in self.servers:
            server = self.servers[server_name]
            
            if tool_name in server.tools:
                tool = server.tools[tool_name]
                return await tool.handler(arguments)
            else:
                raise ValueError(f"Tool not found: {tool_name}")
        
        # Check if this is an external server
        if server_name in self.external_servers:
            url = f"{self.external_servers[server_name]}/tools/{tool_name}"
            
            session = await self.get_session()
            
            async with session.post(url, json=arguments) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise ValueError(f"Error calling external tool: {error_text}")
                
                return await response.json()
        
        raise ValueError(f"Server not found: {server_name}")
    
    async def access_resource(self, server_name: str, uri: str) -> Dict[str, Any]:
        """
        Access a resource on an MCP server.
        
        Args:
            server_name: The name of the server
            uri: The URI of the resource
            
        Returns:
            The resource data
        """
        # Check if this is a local server
        if server_name in self.servers:
            server = self.servers[server_name]
            
            if uri in server.resources:
                resource = server.resources[uri]
                return await resource.handler()
            else:
                raise ValueError(f"Resource not found: {uri}")
        
        # Check if this is an external server
        if server_name in self.external_servers:
            url = f"{self.external_servers[server_name]}/resources/{uri}"
            
            session = await self.get_session()
            
            async with session.get(url) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise ValueError(f"Error accessing external resource: {error_text}")
                
                return await response.json()
        
        raise ValueError(f"Server not found: {server_name}")


# Create a global instance of the proxy
proxy = MCPProxy()
