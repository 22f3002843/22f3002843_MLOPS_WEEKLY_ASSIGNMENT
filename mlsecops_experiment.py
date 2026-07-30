import numpy as np
import pandas as pd
import mlflow
import mlflow.sklearn

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def get_clean_iris_data():
    """Load clean Iris dataset and convert to DataFrame."""
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = pd.Series(iris.target, name='target')
    return X, y, iris.feature_names

def poison_dataset(X, y, corruption_percentage, seed=42):
    """
    Replaces corruption_percentage of samples with:
    - Random feature values within the min/max range of features.
    - Random class labels (0, 1, or 2).
    """
    if corruption_percentage == 0:
        return X.copy(), y.copy()

    np.random.seed(seed)
    X_poisoned = X.copy()
    y_poisoned = y.copy()

    n_samples = len(X)
    n_poison = int(n_samples * (corruption_percentage / 100.0))

    # Randomly pick indices to poison
    poison_indices = np.random.choice(n_samples, size=n_poison, replace=False)

    # Get min and max ranges across features to generate realistic noise
    min_vals = X.min().values
    max_vals = X.max().values

    for idx in poison_indices:
        # Generate random feature values for each column
        random_features = np.random.uniform(low=min_vals, high=max_vals, size=X.shape[1])
        X_poisoned.iloc[idx] = random_features
        # Assign random label (0, 1, or 2)
        y_poisoned.iloc[idx] = np.random.choice([0, 1, 2])

    return X_poisoned, y_poisoned

def run_mlsecops_pipeline():
    # Set MLflow Experiment name
    mlflow.set_experiment("MLSecOps_Iris_Poisoning_Analysis")

    # Load clean data
    X_clean, y_clean, feature_names = get_clean_iris_data()

    # Poisoning levels required by assignment
    corruption_levels = [0, 5, 10, 50]

    for level in corruption_levels:
        print(f"\n==========================================")
        print(f" Running Experiment for {level}% Poisoning Level")
        print(f"==========================================")

        # 1. Generate poisoned dataset
        X_curr, y_curr = poison_dataset(X_clean, y_clean, corruption_percentage=level)

        # Save corrupted dataset copy locally
        dataset_filename = f"iris_poisoned_{level}pct.csv"
        df_to_save = X_curr.copy()
        df_to_save['target'] = y_curr
        df_to_save.to_csv(dataset_filename, index=False)
        print(f"Saved dataset variant: {dataset_filename}")

        # 2. Split into Train/Test sets
        X_train, X_test, y_train, y_test = train_test_split(
            X_curr, y_curr, test_size=0.3, random_state=42, stratify=y_curr
        )

        # 3. MLflow Tracking
        with mlflow.start_run(run_name=f"Poisoning_Level_{level}pct"):
            # Model Definition
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)

            # Predictions
            y_pred = model.predict(X_test)

            # Calculate required metrics (using weighted average for multi-class)
            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, average='weighted')
            rec = recall_score(y_test, y_pred, average='weighted')
            f1 = f1_score(y_test, y_pred, average='weighted')

            print(f"Metrics -> Acc: {acc:.4f} | Prec: {prec:.4f} | Rec: {rec:.4f} | F1: {f1:.4f}")

            # Log Params
            mlflow.log_param("poisoning_percentage", level)
            mlflow.log_param("clean_data_ratio", (100 - level) / 100.0)
            mlflow.log_param("model_type", "RandomForestClassifier")

            # Log Metrics
            mlflow.log_metric("accuracy", acc)
            mlflow.log_metric("precision", prec)
            mlflow.log_metric("recall", rec)
            mlflow.log_metric("f1_score", f1)

            # Log the dataset artifact
            mlflow.log_artifact(dataset_filename)

            # Log the trained model
            mlflow.sklearn.log_model(model, artifact_path="model")

            print(f"MLflow Run completed successfully for {level}% corruption!")

if __name__ == "__main__":
    run_mlsecops_pipeline()