import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from src.data_preparation import load_datasets, merge_and_process_data

class TestDataPreparation(unittest.TestCase):
    def test_load_datasets(self):
        """
        Test if datasets are loaded successfully.
        """
        red, white = load_datasets()
        self.assertGreater(red.count(), 0, "Red wine dataset is empty")
        self.assertGreater(white.count(), 0, "White wine dataset is empty")

    def test_merge_and_process_data(self):
        """
        Test if datasets are merged and processed correctly.
        """
        red, white = load_datasets()
        combined_data = merge_and_process_data(red, white)
        self.assertIn("wine_type", combined_data.columns, "Column 'wine_type' is missing after processing")
        self.assertGreater(combined_data.count(), 0, "Combined dataset is empty")

if __name__ == "__main__":
    unittest.main()
