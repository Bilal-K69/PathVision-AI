"""Graph analysis module for PathVision AI.

Provides utilities for analyzing graph properties and characteristics.
"""

import networkx as nx
from typing import Dict, Any, Optional

from pathvision.models import GraphMetrics
from pathvision.logging_config import logger


class GraphAnalyzer:
    """Analyzes graph properties and generates metrics.
    
    Attributes:
        graph: NetworkX graph to analyze
        metrics: Cached graph metrics
    """
    
    def __init__(self, graph: nx.MultiDiGraph):
        """Initialize analyzer.
        
        Args:
            graph: NetworkX MultiDiGraph to analyze
        """
        self.graph = graph
        self.metrics: Optional[GraphMetrics] = None
        logger.info(f"GraphAnalyzer initialized with {graph.number_of_nodes()} nodes")
    
    def analyze(self) -> GraphMetrics:
        """Perform comprehensive graph analysis.
        
        Returns:
            GraphMetrics object with analysis results
        """
        logger.info("Starting graph analysis")
        
        node_count = self.graph.number_of_nodes()
        edge_count = self.graph.number_of_edges()
        
        # Check if weighted
        is_weighted = self._check_weighted()
        
        # Average degree
        average_degree = self._calculate_average_degree()
        
        # Density
        density = self._calculate_density()
        
        # Connected components
        components = self._get_components()
        largest_component_size = len(max(components, key=len)) if components else 0
        is_connected = len(components) == 1
        
        # Diameter (only for smaller graphs)
        diameter = None
        if is_connected and node_count <= 5000:
            try:
                diameter = nx.diameter(self.graph.to_undirected())
            except Exception:
                logger.warning("Could not calculate diameter")
        
        self.metrics = GraphMetrics(
            node_count=node_count,
            edge_count=edge_count,
            is_weighted=is_weighted,
            is_directed=self.graph.is_directed(),
            average_degree=average_degree,
            density=density,
            largest_component_size=largest_component_size,
            diameter=diameter,
            is_connected=is_connected
        )
        
        logger.info(f"Analysis complete: {self.metrics}")
        return self.metrics
    
    def _check_weighted(self) -> bool:
        """Check if graph has weighted edges.
        
        Returns:
            True if graph has weighted edges
        """
        for u, v, k in self.graph.edges(keys=True):
            if 'length' in self.graph[u][v][k]:
                return True
        return False
    
    def _calculate_average_degree(self) -> float:
        """Calculate average node degree.
        
        Returns:
            Average degree
        """
        if self.graph.number_of_nodes() == 0:
            return 0.0
        
        total_degree = sum(dict(self.graph.degree()).values())
        return total_degree / self.graph.number_of_nodes()
    
    def _calculate_density(self) -> float:
        """Calculate graph density.
        
        Returns:
            Graph density (0 to 1)
        """
        n = self.graph.number_of_nodes()
        m = self.graph.number_of_edges()
        
        if n <= 1:
            return 0.0
        
        max_edges = n * (n - 1) / 2 if not self.graph.is_directed() else n * (n - 1)
        return m / max_edges if max_edges > 0 else 0.0
    
    def _get_components(self) -> list:
        """Get connected components.
        
        Returns:
            List of connected components
        """
        if self.graph.is_directed():
            return list(nx.weakly_connected_components(self.graph))
        else:
            return list(nx.connected_components(self.graph))
    
    def get_sparsity(self) -> float:
        """Get graph sparsity (inverse of density).
        
        Returns:
            Sparsity value (0 to 1)
        """
        if self.metrics is None:
            self.analyze()
        
        return 1.0 - self.metrics.density if self.metrics else 1.0
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get analysis summary as dictionary.
        
        Returns:
            Dictionary with analysis summary
        """
        if self.metrics is None:
            self.analyze()
        
        return self.metrics.to_dict() if self.metrics else {}
