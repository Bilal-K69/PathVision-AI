"""Dijkstra's shortest path algorithm implementation."""

import heapq
from typing import Generator, Dict, Set, Optional, List
import networkx as nx

from pathvision.algorithms.base import PathfindingAlgorithm
from pathvision.models import AlgorithmStepState
from pathvision.logging_config import logger


class Dijkstra(PathfindingAlgorithm):
    """Dijkstra's shortest path algorithm.
    
    Guarantees optimal solution for graphs with non-negative edge weights.
    Explores nodes in order of their distance from the start node.
    """
    
    def search(self) -> Generator[AlgorithmStepState, None, None]:
        """Execute Dijkstra's algorithm with step-by-step execution.
        
        Yields:
            AlgorithmStepState objects at each exploration step
        """
        logger.info(f"Starting Dijkstra search: {self.start_node} -> {self.end_node}")
        
        # Initialize data structures
        distances: Dict[int, float] = {node: float('inf') for node in self.graph.nodes()}
        distances[self.start_node] = 0.0
        
        parent_map: Dict[int, Optional[int]] = {node: None for node in self.graph.nodes()}
        visited: Set[int] = set()
        frontier: Set[int] = set()
        
        # Priority queue: (distance, node)
        pq = [(0.0, self.start_node)]
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            # Skip if already visited
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
                distance_map=distances.copy(),
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
                    distance_map=distances.copy(),
                    queue_size=0,
                    is_final=True,
                    path=path
                )
                logger.info(f"Path found: {len(path)} nodes, distance: {distances[self.end_node]:.2f}m")
                return
            
            # Explore neighbors
            for neighbor in self.graph.neighbors(current):
                if neighbor in visited:
                    continue
                
                edge_weight = self._get_edge_weight(current, neighbor)
                new_distance = distances[current] + edge_weight
                
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    parent_map[neighbor] = current
                    frontier.add(neighbor)
                    heapq.heappush(pq, (new_distance, neighbor))
        
        # No path found
        logger.warning(f"No path found from {self.start_node} to {self.end_node}")
        yield self._create_state(
            current=None,
            visited=visited.copy(),
            frontier=frontier.copy(),
            parent_map=parent_map.copy(),
            distance_map=distances.copy(),
            is_final=True,
            path=None
        )
    
    @staticmethod
    def get_time_complexity() -> str:
        """Dijkstra time complexity."""
        return "O((V + E) log V)"
    
    @staticmethod
    def get_space_complexity() -> str:
        """Dijkstra space complexity."""
        return "O(V)"
    
    @staticmethod
    def is_optimal() -> bool:
        """Dijkstra guarantees optimal solution."""
        return True
    
    @staticmethod
    def uses_heuristic() -> bool:
        """Dijkstra doesn't use heuristic."""
        return False
