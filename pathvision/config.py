"""Configuration management for PathVision AI.

This module handles all configuration settings including:
- Application constants
- Default parameters
- File paths
- UI settings
- Algorithm parameters
- Map settings
"""

import os
from enum import Enum
from pathlib import Path
from typing import Dict, Any, Final
from dataclasses import dataclass
import json


class City(Enum):
    """Available cities for pathfinding visualization."""
    LAHORE = ("Lahore, Pakistan", (31.5497, 74.3436), 0.05)
    KARACHI = ("Karachi, Pakistan", (24.8607, 67.0011), 0.05)
    ISLAMABAD = ("Islamabad, Pakistan", (33.6844, 73.1898), 0.03)
    TOKYO = ("Tokyo, Japan", (35.6762, 139.6503), 0.05)
    LONDON = ("London, United Kingdom", (51.5074, -0.1278), 0.05)
    NEW_YORK = ("New York, USA", (40.7128, -74.0060), 0.05)
    PARIS = ("Paris, France", (48.8566, 2.3522), 0.05)

    def __init__(self, display_name: str, coordinates: tuple, distance: float):
        self.display_name = display_name
        self.coordinates = coordinates
        self.distance = distance


class Algorithm(Enum):
    """Available pathfinding algorithms."""
    DIJKSTRA = "dijkstra"
    ASTAR = "astar"
    BFS = "bfs"
    DFS = "dfs"
    GREEDY = "greedy"
    BIDIRECTIONAL_ASTAR = "bidirectional_astar"


class ColorScheme(Enum):
    """Color scheme for visualization."""
    ROAD_UNVISITED = "#2d3436"  # Dark gray
    ROAD_VISITED = "#3498db"   # Blue
    ROAD_FRONTIER = "#f39c12"  # Orange
    ROAD_PATH = "#f1c40f"      # Yellow
    START_NODE = "#2ecc71"     # Green
    END_NODE = "#e74c3c"       # Red
    CURRENT_NODE = "#9b59b6"   # Purple


@dataclass
class ApplicationConfig:
    """Application-wide configuration."""
    
    # Paths
    APP_ROOT: Path = Path(__file__).parent.parent
    CACHE_DIR: Path = APP_ROOT / "assets" / "cache"
    OUTPUT_DIR: Path = APP_ROOT / "assets" / "output"
    VIDEO_DIR: Path = OUTPUT_DIR / "videos"
    REPORT_DIR: Path = OUTPUT_DIR / "reports"
    SCREENSHOT_DIR: Path = OUTPUT_DIR / "screenshots"
    
    # Create directories if they don't exist
    def __post_init__(self):
        """Initialize directory structure."""
        for directory in [self.CACHE_DIR, self.VIDEO_DIR, self.REPORT_DIR, self.SCREENSHOT_DIR]:
            directory.mkdir(parents=True, exist_ok=True)


@dataclass
class UIConfig:
    """UI-related configuration."""
    
    # Window
    WINDOW_WIDTH: Final[int] = 1600
    WINDOW_HEIGHT: Final[int] = 900
    WINDOW_TITLE: Final[str] = "PathVision AI - Pathfinding Visualization System"
    
    # Theme
    THEME_DARK: bool = True
    BACKGROUND_COLOR: str = "#1e1e1e"
    PRIMARY_COLOR: str = "#3498db"
    SECONDARY_COLOR: str = "#2c3e50"
    TEXT_COLOR: str = "#ecf0f1"
    
    # Panels
    LEFT_PANEL_WIDTH: Final[int] = 250
    RIGHT_PANEL_WIDTH: Final[int] = 300
    BOTTOM_PANEL_HEIGHT: Final[int] = 100
    
    # Animation
    DEFAULT_FPS: Final[int] = 60
    MIN_SPEED: Final[int] = 1
    MAX_SPEED: Final[int] = 100
    DEFAULT_SPEED: Final[int] = 50


@dataclass
class MapConfig:
    """Map loading and caching configuration."""
    
    # Network type
    NETWORK_TYPE: Final[str] = "drive"  # drive, walk, bike, all
    
    # Cache settings
    USE_CACHE: bool = True
    CACHE_NETWORK: bool = True
    CACHE_EXPIRY_DAYS: Final[int] = 30
    
    # Download settings
    TIMEOUT: Final[int] = 300  # seconds
    RETRY_COUNT: Final[int] = 3
    
    # Graph settings
    SIMPLIFY: Final[bool] = True
    CUSTOM_FILTER: Final[str] = '["highway"~"motorway|trunk|primary|secondary|tertiary|residential"]'


@dataclass
class AlgorithmConfig:
    """Algorithm execution configuration."""
    
    # Heuristic (for A* and similar)
    HEURISTIC: Final[str] = "haversine"  # haversine distance
    
    # Execution
    TIMEOUT_SECONDS: Final[int] = 60
    MAX_ITERATIONS: Final[int] = None  # None = unlimited
    
    # Statistics
    COLLECT_STATISTICS: bool = True
    PROFILE_MEMORY: bool = True


@dataclass
class VisualizationConfig:
    """Visualization rendering configuration."""
    
    # Canvas
    DPI: Final[int] = 100
    FIGURE_SIZE: tuple = (12, 9)
    
    # Node rendering
    NODE_SIZE_UNVISITED: Final[int] = 1
    NODE_SIZE_VISITED: Final[int] = 2
    NODE_SIZE_CURRENT: Final[int] = 8
    NODE_SIZE_START: Final[int] = 15
    NODE_SIZE_END: Final[int] = 15
    
    # Edge rendering
    EDGE_WIDTH_UNVISITED: Final[float] = 0.5
    EDGE_WIDTH_VISITED: Final[float] = 1.0
    EDGE_WIDTH_PATH: Final[float] = 2.5
    EDGE_ALPHA_UNVISITED: Final[float] = 0.3
    EDGE_ALPHA_VISITED: Final[float] = 0.8
    EDGE_ALPHA_PATH: Final[float] = 1.0
    
    # Animation
    UPDATE_INTERVAL_MS: Final[int] = 16  # ~60 FPS
    ANIMATION_SMOOTHNESS: Final[float] = 0.5
    SHOW_QUEUE_SIZE: bool = True


# Global configuration instances
APP_CONFIG = ApplicationConfig()
UI_CONFIG = UIConfig()
MAP_CONFIG = MapConfig()
ALGO_CONFIG = AlgorithmConfig()
VIS_CONFIG = VisualizationConfig()
COLOR_CONFIG = ColorScheme()


def load_config_from_file(filepath: str) -> Dict[str, Any]:
    """Load configuration from a JSON file.
    
    Args:
        filepath: Path to configuration JSON file
        
    Returns:
        Dictionary containing configuration settings
        
    Raises:
        FileNotFoundError: If configuration file doesn't exist
        json.JSONDecodeError: If configuration file is invalid JSON
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Configuration file not found: {filepath}")
    
    with open(filepath, 'r') as f:
        return json.load(f)


def save_config_to_file(config: Dict[str, Any], filepath: str) -> None:
    """Save configuration to a JSON file.
    
    Args:
        config: Configuration dictionary to save
        filepath: Path where to save the configuration
    """
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(config, f, indent=2)


def get_city_by_name(name: str) -> City:
    """Get City enum by display name.
    
    Args:
        name: Display name of the city
        
    Returns:
        City enum value
        
    Raises:
        ValueError: If city not found
    """
    for city in City:
        if city.display_name.lower() == name.lower():
            return city
    raise ValueError(f"City '{name}' not found in available cities")


def get_algorithm_by_name(name: str) -> Algorithm:
    """Get Algorithm enum by name.
    
    Args:
        name: Name of the algorithm
        
    Returns:
        Algorithm enum value
        
    Raises:
        ValueError: If algorithm not found
    """
    try:
        return Algorithm[name.upper().replace("-", "_")]
    except KeyError:
        raise ValueError(f"Algorithm '{name}' not found in available algorithms")
