# train.py
import pandas as pd
import joblib
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from google.cloud import storage

BUCKET_NAME = "mlops-bucket-22f3002843" # <-- Replace this
TIMESTAMP = datetime.now().strftime("%Y%m%dT%H%M%S")
ARTIFACT_PREFIX = f"artifacts/{TIMESTAMP}"

storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

# 1. Download Train Data from GCS
blob = bucket.blob("data/train.csv")
blob.download_to_filename("train_downloaded.csv")
train_df = pd.read_csv("train_downloaded.csv")

X_train = train_df.drop(columns=['target'])
y_train = train_df['target']

# 2. Train Model
print(f"Starting execution run: {TIMESTAMP}")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 3. Save Model Locally then Upload to Timestamped GCS Folder
joblib.dump(model, "model.joblib")
model_blob = bucket.blob(f"{ARTIFACT_PREFIX}/model.joblib")
model_blob.upload_from_filename("model.joblib")

# 4. Write and Upload Execution Logs
log_text = f"Execution Timestamp: {TIMESTAMP}\nModel: RandomForestClassifier\nFeatures: {list(X_train.columns)}"
log_blob = bucket.blob(f"{ARTIFACT_PREFIX}/run_log.txt")
log_blob.upload_from_string(log_text)

print(f"Artifacts successfully saved to gs://{BUCKET_NAME}/{ARTIFACT_PREFIX}/")
# Print the timestamp out so you can copy paste it easily for the inference step
print(f"TIMESTAMP_ID={TIMESTAMP}")