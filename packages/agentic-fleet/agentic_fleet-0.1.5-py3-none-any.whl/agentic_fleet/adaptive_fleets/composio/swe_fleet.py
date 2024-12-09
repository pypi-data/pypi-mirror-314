"""Composio SWE Fleet for software engineering tasks."""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel
import logging

from ..base import AdaptiveFleet, AgentConfig
from ...communication import Message, MessageType
from .client import ComposioClient, ComposioConfig

logger = logging.getLogger(__name__)

class ComposioSWEParameters(BaseModel):
    """Parameters for Composio SWE agent."""
    role: str = "software_engineer"
    capabilities: List[str] = [
        "code_review",
        "refactoring",
        "testing",
        "documentation",
    ]
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000
    review_policies: Dict[str, Any] = {
        "required_reviewers": 2,
        "enforce_style": True,
    }

class ComposioSWEFleet(AdaptiveFleet):
    """Fleet specialized in software engineering tasks using Composio."""
    
    def __init__(
        self,
        name: str = "composio-swe-fleet",
        config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize Composio SWE fleet.
        
        Args:
            name: Fleet name
            config: Optional configuration
        """
        super().__init__(name, config)
        self.client = ComposioClient()
        self.agents: Dict[str, str] = {}  # Map of agent_id to composio_agent_id
        
    async def adapt(self, context: Dict[str, Any]) -> None:
        """Adapt SWE fleet based on requirements.
        
        Args:
            context: Current context
        """
        code_tasks = context.get("code_tasks", [])
        
        for task in code_tasks:
            await self._add_swe_agent(task)
            
    async def _add_swe_agent(self, task: str) -> None:
        """Add SWE agent using Composio.
        
        Args:
            task: Code task
        """
        agent_id = f"swe-{task}"
        
        # Create Composio agent
        parameters = ComposioSWEParameters(
            capabilities=[*ComposioSWEParameters().capabilities, task],
        )
        
        agent = await self.client.create_agent(
            agent_type="software_engineer",
            parameters=parameters.dict(),
        )
        
        # Store Composio agent ID
        self.agents[agent_id] = agent["id"]
        
        # Add to fleet
        config = AgentConfig(
            role="swe-specialist",
            capabilities=parameters.capabilities,
            parameters={"task": task},
            priority=1,
        )
        await self.add_agent(agent_id, config)
        
    async def execute(
        self,
        task: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute SWE task using Composio.
        
        Args:
            task: Task description
            context: Task context
            
        Returns:
            Task results
        """
        # Find appropriate agent
        agent_id = next(iter(self.agents.values()))  # Simplified selection
        
        # Execute task with Composio
        result = await self.client.execute_task(
            agent_id=agent_id,
            task={
                "type": "software_engineer",
                "description": task,
                "context": context,
            },
        )
        
        return result
        
    async def evaluate(
        self,
        results: Dict[str, Any],
        context: Dict[str, Any],
    ) -> float:
        """Evaluate SWE results.
        
        Args:
            results: Task results
            context: Evaluation context
            
        Returns:
            Performance score
        """
        # Evaluate based on Composio results
        metrics = results.get("metrics", {})
        weights = {
            "code_quality": 0.3,
            "test_coverage": 0.3,
            "documentation": 0.2,
            "performance": 0.2,
        }
        
        score = sum(
            metrics.get(key, 0.0) * weight
            for key, weight in weights.items()
        )
        
        return score
