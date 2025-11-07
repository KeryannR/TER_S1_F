import unittest
import numpy as np
from mazeAPI import app

class TestSimpleCICD(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_maze_size(self):
        response = self.client.get('/generate?xSize=10&ySize=10')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("grid", data)
        grid = np.array(data["grid"])
        self.assertEqual(grid.shape, (11, 11))

if __name__ == "__main__":
    unittest.main(verbosity=2)
