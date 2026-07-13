"""Breadth-First Search algorithm implementation."""

from collections import deque
from typing import Generator, Dict, Set, Optional, List
import networkx as nx

from pathvision.algorithms.base import PathfindingAlgorithm
from pathvision.models import AlgorithmStepState
from pathvision.logging_config import logger


class BFS(PathfindingAlgorithm):
    """Breadth-First Search algorithm.
    
    Explores nodes level by level. Optimal for unweighted graphs.
    Uses O(V + E) time and O(V) space.
    """
    
    def search(self) -> Generator[AlgorithmStepState, None, None]:
        """Execute BFS with step-by-step execution.
        
        Yields:
            AlgorithmStepState objects at each exploration step
        """
        logger.info(f"Starting BFS: {self.start_node} -> {self.end_node}")
        
        # Initialize data structures
        queue = deque([self.start_node])
        visited: Set[int] = {self.start_node}
        parent_map: Dict[int, Optional[int]] = {self.start_node: None}
        distance_map: Dict[int, float] = {self.start_node: 0.0}
        frontier: Set[int] = {self.start_node}
        
        while queue:
            current = queue.popleft()
            frontier.discard(current)
            
            # Yield current state
            yield self._create_state(
                current=current,
                visited=visited.copy(),
                frontier=frontier.copy(),
                parent_map=parent_map.copy(),
                distance_map=distance_map.copy(),
                queue_size=len(queue)
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
                    visited.add(neighbor)
                    parent_map[neighbor] = current
                    distance_map[neighbor] = distance_map[current] + self._get_edge_weight(current, neighbor)
                    frontier.add(neighbor)
                    queue.append(neighbor)
        
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
        """BFS time complexity."""
        return "O(V + E)"
    
    @staticmethod
    def get_space_complexity() -> str:
        """BFS space complexity."""
        return "O(V)"
    
    @staticmethod
    def is_optimal() -> bool:
        """BFS is optimal for unweighted graphs."""
        return True
    
    @staticmethod
    def uses_heuristic() -> bool:
        """BFS doesn't use heuristic."""
        return False
