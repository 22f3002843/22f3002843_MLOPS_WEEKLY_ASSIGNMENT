import pandas as pd
from sklearn.datasets import load_iris

# Load IRIS
iris = load_iris(as_frame=True)
df = iris.frame.copy()

# Rename columns to simple names
df = df.rename(columns={
    "sepal length (cm)": "sepal_length",
    "sepal width (cm)": "sepal_width",
    "petal length (cm)": "petal_length",
    "petal width (cm)": "petal_width",
    "target": "species_id",
})

# Human-readable label
df["species"] = df["species_id"].map({i: name for i, name in enumerate(iris.target_names)})

# Unique entity id for Feast
df["iris_id"] = range(1, len(df) + 1)

# Synthetic timestamp for static data
df["event_timestamp"] = pd.Timestamp("2026-07-01 00:00:00")

# Save only the feature columns for Feast
feature_df = df[
    ["iris_id", "event_timestamp", "sepal_length", "sepal_width", "petal_length", "petal_width"]
].copy()

feature_df.to_parquet("data/iris_features.parquet", index=False)

# Save label file for training
train_df = df[["iris_id", "event_timestamp", "species_id", "species"]].copy()
train_df.to_parquet("data/iris_labels.parquet", index=False)

print("Saved:")
print(" - data/iris_features.parquet")
print(" - data/iris_labels.parquet")
