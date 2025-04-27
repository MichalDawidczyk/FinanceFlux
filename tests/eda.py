import unittest
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from eda import EDA

class TestEDA(unittest.TestCase):
    def setUp(self):
        """Prepare sample data before each test."""
        self.sample_data = pd.DataFrame({
            "Open": [100, 105, 110, 115, 120],
            "High": [102, 108, 112, 118, 123],
            "Low": [98, 102, 108, 112, 118],
            "Close": [101, 107, 111, 117, 121]
        })

    def test_generate_summary_statistics(self):
        """Ensure key metrics are correctly calculated."""
        eda = EDA()
        metrics = eda.generate_summary_statistics(self.sample_data)
        self.assertAlmostEqual(metrics["Mean"]["Open"], 110.00, places=2)
        self.assertAlmostEqual(metrics["Mean"]["Close"], 111.40, places=2)
        self.assertAlmostEqual(metrics["Median"]["Open"], 110.00, places=2)
        self.assertAlmostEqual(metrics["Standard Deviation"]["High"], 8.23, places=2)
        self.assertEqual(metrics["Min"]["Low"], 98)
        self.assertEqual(metrics["Max"]["High"], 123)

        print("Test Passed: generate_summary_statistics")

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestEDA("test_generate_summary_statistics"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
