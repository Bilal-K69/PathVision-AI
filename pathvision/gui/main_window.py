"""Main application window for PathVision AI.

Provides the primary user interface with layout management and event handling.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox,
    QPushButton, QSlider, QSpinBox, QCheckBox, QGroupBox, QListWidget,
    QListWidgetItem, QTabWidget, QSplitter, QFrame
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont, QColor

from pathvision.config import UI_CONFIG, City, Algorithm
from pathvision.logging_config import logger


class MainWindow(QMainWindow):
    """Main application window.
    
    Attributes:
        window_title: Title of the window
        width: Width of the window in pixels
        height: Height of the window in pixels
    """
    
    # Signals
    city_changed = Signal(str)
    algorithm_changed = Signal(str)
    speed_changed = Signal(int)
    run_clicked = Signal()
    pause_clicked = Signal()
    resume_clicked = Signal()
    reset_clicked = Signal()
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        self.setWindowTitle(UI_CONFIG.WINDOW_TITLE)
        self.setGeometry(100, 100, UI_CONFIG.WINDOW_WIDTH, UI_CONFIG.WINDOW_HEIGHT)
        
        # Initialize UI components
        self._init_ui()
        
        logger.info("MainWindow initialized")
    
    def _init_ui(self) -> None:
        """Initialize user interface components."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Left panel
        left_panel = self._create_left_panel()
        main_layout.addWidget(left_panel, 0)  # Fixed width
        
        # Center panel (visualization)
        center_panel = self._create_center_panel()
        main_layout.addWidget(center_panel, 1)  # Expandable
        
        # Right panel (statistics)
        right_panel = self._create_right_panel()
        main_layout.addWidget(right_panel, 0)  # Fixed width
        
        # Bottom panel (timeline/controls)
        bottom_panel = self._create_bottom_panel()
        main_layout.addWidget(bottom_panel)
    
    def _create_left_panel(self) -> QFrame:
        """Create left control panel.
        
        Returns:
            QFrame containing the left panel
        """
        frame = QFrame()
        frame.setMaximumWidth(UI_CONFIG.LEFT_PANEL_WIDTH)
        frame.setStyleSheet(f"QFrame {{ background-color: {UI_CONFIG.SECONDARY_COLOR}; }}")        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("Controls")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # City selection
        layout.addWidget(QLabel("City:"))
        self.city_combo = QComboBox()
        self.city_combo.addItems([city.display_name for city in City])
        self.city_combo.currentTextChanged.connect(self.city_changed.emit)
        layout.addWidget(self.city_combo)
        
        # Algorithm selection
        layout.addWidget(QLabel("Algorithm:"))
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItems([algo.value.replace('_', ' ').title() for algo in Algorithm])
        self.algorithm_combo.currentTextChanged.connect(self.algorithm_changed.emit)
        layout.addWidget(self.algorithm_combo)
        
        # Speed slider
        layout.addWidget(QLabel("Speed:"))
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setValue(50)
        self.speed_slider.valueChanged.connect(self.speed_changed.emit)
        layout.addWidget(self.speed_slider)
        
        # Control buttons
        layout.addWidget(QLabel("Control:"))
        
        self.run_button = QPushButton("▶ Run")
        self.run_button.clicked.connect(self.run_clicked.emit)
        layout.addWidget(self.run_button)
        
        self.pause_button = QPushButton("⏸ Pause")
        self.pause_button.clicked.connect(self.pause_clicked.emit)
        self.pause_button.setEnabled(False)
        layout.addWidget(self.pause_button)
        
        self.resume_button = QPushButton("▶ Resume")
        self.resume_button.clicked.connect(self.resume_clicked.emit)
        self.resume_button.setEnabled(False)
        layout.addWidget(self.resume_button)
        
        self.reset_button = QPushButton("⟲ Reset")
        self.reset_button.clicked.connect(self.reset_clicked.emit)
        layout.addWidget(self.reset_button)
        
        # Options
        layout.addWidget(QLabel("Options:"))
        self.comparison_checkbox = QCheckBox("Comparison Mode")
        layout.addWidget(self.comparison_checkbox)
        
        self.ai_mode_checkbox = QCheckBox("AI Recommendation")
        layout.addWidget(self.ai_mode_checkbox)
        
        # Spacer
        layout.addStretch()
        
        return frame
    
    def _create_center_panel(self) -> QFrame:
        """Create center visualization panel.
        
        Returns:
            QFrame containing the center panel
        """
        frame = QFrame()
        frame.setStyleSheet(f"QFrame {{ background-color: {UI_CONFIG.BACKGROUND_COLOR}; }}")        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Placeholder for matplotlib canvas
        placeholder = QLabel("Visualization Canvas")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet(f"QLabel {{ color: {UI_CONFIG.TEXT_COLOR}; }}")
        layout.addWidget(placeholder)
        
        return frame
    
    def _create_right_panel(self) -> QFrame:
        """Create right statistics panel.
        
        Returns:
            QFrame containing the right panel
        """
        frame = QFrame()
        frame.setMaximumWidth(UI_CONFIG.RIGHT_PANEL_WIDTH)
        frame.setStyleSheet(f"QFrame {{ background-color: {UI_CONFIG.SECONDARY_COLOR}; }}")        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("Statistics")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Statistics items
        stats = [
            ("Status:", "Idle"),
            ("Current Node:", "-"),
            ("Nodes Visited:", "0"),
            ("Nodes Explored:", "0"),
            ("Distance:", "0 m"),
            ("Path Length:", "0"),
            ("Time:", "0 ms"),
            ("Queue Size:", "0"),
            ("Memory:", "0 MB"),
        ]
        
        for label_text, value_text in stats:
            label = QLabel(label_text)
            label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            value = QLabel(value_text)
            value.setStyleSheet(f"QLabel {{ color: {UI_CONFIG.PRIMARY_COLOR}; }}")
            
            layout.addWidget(label)
            layout.addWidget(value)
        
        # Spacer
        layout.addStretch()
        
        return frame
    
    def _create_bottom_panel(self) -> QFrame:
        """Create bottom timeline/playback panel.
        
        Returns:
            QFrame containing the bottom panel
        """
        frame = QFrame()
        frame.setMaximumHeight(UI_CONFIG.BOTTOM_PANEL_HEIGHT)
        frame.setStyleSheet(f"QFrame {{ background-color: {UI_CONFIG.SECONDARY_COLOR}; }}")        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Timeline label
        timeline_label = QLabel("Timeline: 0 / 0")
        layout.addWidget(timeline_label)
        
        # Timeline slider
        self.timeline_slider = QSlider(Qt.Orientation.Horizontal)
        self.timeline_slider.setMinimum(0)
        layout.addWidget(self.timeline_slider, 1)
        
        # Current step
        step_label = QLabel("Step: 0")
        layout.addWidget(step_label)
        
        return frame
    
    def closeEvent(self, event):
        """Handle window close event.
        
        Args:
            event: Close event
        """
        logger.info("MainWindow closing")
        super().closeEvent(event)
