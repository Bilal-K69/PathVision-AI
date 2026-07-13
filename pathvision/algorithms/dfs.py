"""Depth-First Search algorithm implementation."""

from typing import Generator, Dict, Set, Optional, List
import networkx as nx

from pathvision.algorithms.base import PathfindingAlgorithm
from pathvision.models import AlgorithmStepState
from pathvision.logging_config import logger


class DFS(PathfindingAlgorithm):
    """Depth-First Search algorithm.
    
    Explores as far as possible along each branch before backtracking.
    Does not guarantee shortest path but explores deeply.
    """
    
    def search(self) -> Generator[AlgorithmStepState, None, None]:
        """Execute DFS with step-by-step execution.
        
        Yields:
            AlgorithmStepState objects at each exploration step
        """
        logger.info(f"Starting DFS: {self.start_node} -> {self.end_node}")
        
        visited: Set[int] = set()
        parent_map: Dict[int, Optional[int]] = {}
        distance_map: Dict[int, float] = {self.start_node: 0.0}
        frontier: Set[int] = set()
        stack = [self.start_node]
        
        while stack:
            current = stack.pop()
            
            if current in visited:
                frontier.discard(current)
                continue
            
            visited.add(current)
            frontier.discard(current)
            parent_map[current] = parent_map.get(current, None)
            
            # Yield current state
            yield self._create_state(
                current=current,
                visited=visited.copy(),
                frontier=frontier.copy(),
                parent_map=parent_map.copy(),
                distance_map=distance_map.copy(),
                queue_size=len(stack)
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
                    parent_map[neighbor] = current
                    distance_map[neighbor] = distance_map.get(current, 0) + self._get_edge_weight(current, neighbor)
                    frontier.add(neighbor)
                    stack.append(neighbor)
        
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
        """DFS time complexity."""
        return "O(V + E)"
    
    @staticmethod
    def get_space_complexity() -> str:
        """DFS space complexity."""
        return "O(V)"
    
    @staticmethod
    def is_optimal() -> bool:
        """DFS does not guarantee optimal path."""
        return False
    
    @staticmethod
    def uses_heuristic() -> bool:
        """DFS doesn't use heuristic."""
        return False
