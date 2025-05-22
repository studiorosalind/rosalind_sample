"""
Mock MCP server module.

This module provides mock implementations of MCP server classes and functions.
"""

from typing import Dict, Any, List, Optional, Callable
import json


class Schema:
    """Schema for MCP tools and resources."""
    
    def __init__(self, schema: Dict[str, Any]):
        """
        Initialize the schema.
        
        Args:
            schema: The schema definition
        """
        self.schema = schema


class Tool:
    """Tool for MCP server."""
    
    def __init__(
        self,
        name: str,
        description: str,
        handler: Callable[[Dict[str, Any]], Any],
        input_schema: Schema,
        output_schema: Schema,
    ):
        """
        Initialize the tool.
        
        Args:
            name: The name of the tool
            description: The description of the tool
            handler: The handler function for the tool
            input_schema: The input schema for the tool
            output_schema: The output schema for the tool
        """
        self.name = name
        self.description = description
        self.handler = handler
        self.input_schema = input_schema
        self.output_schema = output_schema


class Resource:
    """Resource for MCP server."""
    
    def __init__(
        self,
        uri: str,
        description: str,
        handler: Callable[[], Any],
        schema: Schema,
    ):
        """
        Initialize the resource.
        
        Args:
            uri: The URI of the resource
            description: The description of the resource
            handler: The handler function for the resource
            schema: The schema for the resource
        """
        self.uri = uri
        self.description = description
        self.handler = handler
        self.schema = schema


class MCPServer:
    """MCP server."""
    
    def __init__(self, name: str, description: str = ""):
        """
        Initialize the MCP server.
        
        Args:
            name: The name of the server
            description: The description of the server
        """
        self.name = name
        self.description = description
        self.tools: Dict[str, Tool] = {}
        self.resources: Dict[str, Resource] = {}
    
    def add_tool(self, tool: Tool) -> None:
        """
        Add a tool to the server.
        
        Args:
            tool: The tool to add
        """
        self.tools[tool.name] = tool
    
    def add_resource(self, resource: Resource) -> None:
        """
        Add a resource to the server.
        
        Args:
            resource: The resource to add
        """
        self.resources[resource.uri] = resource
