import json
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

iris = load_iris()
feature_names = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
species_names = ["setosa", "versicolor", "virginica"]

X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target
)

def write_v1(X, y, path):
    with open(path, "w") as f:
        for row, label in zip(X, y):
            input_text = ", ".join(f"{name}: {val}" for name, val in zip(feature_names, row))
            record = {"input_text": input_text, "output_text": species_names[label]}
            f.write(json.dumps(record) + "\n")

def write_v2(X, y, path):
    with open(path, "w") as f:
        for row, label in zip(X, y):
            sl, sw, pl, pw = row
            input_text = (
                f"A flower specimen has a sepal length of {sl} cm, sepal width of {sw} cm, "
                f"petal length of {pl} cm, and petal width of {pw} cm. Identify the iris species."
            )
            output_text = f"This is Iris {species_names[label]}."
            record = {"input_text": input_text, "output_text": output_text}
            f.write(json.dumps(record) + "\n")

write_v1(X_train, y_train, "iris_v1_train.jsonl")
write_v1(X_test, y_test, "iris_v1_test.jsonl")
write_v2(X_train, y_train, "iris_v2_train.jsonl")
write_v2(X_test, y_test, "iris_v2_test.jsonl")

print("Done. Files created:")
for f in ["iris_v1_train.jsonl", "iris_v1_test.jsonl", "iris_v2_train.jsonl", "iris_v2_test.jsonl"]:
    print(" -", f)