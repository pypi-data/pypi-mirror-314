"""Visualization tools for reasoning paths."""

from typing import Dict, List, Optional, Union
import graphviz
import matplotlib.pyplot as plt
import networkx as nx
from pydantic import BaseModel

class ThoughtNode(BaseModel):
    """Node representing a thought in visualization."""
    id: str
    content: str
    score: float
    metadata: Dict[str, Union[str, float, bool]]

class ReasoningGraph:
    """Graph visualization for reasoning paths."""
    
    def __init__(self) -> None:
        """Initialize reasoning graph."""
        self.graph = nx.DiGraph()
        self.dot = graphviz.Digraph(comment='Reasoning Path')
        
    def add_thought(
        self,
        thought: ThoughtNode,
        parent_id: Optional[str] = None,
    ) -> None:
        """Add thought node to graph.
        
        Args:
            thought: Thought node to add
            parent_id: Optional ID of parent thought
        """
        # Add to networkx graph
        self.graph.add_node(
            thought.id,
            content=thought.content,
            score=thought.score,
            metadata=thought.metadata,
        )
        if parent_id:
            self.graph.add_edge(parent_id, thought.id)
            
        # Add to graphviz
        self.dot.node(
            thought.id,
            f"{thought.content}\nScore: {thought.score:.2f}",
            color=self._get_color(thought.score),
        )
        if parent_id:
            self.dot.edge(parent_id, thought.id)
            
    def _get_color(self, score: float) -> str:
        """Get color based on score.
        
        Args:
            score: Node score
            
        Returns:
            Hex color code
        """
        # Red to green gradient
        r = int(255 * (1 - score))
        g = int(255 * score)
        return f"#{r:02x}{g:02x}00"
    
    def plot_networkx(
        self,
        figsize: tuple = (10, 8),
        with_labels: bool = True,
    ) -> None:
        """Plot graph using networkx.
        
        Args:
            figsize: Figure size
            with_labels: Whether to show labels
        """
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(self.graph)
        
        # Draw nodes
        nx.draw_networkx_nodes(
            self.graph,
            pos,
            node_color=[
                self.graph.nodes[node]["score"]
                for node in self.graph.nodes()
            ],
            cmap=plt.cm.RdYlGn,
            node_size=1000,
        )
        
        # Draw edges
        nx.draw_networkx_edges(self.graph, pos, edge_color='gray')
        
        if with_labels:
            labels = {
                node: f"{data['content']}\n{data['score']:.2f}"
                for node, data in self.graph.nodes(data=True)
            }
            nx.draw_networkx_labels(self.graph, pos, labels)
            
        plt.title("Reasoning Path")
        plt.axis('off')
        plt.show()
        
    def render_graphviz(
        self,
        filename: str = 'reasoning_path',
        format: str = 'png',
    ) -> None:
        """Render graph using graphviz.
        
        Args:
            filename: Output filename
            format: Output format
        """
        self.dot.render(filename, format=format, cleanup=True)
        
class RadarChart:
    """Radar chart for evaluation criteria."""
    
    def plot_criteria(
        self,
        criteria_dict: Dict[str, float],
        figsize: tuple = (8, 8),
    ) -> None:
        """Plot radar chart of evaluation criteria.
        
        Args:
            criteria_dict: Dictionary of criteria names and scores
            figsize: Figure size
        """
        categories = list(criteria_dict.keys())
        values = list(criteria_dict.values())
        
        # Complete the circle
        values += values[:1]
        angles = [
            n / float(len(categories)) * 2 * 3.14159
            for n in range(len(categories))
        ]
        angles += angles[:1]
        
        # Plot
        fig, ax = plt.subplots(
            figsize=figsize,
            subplot_kw=dict(projection='polar'),
        )
        
        # Draw the outline
        ax.plot(angles, values)
        ax.fill(angles, values, alpha=0.25)
        
        # Fix axis to go in the right order
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        
        # Add labels
        for angle, value, category in zip(angles[:-1], values[:-1], categories):
            ax.text(
                angle,
                value + 0.1,
                f'{category}\n({value:.2f})',
                ha='center',
                va='center',
            )
            
        plt.title("Evaluation Criteria")
        plt.show()
