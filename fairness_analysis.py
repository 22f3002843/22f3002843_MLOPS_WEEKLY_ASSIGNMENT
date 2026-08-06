import pandas as pd
import numpy as np

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

from fairlearn.metrics import MetricFrame

# ------------------------------------
# Load Dataset
# ------------------------------------

iris = load_iris()

X = pd.DataFrame(
    iris.data,
    columns=iris.feature_names
)

y = iris.target

# ------------------------------------
# Create Sensitive Attribute
# ------------------------------------

np.random.seed(42)

location = np.random.randint(
    0,
    2,
    len(X)
)

X["location"] = location

# ------------------------------------
# Train only on original features
# ------------------------------------

X_train, X_test, y_train, y_test, loc_train, loc_test = train_test_split(
    X.drop(columns=["location"]),
    y,
    location,
    test_size=0.2,
    random_state=42
)

# ------------------------------------
# Train Model
# ------------------------------------

model = RandomForestClassifier(
    random_state=42
)

model.fit(
    X_train,
    y_train
)

pred = model.predict(X_test)

# ------------------------------------
# Fairness Metrics
# ------------------------------------

metrics = {
    "accuracy": accuracy_score,
    "precision": lambda yt, yp: precision_score(
        yt,
        yp,
        average="macro"
    ),
    "recall": lambda yt, yp: recall_score(
        yt,
        yp,
        average="macro"
    )
}

metric_frame = MetricFrame(
    metrics=metrics,
    y_true=y_test,
    y_pred=pred,
    sensitive_features=loc_test
)

print(metric_frame.by_group)

with open(
    "outputs/fairness_metrics.txt",
    "w"
) as f:
    f.write(str(metric_frame.by_group))

print("\nSaved fairness report.")