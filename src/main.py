from src.data_preparation import load_datasets, merge_and_process_data
from src.smote_balancing import apply_smote
from src.model_training import train_handler
import pickle
import os

def main():
    # Step 1: Load and process datasets
    print("Loading and processing datasets...")
    red, white = load_datasets()
    data = merge_and_process_data(red, white)

    # Step 2: Balance the dataset using SMOTE
    print("Balancing dataset with SMOTE...")
    balanced_data = apply_smote(data)

    # Step 3: Split features and labels
    X = balanced_data.drop("quality", axis=1)
    y = balanced_data["quality"]

    # Step 4: Train and evaluate the model
    print("Training the model...")
    model, X_test, y_test, y_pred = train_handler(X, y)
    
    # Save the model
    model_path = os.path.join("Models", "wine_quality_model.pkl")
    os.makedirs("Models", exist_ok=True)  # Ensure the folder exists
    try:
        print(f"Attempting to save the model to {model_path}")  # Depuración
        with open(model_path, "wb") as f:
            pickle.dump(model, f)
        print(f"Model saved successfully to {model_path}")  # Depuración
    except Exception as e:
        print(f"Error while saving the model: {e}")


if __name__ == "__main__":
    main()
