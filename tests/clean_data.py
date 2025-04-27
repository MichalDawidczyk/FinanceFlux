import unittest
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from clean_data import CleanedData

class TestCleanedData(unittest.TestCase):
    def setUp(self):
        """Prepare sample data before each test."""
        self.sample_data = pd.DataFrame({
            "Date": pd.date_range(start="2024-01-01", periods=5, freq="D"),
            "Open": [100, 105, None, 110, "115"],
            "High": [102, 108, 111, None, "118"],
            "Low": [98, 102, "107", 108, None],
            "Close": ["100", "106", 110, "112", 120],
            "Dividends": [0, 0, 0, 0, 0],
            "Stock Splits": [None, None, None, None, None],
            "Volume": [10000, 12000, 11000, 13000, 12500]
        })

    def test_dropped_columns(self):
        """Ensure unnecessary columns are removed."""
        cleaned_data = CleanedData.clean_historical_data(self.sample_data)
        self.assertNotIn("Dividends", cleaned_data.columns)
        self.assertNotIn("Stock Splits", cleaned_data.columns)
        self.assertNotIn("Volume", cleaned_data.columns)
        print("Test Passed: Dropped Columns")

    def test_nan_removal(self):
        """Ensure NaN values are removed from data."""
        cleaned_data = CleanedData.clean_historical_data(self.sample_data)
        self.assertFalse(cleaned_data.isnull().values.any())
        print("Test Passed: NaN Removal")

    def test_numeric_conversion(self):
        """Ensure financial columns are converted to numeric format."""
        cleaned_data = CleanedData.clean_historical_data(self.sample_data)
        for col in ["Open", "High", "Low", "Close"]:
            self.assertTrue(pd.api.types.is_numeric_dtype(cleaned_data[col]))
        print("Test Passed: Numeric Conversion")

    def test_date_formatting(self):
        """Ensure the 'Date' column is correctly formatted."""
        cleaned_data = CleanedData.clean_historical_data(self.sample_data)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(pd.to_datetime(cleaned_data["Date"])))
        print("Test Passed: Date Formatting")

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestCleanedData("test_dropped_columns"))
    suite.addTest(TestCleanedData("test_nan_removal"))
    suite.addTest(TestCleanedData("test_numeric_conversion"))
    suite.addTest(TestCleanedData("test_date_formatting"))
    runner = unittest.TextTestRunner()
    runner.run(suite)