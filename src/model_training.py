from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split

def train_handler(X, y):
    """
    Train a RandomForest model, evaluate it, and return the model and predictions.
    Args:
        X: Features (Pandas DataFrame).
        y: Target variable (Pandas Series).
    Returns:
        model: Trained RandomForest model.
        X_test, y_test, y_pred: Test data, true labels, and predictions.
    """
    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Initialize the model
    model = RandomForestClassifier(class_weight="balanced", random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Print metrics
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    return model, X_test, y_test, y_pred
