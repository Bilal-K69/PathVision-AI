"""Algorithm comparison module for PathVision AI.

Provides utilities for comparing multiple algorithms on the same graph.
"""

from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

import networkx as nx

from pathvision.algorithms.base import PathfindingAlgorithm
from pathvision.algorithms.dijkstra import Dijkstra
from pathvision.algorithms.astar import AStar
from pathvision.algorithms.bfs import BFS
from pathvision.algorithms.dfs import DFS
from pathvision.algorithms.greedy import GreedyBestFirst
from pathvision.algorithms.bidirectional_astar import BidirectionalAStar
from pathvision.config import Algorithm
from pathvision.execution.executor import AlgorithmExecutor
from pathvision.models import ExecutionStatistics
from pathvision.logging_config import logger


class AlgorithmComparator:
    """Compares performance of multiple algorithms.
    
    Attributes:
        graph: NetworkX graph
        start_node: Starting node
        end_node: Destination node
        results: Comparison results
    """
    
    def __init__(self, graph: nx.MultiDiGraph, start_node: int, end_node: int, city_name: str = "Unknown"):
        """Initialize comparator.
        
        Args:
            graph: NetworkX MultiDiGraph
            start_node: Starting node ID
            end_node: Destination node ID
            city_name: Name of the city for statistics
        """
        self.graph = graph
        self.start_node = start_node
        self.end_node = end_node
        self.city_name = city_name
        self.results: Dict[str, ExecutionStatistics] = {}
        logger.info(f"AlgorithmComparator initialized")
    
    def compare_all(self) -> Dict[str, ExecutionStatistics]:
        """Compare all available algorithms.
        
        Returns:
            Dictionary mapping algorithm names to ExecutionStatistics
        """
        algorithms_to_test = [
            Algorithm.DIJKSTRA,
            Algorithm.ASTAR,
            Algorithm.BFS,
            Algorithm.DFS,
            Algorithm.GREEDY,
            Algorithm.BIDIRECTIONAL_ASTAR
        ]
        
        return self.compare(algorithms_to_test)
    
    def compare(self, algorithms: List[Algorithm]) -> Dict[str, ExecutionStatistics]:
        """Compare specified algorithms.
        
        Args:
            algorithms: List of Algorithm enums to compare
            
        Returns:
            Dictionary mapping algorithm names to ExecutionStatistics
        """
        logger.info(f"Comparing {len(algorithms)} algorithms")
        self.results = {}
        
        # Use thread pool for parallel execution
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {}
            
            for algo in algorithms:
                future = executor.submit(self._execute_algorithm, algo)
                futures[future] = algo
            
            for future in as_completed(futures):
                algo = futures[future]
                try:
                    stats = future.result()
                    self.results[algo.value] = stats
                    logger.info(f"Completed: {algo.value}")
                except Exception as e:
                    logger.error(f"Failed to execute {algo.value}: {e}")
        
        return self.results
    
    def _execute_algorithm(self, algorithm: Algorithm) -> ExecutionStatistics:
        """Execute a single algorithm.
        
        Args:
            algorithm: Algorithm to execute
            
        Returns:
            ExecutionStatistics
        """
        # Create algorithm instance
        algo_instance = self._create_algorithm(algorithm)
        
        # Execute
        executor = AlgorithmExecutor(algo_instance, self.city_name)
        stats = executor.execute()
        
        return stats
    
    def _create_algorithm(self, algorithm: Algorithm) -> PathfindingAlgorithm:
        """Create algorithm instance.
        
        Args:
            algorithm: Algorithm type
            
        Returns:
            Algorithm instance
        """
        if algorithm == Algorithm.DIJKSTRA:
            return Dijkstra(self.graph, self.start_node, self.end_node)
        elif algorithm == Algorithm.ASTAR:
            return AStar(self.graph, self.start_node, self.end_node)
        elif algorithm == Algorithm.BFS:
            return BFS(self.graph, self.start_node, self.end_node)
        elif algorithm == Algorithm.DFS:
            return DFS(self.graph, self.start_node, self.end_node)
        elif algorithm == Algorithm.GREEDY:
            return GreedyBestFirst(self.graph, self.start_node, self.end_node)
        elif algorithm == Algorithm.BIDIRECTIONAL_ASTAR:
            return BidirectionalAStar(self.graph, self.start_node, self.end_node)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
    
    def get_comparison_summary(self) -> Dict[str, Any]:
        """Get comparison summary.
        
        Returns:
            Dictionary with comparison analysis
        """
        if not self.results:
            return {}
        
        summary = {
            'total_comparisons': len(self.results),
            'fastest': min(self.results.items(), key=lambda x: x[1].execution_time_ms),
            'least_explored': min(self.results.items(), key=lambda x: x[1].nodes_explored),
            'lowest_memory': min(self.results.items(), key=lambda x: x[1].memory_used_mb),
            'results': {}
        }
        
        for algo_name, stats in self.results.items():
            summary['results'][algo_name] = {
                'execution_time_ms': stats.execution_time_ms,
                'nodes_visited': stats.nodes_visited,
                'nodes_explored': stats.nodes_explored,
                'path_length': stats.path_length,
                'path_distance': stats.path_distance,
                'memory_used_mb': stats.memory_used_mb,
                'efficiency_ratio': stats.efficiency_ratio
            }
        
        return summary
    
    def get_winner(self, criterion: str = 'execution_time_ms') -> Optional[str]:
        """Get winning algorithm by criterion.
        
        Args:
            criterion: Comparison criterion (execution_time_ms, nodes_explored, memory_used_mb)
            
        Returns:
            Name of winning algorithm or None
        """
        if not self.results:
            return None
        
        if criterion == 'execution_time_ms':
            return min(self.results.items(), key=lambda x: x[1].execution_time_ms)[0]
        elif criterion == 'nodes_explored':
            return min(self.results.items(), key=lambda x: x[1].nodes_explored)[0]
        elif criterion == 'memory_used_mb':
            return min(self.results.items(), key=lambda x: x[1].memory_used_mb)[0]
        else:
            return None
