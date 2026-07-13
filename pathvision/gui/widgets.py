"""Enhanced GUI widgets for PathVision AI.

Provides custom UI components for visualization and control.
"""

from PySide6.QtWidgets import (
    QWidget, QLabel, QProgressBar, QSlider, QPushButton,
    QVBoxLayout, QHBoxLayout, QGroupBox, QComboBox, QCheckBox
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont, QColor

from pathvision.config import UI_CONFIG, COLOR_CONFIG
from pathvision.logging_config import logger


class StatisticsPanel(QWidget):
    """Panel displaying algorithm execution statistics.
    
    Signals:
        updated: Emitted when statistics are updated
    """
    
    updated = Signal()
    
    def __init__(self, parent=None):
        """Initialize statistics panel.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.stats_labels = {}
        self._init_ui()
    
    def _init_ui(self) -> None:
        """Initialize UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # Title
        title = QLabel("Statistics")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Statistics items
        stats_items = [
            ('status', 'Status:', 'Idle'),
            ('current_node', 'Current Node:', '-'),
            ('nodes_visited', 'Nodes Visited:', '0'),
            ('nodes_explored', 'Nodes Explored:', '0'),
            ('distance', 'Distance:', '0 m'),
            ('path_length', 'Path Length:', '0'),
            ('time', 'Execution Time:', '0 ms'),
            ('queue_size', 'Queue Size:', '0'),
            ('memory', 'Memory:', '0 MB'),
        ]
        
        for key, label_text, default_value in stats_items:
            label = QLabel(label_text)
            label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            
            value = QLabel(default_value)
            value.setStyleSheet(f"QLabel {{ color: {UI_CONFIG.PRIMARY_COLOR}; }}")
            
            self.stats_labels[key] = value
            
            layout.addWidget(label)
            layout.addWidget(value)
        
        layout.addStretch()
    
    def update_stat(self, key: str, value: str) -> None:
        """Update a single statistic.
        
        Args:
            key: Statistic key
            value: New value
        """
        if key in self.stats_labels:
            self.stats_labels[key].setText(value)
            self.updated.emit()
    
    def update_all(self, stats_dict: dict) -> None:
        """Update multiple statistics.
        
        Args:
            stats_dict: Dictionary of statistic key-value pairs
        """
        for key, value in stats_dict.items():
            if key in self.stats_labels:
                self.stats_labels[key].setText(str(value))
        self.updated.emit()
    
    def reset(self) -> None:
        """Reset all statistics to default values."""
        self.update_all({
            'status': 'Idle',
            'current_node': '-',
            'nodes_visited': '0',
            'nodes_explored': '0',
            'distance': '0 m',
            'path_length': '0',
            'time': '0 ms',
            'queue_size': '0',
            'memory': '0 MB'
        })


class PlaybackControls(QWidget):
    """Playback control widget for visualization.
    
    Signals:
        play: Emitted when play is clicked
        pause: Emitted when pause is clicked
        step_changed: Emitted when current step changes
    """
    
    play = Signal()
    pause = Signal()
    step_changed = Signal(int)
    
    def __init__(self, parent=None):
        """Initialize playback controls.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self) -> None:
        """Initialize UI components."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        # Play button
        self.play_btn = QPushButton("▶ Play")
        self.play_btn.clicked.connect(self.play.emit)
        layout.addWidget(self.play_btn)
        
        # Pause button
        self.pause_btn = QPushButton("⏸ Pause")
        self.pause_btn.clicked.connect(self.pause.emit)
        self.pause_btn.setEnabled(False)
        layout.addWidget(self.pause_btn)
        
        # Timeline slider
        layout.addWidget(QLabel("Timeline:"))
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.sliderMoved.connect(lambda: self.step_changed.emit(self.slider.value()))
        layout.addWidget(self.slider, 1)
        
        # Step display
        self.step_label = QLabel("0 / 0")
        layout.addWidget(self.step_label)
    
    def set_total_steps(self, total: int) -> None:
        """Set total number of steps.
        
        Args:
            total: Total step count
        """
        self.slider.setMaximum(max(0, total - 1))
        self._update_label()
    
    def set_current_step(self, current: int) -> None:
        """Set current step.
        
        Args:
            current: Current step index
        """
        self.slider.blockSignals(True)
        self.slider.setValue(current)
        self.slider.blockSignals(False)
        self._update_label()
    
    def _update_label(self) -> None:
        """Update step label."""
        current = self.slider.value()
        total = self.slider.maximum() + 1
        self.step_label.setText(f"{current} / {total}")
    
    def set_playing(self, is_playing: bool) -> None:
        """Set playing state.
        
        Args:
            is_playing: Whether playback is active
        """
        self.play_btn.setEnabled(not is_playing)
        self.pause_btn.setEnabled(is_playing)


class AlgorithmSelector(QWidget):
    """Algorithm selection widget.
    
    Signals:
        algorithm_selected: Emitted when algorithm is selected
    """
    
    algorithm_selected = Signal(str)
    
    def __init__(self, algorithms: list, parent=None):
        """Initialize algorithm selector.
        
        Args:
            algorithms: List of algorithm names
            parent: Parent widget
        """
        super().__init__(parent)
        self.algorithms = algorithms
        self._init_ui()
    
    def _init_ui(self) -> None:
        """Initialize UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Label
        label = QLabel("Algorithm:")
        label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(label)
        
        # Combo box
        self.combo = QComboBox()
        self.combo.addItems(self.algorithms)
        self.combo.currentTextChanged.connect(self.algorithm_selected.emit)
        layout.addWidget(self.combo)
    
    def get_selected(self) -> str:
        """Get selected algorithm.
        
        Returns:
            Name of selected algorithm
        """
        return self.combo.currentText()
    
    def set_selected(self, algorithm: str) -> None:
        """Set selected algorithm.
        
        Args:
            algorithm: Algorithm name to select
        """
        index = self.combo.findText(algorithm)
        if index >= 0:
            self.combo.setCurrentIndex(index)


class AdvancedOptionsPanel(QWidget):
    """Advanced options panel.
    
    Signals:
        comparison_mode_toggled: Emitted when comparison mode is toggled
        ai_mode_toggled: Emitted when AI mode is toggled
    """
    
    comparison_mode_toggled = Signal(bool)
    ai_mode_toggled = Signal(bool)
    
    def __init__(self, parent=None):
        """Initialize advanced options panel.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self) -> None:
        """Initialize UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("Advanced Options")
        title.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Comparison mode
        self.comparison_checkbox = QCheckBox("Compare All Algorithms")
        self.comparison_checkbox.toggled.connect(self.comparison_mode_toggled.emit)
        layout.addWidget(self.comparison_checkbox)
        
        # AI mode
        self.ai_checkbox = QCheckBox("AI Recommendation")
        self.ai_checkbox.toggled.connect(self.ai_mode_toggled.emit)
        layout.addWidget(self.ai_checkbox)
        
        layout.addStretch()
    
    def is_comparison_mode(self) -> bool:
        """Check if comparison mode is enabled.
        
        Returns:
            True if comparison mode is enabled
        """
        return self.comparison_checkbox.isChecked()
    
    def is_ai_mode(self) -> bool:
        """Check if AI mode is enabled.
        
        Returns:
            True if AI mode is enabled
        """
        return self.ai_checkbox.isChecked()
