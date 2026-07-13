"""Algorithm recommendation engine for PathVision AI.

Provides intelligent algorithm selection based on graph properties.
"""

from typing import List, Tuple, Dict, Any
import networkx as nx

from pathvision.config import Algorithm
from pathvision.models import GraphMetrics
from pathvision.ai.analyzer import GraphAnalyzer
from pathvision.logging_config import logger


class AlgorithmRecommender:
    """Recommends optimal algorithms based on graph properties.
    
    Uses heuristics to suggest the best algorithm for a given graph.
    """
    
    # Algorithm characteristics
    ALGORITHM_PROFILES = {
        Algorithm.DIJKSTRA: {
            'optimal': True,
            'heuristic': False,
            'weighted': True,
            'best_for': 'General purpose shortest path with weights',
            'time_complexity': 'O((V + E) log V)'
        },
        Algorithm.ASTAR: {
            'optimal': True,
            'heuristic': True,
            'weighted': True,
            'best_for': 'Geographic shortest path with heuristic guidance',
            'time_complexity': 'O((V + E) log V)'
        },
        Algorithm.BFS: {
            'optimal': True,
            'heuristic': False,
            'weighted': False,
            'best_for': 'Unweighted or uniform-weight shortest path',
            'time_complexity': 'O(V + E)'
        },
        Algorithm.DFS: {
            'optimal': False,
            'heuristic': False,
            'weighted': False,
            'best_for': 'Graph exploration and connectivity',
            'time_complexity': 'O(V + E)'
        },
        Algorithm.GREEDY: {
            'optimal': False,
            'heuristic': True,
            'weighted': True,
            'best_for': 'Fast approximation with heuristic guidance',
            'time_complexity': 'O((V + E) log V)'
        },
        Algorithm.BIDIRECTIONAL_ASTAR: {
            'optimal': True,
            'heuristic': True,
            'weighted': True,
            'best_for': 'Geographic shortest path (faster A*)',
            'time_complexity': 'O((V + E) log V)'
        }
    }
    
    def __init__(self, graph: nx.MultiDiGraph):
        """Initialize recommender.
        
        Args:
            graph: NetworkX MultiDiGraph to analyze
        """
        self.graph = graph
        self.analyzer = GraphAnalyzer(graph)
        self.metrics: Dict[str, Any] = {}
        logger.info("AlgorithmRecommender initialized")
    
    def recommend(self) -> Tuple[Algorithm, str]:
        """Recommend best algorithm for the graph.
        
        Returns:
            Tuple of (recommended_algorithm, explanation)
        """
        logger.info("Generating algorithm recommendation")
        
        # Analyze graph
        metrics = self.analyzer.analyze()
        self.metrics = metrics.to_dict()
        
        # Apply heuristics
        recommendation = self._apply_heuristics(metrics)
        algorithm, score, explanation = recommendation
        
        logger.info(f"Recommended: {algorithm.value} (score: {score:.2f})")
        return algorithm, explanation
    
    def recommend_multiple(self, count: int = 3) -> List[Tuple[Algorithm, str, float]]:
        """Recommend multiple algorithms ranked by suitability.
        
        Args:
            count: Number of recommendations to return
            
        Returns:
            List of (algorithm, explanation, score) tuples
        """
        logger.info(f"Generating {count} algorithm recommendations")
        
        metrics = self.analyzer.analyze()
        self.metrics = metrics.to_dict()
        
        # Score all algorithms
        scores = []
        for algo in Algorithm:
            score = self._calculate_score(algo, metrics)
            explanation = self._generate_explanation(algo, metrics, score)
            scores.append((algo, explanation, score))
        
        # Sort by score descending
        scores.sort(key=lambda x: x[2], reverse=True)
        
        return scores[:count]
    
    def _apply_heuristics(self, metrics: GraphMetrics) -> Tuple[Algorithm, float, str]:
        """Apply heuristics to determine best algorithm.
        
        Args:
            metrics: Graph metrics
            
        Returns:
            Tuple of (algorithm, score, explanation)
        """
        best_algo = None
        best_score = -1
        best_explanation = ""
        
        for algo in Algorithm:
            score = self._calculate_score(algo, metrics)
            explanation = self._generate_explanation(algo, metrics, score)
            
            if score > best_score:
                best_score = score
                best_algo = algo
                best_explanation = explanation
        
        return best_algo or Algorithm.DIJKSTRA, best_score, best_explanation
    
    def _calculate_score(self, algorithm: Algorithm, metrics: GraphMetrics) -> float:
        """Calculate suitability score for an algorithm.
        
        Args:
            algorithm: Algorithm to score
            metrics: Graph metrics
            
        Returns:
            Score from 0 to 100
        """
        score = 50.0  # Base score
        profile = self.ALGORITHM_PROFILES[algorithm]
        
        # Weighted graph bonus
        if metrics.is_weighted and profile['weighted']:
            score += 10
        elif not metrics.is_weighted and not profile['weighted']:
            score += 5
        
        # Graph size considerations
        if metrics.node_count < 1000:
            # Small graphs: any algorithm works
            score += 5
        elif metrics.node_count < 10000:
            # Medium graphs: prefer heuristic
            if profile['heuristic']:
                score += 15
            else:
                score -= 5
        else:
            # Large graphs: strongly prefer heuristic
            if profile['heuristic']:
                score += 25
            else:
                score -= 15
        
        # Optimality preference for large graphs
        if metrics.node_count > 5000 and profile['optimal']:
            score += 10
        
        # Density considerations
        if metrics.density > 0.5:  # Dense graph
            if profile['heuristic']:
                score += 5
        else:  # Sparse graph
            if profile['weighted']:
                score += 3
        
        # Bidirectional A* gets bonus for large graphs
        if algorithm == Algorithm.BIDIRECTIONAL_ASTAR and metrics.node_count > 10000:
            score += 20
        
        return min(100.0, max(0.0, score))
    
    def _generate_explanation(self, algorithm: Algorithm, 
                            metrics: GraphMetrics, score: float) -> str:
        """Generate explanation for algorithm recommendation.
        
        Args:
            algorithm: Algorithm
            metrics: Graph metrics
            score: Suitability score
            
        Returns:
            Explanation string
        """
        profile = self.ALGORITHM_PROFILES[algorithm]
        
        explanation = f"{algorithm.value.replace('_', ' ').title()}: "
        explanation += profile['best_for'] + ". "
        
        explanation += f"Graph: {metrics.node_count:,} nodes, "
        explanation += f"{metrics.edge_count:,} edges, "
        explanation += f"density: {metrics.density:.2%}"
        
        if score >= 70:
            explanation += " [Excellent choice]"
        elif score >= 50:
            explanation += " [Good choice]"
        elif score >= 30:
            explanation += " [Acceptable]"
        else:
            explanation += " [Not recommended]"
        
        return explanation
    
    def get_recommendation_details(self) -> Dict[str, Any]:
        """Get detailed recommendation information.
        
        Returns:
            Dictionary with detailed recommendation info
        """
        top_3 = self.recommend_multiple(3)
        
        return {
            'graph_metrics': self.metrics,
            'recommended': {
                'algorithm': top_3[0][0].value,
                'explanation': top_3[0][1],
                'score': top_3[0][2]
            },
            'alternatives': [
                {
                    'algorithm': algo.value,
                    'explanation': explanation,
                    'score': score
                }
                for algo, explanation, score in top_3[1:]
            ]
        }
