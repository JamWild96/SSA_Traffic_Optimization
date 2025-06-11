# SSA Project Map - Python Implementation

This directory contains Python implementations for the Sparrow Search Algorithm (SSA) optimization project with map visualization and traffic simulation capabilities.

## Files Overview

- `map_generator.py` - Main SSA implementation for route optimization with visualization
- `traffic_simulator.py` - Traffic simulation with building overlays and traffic jam visualization
- `requirements.txt` - Python package dependencies

## Setup Instructions

### Option 1: Using Virtual Environment (Recommended)

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Option 2: System-wide Installation

If you prefer system-wide installation (not recommended on macOS with Homebrew Python):
```bash
pip install numpy matplotlib networkx --break-system-packages
```

## Usage

### Map Generator (SSA Optimization)

Run the main SSA optimization:
```bash
python map_generator.py
```

This will:
- Generate a random graph with configurable parameters
- Apply SSA optimization to find the best route
- Create visualization files:
  - `ssa_result.png` - Graph with optimal route highlighted
  - `visit_histogram.png` - Node visit frequency chart
  - `results.txt` - Text summary of results

### Traffic Simulator

The traffic simulator requires CSV input files for graph data, coordinates, route, and optional buildings/traffic jams:

```bash
python traffic_simulator.py --graph graph.csv --coords coords.csv --route route.txt [--places buildings.csv] [--jams traffic_jams.csv]
```

#### Input File Formats:

**graph.csv**: Adjacency matrix format
```
10
0,5.2,0,3.1,0,0,0,0,0,0
5.2,0,2.8,0,0,0,0,0,0,0
...
```

**coords.csv**: Node coordinates
```
node,x,y
0,0.1,0.2
1,0.3,0.4
...
```

**route.txt**: Route as node indices (one per line)
```
0
4
7
2
...
```

**buildings.csv** (optional): Building rectangles
```
name,x1,y1,x2,y2
School,0.1,0.1,0.3,0.4
Hospital,0.6,0.2,0.8,0.5
```

**traffic_jams.csv** (optional): Jammed edges
```
0,1
3,4
7,8
```

## Algorithm Parameters

You can modify these parameters in `map_generator.py`:

- `N_NODES`: Number of nodes in the graph (default: 10)
- `DENSITY`: Connection density threshold (default: 0.6)
- `MAX_ITER`: Maximum SSA iterations (default: 50)
- `POP_SIZE`: Population size for SSA (default: 20)

## Fixed Issues

The following issues have been resolved:

1. **Import Errors**: Fixed `matplotlib.patches.Rectangle` import in traffic simulator
2. **Environment Conflicts**: Created proper virtual environment setup to avoid numpy/matplotlib version conflicts
3. **Missing Dependencies**: Added `requirements.txt` for easy dependency management
4. **Unused Imports**: Removed unused `math` import from map generator

## Troubleshooting

### "Module not found" errors
- Ensure you're using the virtual environment: `source venv/bin/activate`
- Install all dependencies: `pip install -r requirements.txt`

### Matplotlib/NumPy compatibility issues
- Use the virtual environment approach to avoid system package conflicts
- On macOS with Homebrew, avoid mixing system and pip-installed packages

### Graph visualization not displaying
- The code saves plots to PNG files instead of displaying them
- Check for generated `.png` files in the current directory

## Output Files

When running `map_generator.py`, you'll get:
- `ssa_result.png`: Visual representation of the graph with the optimal route
- `visit_histogram.png`: Bar chart showing how often each node was visited during optimization
- `results.txt`: Text file with numerical results

The traffic simulator generates:
- `map.png`: Traffic simulation visualization with buildings, jams, and optimal route