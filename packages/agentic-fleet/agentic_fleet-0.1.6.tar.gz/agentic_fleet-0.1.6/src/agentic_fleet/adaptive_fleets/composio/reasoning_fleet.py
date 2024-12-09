"""Composio Reasoning Fleet for advanced reasoning and analysis tasks."""

from typing import Dict, List, Any, Optional
from enum import Enum
from pydantic import BaseModel
import logging

from ..base import AdaptiveFleet, AgentConfig
from ...communication import Message, MessageType
from .client import ComposioClient, ComposioConfig

logger = logging.getLogger(__name__)

class ReasoningCapability(str, Enum):
    """Capabilities for reasoning agents."""
    DEDUCTION = "deduction"
    INDUCTION = "induction"
    ABDUCTION = "abduction"
    ANALOGY = "analogy"
    COUNTERFACTUAL = "counterfactual"
    CAUSAL = "causal"
    TEMPORAL = "temporal"

class ComposioReasoningParameters(BaseModel):
    """Parameters for Composio Reasoning agent."""
    role: str = "reasoner"
    capabilities: List[ReasoningCapability] = [ReasoningCapability.DEDUCTION]
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000
    context_window: int = 8000

class ComposioReasoningFleet(AdaptiveFleet):
    """Fleet for advanced reasoning and analysis tasks."""

    def __init__(self, protocol=None):
        """Initialize the reasoning fleet.
        
        Args:
            protocol: Communication protocol for fleet coordination
        """
        super().__init__(protocol)
        self.client = ComposioClient()

    async def create_agent(
        self,
        name: str,
        capabilities: Optional[List[ReasoningCapability]] = None,
        parameters: Optional[Dict[str, Any]] = None
    ):
        """Create a new reasoning agent.
        
        Args:
            name: Name of the agent
            capabilities: List of reasoning capabilities
            parameters: Additional parameters for agent configuration
            
        Returns:
            Configured agent instance
        """
        # Set default capabilities if none provided
        if capabilities is None:
            capabilities = [ReasoningCapability.DEDUCTION]
            
        # Create base parameters
        agent_params = ComposioReasoningParameters(
            capabilities=capabilities
        )
        
        # Update with any additional parameters
        if parameters:
            agent_params = agent_params.model_copy(update=parameters)
            
        # Create agent config
        config = AgentConfig(
            name=name,
            role=agent_params.role,
            capabilities=agent_params.capabilities,
            parameters=agent_params.model_dump()
        )
        
        # Register agent with fleet
        agent = await self.client.create_agent(
            agent_type="reasoning",
            parameters=config.model_dump()
        )
        
        return agent

    async def execute_task(
        self,
        agent: Any,
        task: str,
        context: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        """Execute a reasoning task.
        
        Args:
            agent: Agent to execute the task
            task: Task description
            context: Additional context for the task
            **kwargs: Additional arguments for task execution
            
        Returns:
            Task execution results
        """
        # Prepare task message
        message = Message(
            type=MessageType.TASK,
            content={
                "task": task,
                "context": context or {},
                **kwargs
            }
        )
        
        # Send task to agent and get response
        response = await self.client.execute_task(
            agent_id=agent.id,
            task_message=message.model_dump()
        )
        
        return response

    async def analyze(
        self,
        agent: Any,
        data: Any,
        analysis_type: str,
        parameters: Optional[Dict[str, Any]] = None
    ):
        """Perform analysis on data.
        
        Args:
            agent: Agent to perform the analysis
            data: Data to analyze
            analysis_type: Type of analysis to perform
            parameters: Additional parameters for analysis
            
        Returns:
            Analysis results
        """
        # Prepare analysis context
        context = {
            "data": data,
            "analysis_type": analysis_type,
            "parameters": parameters or {}
        }
        
        # Execute analysis task
        result = await self.execute_task(
            agent=agent,
            task=f"Perform {analysis_type} analysis",
            context=context
        )
        
        return result

    async def adapt(self, feedback: Any) -> None:
        """Adapt the fleet based on feedback.
        
        Args:
            feedback: Feedback data for adaptation
        """
        # For now, just log the feedback
        logger.info(f"Received feedback for adaptation: {feedback}")
        
    async def evaluate(self, metrics: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate fleet performance.
        
        Args:
            metrics: Metrics to evaluate
            
        Returns:
            Evaluation results
        """
        # For now, return dummy metrics
        return {
            "accuracy": 0.95,
            "latency": 0.1
        }
        
    async def execute(self, task: Any) -> Any:
        """Execute a task using the fleet.
        
        Args:
            task: Task to execute
            
        Returns:
            Task execution results
        """
        # For now, just execute the task directly
        return await self.execute_task(
            agent=None,  # Will be created as needed
            task=str(task)
        )
