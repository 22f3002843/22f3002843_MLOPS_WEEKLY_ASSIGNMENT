import shap
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

iris = load_iris()

X = pd.DataFrame(
    iris.data,
    columns=iris.feature_names
)

y = iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    random_state=42
)

model = RandomForestClassifier(
    random_state=42
)

model.fit(
    X_train,
    y_train
)

explainer = shap.TreeExplainer(model)

shap_values = explainer.shap_values(X_train)

for i in range(3):

    plt.figure()

    shap.summary_plot(
        shap_values[:, :, i],
        X_train,
        show=False
    )

    plt.savefig(
        f"outputs/shap_class_{i}.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

print("Saved SHAP plots.")