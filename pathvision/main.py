#!/usr/bin/env python3
"""PathVision AI - Main application entry point.

Initializes the application, sets up logging, and launches the GUI.
"""

import sys
import logging
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from pathvision.logging_config import setup_logging
from pathvision.gui.main_window import MainWindow
from pathvision.config import APP_CONFIG, UI_CONFIG


def setup_application_style() -> None:
    """Set up application-wide styling."""
    app = QApplication.instance()
    if app is None:
        return
    
    # Set application style
    app.setStyle('Fusion')
    
    # High DPI scaling
    app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)


def main() -> int:
    """Main application entry point.
    
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        # Set up logging
        logger = setup_logging(
            level=logging.INFO,
            log_file="pathvision.log",
            log_dir=APP_CONFIG.APP_ROOT / "logs"
        )
        
        logger.info("="*60)
        logger.info("PathVision AI - Interactive Pathfinding Visualization")
        logger.info("="*60)
        
        # Verify cache directory exists
        APP_CONFIG.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        logger.info(f"Cache directory: {APP_CONFIG.CACHE_DIR}")
        
        # Create Qt application
        app = QApplication(sys.argv)
        logger.info("Qt Application created")
        
        # Set up application styling
        setup_application_style()
        
        # Create main window
        window = MainWindow()
        logger.info("Main window created")
        
        # Show window
        window.show()
        logger.info("Main window displayed")
        
        # Enter event loop
        logger.info("Entering main event loop")
        exit_code = app.exec()
        
        logger.info(f"Application exit code: {exit_code}")
        return exit_code
        
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
