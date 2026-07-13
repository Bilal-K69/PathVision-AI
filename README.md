# PathVision AI

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![PySide6](https://img.shields.io/badge/ui-PySide6-green.svg)](https://www.qt.io/qt-for-python)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Interactive Pathfinding Visualization and Intelligent Analysis System

A production-quality desktop application that visualizes graph pathfinding algorithms on real-world road networks downloaded from OpenStreetMap. Watch algorithms explore thousands of intersections in real-time with professional animations and detailed statistical analysis.

### Features

✨ **Interactive Visualization**
- Real-world road networks with thousands of intersections
- Smooth animations showing every exploration step
- Interactive zooming and panning
- Play/pause/resume controls with speed adjustment
- Live statistics and performance metrics

🧠 **Advanced Algorithms**
- Dijkstra's Algorithm
- A* Search
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Greedy Best-First Search
- Bidirectional A*

🤖 **AI-Powered Features**
- Intelligent algorithm recommendation engine
- Automatic comparison mode
- Performance analysis and reporting
- Graph property analysis

📊 **Comprehensive Analytics**
- Execution time tracking
- Node exploration metrics
- Memory usage monitoring
- Path length optimization
- Real-time statistics display

🌍 **Global City Support**
- Lahore, Karachi, Islamabad (Pakistan)
- Tokyo, London, New York, Paris (International)
- Automatic network caching
- Instant loading on repeat runs

### System Architecture

```
PathVision/
├── pathvision/
│   ├── __init__.py
│   ├── main.py                 # Application entry point
│   ├── config.py               # Configuration management
│   ├── logging_config.py       # Logging setup
│   ├── utils.py                # Utility functions
│   ├── models.py               # Data models
│   │
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── main_window.py      # Main application window
│   │   ├── widgets.py          # Reusable UI components
│   │   ├── styles.py           # Theme and styling
│   │   └── dialogs.py          # Dialog windows
│   │
│   ├── map/
│   │   ├── __init__.py
│   │   ├── loader.py           # OSMnx map loading
│   │   ├── cache.py            # Cache management
│   │   └── preprocessor.py     # Graph preprocessing
│   │
│   ├── visualization/
│   │   ├── __init__.py
│   │   ├── renderer.py         # Core rendering engine
│   │   ├── animator.py         # Animation system
│   │   └── canvas.py           # Canvas abstraction
│   │
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── base.py             # Base algorithm class
│   │   ├── dijkstra.py         # Dijkstra's algorithm
│   │   ├── astar.py            # A* search
│   │   ├── bfs.py              # Breadth-First Search
│   │   ├── dfs.py              # Depth-First Search
│   │   ├── greedy.py           # Greedy Best-First
│   │   └── bidirectional_astar.py  # Bidirectional A*
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── analyzer.py         # Graph analysis
│   │   ├── recommender.py      # Algorithm recommendation
│   │   ├── comparator.py       # Algorithm comparison
│   │   └── report_generator.py # Report generation
│   │
│   └── execution/
│       ├── __init__.py
│       ├── executor.py         # Algorithm execution engine
│       └── statistics.py       # Statistics collection
│
├── tests/
│   ├── __init__.py
│   ├── test_algorithms.py
│   ├── test_map_loader.py
│   └── test_utilities.py
│
├── assets/
│   ├── cache/                  # Downloaded map cache
│   ├── output/
│   │   ├── videos/
│   │   ├── reports/
│   │   └── screenshots/
│   └── config.json             # Default configuration
│
├── requirements.txt
├── setup.py
├── .gitignore
└── main.py                     # Entry point
```

### Installation

**Requirements:**
- Python 3.13+
- pip or conda
- FFmpeg (optional, for video export)

**Steps:**

1. Clone the repository:
```bash
git clone https://github.com/Bilal-K69/PathVision-AI.git
cd PathVision-AI
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

### Usage

1. **Select a City:** Choose from pre-configured cities in the left panel
2. **Select an Algorithm:** Pick from available pathfinding algorithms
3. **Choose Start Point:** Click on the map to select the starting intersection
4. **Choose End Point:** Click again to select the destination
5. **Run:** Press the Run button to visualize the algorithm
6. **Interact:** Use playback controls to pause, resume, or adjust speed
7. **Analyze:** Review statistics and AI recommendations in the right panel
8. **Compare:** Enable comparison mode to test multiple algorithms simultaneously

### Algorithm Complexity

| Algorithm | Time Complexity | Space Complexity | Optimality | Use Case |
|-----------|-----------------|------------------|------------|-----------|
| Dijkstra | O((V+E)logV) | O(V) | ✓ Optimal | Weighted graphs, general purpose |
| A* | O((V+E)logV) | O(V) | ✓ Optimal | Heuristic-guided search |
| BFS | O(V+E) | O(V) | ✓ Unweighted | Unweighted shortest path |
| DFS | O(V+E) | O(V) | ✗ No | Graph exploration |
| Greedy | O((V+E)logV) | O(V) | ✗ No | Fast approximation |
| Bidirectional A* | O((V+E)logV) | O(V) | ✓ Optimal | Bidirectional heuristic search |

### Architecture Principles

- **Separation of Concerns:** GUI, algorithms, and visualization are completely decoupled
- **Clean Code:** Type hints, docstrings, PEP8 compliance throughout
- **SOLID Principles:** Single responsibility, open/closed design
- **Scalability:** Handles graphs with 50,000+ nodes
- **Performance:** Incremental rendering, optimized drawing
- **Extensibility:** Easy to add new algorithms and cities

### Development

To run tests:
```bash
pytest tests/ -v
```

To check code quality:
```bash
flake8 pathvision/ --max-line-length=100
pylint pathvision/
mypy pathvision/ --strict
```

### Technology Stack

- **GUI:** PySide6 (PyQt6 bindings)
- **Mapping:** OSMnx, NetworkX, GeoPandas
- **Visualization:** Matplotlib, NumPy
- **Geometry:** Shapely
- **Animation:** Custom animation system
- **Export:** FFmpeg, ManimCE (optional)

### Performance Characteristics

- **Typical City Network:** 20,000-50,000 intersections
- **Algorithm Runtime:** 100ms - 5s (depending on algorithm and city size)
- **Visualization Framerate:** 60 FPS
- **Memory Usage:** 200-500 MB (including cached networks)
- **Cache Size:** 50-200 MB per city

### Future Enhancements

- [ ] JavaFX integration for cross-platform deployment
- [ ] 3D visualization mode
- [ ] Real-time traffic simulation
- [ ] Custom graph upload
- [ ] Advanced filtering and analysis
- [ ] Machine learning optimization
- [ ] Network community detection
- [ ] Multi-threading optimization

### License

MIT License - See LICENSE file for details

### Author

Bilal-K69

### Acknowledgments

- OpenStreetMap for map data
- NetworkX for graph algorithms
- OSMnx for map downloading
- Qt/PySide6 for UI framework
