"""Main ReasoningAgent implementation."""

from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel
import time

from ..base import BaseAgent, Tool
from .thinker import ThinkerAgent
from .grader import GraderAgent
from .beam_search import BeamSearch, ThoughtNode

class ReasoningResult(BaseModel):
    """Result of a reasoning task."""
    solution: str
    confidence: float
    reasoning_path: List[str]
    alternatives: List[Tuple[str, float]]
    execution_time: float
    iterations: int

class ReasoningAgent(BaseAgent):
    """
    Implements Tree of Thoughts reasoning with beam search.
    
    Components:
    1. ThinkerAgent: Generates possible next steps
    2. GraderAgent: Evaluates reasoning paths
    3. BeamSearch: Maintains top-k promising paths
    """
    
    def __init__(
        self,
        name: str = "reasoner",
        system_message: str = "I am a reasoning agent that uses Tree of Thoughts to solve complex problems",
        tools: Optional[List[Tool]] = None,
        beam_size: int = 3,
        max_depth: int = 5,
        verbose: bool = False,
    ) -> None:
        """Initialize ReasoningAgent.
        
        Args:
            name: Agent name
            system_message: System prompt
            tools: Available tools
            beam_size: Number of paths to explore
            max_depth: Maximum depth of reasoning
            verbose: Enable verbose logging
        """
        super().__init__(name, system_message, tools, verbose)
        
        # Initialize components
        self.thinker = ThinkerAgent(verbose=verbose)
        self.grader = GraderAgent(verbose=verbose)
        self.beam_search = BeamSearch(beam_size=beam_size)
        
        self.max_depth = max_depth
        self.context: Dict[str, Any] = {}
    
    def solve(
        self,
        problem: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> ReasoningResult:
        """Solve problem using Tree of Thoughts reasoning.
        
        Args:
            problem: Problem description
            context: Additional context
            
        Returns:
            Reasoning result with solution and path
        """
        start_time = time.time()
        self.context = context or {}
        iterations = 0
        
        # Initialize beam search with problem statement
        self.beam_search.initialize(problem)
        current_nodes = [self.beam_search.root]
        
        try:
            # Main reasoning loop
            while iterations < self.max_depth:
                self.log(f"Iteration {iterations + 1}")
                
                # Generate next thoughts for all current nodes
                all_expansions = []
                for node in current_nodes:
                    # Get thoughts from thinker
                    thoughts = self.thinker.generate_thoughts(
                        problem=problem,
                        current_state=node.content,
                        context=self.context,
                    )
                    
                    # Grade each thought
                    for thought in thoughts:
                        path = self.beam_search.get_path(node)
                        evaluation = self.grader.evaluate_thought(
                            thought=thought.content,
                            problem=problem,
                            context=self.context,
                            previous_thoughts=path,
                        )
                        
                        all_expansions.append(
                            (thought.content, evaluation.criteria.total_score)
                        )
                
                # Expand beam search with new thoughts
                current_nodes = self.beam_search.expand_nodes(
                    current_nodes,
                    all_expansions,
                )
                
                # Check if we've found a solution
                best_node = self.beam_search.get_best_node()
                if best_node and best_node.score > 0.95:  # Confidence threshold
                    return self._create_result(
                        best_node,
                        start_time,
                        iterations + 1,
                    )
                
                iterations += 1
            
            # If no perfect solution found, return best attempt
            best_node = self.beam_search.get_best_node()
            if best_node:
                return self._create_result(
                    best_node,
                    start_time,
                    iterations,
                )
            
            raise ValueError("No valid reasoning path found")
            
        except Exception as e:
            self.log(f"Error during reasoning: {e}")
            raise
    
    def _create_result(
        self,
        node: ThoughtNode,
        start_time: float,
        iterations: int,
    ) -> ReasoningResult:
        """Create reasoning result from final node.
        
        Args:
            node: Final reasoning node
            start_time: Start time of reasoning
            iterations: Number of iterations
            
        Returns:
            Formatted reasoning result
        """
        return ReasoningResult(
            solution=node.content,
            confidence=node.score,
            reasoning_path=self.beam_search.get_path(node),
            alternatives=[
                (n.content, n.score)
                for n in self.beam_search.current_nodes
                if n != node
            ],
            execution_time=time.time() - start_time,
            iterations=iterations,
        )
    
    def visualize_reasoning(self, output_file: Optional[str] = None) -> None:
        """Visualize the reasoning tree.
        
        Args:
            output_file: Path to save visualization
        """
        self.beam_search.visualize(output_file)
