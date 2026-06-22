# 🌸 Setting Up the IRIS ML Pipeline on Vertex AI(WEEK 1 ASSIGNMENT)

[![GCP](https://img.shields.io/badge/Google%20Cloud-%234285F4.svg?style=flat-square&logo=google-cloud&logoColor=white)](https://cloud.google.com/)
[![Vertex AI](https://img.shields.io/badge/Vertex%20AI-%234285F4.svg?style=flat-square&logo=google-cloud&logoColor=white)](https://cloud.google.com/vertex-ai)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)

This project implements an end-to-end Machine Learning pipeline for the IRIS classification dataset using Google Cloud Platform (GCP). The pipeline demonstrates data preparation, model training, artifact management, and inference using Google Cloud Storage (GCS) and Vertex AI (agent platform API ) Workbench.

---

## 🎯 Project Overview

The objective is to create a reproducible ML workflow where:
* **Training & evaluation datasets** are stored securely in Google Cloud Storage.
* **Model training** is executed on scalable Google Cloud infrastructure.
* **Model artifacts** are organized and versioned automatically using execution timestamps.
* **Inference** is performed using a separately maintained script.
* **Multiple executions** generate independent artifact folders for full traceability and experimentation.

---

## 🎓 Learning Objectives

* **Understand** Google Cloud Platform services used in modern ML workflows.
* **Leverage** Vertex AI Workbench for collaborative development and execution.
* **Manage** datasets and artifacts within Google Cloud Storage buckets.
* **Build** a reproducible ML training and inference pipeline.
* **Organize** model outputs using timestamp-based versioning for lineage tracking.

---

## 🛠️ Technology Stack

* **Cloud Platform:** Google Cloud Platform (GCP)
* **ML Workspace:** Vertex AI Workbench
* **Object Storage:** Google Cloud Storage (GCS)
* **Runtime Environment:** Python 3
* **Data Manipulation:** Pandas
* **Machine Learning Library:** Scikit-learn (Random Forest Classifier)

---

## ☁️ GCP Resources Used

### Required GCP APIs

| API | Why It Was Needed |
| :--- | :--- |
| **Vertex AI API (Agent platform API)**      | Required to create and use Vertex AI Workbench instances.                                      |
| **Compute Engine API** | Vertex AI Workbench instances run on Compute Engine virtual machines behind the scenes.        |
| **Cloud Storage API**  | Required for creating buckets and uploading/downloading files from GCS using `gcloud storage`. |

### Google Cloud Storage Bucket
```text
gs://mlops-bucket-22f3002843-2026
```

### Bucket Structure
```text
mlops-bucket-22f3002843-2026/
├── data/
│   ├── train.csv
│   └── eval.csv
└── artifacts/
    ├── 20260622_103620/
    │   ├── model.pkl
    │   ├── metrics.json
    │   └── training_log.txt
    └── <future_timestamp_runs>/
```

---

## 📁 Repository Structure

```text
week_1/
├── prepare_data.py
├── train.py
├── inference.py
├── train.csv
├── eval.csv
├── README.md
└── outputs/
    ├── training_output.txt
    └── inference_output.txt
```

---

## 📄 File Descriptions

| File | Type | Purpose | Input | Output |
| :--- | :--- | :--- | :--- | :--- |
| `prepare_data.py` | Python Script | Loads, splits (train/eval), and saves the IRIS dataset. | Built-in IRIS dataset | `train.csv`, `eval.csv` |
| `train.py` | Python Script | Loads training data, trains Random Forest Classifier, generates metrics, creates timestamped folders, and saves outputs. | `train.csv` | `model.pkl`, `metrics.json`, `training_log.txt` |
| `inference.py` | Python Script | Loads trained model and evaluation data to run predictions and calculate accuracy. | Trained model (`model.pkl`), `eval.csv` | Evaluation accuracy |
| `train.csv` | Dataset (CSV) | Contains the training split of the IRIS dataset. | - | - |
| `eval.csv` | Dataset (CSV) | Contains the evaluation split of the IRIS dataset. | - | - |

---

## 🚀 Execution Workflow

### Step 1: Data Preparation
Run the script to download the IRIS dataset and generate the train/eval splits:
```bash
python3 prepare_data.py
```

**Output:**
```text
train.csv
eval.csv
```

---

### Step 2: Upload Dataset to GCS
Copy the generated splits to your GCS data folder:
```bash
gcloud storage cp train.csv gs://mlops-bucket-22f3002843-2026/data/train.csv
gcloud storage cp eval.csv gs://mlops-bucket-22f3002843-2026/data/eval.csv
```

---

### Step 3: Model Training
Train the Random Forest model locally on Vertex AI Workbench:
```bash
python3 train.py
```

**Example Console Output:**
```text
Artifacts saved in:
artifacts/20260622_103620
```

**Generated Artifacts:**
```text
model.pkl
metrics.json
training_log.txt
```

---

### Step 4: Upload Artifacts to GCS
Upload the training outputs to GCS for persistence and tracking:
```bash
gcloud storage cp -r artifacts/* \
gs://mlops-bucket-22f3002843-2026/artifacts/
```

---

### Step 5: Run Inference
Evaluate model accuracy using the evaluation dataset:
```bash
python3 inference.py
```

**Example Output:**
```text
Evaluation Accuracy: 1.0
```

---

### Step 6: Execute Pipeline Multiple Times
The training script can be executed multiple times:
```bash
python3 train.py
```

Each execution generates a unique timestamp-based folder under `artifacts/`:
```text
artifacts/
├── 20260622_103620/
├── 20260622_104215/
└── 20260622_110010/
```
This design ensures reliable model versioning and experiment traceability.

---

## 📊 Sample Results

| Metric | Accuracy Score |
| :--- | :--- |
| **Training Accuracy** | `1.0` |
| **Evaluation Accuracy** | `1.0` |

> ℹ️ **Note:** Results may vary slightly across executions.

---

## 🖥️ Vertex AI Workbench

Development and execution were performed using:
* **Environment:** Vertex AI Workbench
* **Region:** `asia-south1`

**Workbench Capabilities Utilized:**
* Data preparation and preprocessing
* Model training execution
* Inference and evaluation execution
* Seamless integration and data transfer with Google Cloud Storage

---

## 🏁 Conclusion

This project successfully demonstrates an end-to-end Machine Learning workflow on Google Cloud Platform utilizing Vertex AI Workbench and Google Cloud Storage. The pipeline supports reproducible training, dynamic artifact versioning through timestamped folders, and decoupled inference execution, establishing a robust foundation for production-ready MLOps.
