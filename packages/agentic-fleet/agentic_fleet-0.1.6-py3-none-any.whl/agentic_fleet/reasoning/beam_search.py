"""Beam search implementation for managing reasoning paths."""

from typing import List, Optional, Tuple
from dataclasses import dataclass, field
from queue import PriorityQueue

@dataclass
class ThoughtNode:
    """Node in the reasoning tree."""
    content: str
    score: float
    parent: Optional['ThoughtNode'] = None
    children: List['ThoughtNode'] = field(default_factory=list)
    depth: int = 0
    
    def __lt__(self, other: 'ThoughtNode') -> bool:
        """Enable priority queue comparison."""
        return self.score > other.score  # Higher scores have priority

class BeamSearch:
    """Implements beam search for exploring reasoning paths."""
    
    def __init__(self, beam_size: int = 3) -> None:
        """Initialize beam search.
        
        Args:
            beam_size: Number of paths to maintain
        """
        self.beam_size = beam_size
        self.root: Optional[ThoughtNode] = None
        self.current_nodes: List[ThoughtNode] = []
    
    def initialize(self, root_content: str) -> None:
        """Initialize search with root node.
        
        Args:
            root_content: Content for root node
        """
        self.root = ThoughtNode(content=root_content, score=1.0)
        self.current_nodes = [self.root]
    
    def expand_nodes(
        self,
        nodes: List[ThoughtNode],
        expansions: List[Tuple[str, float]],
    ) -> List[ThoughtNode]:
        """Expand current nodes with new thoughts.
        
        Args:
            nodes: Current nodes to expand
            expansions: List of (content, score) tuples for new nodes
            
        Returns:
            New set of current nodes after beam search
        """
        # Create priority queue for beam search
        candidates = PriorityQueue()
        
        # Add all expansions to priority queue
        for parent in nodes:
            for content, score in expansions:
                child = ThoughtNode(
                    content=content,
                    score=score,
                    parent=parent,
                    depth=parent.depth + 1,
                )
                parent.children.append(child)
                candidates.put((-score, id(child), child))  # Negative score for max heap
        
        # Select top-k nodes
        selected = []
        while len(selected) < self.beam_size and not candidates.empty():
            _, _, node = candidates.get()
            selected.append(node)
        
        return selected
    
    def get_path(self, node: ThoughtNode) -> List[str]:
        """Get path from root to node.
        
        Args:
            node: Target node
            
        Returns:
            List of thought contents in path
        """
        path = []
        current = node
        while current:
            path.append(current.content)
            current = current.parent
        return list(reversed(path))
    
    def get_best_node(self) -> Optional[ThoughtNode]:
        """Get highest scoring current node.
        
        Returns:
            Best node or None if no nodes
        """
        if not self.current_nodes:
            return None
        return max(self.current_nodes, key=lambda x: x.score)
    
    def visualize(self, output_file: Optional[str] = None) -> None:
        """Visualize the reasoning tree.
        
        Args:
            output_file: Path to save visualization
        """
        try:
            import graphviz
        except ImportError:
            print("graphviz package required for visualization")
            return
        
        dot = graphviz.Digraph(comment='Reasoning Tree')
        
        def add_nodes(node: ThoughtNode) -> None:
            """Recursively add nodes to graph."""
            node_id = str(id(node))
            dot.node(
                node_id,
                f"{node.content}\n(score: {node.score:.2f})",
            )
            
            for child in node.children:
                child_id = str(id(child))
                dot.edge(node_id, child_id)
                add_nodes(child)
        
        if self.root:
            add_nodes(self.root)
            
        if output_file:
            dot.render(output_file, view=True)
