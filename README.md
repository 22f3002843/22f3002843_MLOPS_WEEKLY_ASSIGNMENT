# 📊 Integrating DVC into the IRIS Pipeline

[![DVC](https://img.shields.io/badge/Data%20Version%20Control-DVC-gradient.svg?style=flat-square&logo=dvc&logoColor=white)](https://dvc.org/)
[![Google Cloud Storage](https://img.shields.io/badge/GCP-Storage-blue.svg?style=flat-square&logo=google-cloud&logoColor=white)](https://cloud.google.com/storage)
[![Git](https://img.shields.io/badge/Version%20Control-Git-orange.svg?style=flat-square&logo=git&logoColor=white)](https://git-scm.com/)
[![MLOps](https://img.shields.io/badge/MLOps-Pipeline-green.svg?style=flat-square)](https://en.wikipedia.org/wiki/MLOps)

An end-to-end, reproducible machine learning workflow for the IRIS classification pipeline. This project integrates **Data Version Control (DVC)** with a **Google Cloud Storage (GCS)** remote backend to decouple codebase versioning from large data and model artifacts.

---

## 🗺️ System Architecture & Workflow

In standard Git repositories, versioning datasets (`.csv`) and model binaries (`.joblib`) leads to severe repository bloat and performance degradation. This architecture separates concerns by tracking codebase versions in Git and offloading heavy assets to Google Cloud Storage (GCS), linked via lightweight metadata pointer files (`.dvc`).

```
  ┌─────────────────────────────────────────────────────────────┐
  │                    Developer Workspace                      │
  │                                                             │
  │  ┌──────────────────────┐        ┌───────────────────────┐  │
  │  │   Code & Metadata    │        │  Data & Model Assets  │  │
  │  │  (Python scripts,     │        │  (train.csv, eval.csv │  │
  │  │   .dvc pointers)     │        │   model.joblib, etc)  │  │
  │  └──────────┬───────────┘        └───────────┬───────────┘  │
  └─────────────┼────────────────────────────────┼──────────────┘
                │ git push                       │ dvc push
                ▼                                ▼
  ┌─────────────────────────┐        ┌──────────────────────────┐
  │         GitHub          │        │   Google Cloud Storage   │
  │  (week_2 Branch Repo)   │        │     (GCS Remote Bucket)  │
  └─────────────────────────┘        └──────────────────────────┘
```

---

## 🛠️ Step-by-Step Task Breakdown

### 📍 Task 1: Initialize DVC
DVC was initialized directly inside the local assignment repository to create the core tracking directory architecture and configuration files.

1. **Verify workspace and checkout active branch:**
   ```bash
   cd ~/22f3002843_MLOPS_WEEKLY_ASSIGNMENT
   git branch
   ```
2. **Initialize DVC inside the repository root:**
   ```bash
   dvc init
   ```
3. **Commit the internal DVC configuration files to Git tracking:**
   ```bash
   git add .dvc/ .dvcignore
   git commit -m "Initialize DVC"
   ```

> ℹ️ **Note:** The `.dvc/` directory contains local settings and cache configurations, while `.dvcignore` specifies which files DVC should ignore, similar to Git's `.gitignore`.

---

### 📍 Task 2: Configure Google Cloud Storage as DVC Remote
To prevent bloating the Git commit database with binaries, a GCS bucket is linked as the remote centralized asset store.

1. **Add GCS bucket as default DVC remote under the alias `myremote`:**
   ```bash
   dvc remote add -d myremote gs://mlops-bucket-22f3002843/dvc_remote
   ```
2. **Commit configuration updates to Git tracking:**
   ```bash
   git add .dvc/config
   git commit -m "Configure GCS bucket as DVC remote"
   ```

> ⚠️ **Important:** The configuration in `.dvc/config` points to `gs://mlops-bucket-22f3002843/dvc_remote`, ensuring any team member with access can fetch the corresponding dataset versions seamlessly.

---

### 📍 Task 3: Version Data & Models Across Iterations
Data and models were tracked across multiple developmental iterations to ensure complete experiment reproducibility and history log coverage.

#### 🔄 Pipeline Iteration Matrix

| Iteration | Description | Associated Git Commit Message | Action Command |
| :--- | :--- | :--- | :--- |
| **Iteration 1** | Baseline IRIS Classification Pipeline | `Track Iteration 1 data and model artifacts using DVC` | `dvc push` |
| **Iteration 2** | Modified Pipeline via Data Augmentation | `Track Iteration 2 data and model artifacts after data augmentation` | `dvc push` |

#### 📂 Iteration 1: Baseline Pipeline
1. Place pipeline components (`prepare_data.py`, `train.py`, `inference.py`), data splits (`train.csv`, `eval.csv`), and model outputs (`model.joblib`, `model_eval.joblib`) into the workspace.
2. Track data splits and model binaries with DVC:
   ```bash
   dvc add train.csv eval.csv model.joblib model_eval.joblib
   ```
3. Staged the pointer files (`.dvc`) and the updated `.gitignore` into Git:
   ```bash
   git add train.csv.dvc eval.csv.dvc model.joblib.dvc model_eval.joblib.dvc .gitignore
   git commit -m "Track Iteration 1 data and model artifacts using DVC"
   ```
4. Push actual binaries to the remote GCS backend:
   ```bash
   dvc push
   ```

#### 📂 Iteration 2: Data Augmentation
1. Simulate pipeline update by augmenting `train.csv` and re-running the training script to generate new `.joblib` model weights.
2. Instruct DVC to capture the modified states:
   ```bash
   dvc add train.csv eval.csv model.joblib model_eval.joblib
   ```
3. Stage and commit updated pointer files to Git history:
   ```bash
   git add train.csv.dvc eval.csv.dvc model.joblib.dvc model_eval.joblib.dvc
   git commit -m "Track Iteration 2 data and model artifacts after data augmentation"
   ```
4. Upload new iteration assets to the GCS remote storage:
   ```bash
   dvc push
   ```

---

### 📍 Task 4: Switch Between Data/Model Versions
We can seamlessly traverse the history timeline using Git checks combined with DVC checkouts to verify reproducibility.

#### Rollback to Iteration 1 (Baseline State)
1. **View the git commit logs to isolate the Iteration 1 target state:**
   ```bash
   git log --oneline
   ```
2. **Checkout the commit hash corresponding to Iteration 1:**
   ```bash
   git checkout <commit-hash-of-iteration-1>
   ```
3. **Synchronize local working directory files with the pointer state:**
   ```bash
   dvc checkout
   ```
   *At this stage, DVC replaces the local dataset files (`train.csv`, `eval.csv`) and model files (`model.joblib`, `model_eval.joblib`) with their original Iteration 1 versions.*

#### Return to Iteration 2 (Latest Augmented State)
1. **Switch back to the main development branch:**
   ```bash
   git checkout week_2
   ```
2. **Synchronize assets back to the updated version:**
   ```bash
   dvc checkout
   ```

---

### 📍 Task 5: Push Code and Configurations
To ensure a fully reproducible workflow for a reviewer, all runtime scripts and configuration changes are synchronized to the upstream tracking repository.

1. **Stage pipeline code execution scripts alongside the documentation:**
   ```bash
   git add prepare_data.py train.py inference.py README.md
   git commit -m "Add core pipeline execution scripts and documentation"
   ```
2. **Push final branch state to upstream Git repository:**
   ```bash
   git push origin week_2
   ```

---

## 📂 Repository File Structure

A view of the files tracked in the branch `week_2` repository:

```text
├── .dvc/                   # DVC configuration directory
│   └── config              # Config defining default GCS remote
├── .dvcignore              # DVC ignore rules
├── .gitignore              # Git ignore (ignores data/model binaries)
├── README.md               # Pipeline documentation
├── eval.csv.dvc            # Pointer file for evaluation dataset
├── train.csv.dvc           # Pointer file for training dataset
├── model.joblib.dvc        # Pointer file for trained model binary
├── model_eval.joblib.dvc   # Pointer file for evaluation model binary
├── prepare_data.py         # Script to fetch, clean, and split dataset
├── train.py                # Script to fit model to training data
└── inference.py            # Script to run predictions and evaluate metrics
```

---

## 🚀 Quick Start: Reproducing the Pipeline

To set up this workspace on a clean system and replicate any exact iteration:

1. **Clone this repository and navigate inside:**
   ```bash
   git clone <your-repository-url>
   cd 22f3002843_MLOPS_WEEKLY_ASSIGNMENT
   git checkout week_2
   ```
2. **Pull data and model binaries from the GCS remote backend:**
   ```bash
   dvc pull
   ```
3. **Run pipeline stages manually:**
   ```bash
   python prepare_data.py
   python train.py
   python inference.py
   ```
4. **Switch to Iteration 1 to test baseline predictions:**
   ```bash
   git checkout <commit-hash-of-iteration-1>
   dvc checkout
   python inference.py
   ```

---

> 💡 **Tip:** Ensure you have Google Cloud SDK authenticated on your system (`gcloud auth application-default login`) to let DVC pull/push files from the cloud GCS bucket remote backend.
