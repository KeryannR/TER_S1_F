from Grid import Grid
from HuntAndKill import HuntAndKill
from collections import deque
import numpy as np

class MazeMetrics:
    def __init__(self, grid: Grid):
        self.grid = grid

    def count_deadends(self) -> int:
        # returns the number of dead ends cells
        return len(self.grid.deadends())

    def average_deadend_distance(self) -> float:
        # avg distance between dead ends via BFS
        deadends = self.grid.deadends()
        if len(deadends) < 2:
            return 0
        distances = []
        for i in range(len(deadends) - 1):
            for j in range(i + 1, len(deadends)):
                d = self._shortest_path_length(deadends[i], deadends[j])
                if d is not None:
                    distances.append(d)
        return np.mean(distances) if distances else 0

    def path_length_distribution(self) -> dict:
        # returns dictionary of path lengths between pairs of cells
        lengths = []
        all_cells = list(self.grid.eachCell())
        for i, cell in enumerate(all_cells):
            for j in range(i + 1, len(all_cells)):
                d = self._shortest_path_length(cell, all_cells[j])
                if d is not None:
                    lengths.append(d)
        return {
            "min": np.min(lengths),
            "max": np.max(lengths),
            "avg": np.mean(lengths)
        }

    def longest_path(self):
        # finds the longest path in the maze using two BFS passes
        start_cell, _ = self._farthest_cell(self.grid.randomCell())
        end_cell, dist = self._farthest_cell(start_cell)
        return (start_cell, end_cell, dist)

    def _shortest_path_length(self, start, goal) -> int:
        # BFS between two cells
        queue = deque([(start, 0)])
        visited = {start}
        while queue:
            cell, dist = queue.popleft()
            if cell == goal:
                return dist
            for linked in cell.getLinks():
                if linked not in visited:
                    visited.add(linked)
                    queue.append((linked, dist + 1))
        return None

    def _farthest_cell(self, start):
        # returns farthest cell and distance
        queue = deque([(start, 0)])
        visited = {start}
        farthest = (start, 0)
        while queue:
            cell, dist = queue.popleft()
            if dist > farthest[1]:
                farthest = (cell, dist)
            for linked in cell.getLinks():
                if linked not in visited:
                    visited.add(linked)
                    queue.append((linked, dist + 1))
        return farthest


if __name__ == "__main__":
    hak = HuntAndKill()
    grid = Grid(10, 10)
    maze = hak.on(grid)
    maze.braid(0.2)

    print(maze)
    metrics = MazeMetrics(maze)

    print("=== METRICS ===")
    print(f"Nb dead ends: {metrics.count_deadends()}")
    print(f"Avg distance between dead ends: {metrics.average_deadend_distance():.2f}")
    path_stats = metrics.path_length_distribution()
    print(f"Path lengths (min={path_stats['min']}, max={path_stats['max']}, avg={path_stats['avg']:.2f})")
    start, end, dist = metrics.longest_path()
    print(f"Longest path between ({start.row},{start.col}) and ({end.row},{end.col}): {dist} cells")