import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
import mlflow.sklearn

def evaluate_registered_model():
    model_name = "Iris_RandomForest_Model"
    
    # Fetching version 1 from the registry dynamically
    # Alternatively, you can use "models:/Iris_RandomForest_Model/latest" depending on your configuration
    model_uri = f"models:/{model_name}/1"
    
    print(f"Fetching model from registry: {model_uri}")
    
    # Load model directly using MLflow
    model = mlflow.sklearn.load_model(model_uri)
    
    # Load evaluation dataset
    try:
        df_eval = pd.read_csv("eval.csv")
    except FileNotFoundError:
        print("Error: eval.csv not found.")
        return
        
    X_eval = df_eval.iloc[:, :-1]
    y_eval = df_eval.iloc[:, -1]
    
    # Run Inference
    predictions = model.predict(X_eval)
    
    # Print metrics
    accuracy = accuracy_score(y_eval, predictions)
    print("\n--- Evaluation Results ---")
    print(f"Model Accuracy on Test Set: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_eval, predictions))

if __name__ == "__main__":
    evaluate_registered_model()