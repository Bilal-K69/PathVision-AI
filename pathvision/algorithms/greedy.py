"""Greedy Best-First Search algorithm implementation."""

import heapq
from typing import Generator, Dict, Set, Optional, List, Callable
import networkx as nx

from pathvision.algorithms.base import PathfindingAlgorithm
from pathvision.models import AlgorithmStepState
from pathvision.logging_config import logger
from pathvision.utils import haversine_distance


class GreedyBestFirst(PathfindingAlgorithm):
    """Greedy Best-First Search algorithm.
    
    Always expands the node with smallest heuristic value.
    Fast but does not guarantee optimal solution.
    """
    
    def __init__(self, graph: nx.MultiDiGraph, start: int, end: int,
                 heuristic: Optional[Callable[[int, int], float]] = None):
        """Initialize Greedy Best-First Search.
        
        Args:
            graph: NetworkX MultiDiGraph
            start: Starting node ID
            end: Destination node ID
            heuristic: Optional heuristic function (default: straight-line distance)
        """
        super().__init__(graph, start, end)
        self.heuristic = heuristic or self._default_heuristic
    
    def _default_heuristic(self, node: int) -> float:
        """Default heuristic: straight-line distance to goal.
        
        Args:
            node: Current node ID
            
        Returns:
            Estimated distance to goal in meters
        """
        try:
            if node not in self.graph.nodes or self.end_node not in self.graph.nodes:
                return 0.0
            
            node_data = self.graph.nodes[node]
            end_data = self.graph.nodes[self.end_node]
            
            lat1 = node_data.get('y', 0)
            lon1 = node_data.get('x', 0)
            lat2 = end_data.get('y', 0)
            lon2 = end_data.get('x', 0)
            
            # Use haversine distance in meters
            distance_km = haversine_distance(lat1, lon1, lat2, lon2)
            return distance_km * 1000  # Convert to meters
            
        except Exception:
            return 0.0
    
    def search(self) -> Generator[AlgorithmStepState, None, None]:
        """Execute Greedy Best-First Search with step-by-step execution.
        
        Yields:
            AlgorithmStepState objects at each exploration step
        """
        logger.info(f"Starting Greedy Best-First search: {self.start_node} -> {self.end_node}")
        
        parent_map: Dict[int, Optional[int]] = {self.start_node: None}
        distance_map: Dict[int, float] = {self.start_node: 0.0}
        visited: Set[int] = set()
        frontier: Set[int] = {self.start_node}
        
        # Priority queue: (heuristic_value, node)
        pq = [(self.heuristic(self.start_node), self.start_node)]
        
        while pq:
            _, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            visited.add(current)
            frontier.discard(current)
            
            # Yield current state
            yield self._create_state(
                current=current,
                visited=visited.copy(),
                frontier=frontier.copy(),
                parent_map=parent_map.copy(),
                distance_map=distance_map.copy(),
                queue_size=len(pq)
            )
            
            # Check if we reached the destination
            if current == self.end_node:
                path = self._reconstruct_path(parent_map, self.end_node)
                yield self._create_state(
                    current=current,
                    visited=visited.copy(),
                    frontier=frontier.copy(),
                    parent_map=parent_map.copy(),
                    distance_map=distance_map.copy(),
                    queue_size=0,
                    is_final=True,
                    path=path
                )
                logger.info(f"Path found: {len(path)} nodes")
                return
            
            # Explore neighbors
            for neighbor in self.graph.neighbors(current):
                if neighbor not in visited:
                    if neighbor not in parent_map:
                        parent_map[neighbor] = current
                        edge_weight = self._get_edge_weight(current, neighbor)
                        distance_map[neighbor] = distance_map.get(current, 0) + edge_weight
                        frontier.add(neighbor)
                        heapq.heappush(pq, (self.heuristic(neighbor), neighbor))
        
        # No path found
        logger.warning(f"No path found from {self.start_node} to {self.end_node}")
        yield self._create_state(
            current=None,
            visited=visited.copy(),
            frontier=frontier.copy(),
            parent_map=parent_map.copy(),
            distance_map=distance_map.copy(),
            is_final=True,
            path=None
        )
    
    @staticmethod
    def get_time_complexity() -> str:
        """Greedy Best-First time complexity."""
        return "O((V + E) log V)"
    
    @staticmethod
    def get_space_complexity() -> str:
        """Greedy Best-First space complexity."""
        return "O(V)"
    
    @staticmethod
    def is_optimal() -> bool:
        """Greedy Best-First does not guarantee optimal solution."""
        return False
    
    @staticmethod
    def uses_heuristic() -> bool:
        """Greedy Best-First uses heuristic function."""
        return True
