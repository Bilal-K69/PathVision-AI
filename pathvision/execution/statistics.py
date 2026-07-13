"""Statistics collection module for PathVision AI.

Provides utilities for collecting and analyzing execution statistics.
"""

from typing import List, Dict, Any, Optional
import statistics

from pathvision.models import ExecutionStatistics
from pathvision.logging_config import logger


class StatisticsCollector:
    """Collects and analyzes statistics from multiple algorithm executions.
    
    Attributes:
        statistics_list: List of ExecutionStatistics objects
    """
    
    def __init__(self):
        """Initialize statistics collector."""
        self.statistics_list: List[ExecutionStatistics] = []
        logger.info("StatisticsCollector initialized")
    
    def add_statistics(self, stats: ExecutionStatistics) -> None:
        """Add execution statistics.
        
        Args:
            stats: ExecutionStatistics object to add
        """
        self.statistics_list.append(stats)
        logger.info(f"Added statistics for {stats.algorithm_name}")
    
    def get_comparison(self) -> Dict[str, Any]:
        """Get comparison of all collected statistics.
        
        Returns:
            Dictionary with comparative analysis
        """
        if not self.statistics_list:
            return {}
        
        # Group by algorithm
        by_algorithm = {}
        for stats in self.statistics_list:
            if stats.algorithm_name not in by_algorithm:
                by_algorithm[stats.algorithm_name] = []
            by_algorithm[stats.algorithm_name].append(stats)
        
        # Analyze each algorithm
        comparison = {}
        for algo_name, stats_list in by_algorithm.items():
            comparison[algo_name] = {
                'count': len(stats_list),
                'avg_time_ms': statistics.mean([s.execution_time_ms for s in stats_list]),
                'avg_nodes_visited': statistics.mean([s.nodes_visited for s in stats_list]),
                'avg_path_length': statistics.mean([s.path_length for s in stats_list]),
                'avg_memory_mb': statistics.mean([s.memory_used_mb for s in stats_list]),
            }
        
        return comparison
    
    def get_best_by_execution_time(self) -> Optional[ExecutionStatistics]:
        """Get statistics with fastest execution.
        
        Returns:
            ExecutionStatistics with minimum execution time
        """
        if not self.statistics_list:
            return None
        return min(self.statistics_list, key=lambda s: s.execution_time_ms)
    
    def get_best_by_nodes_explored(self) -> Optional[ExecutionStatistics]:
        """Get statistics with fewest nodes explored.
        
        Returns:
            ExecutionStatistics with minimum nodes explored
        """
        if not self.statistics_list:
            return None
        return min(self.statistics_list, key=lambda s: s.nodes_explored)
    
    def get_best_by_memory(self) -> Optional[ExecutionStatistics]:
        """Get statistics with lowest memory usage.
        
        Returns:
            ExecutionStatistics with minimum memory usage
        """
        if not self.statistics_list:
            return None
        return min(self.statistics_list, key=lambda s: s.memory_used_mb)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get overall summary of all statistics.
        
        Returns:
            Dictionary with summary statistics
        """
        if not self.statistics_list:
            return {}
        
        times = [s.execution_time_ms for s in self.statistics_list]
        nodes = [s.nodes_visited for s in self.statistics_list]
        memory = [s.memory_used_mb for s in self.statistics_list]
        
        return {
            'total_executions': len(self.statistics_list),
            'avg_execution_time_ms': statistics.mean(times),
            'min_execution_time_ms': min(times),
            'max_execution_time_ms': max(times),
            'avg_nodes_visited': statistics.mean(nodes),
            'total_nodes_explored': sum(nodes),
            'avg_memory_mb': statistics.mean(memory),
            'total_memory_mb': sum(memory),
        }
    
    def clear(self) -> None:
        """Clear all collected statistics."""
        self.statistics_list.clear()
        logger.info("Statistics collector cleared")
