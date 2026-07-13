"""Algorithm execution engine for PathVision AI.

Manages algorithm execution with threading, statistics collection, and state management.
"""

import threading
import time
from typing import Generator, Optional, List, Callable
from enum import Enum
import tracemalloc

from pathvision.algorithms.base import PathfindingAlgorithm
from pathvision.models import AlgorithmStepState, ExecutionStatistics
from pathvision.logging_config import logger


class ExecutionState(Enum):
    """Execution state enumeration."""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class AlgorithmExecutor:
    """Manages algorithm execution with threading and statistics.
    
    Attributes:
        algorithm: PathfindingAlgorithm instance
        state: Current execution state
        statistics: Collected statistics
        steps: List of execution steps
    """
    
    def __init__(self, algorithm: PathfindingAlgorithm, city_name: str = "Unknown"):
        """Initialize executor.
        
        Args:
            algorithm: PathfindingAlgorithm instance to execute
            city_name: Name of the city for statistics
        """
        self.algorithm = algorithm
        self.city_name = city_name
        self.state = ExecutionState.IDLE
        self.statistics: Optional[ExecutionStatistics] = None
        self.steps: List[AlgorithmStepState] = []
        self.current_step = 0
        self.is_paused = False
        self.stop_requested = False
        self._lock = threading.Lock()
        self._execution_thread: Optional[threading.Thread] = None
        
        logger.info(f"AlgorithmExecutor initialized for {algorithm.name}")
    
    def execute(self, on_step: Optional[Callable[[AlgorithmStepState], None]] = None) -> ExecutionStatistics:
        """Execute algorithm and collect statistics.
        
        Args:
            on_step: Optional callback for each step
            
        Returns:
            ExecutionStatistics object
        """
        logger.info(f"Starting execution: {self.algorithm.name}")
        self.state = ExecutionState.RUNNING
        self.steps = []
        self.stop_requested = False
        
        # Start memory tracking
        tracemalloc.start()
        start_time = time.time()
        start_memory = tracemalloc.get_traced_memory()[0]
        
        try:
            # Execute algorithm generator
            for step in self.algorithm.search():
                if self.stop_requested:
                    break
                
                # Wait if paused
                while self.is_paused and not self.stop_requested:
                    time.sleep(0.1)
                
                self.steps.append(step)
                self.current_step = len(self.steps) - 1
                
                # Call callback
                if on_step:
                    on_step(step)
            
            # Collect final statistics
            end_time = time.time()
            end_memory = tracemalloc.get_traced_memory()[0]
            
            if self.steps:
                final_step = self.steps[-1]
                path_length = len(final_step.path) if final_step.path else 0
                path_distance = final_step.path_distance or 0.0
            else:
                path_length = 0
                path_distance = 0.0
            
            self.statistics = ExecutionStatistics(
                algorithm_name=self.algorithm.name,
                city_name=self.city_name,
                start_node=self.algorithm.start_node,
                end_node=self.algorithm.end_node,
                execution_time_ms=(end_time - start_time) * 1000,
                nodes_visited=len(self.steps[-1].visited_nodes) if self.steps else 0,
                nodes_explored=len([s for s in self.steps if s.current_node is not None]),
                path_length=path_length,
                path_distance=path_distance,
                memory_used_mb=(end_memory - start_memory) / (1024 * 1024),
                queue_max_size=max([s.queue_size for s in self.steps] or [0]),
                steps_count=len(self.steps),
                graph_nodes_total=self.algorithm.graph.number_of_nodes(),
                graph_edges_total=self.algorithm.graph.number_of_edges(),
                time_complexity=self.algorithm.get_time_complexity(),
                space_complexity=self.algorithm.get_space_complexity()
            )
            
            self.state = ExecutionState.COMPLETED
            logger.info(f"Execution completed: {self.statistics.execution_time_ms:.2f}ms")
            
        except Exception as e:
            logger.error(f"Execution failed: {e}")
            self.state = ExecutionState.FAILED
            raise
        
        finally:
            tracemalloc.stop()
        
        return self.statistics
    
    def execute_async(self, on_step: Optional[Callable[[AlgorithmStepState], None]] = None,
                     on_complete: Optional[Callable[[ExecutionStatistics], None]] = None) -> None:
        """Execute algorithm asynchronously in a separate thread.
        
        Args:
            on_step: Optional callback for each step
            on_complete: Optional callback when execution completes
        """
        def run():
            try:
                stats = self.execute(on_step)
                if on_complete:
                    on_complete(stats)
            except Exception as e:
                logger.error(f"Async execution failed: {e}")
                self.state = ExecutionState.FAILED
        
        self._execution_thread = threading.Thread(target=run, daemon=False)
        self._execution_thread.start()
    
    def pause(self) -> None:
        """Pause execution."""
        with self._lock:
            if self.state == ExecutionState.RUNNING:
                self.is_paused = True
                self.state = ExecutionState.PAUSED
                logger.info("Execution paused")
    
    def resume(self) -> None:
        """Resume execution."""
        with self._lock:
            if self.state == ExecutionState.PAUSED:
                self.is_paused = False
                self.state = ExecutionState.RUNNING
                logger.info("Execution resumed")
    
    def stop(self) -> None:
        """Stop execution."""
        with self._lock:
            self.stop_requested = True
            self.is_paused = False
            logger.info("Stop requested")
    
    def get_current_step(self) -> Optional[AlgorithmStepState]:
        """Get current step state.
        
        Returns:
            Current AlgorithmStepState or None
        """
        if 0 <= self.current_step < len(self.steps):
            return self.steps[self.current_step]
        return None
    
    def get_step(self, index: int) -> Optional[AlgorithmStepState]:
        """Get step by index.
        
        Args:
            index: Step index
            
        Returns:
            AlgorithmStepState at index or None
        """
        if 0 <= index < len(self.steps):
            return self.steps[index]
        return None
    
    def set_step(self, index: int) -> bool:
        """Set current step to index.
        
        Args:
            index: Target step index
            
        Returns:
            True if successful, False otherwise
        """
        if 0 <= index < len(self.steps):
            self.current_step = index
            return True
        return False
    
    def get_progress(self) -> float:
        """Get execution progress as percentage.
        
        Returns:
            Progress from 0.0 to 1.0
        """
        if not self.steps:
            return 0.0
        return min(1.0, (self.current_step + 1) / len(self.steps))
    
    def is_complete(self) -> bool:
        """Check if execution is complete.
        
        Returns:
            True if execution is complete
        """
        return self.state == ExecutionState.COMPLETED
    
    def wait_for_completion(self, timeout: Optional[float] = None) -> bool:
        """Wait for async execution to complete.
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if completed, False if timeout
        """
        if self._execution_thread:
            self._execution_thread.join(timeout)
            return not self._execution_thread.is_alive()
        return True
