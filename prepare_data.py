from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pandas as pd

iris = load_iris()

df = pd.DataFrame(
    iris.data,
    columns=iris.feature_names
)

df["target"] = iris.target

train_df, eval_df = train_test_split(
    df,
    test_size=0.2,
    random_state=42,
    stratify=df["target"]
)

train_df.to_csv("train.csv", index=False)
eval_df.to_csv("eval.csv", index=False)

print("Train:", train_df.shape)
print("Eval:", eval_df.shape)