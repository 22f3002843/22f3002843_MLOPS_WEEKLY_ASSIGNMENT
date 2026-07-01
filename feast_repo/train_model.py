import pandas as pd
from feast import FeatureStore
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import joblib

store = FeatureStore(repo_path=".")

labels = pd.read_parquet("data/iris_labels.parquet")

entity_df = labels[["iris_id", "event_timestamp", "species_id"]].copy()

feature_refs = [
    "iris_features:sepal_length",
    "iris_features:sepal_width",
    "iris_features:petal_length",
    "iris_features:petal_width",
]

training_df = store.get_historical_features(
    entity_df=entity_df,
    features=feature_refs,
).to_df()

print(training_df.head())

X = training_df[[
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
]]
y = training_df["species_id"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = LogisticRegression(max_iter=500)
model.fit(X_train, y_train)

preds = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, preds))

joblib.dump(model, "iris_model.pkl")
print("Saved iris_model.pkl")