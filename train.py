import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature

def train_and_log_model():
    # 1. Load your dataset (assuming train.csv is in your root directory)
    # If your data is structured with features and a 'target' column, adapt accordingly.
    try:
        df = pd.read_csv("train.csv")
    except FileNotFoundError:
        print("Error: train.csv not found. Please ensure your data path is correct.")
        return

    # Splitting features and targets (Assuming the last column is the label)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # 2. Set the MLflow Experiment Name
    mlflow.set_experiment("Iris_Classification_Experiment")

    # Define hyperparameter combinations to try (Task 1: Vary at least 2 hyperparameters)
    hyperparameter_grid = [
        {"n_estimators": 10, "max_depth": 3},
        {"n_estimators": 50, "max_depth": 5},
        {"n_estimators": 100, "max_depth": 7}
    ]

    # Model Registry Configuration Name
    model_registry_name = "Iris_RandomForest_Model"

    for idx, params in enumerate(hyperparameter_grid):
        # Start a unique MLflow run for each configuration
        run_name = f"rf_run_config_{idx}"
        with mlflow.start_run(run_name=run_name):
            print(f"Starting Run: {run_name} with params {params}")
            
            # Initialize model with current hyperparameters
            model = RandomForestClassifier(
                n_estimators=params["n_estimators"], 
                max_depth=params["max_depth"], 
                random_state=42
            )
            
            # Train the model
            model.fit(X_train, y_train)
            
            # Predict & Evaluate
            predictions = model.predict(X_val)
            accuracy = accuracy_score(y_val, predictions)
            precision = precision_score(y_val, predictions, average='macro', zero_division=0)
            recall = recall_score(y_val, predictions, average='macro', zero_division=0)

            # 3. Log Parameters to MLflow (Task 2)
            mlflow.log_params(params)

            # 4. Log Evaluation Metrics to MLflow (Task 2)
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("recall", recall)

            # Infer input/output signature for the model registry validation
            signature = infer_signature(X_train, predictions)

            # 5. Log the Model and Register it directly (Task 2 & 4)
            # The registered_model_name argument automatically creates/adds to the Model Registry
            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="iris_model_artifact",
                signature=signature,
                registered_model_name=model_registry_name
            )
            
            print(f"Run {run_name} complete. Accuracy: {accuracy:.4f}")

if __name__ == "__main__":
    train_and_log_model()