import joblib
import pandas as pd
from feast import FeatureStore

store = FeatureStore(repo_path=".")
model = joblib.load("iris_model.pkl")

feature_refs = [
    "iris_features:sepal_length",
    "iris_features:sepal_width",
    "iris_features:petal_length",
    "iris_features:petal_width",
]

entity_rows = [{"iris_id": 1}, {"iris_id": 2}, {"iris_id": 3}]

online = store.get_online_features(
    features=feature_refs,
    entity_rows=entity_rows,
).to_dict()

print(online)

online_df = pd.DataFrame(online)
X_live = online_df[[
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
]]

preds = model.predict(X_live)
print("Predictions:", preds)