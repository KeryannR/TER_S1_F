import unittest
import numpy as np
from mazeAPI import app

class TestBasicMaze(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_maze_size(self):
        response = self.client.get('/generate?xSize=10&ySize=10')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("grid", data)
        grid = np.array(data["grid"])
        self.assertEqual(grid.shape, (11, 11))

    def test_get_maze_by_id(self):
        test_id = "690d1d58b9055ebd0f144bb6"
        response = self.client.get(f'/get?id={test_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        for key in ["_id", "grid", "height", "width", "legend", "options"]:
            self.assertIn(key, data)

        self.assertEqual(data["_id"], test_id)

        grid = np.array(data["grid"])
        self.assertEqual(grid.shape, (15, 15))

        self.assertTrue(np.all(np.isin(grid, [0, 1])))

    def test_maze_size_odd(self):
        xSize, ySize = 14, 14
        response = self.client.get(f'/generate?xSize={xSize}&ySize={ySize}')
        data = response.get_json()
        grid = np.array(data["grid"])
        self.assertEqual(grid.shape[0] % 2, 1)
        self.assertEqual(grid.shape[1] % 2, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
