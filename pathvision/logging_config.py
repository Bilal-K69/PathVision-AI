"""Logging configuration for PathVision AI.

Provides centralized logging setup with file and console handlers.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    log_dir: Optional[Path] = None
) -> logging.Logger:
    """Set up logging configuration.
    
    Args:
        level: Logging level (default: INFO)
        log_file: Filename for log file (optional)
        log_dir: Directory for log files (default: ./logs)
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("pathvision")
    logger.setLevel(level)
    
    # Log format
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        if log_dir is None:
            log_dir = Path("./logs")
        
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / log_file
        
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Create module-level logger
logger = setup_logging()
