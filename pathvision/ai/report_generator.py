"""Report generation module for PathVision AI.

Provides utilities for generating reports in multiple formats.
"""

import json
import csv
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from pathvision.models import ExecutionStatistics
from pathvision.config import APP_CONFIG
from pathvision.logging_config import logger


class ReportGenerator:
    """Generates reports from execution statistics.
    
    Supports JSON, CSV, and plain text formats.
    """
    
    def __init__(self, output_dir: Optional[Path] = None):
        """Initialize report generator.
        
        Args:
            output_dir: Output directory for reports (default: APP_CONFIG.REPORT_DIR)
        """
        self.output_dir = output_dir or APP_CONFIG.REPORT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"ReportGenerator initialized: {self.output_dir}")
    
    def generate_json(self, statistics: List[ExecutionStatistics], 
                     filename: Optional[str] = None) -> Path:
        """Generate JSON report.
        
        Args:
            statistics: List of ExecutionStatistics objects
            filename: Optional output filename
            
        Returns:
            Path to generated report
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.json"
        
        report_data = {
            'generated_at': datetime.now().isoformat(),
            'executions': [stats.to_dict() for stats in statistics]
        }
        
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"Generated JSON report: {filepath}")
        return filepath
    
    def generate_csv(self, statistics: List[ExecutionStatistics],
                    filename: Optional[str] = None) -> Path:
        """Generate CSV report.
        
        Args:
            statistics: List of ExecutionStatistics objects
            filename: Optional output filename
            
        Returns:
            Path to generated report
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.csv"
        
        if not statistics:
            logger.warning("No statistics to generate CSV report")
            return Path()
        
        # Get all keys from first stats object
        keys = list(statistics[0].to_dict().keys())
        
        filepath = self.output_dir / filename
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for stats in statistics:
                writer.writerow(stats.to_dict())
        
        logger.info(f"Generated CSV report: {filepath}")
        return filepath
    
    def generate_text(self, statistics: List[ExecutionStatistics],
                     filename: Optional[str] = None) -> Path:
        """Generate plain text report.
        
        Args:
            statistics: List of ExecutionStatistics objects
            filename: Optional output filename
            
        Returns:
            Path to generated report
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.txt"
        
        lines = []
        lines.append("=" * 80)
        lines.append("PathVision AI - Algorithm Execution Report")
        lines.append("=" * 80)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        for i, stats in enumerate(statistics, 1):
            lines.append(f"Execution {i}: {stats.algorithm_name}")
            lines.append("-" * 40)
            lines.append(f"  City: {stats.city_name}")
            lines.append(f"  Path: {stats.start_node} → {stats.end_node}")
            lines.append(f"  Execution Time: {stats.execution_time_ms:.2f} ms")
            lines.append(f"  Nodes Visited: {stats.nodes_visited}")
            lines.append(f"  Nodes Explored: {stats.nodes_explored}")
            lines.append(f"  Path Length: {stats.path_length} nodes")
            lines.append(f"  Path Distance: {stats.path_distance:.2f} m")
            lines.append(f"  Memory Used: {stats.memory_used_mb:.2f} MB")
            lines.append(f"  Queue Max Size: {stats.queue_max_size}")
            lines.append(f"  Efficiency Ratio: {stats.efficiency_ratio:.3f}")
            lines.append(f"  Exploration: {stats.exploration_percentage:.1f}%")
            lines.append(f"  Complexity: O({stats.time_complexity}) time, O({stats.space_complexity}) space")
            lines.append("")
        
        lines.append("=" * 80)
        
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            f.write('\n'.join(lines))
        
        logger.info(f"Generated text report: {filepath}")
        return filepath
    
    def generate_comparison_report(self, statistics_dict: Dict[str, List[ExecutionStatistics]],
                                  filename: Optional[str] = None) -> Path:
        """Generate comparison report for multiple algorithm runs.
        
        Args:
            statistics_dict: Dictionary mapping algorithm names to statistics lists
            filename: Optional output filename
            
        Returns:
            Path to generated report
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"comparison_{timestamp}.json"
        
        report_data = {
            'generated_at': datetime.now().isoformat(),
            'algorithms': {}
        }
        
        for algo_name, stats_list in statistics_dict.items():
            report_data['algorithms'][algo_name] = [
                stats.to_dict() for stats in stats_list
            ]
        
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"Generated comparison report: {filepath}")
        return filepath
    
    def generate_all_formats(self, statistics: List[ExecutionStatistics],
                           base_filename: Optional[str] = None) -> Dict[str, Path]:
        """Generate reports in all supported formats.
        
        Args:
            statistics: List of ExecutionStatistics objects
            base_filename: Base filename (without extension)
            
        Returns:
            Dictionary mapping format names to file paths
        """
        if base_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"report_{timestamp}"
        
        results = {
            'json': self.generate_json(statistics, f"{base_filename}.json"),
            'csv': self.generate_csv(statistics, f"{base_filename}.csv"),
            'text': self.generate_text(statistics, f"{base_filename}.txt")
        }
        
        logger.info(f"Generated all report formats: {base_filename}")
        return results
