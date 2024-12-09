"""Grader agent for evaluating reasoning paths."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from ..base import BaseAgent, Tool

class EvaluationCriteria(BaseModel):
    """Evaluation criteria for grading thoughts."""
    
    relevance: float = Field(
        default=0.0,
        description="How relevant the thought is to solving the problem",
        ge=0.0,
        le=1.0,
    )
    novelty: float = Field(
        default=0.0,
        description="How novel/creative the thought is",
        ge=0.0,
        le=1.0,
    )
    feasibility: float = Field(
        default=0.0,
        description="How feasible/practical the thought is to implement",
        ge=0.0,
        le=1.0,
    )
    completeness: float = Field(
        default=0.0,
        description="How complete/thorough the thought is",
        ge=0.0,
        le=1.0,
    )
    efficiency: float = Field(
        default=0.0,
        description="How efficient the proposed solution is",
        ge=0.0,
        le=1.0,
    )
    risk: float = Field(
        default=0.0,
        description="Level of risk/uncertainty (lower is better)",
        ge=0.0,
        le=1.0,
    )
    impact: float = Field(
        default=0.0,
        description="Potential impact if successful",
        ge=0.0,
        le=1.0,
    )
    
    def weighted_score(self, weights: Optional[Dict[str, float]] = None) -> float:
        """Calculate weighted score across all criteria.
        
        Args:
            weights: Optional weights for each criterion
            
        Returns:
            Weighted score between 0 and 1
        """
        if weights is None:
            weights = {
                "relevance": 0.25,
                "novelty": 0.1,
                "feasibility": 0.2,
                "completeness": 0.15,
                "efficiency": 0.1,
                "risk": 0.1,
                "impact": 0.1,
            }
            
        score = 0.0
        for field, weight in weights.items():
            score += getattr(self, field) * weight
        return score

class ThoughtEvaluation(BaseModel):
    """Evaluation of a thought path."""
    thought_content: str
    criteria: EvaluationCriteria
    feedback: str
    suggestions: List[str]

class GraderAgent(BaseAgent):
    """Agent responsible for evaluating reasoning paths."""
    
    def __init__(
        self,
        name: str = "grader",
        system_message: str = """I am a Grader agent that evaluates reasoning paths.
        I carefully assess each path based on multiple criteria and provide detailed feedback.""",
        tools: Optional[List[Tool]] = None,
        verbose: bool = False,
    ) -> None:
        """Initialize GraderAgent.
        
        Args:
            name: Agent name
            system_message: System prompt
            tools: Available tools
            verbose: Enable verbose logging
        """
        super().__init__(name, system_message, tools, verbose)
    
    def evaluate_thought(
        self,
        thought: str,
        problem: str,
        context: Dict[str, Any],
        previous_thoughts: List[str],
    ) -> ThoughtEvaluation:
        """Evaluate a thought based on multiple criteria.
        
        Args:
            thought: Thought to evaluate
            problem: Original problem
            context: Additional context
            previous_thoughts: Previous thoughts in path
            
        Returns:
            Thought evaluation
        """
        prompt = self._create_evaluation_prompt(
            thought,
            problem,
            context,
            previous_thoughts,
        )
        
        # In real implementation, this would use LLM to evaluate
        # Placeholder implementation
        criteria = EvaluationCriteria(
            relevance=0.8,
            novelty=0.6,
            feasibility=0.7,
            completeness=0.75,
            efficiency=0.65,
            risk=0.3,
            impact=0.7,
        )
        
        return ThoughtEvaluation(
            thought_content=thought,
            criteria=criteria,
            feedback="Good progress toward solution",
            suggestions=["Consider edge cases"],
        )
    
    def _create_evaluation_prompt(
        self,
        thought: str,
        problem: str,
        context: Dict[str, Any],
        previous_thoughts: List[str],
    ) -> str:
        """Create prompt for thought evaluation.
        
        Args:
            thought: Thought to evaluate
            problem: Problem description
            context: Additional context
            previous_thoughts: Previous thoughts
            
        Returns:
            Formatted prompt
        """
        previous = "\n".join(f"- {t}" for t in previous_thoughts)
        
        return f"""Given the problem: {problem}

Previous thoughts:
{previous}

Current thought to evaluate:
{thought}

Additional context:
{context}

Evaluate this thought based on:
1. Relevance (0-1): How relevant is it to solving the problem?
2. Novelty (0-1): How creative/innovative is the approach?
3. Feasibility (0-1): How feasible/practical is the thought to implement?
4. Completeness (0-1): How complete/thorough is the thought?
5. Efficiency (0-1): How efficient is the proposed solution?
6. Risk (0-1): Level of risk/uncertainty (lower is better)
7. Impact (0-1): Potential impact if successful

For each criterion:
1. Assign a score between 0 and 1
2. Provide specific justification
3. Suggest potential improvements

Also consider:
- How well does it build on previous thoughts?
- Are there any logical flaws or gaps?
- What are the strongest and weakest aspects?"""
