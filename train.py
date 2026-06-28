from datetime import datetime
import pandas as pd
import pickle
import json
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

train_df = pd.read_csv("train.csv")

X = train_df.drop("target", axis=1)
y = train_df["target"]

model = RandomForestClassifier(
    random_state=42
)

model.fit(X, y)

pred = model.predict(X)

accuracy = accuracy_score(y, pred)

artifact_dir = f"artifacts/{timestamp}"

os.makedirs(
    artifact_dir,
    exist_ok=True
)

with open(
    f"{artifact_dir}/model.pkl",
    "wb"
) as f:
    pickle.dump(model, f)

with open(
    f"{artifact_dir}/metrics.json",
    "w"
) as f:
    json.dump(
        {"accuracy": float(accuracy)},
        f
    )

with open(
    f"{artifact_dir}/training_log.txt",
    "w"
) as f:
    f.write(
        f"Training Accuracy: {accuracy}"
    )

print("Artifacts saved in:")
print(artifact_dir)
