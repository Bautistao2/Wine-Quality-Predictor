import unittest
from src.feature_importance import plot_feature_importance
from src.model_training import train_model
from src.smote_balancing import apply_smote
from src.data_preparation import load_datasets, merge_and_process_data

class TestFeatureImportance(unittest.TestCase):
    def test_plot_feature_importance(self):
        """
        Test if feature importance can be plotted without errors.
        """
        red, white = load_datasets()
        combined_data = merge_and_process_data(red, white)
        balanced_data = apply_smote(combined_data)

        X = balanced_data.drop("quality", axis=1)
        y = balanced_data["quality"]

        # Train the model
        model = train_model(X, y)

        try:
            plot_feature_importance(model, X.columns)
        except Exception as e:
            self.fail(f"Feature importance plot failed with error: {e}")

if __name__ == "__main__":
    unittest.main()
