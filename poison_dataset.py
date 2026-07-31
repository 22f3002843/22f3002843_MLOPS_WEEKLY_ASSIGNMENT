import os
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris

# Make results reproducible
np.random.seed(42)

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Load original IRIS dataset
iris = load_iris()

X = iris.data
y = iris.target

feature_names = iris.feature_names

# Create clean dataframe
clean_df = pd.DataFrame(X, columns=feature_names)
clean_df["target"] = y

# Save clean dataset
clean_df.to_csv("data/iris_clean.csv", index=False)

print("Saved: iris_clean.csv")


def poison_dataset(df, corruption_percent):
    poisoned = df.copy()

    total_rows = len(poisoned)

    poison_count = int(total_rows * corruption_percent / 100)

    poison_indices = np.random.choice(
        total_rows,
        poison_count,
        replace=False
    )

    random_features = np.random.uniform(
        low=X.min(),
        high=X.max(),
        size=(poison_count, 4)
    )

    random_labels = np.random.randint(
        0,
        3,
        size=poison_count
    )

    poisoned.loc[
        poison_indices,
        feature_names
    ] = random_features

    poisoned.loc[
        poison_indices,
        "target"
    ] = random_labels

    return poisoned


for level in [5, 10, 50]:

    poisoned_df = poison_dataset(clean_df, level)

    filename = f"data/iris_poisoned_{level}.csv"

    poisoned_df.to_csv(filename, index=False)

    print(f"Saved: {filename}")

print("\nAll poisoned datasets created successfully.")