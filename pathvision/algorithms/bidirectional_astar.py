"""Bidirectional A* algorithm implementation."""

import heapq
from typing import Generator, Dict, Set, Optional, List, Callable, Tuple
import networkx as nx

from pathvision.algorithms.base import PathfindingAlgorithm
from pathvision.models import AlgorithmStepState
from pathvision.logging_config import logger
from pathvision.utils import haversine_distance


class BidirectionalAStar(PathfindingAlgorithm):
    """Bidirectional A* algorithm.
    
    Searches simultaneously from both start and goal nodes, typically much faster
    than unidirectional A* while still guaranteeing optimal solution.
    """
    
    def __init__(self, graph: nx.MultiDiGraph, start: int, end: int,
                 heuristic: Optional[Callable[[int, int], float]] = None):
        """Initialize Bidirectional A* algorithm.
        
        Args:
            graph: NetworkX MultiDiGraph
            start: Starting node ID
            end: Destination node ID
            heuristic: Optional heuristic function (default: straight-line distance)
        """
        super().__init__(graph, start, end)
        self.heuristic = heuristic or self._default_heuristic
    
    def _default_heuristic(self, node: int, target: int) -> float:
        """Default heuristic: straight-line distance between nodes.
        
        Args:
            node: Current node ID
            target: Target node ID
            
        Returns:
            Estimated distance in meters
        """
        try:
            if node not in self.graph.nodes or target not in self.graph.nodes:
                return 0.0
            
            node_data = self.graph.nodes[node]
            target_data = self.graph.nodes[target]
            
            lat1 = node_data.get('y', 0)
            lon1 = node_data.get('x', 0)
            lat2 = target_data.get('y', 0)
            lon2 = target_data.get('x', 0)
            
            distance_km = haversine_distance(lat1, lon1, lat2, lon2)
            return distance_km * 1000
            
        except Exception:
            return 0.0
    
    def search(self) -> Generator[AlgorithmStepState, None, None]:
        """Execute Bidirectional A* with step-by-step execution.
        
        Yields:
            AlgorithmStepState objects at each exploration step
        """
        logger.info(f"Starting Bidirectional A*: {self.start_node} <-> {self.end_node}")
        
        # Forward search data structures
        g_forward: Dict[int, float] = {node: float('inf') for node in self.graph.nodes()}
        g_forward[self.start_node] = 0.0
        parent_forward: Dict[int, Optional[int]] = {}
        
        # Backward search data structures
        g_backward: Dict[int, float] = {node: float('inf') for node in self.graph.nodes()}
        g_backward[self.end_node] = 0.0
        parent_backward: Dict[int, Optional[int]] = {}
        
        visited_forward: Set[int] = set()
        visited_backward: Set[int] = set()
        
        # Priority queues
        pq_forward = [(self._default_heuristic(self.start_node, self.end_node), self.start_node)]
        pq_backward = [(self._default_heuristic(self.end_node, self.start_node), self.end_node)]
        
        best_path = None
        best_cost = float('inf')
        
        while pq_forward or pq_backward:
            # Forward step
            if pq_forward and (not pq_backward or pq_forward[0][0] <= pq_backward[0][0]):
                _, current = heapq.heappop(pq_forward)
                
                if current in visited_forward:
                    continue
                
                visited_forward.add(current)
                
                # Check for meeting point
                if current in visited_backward:
                    path = self._combine_paths(parent_forward, parent_backward, current)
                    cost = g_forward[current] + g_backward[current]
                    if cost < best_cost:
                        best_path = path
                        best_cost = cost
                
                # Explore neighbors
                for neighbor in self.graph.neighbors(current):
                    if neighbor not in visited_forward:
                        edge_weight = self._get_edge_weight(current, neighbor)
                        tentative_g = g_forward[current] + edge_weight
                        
                        if tentative_g < g_forward[neighbor]:
                            parent_forward[neighbor] = current
                            g_forward[neighbor] = tentative_g
                            f = tentative_g + self._default_heuristic(neighbor, self.end_node)
                            heapq.heappush(pq_forward, (f, neighbor))
            
            # Backward step
            if pq_backward and (not pq_forward or pq_backward[0][0] < pq_forward[0][0]):
                _, current = heapq.heappop(pq_backward)
                
                if current in visited_backward:
                    continue
                
                visited_backward.add(current)
                
                # Check for meeting point
                if current in visited_forward:
                    path = self._combine_paths(parent_forward, parent_backward, current)
                    cost = g_forward[current] + g_backward[current]
                    if cost < best_cost:
                        best_path = path
                        best_cost = cost
                
                # Explore neighbors
                for neighbor in self.graph.neighbors(current):
                    if neighbor not in visited_backward:
                        edge_weight = self._get_edge_weight(current, neighbor)
                        tentative_g = g_backward[current] + edge_weight
                        
                        if tentative_g < g_backward[neighbor]:
                            parent_backward[neighbor] = current
                            g_backward[neighbor] = tentative_g
                            f = tentative_g + self._default_heuristic(neighbor, self.start_node)
                            heapq.heappush(pq_backward, (f, neighbor))
            
            # Yield current state (combined view)
            combined_visited = visited_forward | visited_backward
            yield self._create_state(
                current=None,
                visited=combined_visited.copy(),
                frontier=(set(dict(pq_forward)) | set(dict(pq_backward))),
                parent_map=parent_forward.copy(),
                distance_map=g_forward.copy(),
                queue_size=len(pq_forward) + len(pq_backward)
            )
        
        if best_path:
            yield self._create_state(
                current=None,
                visited=(visited_forward | visited_backward),
                frontier=set(),
                parent_map=parent_forward.copy(),
                distance_map=g_forward.copy(),
                queue_size=0,
                is_final=True,
                path=best_path
            )
            logger.info(f"Path found: {len(best_path)} nodes, distance: {best_cost:.2f}m")
        else:
            logger.warning(f"No path found")
            yield self._create_state(
                current=None,
                visited=(visited_forward | visited_backward),
                frontier=set(),
                parent_map={},
                distance_map={},
                is_final=True,
                path=None
            )
    
    def _combine_paths(self, parent_forward: Dict[int, Optional[int]],
                      parent_backward: Dict[int, Optional[int]], meeting_point: int) -> List[int]:
        """Combine forward and backward paths at meeting point.
        
        Args:
            parent_forward: Forward parent map
            parent_backward: Backward parent map
            meeting_point: Node where paths meet
            
        Returns:
            Complete path from start to end
        """
        # Reconstruct forward path
        forward_path = []
        current = meeting_point
        while current is not None:
            forward_path.append(current)
            current = parent_forward.get(current)
        forward_path.reverse()
        
        # Reconstruct backward path
        backward_path = []
        current = parent_backward.get(meeting_point)
        while current is not None:
            backward_path.append(current)
            current = parent_backward.get(current)
        
        return forward_path + backward_path
    
    @staticmethod
    def get_time_complexity() -> str:
        """Bidirectional A* time complexity."""
        return "O((V + E) log V)"
    
    @staticmethod
    def get_space_complexity() -> str:
        """Bidirectional A* space complexity."""
        return "O(V)"
    
    @staticmethod
    def is_optimal() -> bool:
        """Bidirectional A* guarantees optimal solution."""
        return True
    
    @staticmethod
    def uses_heuristic() -> bool:
        """Bidirectional A* uses heuristic function."""
        return True
