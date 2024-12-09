"""Composio API client."""

import os
from typing import Dict, Any, Optional
import httpx
from pydantic import BaseModel, Field
import logging
from dotenv import load_dotenv

from .exceptions import ComposioAuthError, ComposioAPIError

logger = logging.getLogger(__name__)

class ComposioConfig(BaseModel):
    """Composio API configuration."""
    api_key: str = Field(..., description="Composio API key")
    api_url: str = Field(
        default="https://api.composio.dev/v1",
        description="Composio API base URL",
    )

class ComposioClient:
    """Client for interacting with Composio API."""
    
    def __init__(self, config: Optional[ComposioConfig] = None):
        """Initialize Composio client.
        
        Args:
            config: Optional configuration, will load from env if not provided
            
        Raises:
            ComposioAuthError: If API key is not provided
        """
        if config is None:
            load_dotenv()
            api_key = os.getenv("COMPOSIO_API_KEY")
            if not api_key:
                raise ComposioAuthError("COMPOSIO_API_KEY not found in environment")
                
            config = ComposioConfig(
                api_key=api_key,
                api_url=os.getenv("COMPOSIO_API_URL", "https://api.composio.dev/v1"),
            )
        self.config = config
        self.client = httpx.AsyncClient(
            base_url=config.api_url,
            headers={
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json",
            },
            timeout=30.0,  # 30 second timeout
        )
        
    async def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle API response.
        
        Args:
            response: HTTP response
            
        Returns:
            Response data
            
        Raises:
            ComposioAuthError: If authentication fails
            ComposioAPIError: If API request fails
        """
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ComposioAuthError("Invalid API key") from e
            elif e.response.status_code == 403:
                raise ComposioAuthError("Insufficient permissions") from e
            else:
                raise ComposioAPIError(
                    f"API request failed: {e.response.text}"
                ) from e
                
        return response.json()
        
    async def create_agent(
        self,
        agent_type: str,
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Create a new Composio agent.
        
        Args:
            agent_type: Type of agent to create
            parameters: Agent configuration parameters
            
        Returns:
            Created agent details
            
        Raises:
            ComposioAuthError: If authentication fails
            ComposioAPIError: If agent creation fails
        """
        response = await self.client.post(
            "/agents",
            json={
                "type": agent_type,
                "parameters": parameters,
            },
        )
        return await self._handle_response(response)
        
    async def get_agent(self, agent_id: str) -> Dict[str, Any]:
        """Get agent details.
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Agent details
            
        Raises:
            ComposioAuthError: If authentication fails
            ComposioAPIError: If agent retrieval fails
        """
        response = await self.client.get(f"/agents/{agent_id}")
        return await self._handle_response(response)
        
    async def execute_task(
        self,
        agent_id: str,
        task: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute task with agent.
        
        Args:
            agent_id: Agent ID
            task: Task details
            
        Returns:
            Task results
            
        Raises:
            ComposioAuthError: If authentication fails
            ComposioAPIError: If task execution fails
        """
        response = await self.client.post(
            f"/agents/{agent_id}/execute",
            json=task,
        )
        return await self._handle_response(response)
        
    async def close(self) -> None:
        """Close client connection."""
        await self.client.aclose()
