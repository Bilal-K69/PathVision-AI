"""Base class for pathfinding algorithms in PathVision AI.

Defines the interface that all pathfinding algorithms must implement.
"""

from abc import ABC, abstractmethod
from typing import Generator, Dict, Set, List, Optional, Tuple
import networkx as nx
from pathvision.models import AlgorithmStepState
from pathvision.logging_config import logger


class PathfindingAlgorithm(ABC):
    """Abstract base class for pathfinding algorithms.
    
    All algorithms must implement step-by-step execution that yields
    AlgorithmStepState objects for visualization.
    
    Attributes:
        name: Name of the algorithm
        graph: NetworkX graph
        start_node: Starting node ID
        end_node: Destination node ID
    """
    
    def __init__(self, graph: nx.MultiDiGraph, start: int, end: int):
        """Initialize the algorithm.
        
        Args:
            graph: NetworkX MultiDiGraph representing the road network
            start: Starting node ID
            end: Destination node ID
        """
        self.name = self.__class__.__name__
        self.graph = graph
        self.start_node = start
        self.end_node = end
        self.steps_executed = 0
        logger.info(f"{self.name} initialized: {start} -> {end}")
    
    @abstractmethod
    def search(self) -> Generator[AlgorithmStepState, None, None]:
        """Execute the pathfinding algorithm.
        
        Must yield AlgorithmStepState objects representing each exploration step.
        The final state should have is_final=True and contain the path if found.
        
        Yields:
            AlgorithmStepState objects representing algorithm progression
        """
        pass
    
    def _get_edge_weight(self, u: int, v: int) -> float:
        """Get weight of an edge.
        
        Args:
            u: Source node ID
            v: Destination node ID
            
        Returns:
            Edge weight (defaults to 1.0 if not specified)
        """
        try:
            edge_data = self.graph.get_edge_data(u, v)
            if edge_data is None:
                return float('inf')
            
            # Handle MultiDiGraph
            if isinstance(edge_data, dict):
                first_key = list(edge_data.keys())[0]
                weight = edge_data[first_key].get('length', 1.0)
                return float(weight)
            
            return 1.0
        except Exception:
            return 1.0
    
    def _reconstruct_path(self, parent_map: Dict[int, Optional[int]], end: int) -> List[int]:
        """Reconstruct path from parent map.
        
        Args:
            parent_map: Mapping of nodes to their parents
            end: End node ID
            
        Returns:
            List of node IDs representing the path
        """
        path = []
        current = end
        
        while current is not None:
            path.append(current)
            current = parent_map.get(current)
        
        path.reverse()
        return path
    
    def _calculate_path_distance(self, path: List[int]) -> float:
        """Calculate total distance of a path.
        
        Args:
            path: List of node IDs
            
        Returns:
            Total distance in meters
        """
        if len(path) < 2:
            return 0.0
        
        distance = 0.0
        for i in range(len(path) - 1):
            distance += self._get_edge_weight(path[i], path[i + 1])
        
        return distance
    
    def _create_state(self,
                     current: Optional[int] = None,
                     visited: Optional[Set[int]] = None,
                     frontier: Optional[Set[int]] = None,
                     parent_map: Optional[Dict[int, Optional[int]]] = None,
                     distance_map: Optional[Dict[int, float]] = None,
                     queue_size: int = 0,
                     is_final: bool = False,
                     path: Optional[List[int]] = None) -> AlgorithmStepState:
        """Create an algorithm step state.
        
        Args:
            current: Current node being explored
            visited: Set of visited nodes
            frontier: Set of frontier nodes
            parent_map: Parent map for path reconstruction
            distance_map: Distance map
            queue_size: Size of search queue
            is_final: Whether this is the final state
            path: Final path if found
            
        Returns:
            AlgorithmStepState object
        """
        self.steps_executed += 1
        
        state = AlgorithmStepState(
            current_node=current,
            visited_nodes=visited or set(),
            frontier_nodes=frontier or set(),
            parent_map=parent_map or {},
            distance_map=distance_map or {},
            queue_size=queue_size,
            is_final=is_final,
            path=path,
            path_distance=self._calculate_path_distance(path) if path else None
        )
        
        return state
    
    def get_algorithm_info(self) -> Dict[str, str]:
        """Get information about the algorithm.
        
        Returns:
            Dictionary with algorithm metadata
        """
        return {
            'name': self.name,
            'time_complexity': self.get_time_complexity(),
            'space_complexity': self.get_space_complexity(),
            'optimal': str(self.is_optimal()),
            'heuristic': str(self.uses_heuristic())
        }
    
    @staticmethod
    @abstractmethod
    def get_time_complexity() -> str:
        """Get time complexity of the algorithm.
        
        Returns:
            Time complexity as string (e.g., "O((V+E)logV)")
        """
        pass
    
    @staticmethod
    @abstractmethod
    def get_space_complexity() -> str:
        """Get space complexity of the algorithm.
        
        Returns:
            Space complexity as string (e.g., "O(V)")
        """
        pass
    
    @staticmethod
    @abstractmethod
    def is_optimal() -> bool:
        """Check if algorithm guarantees optimal solution.
        
        Returns:
            True if algorithm is optimal
        """
        pass
    
    @staticmethod
    @abstractmethod
    def uses_heuristic() -> bool:
        """Check if algorithm uses heuristic function.
        
        Returns:
            True if algorithm uses heuristic
        """
        pass
