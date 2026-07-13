"""A* shortest path algorithm implementation."""

import heapq
import math
from typing import Generator, Dict, Set, Optional, List, Callable
import networkx as nx

from pathvision.algorithms.base import PathfindingAlgorithm
from pathvision.models import AlgorithmStepState
from pathvision.logging_config import logger
from pathvision.utils import haversine_distance


class AStar(PathfindingAlgorithm):
    """A* shortest path algorithm.
    
    Uses a heuristic function to guide the search, typically faster than Dijkstra
    while still guaranteeing optimal solution. Works well with geographic coordinates.
    """
    
    def __init__(self, graph: nx.MultiDiGraph, start: int, end: int, 
                 heuristic: Optional[Callable[[int, int], float]] = None):
        """Initialize A* algorithm.
        
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
        """Execute A* algorithm with step-by-step execution.
        
        Yields:
            AlgorithmStepState objects at each exploration step
        """
        logger.info(f"Starting A* search: {self.start_node} -> {self.end_node}")
        
        # Initialize data structures
        g_score: Dict[int, float] = {node: float('inf') for node in self.graph.nodes()}
        g_score[self.start_node] = 0.0
        
        f_score: Dict[int, float] = {node: float('inf') for node in self.graph.nodes()}
        f_score[self.start_node] = self.heuristic(self.start_node)
        
        parent_map: Dict[int, Optional[int]] = {node: None for node in self.graph.nodes()}
        visited: Set[int] = set()
        frontier: Set[int] = {self.start_node}
        
        # Priority queue: (f_score, node)
        pq = [(f_score[self.start_node], self.start_node)]
        
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
                distance_map=g_score.copy(),
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
                    distance_map=g_score.copy(),
                    queue_size=0,
                    is_final=True,
                    path=path
                )
                logger.info(f"Path found: {len(path)} nodes, distance: {g_score[self.end_node]:.2f}m")
                return
            
            # Explore neighbors
            for neighbor in self.graph.neighbors(current):
                if neighbor in visited:
                    continue
                
                edge_weight = self._get_edge_weight(current, neighbor)
                tentative_g = g_score[current] + edge_weight
                
                if tentative_g < g_score[neighbor]:
                    parent_map[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor)
                    frontier.add(neighbor)
                    heapq.heappush(pq, (f_score[neighbor], neighbor))
        
        # No path found
        logger.warning(f"No path found from {self.start_node} to {self.end_node}")
        yield self._create_state(
            current=None,
            visited=visited.copy(),
            frontier=frontier.copy(),
            parent_map=parent_map.copy(),
            distance_map=g_score.copy(),
            is_final=True,
            path=None
        )
    
    @staticmethod
    def get_time_complexity() -> str:
        """A* time complexity."""
        return "O((V + E) log V)"
    
    @staticmethod
    def get_space_complexity() -> str:
        """A* space complexity."""
        return "O(V)"
    
    @staticmethod
    def is_optimal() -> bool:
        """A* with admissible heuristic guarantees optimal solution."""
        return True
    
    @staticmethod
    def uses_heuristic() -> bool:
        """A* uses heuristic function."""
        return True
