"""Base classes for adaptive fleets."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class AgentConfig(BaseModel):
    """Configuration for an agent in the fleet."""
    role: str
    capabilities: List[str]
    parameters: Dict[str, Any] = Field(default_factory=dict)
    priority: int = 0

class AdaptiveFleet(ABC):
    """Base class for adaptive fleets."""
    
    def __init__(
        self,
        name: str,
        config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize adaptive fleet.
        
        Args:
            name: Fleet name
            config: Optional configuration
        """
        self.name = name
        self.config = config or {}
        self.agents: Dict[str, AgentConfig] = {}
        
    @abstractmethod
    async def adapt(self, context: Dict[str, Any]) -> None:
        """Adapt fleet composition based on context.
        
        Args:
            context: Current context
        """
        pass
        
    @abstractmethod
    async def execute(
        self,
        task: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute task using fleet.
        
        Args:
            task: Task description
            context: Task context
            
        Returns:
            Task results
        """
        pass
        
    @abstractmethod
    async def evaluate(
        self,
        results: Dict[str, Any],
        context: Dict[str, Any],
    ) -> float:
        """Evaluate fleet performance.
        
        Args:
            results: Task results
            context: Evaluation context
            
        Returns:
            Performance score
        """
        pass
        
    async def add_agent(self, agent_id: str, config: AgentConfig) -> None:
        """Add agent to fleet.
        
        Args:
            agent_id: Agent identifier
            config: Agent configuration
        """
        self.agents[agent_id] = config
        
    async def remove_agent(self, agent_id: str) -> None:
        """Remove agent from fleet.
        
        Args:
            agent_id: Agent identifier
        """
        if agent_id in self.agents:
            del self.agents[agent_id]
            
    def get_agent_config(self, agent_id: str) -> Optional[AgentConfig]:
        """Get agent configuration.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Agent configuration if exists
        """
        return self.agents.get(agent_id)
        
    def list_agents(self) -> List[str]:
        """List all agents in fleet.
        
        Returns:
            List of agent identifiers
        """
        return list(self.agents.keys())
