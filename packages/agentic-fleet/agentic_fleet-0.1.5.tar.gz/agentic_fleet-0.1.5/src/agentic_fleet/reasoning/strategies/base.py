"""Base strategy interface."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class StrategyMetadata(BaseModel):
    """Metadata about strategy application."""
    name: str
    description: str
    applicability_score: float
    confidence: float
    steps_taken: List[str]
    artifacts: Dict[str, Any]

class Strategy(ABC):
    """Base class for problem-solving strategies."""
    
    def __init__(self, name: str, description: str) -> None:
        """Initialize strategy.
        
        Args:
            name: Strategy name
            description: Strategy description
        """
        self.name = name
        self.description = description
    
    @abstractmethod
    def is_applicable(self, problem: str, context: Dict[str, Any]) -> float:
        """Check if strategy is applicable to problem.
        
        Args:
            problem: Problem description
            context: Problem context
            
        Returns:
            Applicability score between 0 and 1
        """
        pass
    
    @abstractmethod
    def apply(
        self,
        problem: str,
        context: Dict[str, Any],
        **kwargs: Any,
    ) -> List[str]:
        """Apply strategy to generate next thoughts.
        
        Args:
            problem: Problem description
            context: Problem context
            **kwargs: Additional parameters
            
        Returns:
            List of generated thoughts
        """
        pass
    
    @abstractmethod
    def get_prompt_template(self) -> str:
        """Get prompt template for strategy.
        
        Returns:
            Prompt template string
        """
        pass
    
    def get_metadata(self) -> StrategyMetadata:
        """Get strategy metadata.
        
        Returns:
            Strategy metadata
        """
        return StrategyMetadata(
            name=self.name,
            description=self.description,
            applicability_score=0.0,
            confidence=0.0,
            steps_taken=[],
            artifacts={},
        )
