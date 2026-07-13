"""Data models for PathVision AI.

Defines core data structures for:
- Algorithm execution states
- Graph nodes and edges
- Statistics and metrics
"""

from dataclasses import dataclass, field
from typing import Set, Dict, List, Tuple, Optional, Any
from enum import Enum
import time


class ExecutionState(Enum):
    """State of algorithm execution."""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AlgorithmStepState:
    """State of a single algorithm step during execution.
    
    Attributes:
        current_node: Currently explored node
        visited_nodes: Set of all visited nodes
        frontier_nodes: Set of nodes in the frontier/queue
        parent_map: Mapping of nodes to their parents (for path reconstruction)
        distance_map: Mapping of nodes to their distances from start
        queue_size: Size of the search queue
        timestamp: Time when this step occurred
        is_final: Whether this is the final state
        path: Final path if found, None otherwise
        path_distance: Total distance of the path if found
    """
    current_node: Optional[int] = None
    visited_nodes: Set[int] = field(default_factory=set)
    frontier_nodes: Set[int] = field(default_factory=set)
    parent_map: Dict[int, Optional[int]] = field(default_factory=dict)
    distance_map: Dict[int, float] = field(default_factory=dict)
    queue_size: int = 0
    timestamp: float = field(default_factory=time.time)
    is_final: bool = False
    path: Optional[List[int]] = None
    path_distance: Optional[float] = None
    
    def copy(self) -> 'AlgorithmStepState':
        """Create a deep copy of the state.
        
        Returns:
            New AlgorithmStepState with copied data
        """
        return AlgorithmStepState(
            current_node=self.current_node,
            visited_nodes=self.visited_nodes.copy(),
            frontier_nodes=self.frontier_nodes.copy(),
            parent_map=self.parent_map.copy(),
            distance_map=self.distance_map.copy(),
            queue_size=self.queue_size,
            timestamp=self.timestamp,
            is_final=self.is_final,
            path=self.path.copy() if self.path else None,
            path_distance=self.path_distance
        )


@dataclass
class ExecutionStatistics:
    """Statistics collected during algorithm execution.
    
    Attributes:
        algorithm_name: Name of the algorithm
        city_name: Name of the city/graph
        start_node: Starting node ID
        end_node: Destination node ID
        execution_time_ms: Total execution time in milliseconds
        nodes_visited: Number of nodes visited
        nodes_explored: Number of nodes explored
        path_length: Length of the final path
        path_distance: Total distance of the path
        memory_used_mb: Memory used during execution
        queue_max_size: Maximum queue size during execution
        steps_count: Total number of exploration steps
        start_time: Timestamp when execution started
        end_time: Timestamp when execution ended
        graph_nodes_total: Total nodes in the graph
        graph_edges_total: Total edges in the graph
        time_complexity: Theoretical time complexity
        space_complexity: Theoretical space complexity
    """
    algorithm_name: str
    city_name: str
    start_node: int
    end_node: int
    execution_time_ms: float = 0.0
    nodes_visited: int = 0
    nodes_explored: int = 0
    path_length: int = 0
    path_distance: float = 0.0
    memory_used_mb: float = 0.0
    queue_max_size: int = 0
    steps_count: int = 0
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    graph_nodes_total: int = 0
    graph_edges_total: int = 0
    time_complexity: str = "O(1)"
    space_complexity: str = "O(1)"
    
    @property
    def exploration_percentage(self) -> float:
        """Calculate percentage of graph explored.
        
        Returns:
            Percentage of nodes explored relative to total nodes
        """
        if self.graph_nodes_total == 0:
            return 0.0
        return (self.nodes_explored / self.graph_nodes_total) * 100
    
    @property
    def efficiency_ratio(self) -> float:
        """Calculate efficiency ratio (path_length / nodes_explored).
        
        Returns:
            Efficiency ratio (lower is better)
        """
        if self.nodes_explored == 0:
            return 0.0
        return self.path_length / self.nodes_explored
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert statistics to dictionary.
        
        Returns:
            Dictionary representation of statistics
        """
        return {
            'algorithm': self.algorithm_name,
            'city': self.city_name,
            'start_node': self.start_node,
            'end_node': self.end_node,
            'execution_time_ms': self.execution_time_ms,
            'nodes_visited': self.nodes_visited,
            'nodes_explored': self.nodes_explored,
            'path_length': self.path_length,
            'path_distance': self.path_distance,
            'memory_used_mb': self.memory_used_mb,
            'queue_max_size': self.queue_max_size,
            'steps_count': self.steps_count,
            'exploration_percentage': self.exploration_percentage,
            'efficiency_ratio': self.efficiency_ratio,
        }


@dataclass
class GraphMetrics:
    """Metrics describing a graph structure.
    
    Attributes:
        node_count: Total number of nodes
        edge_count: Total number of edges
        is_weighted: Whether edges have weights
        is_directed: Whether graph is directed
        average_degree: Average degree of nodes
        density: Graph density (edges / possible_edges)
        largest_component_size: Size of largest connected component
        diameter: Diameter of the graph
        is_connected: Whether graph is connected
    """
    node_count: int
    edge_count: int
    is_weighted: bool = True
    is_directed: bool = False
    average_degree: float = 0.0
    density: float = 0.0
    largest_component_size: int = 0
    diameter: Optional[int] = None
    is_connected: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary.
        
        Returns:
            Dictionary representation of metrics
        """
        return {
            'node_count': self.node_count,
            'edge_count': self.edge_count,
            'is_weighted': self.is_weighted,
            'is_directed': self.is_directed,
            'average_degree': self.average_degree,
            'density': self.density,
            'largest_component_size': self.largest_component_size,
            'diameter': self.diameter,
            'is_connected': self.is_connected,
        }
