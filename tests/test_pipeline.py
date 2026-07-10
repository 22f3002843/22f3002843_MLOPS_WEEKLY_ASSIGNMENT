import os
import pandas as pd
import joblib
import pytest

# Paths to the artifacts that DVC will pull
DATA_PATH = "eval.csv"
MODEL_PATH = "model.joblib"

# --- TASK 1: DATA VALIDATION TESTS ---

def test_data_existence():
    """Check if the evaluation data file exists."""
    assert os.path.exists(DATA_PATH), f"Evaluation data not found at {DATA_PATH}"

def test_data_schema():
    """Validate data schema, shapes, and missing values."""
    df = pd.read_csv(DATA_PATH)
    
    # 1. Check for missing values
    assert df.isnull().sum().sum() == 0, "Data contains missing values!"
    
    # 2. Check minimum row count
    assert len(df) > 0, "Evaluation dataset is empty!"
    
    # 3. Check expected column count (4 features + 1 target = 5 columns)
    assert df.shape[1] == 5, f"Expected 5 columns, but got {df.shape[1]}"


# --- TASK 2: MODEL EVALUATION TESTS ---

def test_model_existence():
    """Check if the model file exists."""
    assert os.path.exists(MODEL_PATH), f"Model file not found at {MODEL_PATH}"

def test_model_performance():
    """Load the model, run inference, and assert performance metrics."""
    # Load model and data
    model = joblib.load(MODEL_PATH)
    df = pd.read_csv(DATA_PATH)
    
    # Assuming the target column is named 'target' or it's the last column
    X = df.iloc[:, :-1]
    y_true = df.iloc[:, -1]
    
    # Run Inference
    y_pred = model.predict(X)
    
    # Calculate Accuracy
    from sklearn.metrics import accuracy_score
    accuracy = accuracy_score(y_true, y_pred)
    
    print(f"\n[METRIC] Evaluation Accuracy: {accuracy:.4f}")
    
    # Quality Gate Assertion (e.g., must be greater than 80%)
    assert accuracy >= 0.80, f"Model accuracy dropped to {accuracy:.4f}! Quality gate failed."