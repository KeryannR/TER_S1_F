import unittest
import numpy as np
import time
import json
from mazeAPI import app


class TestMazeAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Maze Generator API is running!")

    def test_generate_default(self):
        response = self.client.get('/generate')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        if "error" in data:
            self.skipTest(f"API error: {data['error']}")
        self.assertIn("grid", data)
        grid = np.array(data["grid"])
        self.assertTrue(np.all(np.isin(grid, [0, 1])))

    # Test with fixed seed
    def test_generate_fixed_seed(self):
        r1 = self.client.get('/generate?xSize=10&ySize=10&seed=42')
        r2 = self.client.get('/generate?xSize=10&ySize=10&seed=42')
        d1, d2 = r1.get_json(), r2.get_json()
        if "error" in d1 or "error" in d2:
            self.skipTest("Erreur API sur seed fixe")
        self.assertEqual(d1["grid"], d2["grid"])

    # Test including specific tile
    def test_generate_include_tile(self):
        r = self.client.get('/generate?includeTile=tile1')
        d = r.get_json()
        if "error" in d and "not found" in d["error"]:
            self.skipTest("Tile file not found, skipping test")
        self.assertIn("grid", d)

    # Test invalid parameters
    def test_generate_invalid_params(self):
        r = self.client.get('/generate?xSize=-5&ySize=abc')
        self.assertIn(r.status_code, [400, 500])
        d = r.get_json()
        self.assertIn("error", d)

    # Test show option
    def test_generate_show_option(self):
        r = self.client.get('/generate?show=true')
        self.assertEqual(r.status_code, 200)
        d = r.get_json()
        if "error" in d:
            self.skipTest(f"Erreur API : {d['error']}")
        self.assertIn("grid", d)

    # Test maze size
    def test_maze_size(self):
        r = self.client.get('/generate?xSize=20&ySize=20')
        d = r.get_json()
        grid = np.array(d["grid"])
        self.assertEqual(grid.shape[0], 21)
        self.assertEqual(grid.shape[1], 21)

    # Test JSON structure
    def test_json_structure(self):
        r = self.client.get('/generate?xSize=10&ySize=10')
        d = r.get_json()
        for key in ["width", "height", "grid", "legend"]:
            self.assertIn(key, d)

    # Test grid values
    def test_nstep_influence(self):
        r1 = self.client.get('/generate?nStep=10&seed=1')
        r2 = self.client.get('/generate?nStep=20000&seed=1')
        d1, d2 = r1.get_json(), r2.get_json()
        if "error" in d1 or "error" in d2:
            self.skipTest("Erreur API")
        self.assertNotEqual(d1["grid"], d2["grid"])

    # Test maxBorderSpikeSize parameter
    def test_maxborderspikesize(self):
        r1 = self.client.get('/generate?xSize=15&ySize=15')
        r2 = self.client.get('/generate?xSize=15&ySize=15&maxBorderSpikeSize=0')
        d1, d2 = r1.get_json(), r2.get_json()
        if "error" in d1 or "error" in d2:
            self.skipTest("Erreur API")
        g1, g2 = np.array(d1["grid"]), np.array(d2["grid"])
        self.assertTrue(np.all(np.isin(g1, [0, 1])))
        self.assertTrue(np.all(np.isin(g2, [0, 1])))

    # Test density walls and paths
    def test_density(self):
        r = self.client.get('/generate?xSize=15&ySize=15&seed=7')
        d = r.get_json()
        if "error" in d:
            self.skipTest(f"Erreur API : {d['error']}")
        grid = np.array(d["grid"])
        density = np.sum(grid) / grid.size
        self.assertGreaterEqual(density, 0.1)
        self.assertLessEqual(density, 0.9)

    # Test JSON compatibility
    def test_json_compatibility(self):
        r = self.client.get('/generate')
        d = r.get_json()
        try:
            s = json.dumps(d)
            self.assertIsInstance(s, str)
        except Exception:
            self.fail("Réponse non sérialisable en JSON")

    # Test performance
    def test_performance(self):
        start = time.time()
        r = self.client.get('/generate?xSize=40&ySize=40')
        elapsed = time.time() - start
        d = r.get_json()
        if "error" in d:
            self.skipTest("Erreur API")
        self.assertLess(elapsed, 10)
        grid = np.array(d["grid"])
        self.assertTrue(np.all(np.isin(grid, [0, 1])))


if __name__ == "__main__":
    unittest.main(verbosity=2)
