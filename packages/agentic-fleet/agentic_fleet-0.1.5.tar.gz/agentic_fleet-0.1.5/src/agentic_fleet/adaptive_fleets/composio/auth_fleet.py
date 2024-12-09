"""Composio Auth Fleet for authentication and authorization tasks."""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel
import logging

from ..base import AdaptiveFleet, AgentConfig
from ...communication import Message, MessageType
from .client import ComposioClient, ComposioConfig

logger = logging.getLogger(__name__)

class ComposioAuthParameters(BaseModel):
    """Parameters for Composio Auth agent."""
    role: str = "auth"
    capabilities: List[str] = ["authentication", "authorization"]
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000

class ComposioAuthFleet(AdaptiveFleet):
    """Fleet specialized in authentication and authorization using Composio."""
    
    def __init__(
        self,
        name: str = "composio-auth-fleet",
        config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize Composio Auth fleet.
        
        Args:
            name: Fleet name
            config: Optional configuration
        """
        super().__init__(name, config)
        self.client = ComposioClient()
        self.agents: Dict[str, str] = {}  # Map of agent_id to composio_agent_id
        
    async def adapt(self, context: Dict[str, Any]) -> None:
        """Adapt auth fleet based on requirements.
        
        Args:
            context: Current context
        """
        auth_requirements = context.get("auth_requirements", [])
        
        for requirement in auth_requirements:
            await self._add_auth_agent(requirement)
            
    async def _add_auth_agent(self, requirement: str) -> None:
        """Add authentication agent using Composio.
        
        Args:
            requirement: Auth requirement
        """
        agent_id = f"auth-{requirement}"
        
        # Create Composio agent
        parameters = ComposioAuthParameters(
            capabilities=[*ComposioAuthParameters().capabilities, requirement],
        )
        
        agent = await self.client.create_agent(
            agent_type="auth",
            parameters=parameters.dict(),
        )
        
        # Store Composio agent ID
        self.agents[agent_id] = agent["id"]
        
        # Add to fleet
        config = AgentConfig(
            role="auth-specialist",
            capabilities=parameters.capabilities,
            parameters={"requirement": requirement},
            priority=2,
        )
        await self.add_agent(agent_id, config)
        
    async def execute(
        self,
        task: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute authentication task using Composio.
        
        Args:
            task: Task description
            context: Task context
            
        Returns:
            Auth results
        """
        # Find appropriate agent
        agent_id = next(iter(self.agents.values()))  # Simplified selection
        
        # Execute task with Composio
        result = await self.client.execute_task(
            agent_id=agent_id,
            task={
                "type": "auth",
                "description": task,
                "context": context,
            },
        )
        
        return result
