"""Base agent class and common utilities."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class Tool(BaseModel):
    """Base class for agent tools."""
    name: str
    description: str
    
    @abstractmethod
    def execute(self, **kwargs: Any) -> Any:
        """Execute the tool with given parameters."""
        pass

class BaseAgent(ABC):
    """Base class for all agents in the fleet."""
    
    def __init__(
        self,
        name: str,
        system_message: str,
        tools: Optional[List[Tool]] = None,
        verbose: bool = False,
    ) -> None:
        """Initialize base agent.
        
        Args:
            name: Agent name
            system_message: System prompt for the agent
            tools: List of tools available to the agent
            verbose: Enable verbose logging
        """
        self.name = name
        self.system_message = system_message
        self.tools = tools or []
        self.verbose = verbose
        self.memory: Dict[str, Any] = {}
    
    @abstractmethod
    def execute(self, task: str, **kwargs: Any) -> Any:
        """Execute a task with the agent.
        
        Args:
            task: Task description
            **kwargs: Additional task parameters
            
        Returns:
            Task execution result
        """
        pass
    
    def add_tool(self, tool: Tool) -> None:
        """Add a tool to the agent's capabilities.
        
        Args:
            tool: Tool to add
        """
        self.tools.append(tool)
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name.
        
        Args:
            name: Tool name
            
        Returns:
            Tool if found, None otherwise
        """
        return next((t for t in self.tools if t.name == name), None)
    
    def log(self, message: str) -> None:
        """Log a message if verbose mode is enabled.
        
        Args:
            message: Message to log
        """
        if self.verbose:
            print(f"[{self.name}] {message}")
    
    def clear_memory(self) -> None:
        """Clear agent's memory."""
        self.memory.clear()
