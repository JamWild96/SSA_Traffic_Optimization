#!/usr/bin/env python3
"""
simulate.py
Loads map.json and runs a simple BFS pathfinding from (0,0) to (n-1,n-1).
Prints the path if found, or a message if unreachable.
"""

import json
from collections import deque

def load_map(filename="map.json"):
    """
    Load the JSON grid file and return as a 2D list of ints.
    """
    with open(filename) as f:
        return json.load(f)

def find_path(grid):
    """
    Perform BFS on the grid to find a shortest path from start to goal.

    @param grid 2D list where 0=free, 1=obstacle
    @return     List of (row, col) tuples if path exists, else None
    """
    n = len(grid)
    start, goal = (0, 0), (n-1, n-1)
    if grid[0][0] or grid[n-1][n-1]:
        return None

    visited = [[False]*n for _ in range(n)]
    prev = {}  # Changed from 2D list to dictionary to fix type error
    q = deque([start])
    visited[0][0] = True
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]

    while q:
        x, y = q.popleft()
        if (x, y) == goal:
            break
        for dx, dy in dirs:
            nx, ny = x+dx, y+dy
            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and grid[nx][ny] == 0:
                visited[nx][ny] = True
                prev[nx][ny] = (x, y)
                q.append((nx, ny))

    if not visited[goal[0]][goal[1]]:
        return None

    path = []
    cur = goal
    while cur:
        path.append(cur)
        cur = prev[cur[0]][cur[1]]
    path.reverse()
    return path

if __name__ == "__main__":
    grid = load_map()
    path = find_path(grid)
    if path:
        print(f"Found path of length {len(path)}:")
        print(path)
    else:
        print("No path found.")
