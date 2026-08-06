import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris

from scipy.stats import ks_2samp

iris = load_iris()

X = pd.DataFrame(
    iris.data,
    columns=iris.feature_names
)

production = X.copy()

production["petal length (cm)"] += 1.5

report = []

for col in X.columns:

    stat, p = ks_2samp(
        X[col],
        production[col]
    )

    line = f"{col}: KS={stat:.3f}, p-value={p:.5f}"

    print(line)

    report.append(line)

plt.figure(figsize=(10,5))

for col in X.columns:

    plt.hist(
        X[col],
        alpha=0.5,
        label=f"Train {col}"
    )

    plt.hist(
        production[col],
        alpha=0.5,
        label=f"Production {col}"
    )

plt.legend()

plt.tight_layout()

plt.savefig(
    "outputs/drift_plot.png"
)

with open(
    "outputs/drift_report.txt",
    "w"
) as f:

    f.write("\n".join(report))

print("Drift report saved.")