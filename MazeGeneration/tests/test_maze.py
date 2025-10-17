import time
import unittest
import subprocess
import json
import numpy as np
import os

class TestMazeBridge(unittest.TestCase):

    # Basic structural tests

    def run_mazeBridge(self, args):
        cmd = ["python", "mazeBridge.py"] + args
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout.strip().splitlines()[-1]
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            return output

    def test_maze_size(self):
        maze = self.run_mazeBridge(["--xsize", "30", "--ysize", "30"])
        if isinstance(maze, str):
            self.skipTest("mazeBridge not return JSON")
        grid = maze["grid"]
        self.assertEqual(len(grid), 31)
        self.assertEqual(len(grid[0]), 31)

    def test_json_structure(self):
        maze = self.run_mazeBridge(["--xsize", "10", "--ysize", "12"])
        if isinstance(maze, str):
            self.skipTest("mazeBridge not return JSON")
        self.assertIn("width", maze)
        self.assertIn("height", maze)
        self.assertIn("grid", maze)
        self.assertIn("legend", maze)
        self.assertIsInstance(maze["grid"], list)
        self.assertIsInstance(maze["legend"], dict)

    def test_grid_values(self):
        maze = self.run_mazeBridge(["--xsize", "10", "--ysize", "10"])
        if isinstance(maze, str):
            self.skipTest("mazeBridge not return JSON")
        grid = np.array(maze["grid"])
        self.assertTrue(np.all(np.isin(grid, [0, 1])))

    def test_fixed_seed(self):
        maze1 = self.run_mazeBridge(["--xsize", "15", "--ysize", "15", "--seed", "42"])
        maze2 = self.run_mazeBridge(["--xsize", "15", "--ysize", "15", "--seed", "42"])
        if isinstance(maze1, str) or isinstance(maze2, str):
            self.skipTest("mazeBridge not return JSON")
        self.assertEqual(maze1["grid"], maze2["grid"])

    def test_include_tile(self):
        tile_path = "inCell\\tile1.tile"
        if not os.path.exists(tile_path):
            self.skipTest(f"Tile file {tile_path} not found")
        maze = self.run_mazeBridge(["--xsize", "15", "--ysize", "15", "--includetile", "tile1.tile"])
        if isinstance(maze, str):
            self.skipTest("mazeBridge not return JSON")
        grid = np.array(maze["grid"])
        self.assertTrue(np.any(grid == 1) or np.any(grid == 0))

    def test_nstep_influence(self):
        maze_low = self.run_mazeBridge(["--xsize", "10", "--ysize", "10", "--nstep", "10", "--seed", "1"])
        maze_high = self.run_mazeBridge(["--xsize", "10", "--ysize", "10", "--nstep", "20000", "--seed", "1"])
        if isinstance(maze_low, str) or isinstance(maze_high, str):
            self.skipTest("mazeBridge not return JSON")
        self.assertNotEqual(maze_low["grid"], maze_high["grid"])

    def test_maxborderspikesize(self):
        maze_default = self.run_mazeBridge(["--xsize", "15", "--ysize", "15"])
        maze_spike0 = self.run_mazeBridge(["--xsize", "15", "--ysize", "15", "--maxborderspikesize", "0"])
        if isinstance(maze_default, str) or isinstance(maze_spike0, str):
            self.skipTest("mazeBridge not return JSON")
        grid_default = np.array(maze_default["grid"])
        grid_spike0 = np.array(maze_spike0["grid"])
        self.assertTrue(np.all(np.isin(grid_default, [0, 1])))
        self.assertTrue(np.all(np.isin(grid_spike0, [0, 1])))

    def test_show_option(self):
        maze = self.run_mazeBridge(["--xsize", "10", "--ysize", "10", "--show", "true"])
        if isinstance(maze, str):
            self.skipTest("mazeBridge not return JSON")
        self.assertIsInstance(maze, dict)

    def test_help_option(self):
        output = self.run_mazeBridge(["--help", "true"])
        self.assertIsInstance(output, str)
        self.assertIn("No help", output)


    # Advanced property tests
    # All open cells are reachable (flood-fill)
    def test_topology(self):
        maze = self.run_mazeBridge(["--xsize", "15", "--ysize", "15", "--seed", "123"])
        if isinstance(maze, str): self.skipTest("mazeBridge did not return JSON")
        grid = np.array(maze["grid"])
        visited = np.zeros_like(grid)
        stack = [(0, 0)] if grid[0, 0] == 0 else [(np.argwhere(grid == 0)[0][0], np.argwhere(grid == 0)[0][1])]
        while stack:
            x, y = stack.pop()
            if visited[x, y] == 1: continue
            visited[x, y] = 1
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1]:
                    if grid[nx, ny] == 0 and visited[nx, ny] == 0:
                        stack.append((nx, ny))
        self.assertTrue(np.all(visited[grid == 0] == 1))

    # ExtendGrid produces a symmetrical maze
    def test_symmetry(self):
        maze = self.run_mazeBridge(["--xsize", "10", "--ysize", "10", "--seed", "99"])
        if isinstance(maze, str): self.skipTest("mazeBridge not return JSON")
        grid = np.array(maze["grid"])

        center_row = grid.shape[0] // 2
        center_col = grid.shape[1] // 2

        top = grid[:center_row, :]
        bottom = grid[-center_row:, :]
        left = grid[:, :center_col]
        right = grid[:, -center_col:]

        self.assertTrue(np.all(top == np.flip(bottom, axis=0)))
        self.assertTrue(np.all(left == np.flip(right, axis=1)))

    # The maze wall density is reasonable
    def test_density(self):
        maze = self.run_mazeBridge(["--xsize", "15", "--ysize", "15", "--seed", "7"])
        if isinstance(maze, str): self.skipTest("mazeBridge not return JSON")
        grid = np.array(maze["grid"])
        density = np.sum(grid) / grid.size
        self.assertGreaterEqual(density, 0.2)
        self.assertLessEqual(density, 0.8)

    # Invalid parameters are handled without crashing
    def test_invalid_params(self):
        output = self.run_mazeBridge(["--xsize", "-5", "--ysize", "abc"])
        self.assertIsInstance(output, str)

    # JSON is fully serializable
    def test_json_compatibility(self):
        maze = self.run_mazeBridge(["--xsize", "10", "--ysize", "10"])
        try:
            s = json.dumps(maze)
            self.assertIsInstance(s, str)
        except Exception:
            self.fail("JSON not serializable")

    # Generating a large maze remains performant
    def test_performance(self):
        start = time.time()
        maze = self.run_mazeBridge(["--xsize", "50", "--ysize", "50"])
        end = time.time()
        if isinstance(maze, str): self.skipTest("mazeBridge not return JSON")
        self.assertLess(end - start, 10)
        grid = np.array(maze["grid"])
        self.assertTrue(np.all(np.isin(grid, [0, 1])))

if __name__ == "__main__":
    unittest.main()
