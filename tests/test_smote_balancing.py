import unittest
from src.smote_balancing import apply_smote
from src.data_preparation import load_datasets, merge_and_process_data

class TestSmoteBalancing(unittest.TestCase):
    def test_apply_smote(self):
        """
        Test if SMOTE balances the dataset correctly.
        """
        red, white = load_datasets()
        combined_data = merge_and_process_data(red, white)
        balanced_data = apply_smote(combined_data)

        self.assertIn("quality", balanced_data.columns, "Target column 'quality' is missing after SMOTE")
        self.assertGreater(len(balanced_data), 0, "Balanced dataset is empty")

if __name__ == "__main__":
    unittest.main()
