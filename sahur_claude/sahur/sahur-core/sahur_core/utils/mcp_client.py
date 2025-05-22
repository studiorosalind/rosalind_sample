from typing import Dict, List, Any, Optional
import json
import aiohttp
import logging

logger = logging.getLogger(__name__)


class MCPClient:
    """
    Client for interacting with MCP (Model Context Protocol) servers.
    
    This client provides methods for calling MCP tools and accessing MCP resources.
    """
    
    def __init__(self, base_url: str):
        """
        Initialize the MCP client.
        
        Args:
            base_url: The base URL of the MCP server
        """
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        """Set up the client session when entering an async context."""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close the client session when exiting an async context."""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def call_tool(
        self,
        server_name: str,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Call an MCP tool.
        
        Args:
            server_name: The name of the MCP server
            tool_name: The name of the tool to call
            arguments: The arguments to pass to the tool
            
        Returns:
            The result of the tool call
        """
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        url = f"{self.base_url}/tools/{server_name}/{tool_name}"
        
        try:
            async with self.session.post(url, json=arguments) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Error calling MCP tool: {error_text}")
                    raise Exception(f"Error calling MCP tool: {error_text}")
                
                return await response.json()
        except Exception as e:
            logger.exception(f"Exception calling MCP tool: {e}")
            raise
    
    async def access_resource(
        self,
        server_name: str,
        uri: str
    ) -> Dict[str, Any]:
        """
        Access an MCP resource.
        
        Args:
            server_name: The name of the MCP server
            uri: The URI of the resource to access
            
        Returns:
            The resource data
        """
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        url = f"{self.base_url}/resources/{server_name}/{uri}"
        
        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Error accessing MCP resource: {error_text}")
                    raise Exception(f"Error accessing MCP resource: {error_text}")
                
                return await response.json()
        except Exception as e:
            logger.exception(f"Exception accessing MCP resource: {e}")
            raise
    
    async def get_cause_context(self, event_transaction_id: str) -> Dict[str, Any]:
        """
        Get cause context information for an issue.
        
        Args:
            event_transaction_id: The transaction ID associated with the issue
            
        Returns:
            The cause context data
        """
        return await self.call_tool(
            server_name="sahur-mcp",
            tool_name="getCauseContext",
            arguments={"eventTransactionId": event_transaction_id}
        )
    
    async def get_history_context(self, issue_description: str) -> Dict[str, Any]:
        """
        Get historical context information for an issue.
        
        Args:
            issue_description: The description of the issue
            
        Returns:
            The history context data
        """
        return await self.call_tool(
            server_name="sahur-mcp",
            tool_name="getHistoryContext",
            arguments={"issueDescription": issue_description}
        )
    
    async def get_file_content(self, repo: str, path: str, ref: str = "main") -> str:
        """
        Get the content of a file from a GitHub repository.
        
        Args:
            repo: The repository in the format "owner/repo"
            path: The path to the file
            ref: The branch or commit reference
            
        Returns:
            The file content
        """
        result = await self.call_tool(
            server_name="github",
            tool_name="getFileContent",
            arguments={
                "repo": repo,
                "path": path,
                "ref": ref
            }
        )
        
        return result.get("content", "")
