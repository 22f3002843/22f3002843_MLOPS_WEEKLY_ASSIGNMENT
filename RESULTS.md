# IRIS Fine-Tuning Results: v1 (Raw) vs v2 (Natural Language)

**Generated:** 2026-08-22 19:57 UTC
**Project:** `mlops-501911`
**Base model:** `gemini-2.5-flash`
**Platform:** Vertex AI Supervised Fine-Tuning

## Hyperparameters

| Parameter | Value |
|---|---|
| Epochs | 5 |
| Learning rate multiplier | 1.0 |

Same hyperparameters used for both jobs so data representation is the only variable.

## Tuning Jobs

| Version | Job Resource Name | Endpoint | State |
|---|---|---|---|
| v1 - Raw | `projects/588656205385/locations/us-central1/tuningJobs/4076595636659552256` | `projects/588656205385/locations/us-central1/endpoints/145070113924579328` | JOB_STATE_SUCCEEDED |
| v2 - Natural Language | `projects/588656205385/locations/us-central1/tuningJobs/883543500853870592` | `projects/588656205385/locations/us-central1/endpoints/8939474286272315392` | JOB_STATE_SUCCEEDED |

## Evaluation Results

Test set size: 30 held-out samples per model.

### v1 - Raw Feature Format

- **Accuracy:** 0.567
- **Format compliance:** 1.000

| Class | Precision | Recall | F1 |
|---|---|---|---|
| setosa | 0.455 | 1.000 | 0.625 |
| versicolor | 1.000 | 0.200 | 0.333 |
| virginica | 0.833 | 0.500 | 0.625 |

### v2 - Natural Language Description Format

- **Accuracy:** 0.400
- **Format compliance:** 1.000

| Class | Precision | Recall | F1 |
|---|---|---|---|
| setosa | 0.357 | 1.000 | 0.526 |
| versicolor | 0.000 | 0.000 | 0.000 |
| virginica | 1.000 | 0.200 | 0.333 |

## Comparison

| Metric | v1 - Raw | v2 - Natural Language | Delta (v1 - v2) |
|---|---|---|---|
| Accuracy | 0.567 | 0.400 | +0.167 |
| Format compliance | 1.000 | 1.000 | +0.000 |

**Winner: v1 raw features**

## Interpretation

v1 (raw feature strings) outperformed the other by 16.7 accuracy points. Both achieved identical format compliance, indicating fine-tuning reliably fixes output structure regardless of input representation, but does not guarantee output correctness. With a small (~120-example) training set, the extra linguistic wrapping in v2 appears to add noise rather than signal for this numeric classification task.

This demonstrates a core LLMOps evaluation lesson: format compliance and task
accuracy are independent dimensions. A fine-tuned LLM can be 100% reliable in
*how* it responds while still being wrong about *what* it responds — a failure
mode that traditional classifiers, which either predict a valid class or error
out, do not exhibit in the same way.
