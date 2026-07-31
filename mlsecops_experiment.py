import pandas as pd
import mlflow

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

datasets = {
    0: "data/iris_clean.csv",
    5: "data/iris_poisoned_5.csv",
    10: "data/iris_poisoned_10.csv",
    50: "data/iris_poisoned_50.csv"
}

mlflow.set_experiment("Week_8_MLSecOps_IRIS")

for poison_level, file_path in datasets.items():

    print("=" * 50)
    print(f"Training with {poison_level}% poisoned dataset")
    print("=" * 50)

    df = pd.read_csv(file_path)

    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = DecisionTreeClassifier(random_state=42)

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    precision = precision_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    with mlflow.start_run(run_name=f"{poison_level}_percent_poison"):

        mlflow.log_param(
            "poisoning_level",
            f"{poison_level}%"
        )

        mlflow.log_metric(
            "accuracy",
            accuracy
        )

        mlflow.log_metric(
            "precision",
            precision
        )

        mlflow.log_metric(
            "recall",
            recall
        )

        mlflow.log_metric(
            "f1_score",
            f1
        )

        mlflow.sklearn.log_model(
            model,
            "decision_tree_model"
        )

    print(f"Accuracy  : {accuracy:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1 Score  : {f1:.4f}")

print("\nAll MLflow runs completed successfully.")