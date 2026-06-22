import pickle
import pandas as pd
from sklearn.metrics import accuracy_score

latest_model = "model.pkl"

with open(latest_model, "rb") as f:
    model = pickle.load(f)

eval_df = pd.read_csv("eval.csv")

X = eval_df.drop("target", axis=1)
y = eval_df["target"]

pred = model.predict(X)

acc = accuracy_score(y, pred)

print("Evaluation Accuracy:", acc)
