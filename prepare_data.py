# prepare_data.py
import pandas as pd
from sklearn.model_selection import train_test_split
from google.cloud import storage
import os

# 1. Load Dataset
from sklearn.datasets import load_iris
iris = load_iris()
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df['target'] = iris.target

# 2. Split Data
train_df, eval_df = train_test_split(df, test_size=0.2, random_state=42)

# Save locally temporarily
train_df.to_csv("train.csv", index=False)
eval_df.to_csv("eval.csv", index=False)

# 3. Upload to GCS
BUCKET_NAME = "mlops-bucket-22f3002843" # <-- Replace this
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

for filename in ["train.csv", "eval.csv"]:
    blob = bucket.blob(f"data/{filename}")
    blob.upload_from_filename(filename)
    print(f"Uploaded {filename} to gs://{BUCKET_NAME}/data/{filename}")
