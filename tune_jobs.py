import vertexai
from vertexai.preview.tuning import sft
import os

PROJECT_ID = os.environ["PROJECT_ID"]
BUCKET = os.environ["BUCKET"]
LOCATION = "us-central1"
TUNE_MODEL = "gemini-2.5-flash"  # cost-efficient, supports supervised tuning  

vertexai.init(project=PROJECT_ID, location=LOCATION)

# Job 1: v1 (raw features)
job_v1 = sft.train(
    source_model=TUNE_MODEL,
    train_dataset=f"gs://{BUCKET}/v1/iris_v1_train_tuning.jsonl",
    epochs=5,
    learning_rate_multiplier=1.0,
    tuned_model_display_name="iris-v1-raw",
)

job_v2 = sft.train(
    source_model=TUNE_MODEL,
    train_dataset=f"gs://{BUCKET}/v2/iris_v2_train_tuning.jsonl",
    epochs=5,
    learning_rate_multiplier=1.0,
    tuned_model_display_name="iris-v2-description",
)
print("v2 job:", job_v2.resource_name)