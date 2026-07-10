import os
import pandas as pd
import pytest
import joblib

# ==========================================
# TASK 1: DATA VALIDATION TESTS
# ==========================================

def test_data_schema_and_missing_values():
    # Check if data files exist
    assert os.path.exists("train.csv"), "Training data file missing!"
    assert os.path.exists("eval.csv"), "Evaluation data file missing!"
    
    # Load datasets
    train_df = pd.read_csv("train.csv")
    eval_df = pd.read_csv("eval.csv")
    
    # 1. Check for missing values
    assert train_df.isnull().sum().sum() == 0, "Training data contains missing values!"
    assert eval_df.isnull().sum().sum() == 0, "Evaluation data contains missing values!"
    
    # 2. Check for expected columns (Assuming classic Iris dataset columns + target)
    expected_min_columns = 5
    assert len(train_df.columns) >= expected_min_columns, "Train dataframe columns mismatch!"
    assert len(eval_df.columns) >= expected_min_columns, "Evaluation dataframe columns mismatch!"

# ==========================================
# TASK 2: MODEL EVALUATION TESTS
# ==========================================

def test_model_performance():
    # Update this path to where your trained model artifact is saved (e.g., model.joblib)
    model_path = "model.joblib" 
    
    # If the model file hasn't been pulled yet locally, we check your inference output
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        eval_df = pd.read_csv("eval.csv")
        
        # Split features and target (adjust column names/indices based on your week 2 setup)
        X_eval = eval_df.iloc[:, :-1]
        y_eval = eval_df.iloc[:, -1]
        
        # Get predictions and calculate accuracy
        predictions = model.predict(X_eval)
        accuracy = (predictions == y_eval).mean()
        
        # Quality Gate: Ensure accuracy meets a minimum threshold (e.g., 80%)
        assert accuracy >= 0.80, f"Model quality degraded! Accuracy is {accuracy:.2f}"
    else:
        # Fallback sanity check: if running before dvc pull in local environment
        assert os.path.exists("inference.py"), "Inference script missing!"