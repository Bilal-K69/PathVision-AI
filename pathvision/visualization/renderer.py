"""Visualization renderer for PathVision AI.

Provides rendering of algorithm execution using Matplotlib.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtWidgets import QWidget, QVBoxLayout

import networkx as nx
import numpy as np
from typing import Optional, Set, List, Tuple

from pathvision.models import AlgorithmStepState
from pathvision.config import VIS_CONFIG, COLOR_CONFIG
from pathvision.logging_config import logger


class NetworkVisualizer:
    """Visualizes algorithm execution on road networks.
    
    Attributes:
        graph: NetworkX graph to visualize
        pos: Node positions (latitude, longitude)
        figure: Matplotlib figure
        ax: Matplotlib axes
    """
    
    def __init__(self, graph: nx.MultiDiGraph, figsize: Tuple[int, int] = (12, 9)):
        """Initialize visualizer.
        
        Args:
            graph: NetworkX MultiDiGraph to visualize
            figsize: Figure size in inches
        """
        self.graph = graph
        self.figsize = figsize
        self.pos = None
        self.figure = None
        self.ax = None
        self._init_positions()
        logger.info(f"NetworkVisualizer initialized with {graph.number_of_nodes()} nodes")
    
    def _init_positions(self) -> None:
        """Initialize node positions from graph coordinates."""
        self.pos = {}
        for node in self.graph.nodes():
            try:
                node_data = self.graph.nodes[node]
                x = node_data.get('x', 0)
                y = node_data.get('y', 0)
                self.pos[node] = (x, y)
            except Exception as e:
                logger.warning(f"Could not get coordinates for node {node}: {e}")
                self.pos[node] = (0, 0)
    
    def create_figure(self) -> Figure:
        """Create matplotlib figure.
        
        Returns:
            Matplotlib Figure object
        """
        self.figure = plt.Figure(figsize=self.figsize, dpi=VIS_CONFIG.DPI)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_aspect('equal')
        self.ax.set_facecolor('#1e1e1e')
        self.figure.patch.set_facecolor('#1e1e1e')
        logger.info("Created matplotlib figure")
        return self.figure
    
    def render_step(self, state: AlgorithmStepState, start_node: int, end_node: int) -> None:
        """Render a single algorithm step.
        
        Args:
            state: AlgorithmStepState to render
            start_node: Start node ID
            end_node: End node ID
        """
        if self.figure is None or self.ax is None:
            self.create_figure()
        
        self.ax.clear()
        self.ax.set_facecolor('#1e1e1e')
        
        try:
            # Draw edges
            self._draw_edges(state)
            
            # Draw nodes
            self._draw_nodes(state, start_node, end_node)
            
            # Draw path if found
            if state.path:
                self._draw_path(state.path)
            
            # Set limits
            if self.pos:
                xs = [p[0] for p in self.pos.values()]
                ys = [p[1] for p in self.pos.values()]
                if xs and ys:
                    margin = 0.001
                    self.ax.set_xlim(min(xs) - margin, max(xs) + margin)
                    self.ax.set_ylim(min(ys) - margin, max(ys) + margin)
            
            self.ax.axis('off')
            self.figure.canvas.draw()
            
        except Exception as e:
            logger.error(f"Error rendering step: {e}")
    
    def _draw_edges(self, state: AlgorithmStepState) -> None:
        """Draw edges with different colors based on state.
        
        Args:
            state: Current algorithm state
        """
        # Draw unvisited edges
        unvisited_edges = []
        for u, v in self.graph.edges():
            if u not in state.visited_nodes or v not in state.visited_nodes:
                unvisited_edges.append((u, v))
        
        if unvisited_edges:
            nx.draw_networkx_edges(
                self.graph, self.pos,
                edgelist=unvisited_edges,
                ax=self.ax,
                edge_color=COLOR_CONFIG.ROAD_UNVISITED.value,
                width=VIS_CONFIG.EDGE_WIDTH_UNVISITED,
                alpha=VIS_CONFIG.EDGE_ALPHA_UNVISITED,
                arrows=False
            )
        
        # Draw visited edges
        visited_edges = []
        for u, v in self.graph.edges():
            if u in state.visited_nodes and v in state.visited_nodes:
                visited_edges.append((u, v))
        
        if visited_edges:
            nx.draw_networkx_edges(
                self.graph, self.pos,
                edgelist=visited_edges,
                ax=self.ax,
                edge_color=COLOR_CONFIG.ROAD_VISITED.value,
                width=VIS_CONFIG.EDGE_WIDTH_VISITED,
                alpha=VIS_CONFIG.EDGE_ALPHA_VISITED,
                arrows=False
            )
    
    def _draw_nodes(self, state: AlgorithmStepState, start_node: int, end_node: int) -> None:
        """Draw nodes with different colors based on state.
        
        Args:
            state: Current algorithm state
            start_node: Start node ID
            end_node: End node ID
        """
        # Draw unvisited nodes
        unvisited = set(self.graph.nodes()) - state.visited_nodes - state.frontier_nodes
        if unvisited:
            nx.draw_networkx_nodes(
                self.graph, self.pos,
                nodelist=list(unvisited),
                ax=self.ax,
                node_color='gray',
                node_size=VIS_CONFIG.NODE_SIZE_UNVISITED,
                alpha=0.3
            )
        
        # Draw frontier nodes
        if state.frontier_nodes:
            nx.draw_networkx_nodes(
                self.graph, self.pos,
                nodelist=list(state.frontier_nodes),
                ax=self.ax,
                node_color=COLOR_CONFIG.ROAD_FRONTIER.value,
                node_size=VIS_CONFIG.NODE_SIZE_VISITED,
                alpha=0.7
            )
        
        # Draw visited nodes
        visited_only = state.visited_nodes - {state.current_node, start_node, end_node}
        if visited_only:
            nx.draw_networkx_nodes(
                self.graph, self.pos,
                nodelist=list(visited_only),
                ax=self.ax,
                node_color=COLOR_CONFIG.ROAD_VISITED.value,
                node_size=VIS_CONFIG.NODE_SIZE_VISITED,
                alpha=0.8
            )
        
        # Draw current node
        if state.current_node:
            nx.draw_networkx_nodes(
                self.graph, self.pos,
                nodelist=[state.current_node],
                ax=self.ax,
                node_color=COLOR_CONFIG.CURRENT_NODE.value,
                node_size=VIS_CONFIG.NODE_SIZE_CURRENT
            )
        
        # Draw start node
        nx.draw_networkx_nodes(
            self.graph, self.pos,
            nodelist=[start_node],
            ax=self.ax,
            node_color=COLOR_CONFIG.START_NODE.value,
            node_size=VIS_CONFIG.NODE_SIZE_START
        )
        
        # Draw end node
        nx.draw_networkx_nodes(
            self.graph, self.pos,
            nodelist=[end_node],
            ax=self.ax,
            node_color=COLOR_CONFIG.END_NODE.value,
            node_size=VIS_CONFIG.NODE_SIZE_END
        )
    
    def _draw_path(self, path: List[int]) -> None:
        """Draw the final path.
        
        Args:
            path: List of node IDs representing the path
        """
        if len(path) < 2:
            return
        
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        
        nx.draw_networkx_edges(
            self.graph, self.pos,
            edgelist=path_edges,
            ax=self.ax,
            edge_color=COLOR_CONFIG.ROAD_PATH.value,
            width=VIS_CONFIG.EDGE_WIDTH_PATH,
            alpha=VIS_CONFIG.EDGE_ALPHA_PATH,
            arrows=False
        )
    
    def get_canvas_widget(self) -> QWidget:
        """Get FigureCanvas as Qt widget.
        
        Returns:
            QWidget containing the matplotlib canvas
        """
        if self.figure is None:
            self.create_figure()
        
        canvas = FigureCanvas(self.figure)
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        return widget
