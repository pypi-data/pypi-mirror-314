# File: tests/test_clustering.py
import unittest
import numpy as np
from spinex_clustering import SPINEX_Clustering

class TestSPINEXClustering(unittest.TestCase):
    def setUp(self):
        self.X = np.random.randn(100, 10)
        self.model = SPINEX_Clustering(threshold='auto')

    def test_basic_clustering(self):
        labels = self.model.fit_predict(self.X)
        self.assertEqual(len(labels), len(self.X))
        self.assertTrue(isinstance(labels[0], (int, np.integer)))

    def test_parameter_validation(self):
        with self.assertRaises(ValueError):
            SPINEX_Clustering(threshold='invalid')

if __name__ == '__main__':
    unittest.main()