from imblearn.over_sampling import SMOTE
import pandas as pd
from collections import Counter

def apply_smote(data_spark):
    """
    Apply SMOTE to balance the dataset.
    Args:
        data_spark: PySpark DataFrame containing the dataset.

    Returns:
        Pandas DataFrame with balanced classes.
    """
    # Convert PySpark DataFrame to Pandas
    data_pd = data_spark.toPandas()
    
    # Separate features and target
    X = data_pd.drop("quality", axis=1)
    y = data_pd["quality"]
    
    print("Class distribution before SMOTE:", Counter(y))
    
    # Apply SMOTE
    smote = SMOTE(random_state=42, k_neighbors=4)
    X_resampled, y_resampled = smote.fit_resample(X, y)
    
    print("Class distribution after SMOTE:", Counter(y_resampled))
    
    # Return balanced DataFrame
    balanced_data_pd = pd.concat(
        [pd.DataFrame(X_resampled, columns=X.columns), pd.DataFrame(y_resampled, columns=["quality"])],
        axis=1
    )
    return balanced_data_pd
