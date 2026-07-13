"""Utility functions for PathVision AI.

Provides helper functions for common operations including:
- Coordinate transformations
- Distance calculations
- Formatting utilities
- Validation functions
"""

import math
from typing import Tuple, List, Optional
from pathvision.logging_config import logger


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate great-circle distance between two points using Haversine formula.
    
    Args:
        lat1: Latitude of first point in degrees
        lon1: Longitude of first point in degrees
        lat2: Latitude of second point in degrees
        lon2: Longitude of second point in degrees
        
    Returns:
        Distance in kilometers
    """
    R = 6371.0  # Earth radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c


def euclidean_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate Euclidean distance between two points.
    
    Args:
        x1: X-coordinate of first point
        y1: Y-coordinate of first point
        x2: X-coordinate of second point
        y2: Y-coordinate of second point
        
    Returns:
        Euclidean distance
    """
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def manhattan_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate Manhattan distance between two points.
    
    Args:
        x1: X-coordinate of first point
        y1: Y-coordinate of first point
        x2: X-coordinate of second point
        y2: Y-coordinate of second point
        
    Returns:
        Manhattan distance
    """
    return abs(x2 - x1) + abs(y2 - y1)


def format_distance(distance_m: float) -> str:
    """Format distance in meters to human-readable string.
    
    Args:
        distance_m: Distance in meters
        
    Returns:
        Formatted distance string (e.g., "2.5 km", "500 m")
    """
    if distance_m >= 1000:
        return f"{distance_m / 1000:.2f} km"
    else:
        return f"{distance_m:.0f} m"


def format_time(milliseconds: float) -> str:
    """Format time in milliseconds to human-readable string.
    
    Args:
        milliseconds: Time in milliseconds
        
    Returns:
        Formatted time string (e.g., "2.5 s", "500 ms")
    """
    if milliseconds >= 1000:
        return f"{milliseconds / 1000:.2f} s"
    else:
        return f"{milliseconds:.0f} ms"


def format_memory(bytes_count: float) -> str:
    """Format memory size in bytes to human-readable string.
    
    Args:
        bytes_count: Size in bytes
        
    Returns:
        Formatted size string (e.g., "2.5 MB", "500 KB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_count < 1024:
            return f"{bytes_count:.2f} {unit}"
        bytes_count /= 1024
    return f"{bytes_count:.2f} TB"


def validate_coordinates(latitude: float, longitude: float) -> bool:
    """Validate geographic coordinates.
    
    Args:
        latitude: Latitude in degrees (-90 to 90)
        longitude: Longitude in degrees (-180 to 180)
        
    Returns:
        True if coordinates are valid, False otherwise
    """
    return -90 <= latitude <= 90 and -180 <= longitude <= 180


def is_valid_node_id(node_id: int) -> bool:
    """Validate node ID.
    
    Args:
        node_id: Node ID to validate
        
    Returns:
        True if node ID is valid, False otherwise
    """
    return isinstance(node_id, int) and node_id >= 0


def clamp(value: float, min_value: float, max_value: float) -> float:
    """Clamp a value between min and max.
    
    Args:
        value: Value to clamp
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        
    Returns:
        Clamped value
    """
    return max(min_value, min(value, max_value))


def chunks(list_obj: List, chunk_size: int) -> List[List]:
    """Split a list into chunks of specified size.
    
    Args:
        list_obj: List to split
        chunk_size: Size of each chunk
        
    Returns:
        List of chunks
    """
    return [list_obj[i:i + chunk_size] for i in range(0, len(list_obj), chunk_size)]


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is zero.
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if division by zero
        
    Returns:
        Result of division or default value
    """
    return numerator / denominator if denominator != 0 else default
