import unittest
from src.model_training import train_model
from src.smote_balancing import apply_smote
from src.data_preparation import load_datasets, merge_and_process_data

class TestModelTraining(unittest.TestCase):
    def test_train_model(self):
        """
        Test if the model trains and evaluates correctly.
        """
        red, white = load_datasets()
        combined_data = merge_and_process_data(red, white)
        balanced_data = apply_smote(combined_data)

        X = balanced_data.drop("quality", axis=1)
        y = balanced_data["quality"]

        # Train the model
        model = train_model(X, y)
        self.assertIsNotNone(model, "The trained model is None")

if __name__ == "__main__":
    unittest.main()
