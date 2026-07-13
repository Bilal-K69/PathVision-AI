"""GUI styles for PathVision AI.

Provides styling and theming utilities.
"""

from typing import Dict
from pathvision.config import UI_CONFIG


def get_dark_stylesheet() -> str:
    """Get dark theme stylesheet.
    
    Returns:
        QSS stylesheet string
    """
    return f"""
    QWidget {{
        background-color: {UI_CONFIG.BACKGROUND_COLOR};
        color: {UI_CONFIG.TEXT_COLOR};
    }}
    
    QPushButton {{
        background-color: {UI_CONFIG.PRIMARY_COLOR};
        color: {UI_CONFIG.TEXT_COLOR};
        border: none;
        padding: 5px 15px;
        border-radius: 3px;
        font-weight: bold;
    }}
    
    QPushButton:hover {{
        background-color: {lighten_color(UI_CONFIG.PRIMARY_COLOR, 20)};
    }}
    
    QPushButton:pressed {{
        background-color: {darken_color(UI_CONFIG.PRIMARY_COLOR, 20)};
    }}
    
    QPushButton:disabled {{
        background-color: gray;
        color: darkgray;
    }}
    
    QComboBox {{
        background-color: {UI_CONFIG.SECONDARY_COLOR};
        color: {UI_CONFIG.TEXT_COLOR};
        border: 1px solid {UI_CONFIG.PRIMARY_COLOR};
        padding: 3px;
        border-radius: 3px;
    }}
    
    QSlider::groove:horizontal {{
        border: 1px solid {UI_CONFIG.PRIMARY_COLOR};
        height: 8px;
        background: {UI_CONFIG.SECONDARY_COLOR};
        border-radius: 4px;
    }}
    
    QSlider::handle:horizontal {{
        background: {UI_CONFIG.PRIMARY_COLOR};
        border: 1px solid {UI_CONFIG.PRIMARY_COLOR};
        width: 12px;
        margin: -2px 0;
        border-radius: 6px;
    }}
    
    QSlider::handle:horizontal:hover {{
        background: {lighten_color(UI_CONFIG.PRIMARY_COLOR, 20)};
    }}
    
    QLabel {{
        color: {UI_CONFIG.TEXT_COLOR};
    }}
    
    QGroupBox {{
        border: 1px solid {UI_CONFIG.PRIMARY_COLOR};
        border-radius: 3px;
        margin-top: 8px;
        padding-top: 8px;
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 3px 0 3px;
    }}
    
    QCheckBox {{
        color: {UI_CONFIG.TEXT_COLOR};
        spacing: 5px;
    }}
    
    QCheckBox::indicator {{
        width: 16px;
        height: 16px;
    }}
    
    QCheckBox::indicator:unchecked {{
        background-color: {UI_CONFIG.SECONDARY_COLOR};
        border: 1px solid {UI_CONFIG.PRIMARY_COLOR};
        border-radius: 2px;
    }}
    
    QCheckBox::indicator:checked {{
        background-color: {UI_CONFIG.PRIMARY_COLOR};
        border: 1px solid {UI_CONFIG.PRIMARY_COLOR};
        border-radius: 2px;
    }}
    
    QProgressBar {{
        border: 1px solid {UI_CONFIG.PRIMARY_COLOR};
        border-radius: 3px;
        text-align: center;
        height: 20px;
    }}
    
    QProgressBar::chunk {{
        background-color: {UI_CONFIG.PRIMARY_COLOR};
    }}
    """


def lighten_color(hex_color: str, percent: int) -> str:
    """Lighten a hex color.
    
    Args:
        hex_color: Hex color string (e.g., "#3498db")
        percent: Percentage to lighten (0-100)
        
    Returns:
        Lightened hex color string
    """
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    lightened = tuple(min(255, int(c + (255 - c) * percent / 100)) for c in rgb)
    
    return '#{:02x}{:02x}{:02x}'.format(*lightened)


def darken_color(hex_color: str, percent: int) -> str:
    """Darken a hex color.
    
    Args:
        hex_color: Hex color string (e.g., "#3498db")
        percent: Percentage to darken (0-100)
        
    Returns:
        Darkened hex color string
    """
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    darkened = tuple(max(0, int(c * (1 - percent / 100))) for c in rgb)
    
    return '#{:02x}{:02x}{:02x}'.format(*darkened)
