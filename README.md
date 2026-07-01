# Week 3 - Integrating Feast Feature Store into the IRIS Pipeline


**MLOps Weekly Assignment – Week 3**

---

## 📌 Table of Contents

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [Learning Outcomes](#learning-outcomes)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Assignment Tasks](#assignment-tasks)
- [My Implementation Approach](#my-implementation-approach)
- [Workflow](#workflow)
- [Feast Concepts Used](#feast-concepts-used)
- [Offline vs Online Feature Retrieval](#offline-vs-online-feature-retrieval)
- [How the Pipeline Works](#how-the-pipeline-works)
- [Outputs Generated](#outputs-generated)
- [Results](#results)
- [Conclusion](#conclusion)

---

## 🔍 Project Overview

This assignment focuses on integrating **Feast Feature Store** into the existing IRIS Machine Learning pipeline developed in the previous assignments.

In Week 2, the pipeline used **DVC (Data Version Control)** to version datasets and model artifacts. Although DVC solves dataset and model versioning, it does not solve another important production problem called **training-serving skew**.

To address this issue, Feast is introduced as a centralized Feature Store that provides a single source of truth for all machine learning features.

The objective of this assignment is to modify the existing pipeline so that both training and inference retrieve the same engineered features directly from Feast instead of manually reading feature columns from CSV files.

---

## ⚠️ Problem Statement

Machine Learning models often fail in production because the features used during training differ from those used during inference.

This problem is called **Training-Serving Skew**.

Common reasons include:
* Different preprocessing logic
* Duplicate feature engineering code
* Manual feature transformations
* Data inconsistency

The objective of this assignment is to eliminate this issue by integrating **Feast Feature Store** into the IRIS ML pipeline.

---

## 🎯 Objectives

The objectives of this assignment are:
* Understand the role of Feature Stores in MLOps
* Initialize a Feast Feature Repository
* Define Entities, Data Sources and Feature Views
* Register feature definitions
* Materialize features into the Online Store
* Retrieve historical features for model training
* Retrieve online features for real-time inference
* Demonstrate training-serving consistency

---

## 🧠 Learning Outcomes

After completing this assignment I learned:
* Why Feature Stores are important in production ML systems
* Difference between Offline Store and Online Store
* Difference between DVC and Feast
* How Feast eliminates Training-Serving Skew
* How historical and online feature retrieval works
* How production ML pipelines manage feature engineering

---

## 🛠️ Technology Stack

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Feast](https://img.shields.io/badge/Feast-orange?style=for-the-badge) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) ![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white) ![Parquet](https://img.shields.io/badge/Apache_Parquet-blue?style=for-the-badge) ![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white) ![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)

---

## 📂 Project Structure

```
22f3002843_MLOPS_WEEKLY_ASSIGNMENT
│
├── data
│   ├── train.csv
│   └── eval.csv
│
├── feast_repo
│   │
│   ├── data
│   │   ├── iris_features.parquet
│   │   └── iris_labels.parquet
│   │
│   ├── outputs
│   │   ├── feast_apply_output.txt
│   │   ├── materialize_output.txt
│   │   ├── training_output.txt
│   │   └── inference_output.txt
│   │
│   ├── feature_store.yaml
│   ├── iris_features.py
│   ├── prepare_iris_data.py
│   ├── train_model.py
│   └── predict_online.py
│
├── README.md
└── .gitignore
```

### 📂 File & Folder Explanations

| File / Folder | Short Description | Key Details / Output / API |
| :--- | :--- | :--- |
| **README.md** | Project documentation. | Overview, workflow, structure & results. |
| **.gitignore** | Git configuration. | Prevents committing models, caches, and logs. |
| **data/** | Contains raw datasets (`train.csv`, `eval.csv`). | Input data source for the pipeline. |
| **feast_repo/feature_store.yaml** | Feast store configuration. | SQLite online store provider configuration. |
| **feast_repo/prepare_iris_data.py** | Prepares dataset for Feast by converting to Parquet. | Adds synthetic timestamps and `iris_id`. |
| **feast_repo/iris_features.py** | Feature View & Entity definitions. | Single source of truth for features. |
| **feast_repo/train_model.py** | Model training script. | Historical retrieval with `get_historical_features()`. |
| **feast_repo/predict_online.py** | Online inference script. | Online retrieval with `get_online_features()`. |
| **feast_repo/data/** | Stores offline parquet data. | `iris_features.parquet`, `iris_labels.parquet`. |
| **feast_repo/outputs/** | Execution log files. | Logs for `apply`, `materialize`, `train`, and `predict`. |

---

## 📋 Assignment Tasks

### **Task 1**
Initialize a Feast Feature Repository.
* *Completed by creating:*
  * `feature_store.yaml`
  * local SQLite backend
  * Feast project configuration

### **Task 2**
Define:
* Entity
* Data Source
* Feature View
* *Completed using:* `iris_features.py`

### **Task 3**
Register feature definitions and materialize features.
* *Commands executed:*
  ```bash
  feast apply
  feast materialize START_TIME END_TIME
  ```

### **Task 4**
Retrieve historical features from the Offline Store.
* *Completed using:* `get_historical_features()` inside `train_model.py`

### **Task 5**
Retrieve online features from the Online Store.
* *Completed using:* `get_online_features()` inside `predict_online.py`

---

## 🚀 My Implementation Approach

I completed this assignment in the following sequence.

### **Step 1**
Installed Feast and required Python libraries.
```bash
pip install feast
```

### **Step 2**
Created a local Feast Repository.
* Inside the repository I added:
  * Feature Store configuration
  * Data folder
  * Python scripts

### **Step 3**
Prepared the dataset.
* The original IRIS dataset was converted into Parquet format.
* Additional columns were created:
  * `iris_id`
  * `event_timestamp`
* The synthetic timestamp is required because Feast performs point-in-time feature retrieval.

### **Step 4**
Defined Feature Store components. I created:
* **Entity:** `iris_id` (This uniquely identifies every Iris sample.)
* **Data Source:** A FileSource pointing to `iris_features.parquet`
* **Feature View:** Containing:
  * `sepal_length`
  * `sepal_width`
  * `petal_length`
  * `petal_width`

### **Step 5**
Applied Feature Definitions.
```bash
feast apply
```
This command registers the **Entity**, **Feature View**, and **Data Source** inside the Feast Registry.

### **Step 6**
Materialized Features.
```bash
feast materialize
```
This copied feature values from the Offline Store into the SQLite Online Store.

### **Step 7**
Training.
* Instead of reading feature columns directly from CSV files, the model retrieves historical features from Feast using `get_historical_features()`.
* The retrieved features are then used to train the Logistic Regression classifier.

### **Step 8**
Inference.
* During prediction, feature values are retrieved using `get_online_features()`.
* The retrieved features are then passed to the trained model.
* This ensures both training and inference use identical feature definitions.

---

## 🔄 Workflow

```mermaid
graph LR
    Raw[Raw Dataset] --> Prep[prepare_iris_data.py]
    Prep --> Parquet[Parquet Files]
    Parquet --> Definitions[Entity + Feature View]
    Definitions --> Apply[Feast Apply]
    Apply --> Registry[Registry Created]
    Registry --> Mat[Materialize]
    Mat --> SQLite[SQLite Online Store]
    SQLite --> Hist[Historical Features]
    Hist --> Train[Model Training]
    Train --> Online[Online Features]
    Online --> Predict[Prediction]
```

---

## 🧠 Feast Concepts Used

* **Entity:** Represents the object being described. Example: `iris_id`
* **Data Source:** The source containing feature values. Example: `iris_features.parquet`
* **Feature View:** Logical grouping of related features. Contains `Sepal Length`, `Sepal Width`, `Petal Length`, and `Petal Width`.
* **Offline Store:** Used during training to provide historical feature retrieval.
* **Online Store:** Used during inference to provide low-latency feature retrieval.
* **Materialization:** Copies feature values from Offline Store into Online Store.

---

## 🔄 Offline vs Online Feature Retrieval

### **Offline Retrieval**
* **Usage:** Used during training.
* **API used:** `get_historical_features()`
* **Purpose:** Retrieve historical feature values.

### **Online Retrieval**
* **Usage:** Used during inference.
* **API used:** `get_online_features()`
* **Purpose:** Retrieve latest feature values for prediction.

---

## ⚙️ How the Pipeline Works

### **Training Flow**
```mermaid
graph LR
    CSV[CSV] --> PrepData[Prepare Data]
    PrepData --> ParquetFile[Parquet]
    ParquetFile --> OfflineStore[Feast Offline Store]
    OfflineStore --> HistFeatures[Historical Features]
    HistFeatures --> ModelTrain[Model Training]
```

### **Inference Flow**
```mermaid
graph LR
    SampleID[Sample ID] --> OnlineStore[Feast Online Store]
    OnlineStore --> FeatureRetrieval[Feature Retrieval]
    FeatureRetrieval --> Prediction[Prediction]
```

---

## 💾 Outputs Generated

The following output files demonstrate successful execution:

* 📄 **`feast_apply_output.txt`:** Contains the feature registration logs.
* 📄 **`materialize_output.txt`:** Contains the materialization logs.
* 📄 **`training_output.txt`:** Contains model training output and accuracy.
* 📄 **`inference_output.txt`:** Contains online feature retrieval logs and predictions.

---

## 🏆 Results

Successfully completed:
* [x] Feature Repository Initialization
* [x] Entity Definition
* [x] Data Source Definition
* [x] Feature View Definition
* [x] Feast Apply
* [x] Materialization
* [x] Historical Feature Retrieval
* [x] Online Feature Retrieval
* [x] Model Training
* [x] Real-time Prediction

The pipeline now retrieves identical features for both training and inference, reducing the risk of training-serving skew.

---

## 🏁 Conclusion

This assignment demonstrated how Feast can be integrated into an existing Machine Learning pipeline to provide centralized feature management.

Unlike manually reading feature columns from datasets, Feast allows feature engineering to be defined only once and reused consistently across training and serving environments.

The completed pipeline successfully:
* Uses a Feature Store
* Retrieves historical features during training
* Retrieves online features during inference
* Eliminates duplicate feature engineering logic
* Demonstrates a production-style MLOps workflow

Overall, this assignment provided hands-on experience with Feature Stores and highlighted their importance in building reliable, scalable, and production-ready Machine Learning systems.
