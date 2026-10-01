An end-to-end machine learning platform for bank account/application fraud detection, risk scoring, model explainability, real-time application scoring, and analyst investigation.

---

## Overview

Fraud detection is a highly imbalanced classification problem where fraudulent applications represent a small fraction of total applications.

This project develops an end-to-end fraud detection system using the **Bank Account Fraud (BAF)** dataset.

The system covers:

```text
Data
  ↓
Exploratory Data Analysis
  ↓
Preprocessing & Feature Engineering
  ↓
XGBoost Fraud Classifier
  ↓
Probability Calibration
  ↓
Temporal Evaluation
  ↓
Threshold Optimization
  ↓
SHAP Explainability
  ↓
FastAPI Scoring API
  ↓
Streamlit Analyst Dashboard
````

---

# 1. Problem Statement

The objective is to build a fraud detection system that can:

* Handle highly imbalanced fraud data
* Generate fraud probabilities
* Select an operational classification threshold
* Evaluate performance on future time periods
* Explain individual predictions
* Provide application-level real-time scoring through an API
* Provide an analyst interface for investigation

The BAF dataset contains approximately **1,000,000 applications** with an overall fraud rate of **1.1029%**.

This means that fraud detection must be evaluated using metrics that are appropriate for severe class imbalance rather than relying primarily on accuracy.

---

# 2. Dataset & Class Imbalance

### Dataset

| Property           |        Value |
| ------------------ | -----------: |
| Total applications |    1,000,000 |
| Fraud rate         |      1.1029% |
| Legitimate rate    |     98.8971% |
| Target variable    | `fraud_bool` |

The strong class imbalance makes **Precision-Recall AUC (PR-AUC)** particularly important for evaluating fraud detection performance.

---

# 3. Exploratory Data Analysis

The dataset was analyzed for:

* Class imbalance
* Numerical feature distributions
* Categorical variables
* Sentinel values
* Fraud rates across categorical variables
* Feature behavior
* Missing-value patterns

Several variables use `-1` as a sentinel value indicating that information is unavailable.

Examples include:

```text
prev_address_months_count
current_address_months_count
bank_months_count
device_distinct_emails_8w
```

Other variables legitimately contain negative values and were therefore not blindly converted into missing values.

---

# 4. Preprocessing & Feature Engineering

The data was split using a stratified:

```text
70% Training
15% Validation
15% Test
```

Dataset sizes:

| Split      |    Rows |
| ---------- | ------: |
| Training   | 700,000 |
| Validation | 150,000 |
| Test       | 150,000 |

### Preprocessing steps

* Train/validation/test splitting
* Sentinel-value handling
* Missing-value indicators
* Median imputation
* One-hot encoding
* Train-only preprocessing fitting
* Consistent feature ordering

Four sentinel columns received explicit missing indicators.

The preprocessing pipeline transformed the original features into:

**55 model features**

The preprocessing pipeline was fitted only on the training data to avoid preprocessing leakage.

---

# 5. XGBoost Fraud Classifier

The primary supervised model is **XGBoost**.

The model was selected for the tabular classification problem because it can capture:

* Non-linear relationships
* Feature interactions
* Complex decision boundaries
* Large-scale tabular patterns

Class imbalance was addressed using:

```text
scale_pos_weight
```

### Final model configuration

```text
n_estimators       = 500
max_depth           = 4
min_child_weight    = 1
learning_rate       = 0.05
subsample           = 0.8
colsample_bytree    = 0.8
reg_alpha           = 0
reg_lambda          = 1.0
objective           = binary:logistic
eval_metric         = aucpr
```

---

# 6. Baseline vs Tuned Model

The baseline XGBoost model achieved:

| Metric  | Baseline |
| ------- | -------: |
| PR-AUC  |   0.1591 |
| ROC-AUC |   0.8859 |

After hyperparameter tuning:

| Metric             |  Tuned |
| ------------------ | -----: |
| Validation PR-AUC  | 0.1738 |
| Validation ROC-AUC | 0.8963 |

This represents an improvement in PR-AUC from approximately **0.1591 → 0.1738** on the validation set.

---

# 7. Probability Calibration

Raw tree-model probabilities were calibrated using **Isotonic Calibration**.

Calibration was evaluated using:

* PR-AUC
* ROC-AUC
* Brier Score

### Calibrated validation performance

| Metric      |   Result |
| ----------- | -------: |
| PR-AUC      | 0.173854 |
| ROC-AUC     | 0.896411 |
| Brier Score | 0.009886 |

### Final non-temporal test performance

| Metric      |       Result |
| ----------- | -----------: |
| PR-AUC      | **0.177494** |
| ROC-AUC     | **0.903680** |
| Brier Score | **0.009840** |

Because the fraud class represents only **1.1029%** of the dataset, PR-AUC is emphasized over accuracy.

---

# 8. Classification Threshold

A default probability threshold of `0.5` is not necessarily appropriate for a highly imbalanced fraud detection system.

Different thresholds were evaluated using:

* Precision
* Recall
* F1-score
* False positives
* False negatives
* Relative fraud-review costs

### Non-temporal test at threshold 0.12

| Metric    | Result |
| --------- | -----: |
| Precision | 21.49% |
| Recall    | 28.54% |
| F1-score  | 24.52% |

The final temporal operating threshold selected during validation was:

```text
0.09
```

This threshold was selected based on the operational trade-off between detecting fraud and generating investigation alerts.

---

# 9. Isolation Forest Experiment

An unsupervised **Isolation Forest** model was evaluated as an anomaly-detection approach.

Results:

| Metric  | Isolation Forest |
| ------- | ---------------: |
| PR-AUC  |          0.01295 |
| ROC-AUC |          0.53956 |

Correlation between the XGBoost fraud score and Isolation Forest score:

```text
0.01949
```

The experiment did not provide useful complementary information for the final fraud scoring pipeline.

Therefore, Isolation Forest was **not included in the final scoring system**.

---

# 10. SHAP Explainability

SHAP was used to explain both global model behavior and individual fraud predictions.

The system provides:

* Global feature importance
* Individual prediction explanations
* Positive feature contributions
* Negative feature contributions
* Top contributing features

### Top global SHAP features

| Rank | Feature | Mean |SHAP| |
|---:|---|---:|
| 1 | `housing_status_BA` | 0.511402 |
| 2 | `device_os_windows` | 0.417484 |
| 3 | `phone_home_valid` | 0.393635 |
| 4 | `keep_alive_session` | 0.376641 |
| 5 | `has_other_cards` | 0.343633 |
| 6 | `name_email_similarity` | 0.324145 |
| 7 | `prev_address_months_count_missing` | 0.322524 |
| 8 | `current_address_months_count` | 0.285160 |
| 9 | `income` | 0.273786 |
| 10 | `email_is_free` | 0.260326 |
| 11 | `bank_branch_count_8w` | 0.220051 |
| 12 | `intended_balcon_amount` | 0.197063 |
| 13 | `credit_risk_score` | 0.166055 |
| 14 | `velocity_4w` | 0.156407 |
| 15 | `days_since_request` | 0.152509 |

SHAP values describe **model behavior** and are not interpreted as causal relationships.

---

# 11. Temporal Evaluation

A chronological evaluation was performed to test whether the model generalizes to future periods.

### Temporal split

```text
Training    → Months 0–4
Validation  → Month 5
Future Test → Months 6–7
```

Dataset sizes:

| Period      |    Rows |
| ----------- | ------: |
| Training    | 675,666 |
| Validation  | 119,323 |
| Future Test | 205,011 |

### Temporal validation

| Metric                 |   Result |
| ---------------------- | -------: |
| Raw PR-AUC             | 0.191810 |
| Raw ROC-AUC            | 0.896511 |
| Calibrated PR-AUC      | 0.192239 |
| Calibrated ROC-AUC     | 0.896274 |
| Calibrated Brier Score | 0.010578 |

### Future temporal test

| Metric      |       Result |
| ----------- | -----------: |
| PR-AUC      | **0.188659** |
| ROC-AUC     | **0.891654** |
| Brier Score | **0.012634** |

Feature distribution drift was also evaluated using Population Stability Index (PSI).

### Highest observed PSI values

| Feature                            |    PSI |
| ---------------------------------- | -----: |
| `velocity_4w`                      | 3.7386 |
| `velocity_24h`                     | 1.8917 |
| `velocity_6h`                      | 1.0886 |
| `zip_count_4w`                     | 0.4910 |
| `date_of_birth_distinct_emails_4w` | 0.4548 |
| `credit_risk_score`                | 0.2613 |

The temporal evaluation did not show a major collapse in model discrimination over the evaluated future period.

---

# 12. Cost-Sensitive Threshold Optimization

Threshold selection was also evaluated using relative fraud-review cost assumptions.

Validation-derived thresholds:

| Relative Cost | Selected Threshold |
| ------------- | -----------------: |
| 1:1           |               0.38 |
| 2:1           |               0.26 |
| 5:1           |               0.13 |
| 10:1          |               0.08 |
| 20:1          |               0.04 |

The operational threshold used by the current API and dashboard is:

```text
0.09
```

This threshold should be interpreted as an operational configuration rather than a universal optimum.

---

# 13. Threshold 0.09 — Temporal Performance

The threshold `0.09` was selected during temporal validation.

### Validation

| Metric     |  Result |
| ---------- | ------: |
| Precision  |  23.93% |
| Recall     |  30.90% |
| F1-score   |  26.97% |
| Alerts     |   1,822 |
| Alert Rate | 1.5269% |

### Future Test

| Metric     |     Result |
| ---------- | ---------: |
| Precision  | **24.34%** |
| Recall     | **27.07%** |
| F1-score   | **25.63%** |
| Alerts     |      3,201 |
| Alert Rate |     1.561% |

---

# 14. Fraud Case Investigation

The system supports investigation of individual applications using model predictions and SHAP explanations.

For each application, the system provides:

```text
Application
     ↓
Fraud Probability
     ↓
Threshold
     ↓
Risk Level
     ↓
Model Decision
     ↓
SHAP Factors
     ↓
Application Features
```

This allows an analyst to inspect which model features contributed most strongly to a prediction.

### Example investigation

At threshold `0.09`, a validation set investigation produced:

| Case Type              | Probability | Result      |
| ---------------------- | ----------: | ----------- |
| True Positive example  |    0.994575 | Flagged     |
| False Positive example |    0.756410 | Flagged     |
| False Negative example |    0.089133 | Not flagged |

Example True Positive SHAP contributors included:

```text
proposed_credit_limit       +0.888862
credit_risk_score           +0.780624
housing_status_BA           +0.667315
device_os_windows           +0.446558
income                      +0.405606
```

Example False Negative contributors included:

```text
credit_risk_score           +0.816832
housing_status_BA           +0.641314
foreign_request             +0.592525
device_os_windows           +0.436888
income                      +0.404368
```

SHAP explanations are model explanations and should not be interpreted as causal evidence.

---

# 15. FastAPI Fraud Scoring API

The trained model is exposed through a FastAPI inference service.

```text
Application Features
        ↓
FastAPI
        ↓
Preprocessing Pipeline
        ↓
Calibrated XGBoost
        ↓
Fraud Probability
        ↓
Threshold = 0.09
        ↓
Risk Level / Model Decision
```

## API Endpoints

| Endpoint                | Purpose                          |
| ----------------------- | -------------------------------- |
| `GET /health`           | Check API and model status       |
| `POST /predict`         | Score a single application       |
| `POST /predict/batch`   | Score multiple applications      |
| `POST /predict/explain` | Score and explain an application |

### Example response

```json
{
  "fraud_probability": 0.022186,
  "threshold": 0.09,
  "risk_level": "LOW",
  "decision": "DO_NOT_FLAG"
}
```

---

# 16. API Performance

Local inference benchmarks were performed on the running FastAPI service.

### Single-request inference

| Metric           |          Result |
| ---------------- | --------------: |
| Requests         |           1,000 |
| Warm-up requests |              10 |
| Mean latency     |   **14.451 ms** |
| P50 latency      |   **13.934 ms** |
| P95 latency      |   **20.322 ms** |
| P99 latency      |   **23.585 ms** |
| Minimum latency  |        9.802 ms |
| Maximum latency  |       56.666 ms |
| Throughput       | **69.20 req/s** |

### Batch inference

| Batch Size |  Total Time | Time / Request |   Throughput |
| ---------: | ----------: | -------------: | -----------: |
|         10 |   46.043 ms |       4.604 ms | 217.19 req/s |
|         50 |  168.626 ms |       3.373 ms | 296.51 req/s |
|        100 |  294.131 ms |       2.941 ms | 339.98 req/s |
|        500 | 1471.674 ms |       2.943 ms | 339.75 req/s |

### SHAP explanation endpoint

| Metric       |          Result |
| ------------ | --------------: |
| Requests     |             100 |
| Mean latency |   **31.543 ms** |
| P50 latency  |   **23.702 ms** |
| P95 latency  |   **89.808 ms** |
| P99 latency  |  **109.751 ms** |
| Throughput   | **31.70 req/s** |

The explanation endpoint is slower because SHAP computation adds additional inference overhead.

---

# 17. Streamlit Fraud Analyst Dashboard

A Streamlit dashboard was built on top of the FastAPI scoring service.

## Analyst Console

The Analyst Console provides:

* Application case queue
* Fraud probability
* Risk level
* Case status
* Risk distribution
* Case status distribution
* SHAP explanations
* Application details
* Analyst workflow
* Portfolio-level dashboard metrics

### Dashboard Metrics

The dashboard tracks:

```text
Total Applications
High-Risk Cases
Scored Cases
Average Fraud Probability
New Cases
Reviewing Cases
Escalated Cases
Cleared Cases
API Status
```

### Analyst Case Workflow

```text
NEW
 ↓
REVIEWING
 ↓
 ├── CLEARED
 └── ESCALATED
```

The **model decision** and **analyst case status** are deliberately kept separate.

The model provides a risk signal; the analyst controls the operational case status.

---

# 18. Test Application

The dashboard also contains a Test Application interface.

```text
Raw Application Features
        ↓
Streamlit
        ↓
FastAPI
        ↓
Preprocessing
        ↓
Calibrated XGBoost
        ↓
Fraud Probability
        ↓
SHAP Explanation
        ↓
Dashboard
```

The Test Application allows individual application inputs to be submitted directly to the same inference pipeline used by the API.

The API accepts the original raw application features and performs the required preprocessing internally.

---

# 19. System Architecture

```text
                    +-----------------------+
                    | Bank Account          |
                    | Application           |
                    +-----------+-----------+
                                |
                                v
                    +-----------------------+
                    | FastAPI               |
                    | Inference Service     |
                    +-----------+-----------+
                                |
                                v
                    +-----------------------+
                    | Preprocessing         |
                    |                       |
                    | Missing Indicators    |
                    | Imputation             |
                    | One-Hot Encoding      |
                    +-----------+-----------+
                                |
                                v
                    +-----------------------+
                    | Calibrated XGBoost    |
                    +-----------+-----------+
                                |
                    +-----------+-----------+
                    |                       |
                    v                       v
           Fraud Probability             SHAP
                    |                 Explanation
                    v
              Threshold 0.09
                    |
                    v
             Risk / Decision
                    |
                    v
            +---------------+
            | Streamlit     |
            | Analyst UI    |
            +-------+-------+
                    |
          +---------+---------+
          |                   |
          v                   v
      Case Queue        Investigation
```

---

# 20. Technology Stack

### Machine Learning

* Python
* Pandas
* NumPy
* Scikit-learn
* XGBoost
* SHAP

### Backend

* FastAPI
* Pydantic
* Uvicorn

### Dashboard

* Streamlit

### Development

* Jupyter Notebook
* Git
* GitHub

---

# 21. Project Structure

```text
adaptive-bank-fraud-detection/
│
├── api/
│   ├── __init__.py
│   ├── explainer.py
│   ├── main.py
│   ├── model_service.py
│   └── schemas.py
│
├── dashboard/
│   └── app.py
│
├── notebooks/
│   ├── cleaning.ipynb
│   └── unique_values.txt
│
├── notes/
│   ├── notes_pahse_1_Problem_&_Dataset.md
│   ├── notes_phase_2_preprocessing_pipeline.md
│   ├── notes_phase_3_model_training.md
│   ├── notes_phase_4_hyperparameter_tuning.md
│   ├── notes_phase_5_and_6_isolation_forest_and_shap.md
│   ├── phase_7_month_wise_evaluation.md
│   ├── phase_8_cost_sensitive_threshold_optimization.md
│   ├── phase_9_explainibility_and_fruad_case_investigation.md
│   ├── phase_10_real_time_fraud_scoring_api.md
│   └── phase_11_fraud_analyst_dashboard.md
│
├── benchmark.py
├── benchmark_batch.py
├── benchmark_explain.py
├── features.md
├── requirements.txt
├── test_inference.py
├── README.md
└── .gitignore
```

---

# 22. Running Locally

## 1. Clone the repository

```bash
git clone <repository-url>
cd adaptive-bank-fraud-detection
```

## 2. Create a virtual environment

```bash
python -m venv .venv
```

## 3. Activate the environment

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 5. Start FastAPI

```bash
uvicorn api.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

## 6. Start Streamlit

Open another terminal:

```bash
streamlit run dashboard/app.py
```

---

# 23. Limitations & Scope

* The original BAF dataset is not included in the repository.
* Large trained model artifacts are excluded from Git.
* The BAF dataset represents bank account/application fraud rather than a literal high-frequency transaction stream.
* The current API provides application-level real-time scoring.
* The current implementation is an ML engineering prototype rather than a production banking deployment.
* Model predictions are risk signals and do not automatically determine final business decisions.
* The dashboard currently operates on demonstration/synthetic application cases rather than a live bank case-management system.
* Production authentication, deployment infrastructure, monitoring infrastructure, and automated model retraining are outside the current scope.
* The evaluated temporal period is limited to the available future months in the dataset.
* SHAP explanations describe model behavior and should not be interpreted as causal explanations.

---

# 24. Project Status

| Component                   | Status   |
| --------------------------- | -------- |
| Exploratory Data Analysis   | Complete |
| Preprocessing               | Complete |
| XGBoost Model               | Complete |
| Hyperparameter Tuning       | Complete |
| Probability Calibration     | Complete |
| Isolation Forest Experiment | Complete |
| SHAP Explainability         | Complete |
| Temporal Evaluation         | Complete |
| Threshold Optimization      | Complete |
| Fraud Case Investigation    | Complete |
| FastAPI Scoring API         | Complete |
| Batch Inference             | Complete |
| API Benchmarking            | Complete |
| Streamlit Analyst Dashboard | Complete |

---

# 25. Key Results Summary

| Area                          | Result                 |
| ----------------------------- | ---------------------- |
| Dataset Size                  | 1,000,000 applications |
| Fraud Rate                    | 1.1029%                |
| Model                         | XGBoost                |
| Processed Features            | 55                     |
| Non-temporal Test PR-AUC      | **0.177494**           |
| Non-temporal Test ROC-AUC     | **0.903680**           |
| Non-temporal Test Brier Score | **0.009840**           |
| Temporal Future-Test PR-AUC   | **0.188659**           |
| Temporal Future-Test ROC-AUC  | **0.891654**           |
| Operational Threshold         | **0.09**               |
| Future-Test Precision @ 0.09  | **24.34%**             |
| Future-Test Recall @ 0.09     | **27.07%**             |
| Future-Test F1 @ 0.09         | **25.63%**             |
| Single-Request Mean Latency   | **14.451 ms**          |
| Single-Request P95            | **20.322 ms**          |
| Single-Request Throughput     | **69.20 req/s**        |
| Batch Throughput @ 100        | **339.98 req/s**       |
| SHAP Endpoint Mean Latency    | **31.543 ms**          |

---

# 26. Final System

The completed system combines:

```text
Machine Learning
      +
Probability Calibration
      +
Temporal Validation
      +
Cost-Sensitive Thresholding
      +
SHAP Explainability
      +
FastAPI
      +
Batch Inference
      +
Streamlit Analyst Dashboard
```

The resulting platform provides an end-to-end prototype for **bank account/application fraud risk scoring and analyst investigation**, from raw application features through model prediction, explanation, API inference, and dashboard-based case handling.

---

# Author

**Mayank Asutkar**

Computer Science & Engineering
Sardar Patel Institute of Technology, Mumbai

```
```
