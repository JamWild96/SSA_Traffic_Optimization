#!/usr/bin/env python3
"""
map_gen.py
Generates a random GRID_SIZE×GRID_SIZE map with obstacles and saves to map.json.

- 0 = free cell
- 1 = obstacle
"""

import json      # for JSON serialization
import random    # for random obstacle placement

GRID_SIZE = 20       # Width and height of square grid
OBSTACLE_RATIO = 0.2 # Fraction of cells to block

def generate_map():
    """
    Create a 2D grid (list of lists) with 0 or 1 entries.
    1 indicates an obstacle, placed with probability OBSTACLE_RATIO.
    """
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if random.random() < OBSTACLE_RATIO:
                grid[i][j] = 1
    return grid

def save_map(grid, filename="map.json"):
    """
    Write the grid to a JSON file.
    """
    with open(filename, "w") as f:
        json.dump(grid, f)

if __name__ == "__main__":
    grid = generate_map()
    save_map(grid)
    print("Generated map saved to map.json")
