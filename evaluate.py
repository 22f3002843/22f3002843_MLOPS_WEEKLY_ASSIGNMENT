import json
import vertexai
from vertexai.generative_models import GenerativeModel
from sklearn.metrics import precision_recall_fscore_support, accuracy_score

vertexai.init(project="mlops-501911", location="us-central1")

ENDPOINT_V1 = "projects/588656205385/locations/us-central1/endpoints/145070113924579328"
ENDPOINT_V2 = "projects/588656205385/locations/us-central1/endpoints/8939474286272315392"

VALID_LABELS = {"setosa", "versicolor", "virginica"}

def load_jsonl(path):
    with open(path) as f:
        return [json.loads(line) for line in f]

def extract_label(raw_output):
    text = raw_output.strip().lower()
    for label in VALID_LABELS:
        if label in text:
            return label
    return None  # malformed / non-compliant

def evaluate(endpoint, test_records, version_name):
    model = GenerativeModel(endpoint)
    y_true, y_pred = [], []
    compliant_count = 0

    for rec in test_records:
        true_label = extract_label(rec["output_text"])
        response = model.generate_content(rec["input_text"])
        pred_label = extract_label(response.text)

        if pred_label is not None:
            compliant_count += 1
        y_true.append(true_label)
        y_pred.append(pred_label if pred_label else "INVALID")

    acc = accuracy_score(y_true, y_pred)
    labels = sorted(VALID_LABELS)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, average=None, zero_division=0
    )
    format_compliance = compliant_count / len(test_records)

    print(f"\n=== {version_name} ===")
    print(f"Accuracy: {acc:.3f}")
    print(f"Format compliance: {format_compliance:.3f}")
    for lbl, p, r, f in zip(labels, precision, recall, f1):
        print(f"  {lbl}: precision={p:.3f} recall={r:.3f} f1={f:.3f}")

    return {"accuracy": acc, "format_compliance": format_compliance}

v1_test = load_jsonl("iris_v1_test.jsonl")
v2_test = load_jsonl("iris_v2_test.jsonl")

results_v1 = evaluate(ENDPOINT_V1, v1_test, "v1 - Raw Features")
results_v2 = evaluate(ENDPOINT_V2, v2_test, "v2 - Natural Language")

print("\n=== Comparison ===")
print(f"v1 accuracy: {results_v1['accuracy']:.3f} | v2 accuracy: {results_v2['accuracy']:.3f}")
print(f"v1 format compliance: {results_v1['format_compliance']:.3f} | v2 format compliance: {results_v2['format_compliance']:.3f}")