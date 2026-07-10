# inference.py
import sys
import pandas as pd
import joblib
from google.cloud import storage
from sklearn.metrics import accuracy_score

if len(sys.argv) < 2:
    print("Error: Please provide the execution timestamp. Example: python inference.py 20260709T230000")
    sys.exit(1)

TIMESTAMP = sys.argv[1]
BUCKET_NAME = "mlops-bucket-22f3002843" # <-- Replace this

storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

# 1. Download Evaluation Data
bucket.blob("data/eval.csv").download_to_filename("eval_downloaded.csv")
eval_df = pd.read_csv("eval_downloaded.csv")
X_eval = eval_df.drop(columns=['target'])
y_eval = eval_df['target']

# 2. Download Specific Model Artifact from GCS
model_path = f"artifacts/{TIMESTAMP}/model.joblib"
blob = bucket.blob(model_path)
blob.download_to_filename("model_eval.joblib")
model = joblib.load("model_eval.joblib")

# 3. Run Inference
predictions = model.predict(X_eval)
accuracy = accuracy_score(y_eval, predictions)

print(f"--- Inference Results for Run: {TIMESTAMP} ---")
print(f"Evaluation Accuracy: {accuracy * 100:.2f}%")
