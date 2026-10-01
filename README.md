# Adaptive Bank Account Fraud Detection & Risk Intelligence Platform

An end-to-end machine learning platform for bank account/application fraud detection, risk scoring, model explainability, real-time inference, and analyst investigation.

---

## ?? Overview

Fraud detection is a highly imbalanced classification problem where fraudulent applications represent a small fraction of total applications.

This project develops an end-to-end fraud detection system using the **Bank Account Fraud (BAF)** dataset.

The system covers the complete workflow:

`	ext
Data
  ?
Exploratory Data Analysis
  ?
Preprocessing & Feature Engineering
  ?
XGBoost Fraud Classifier
  ?
Probability Calibration
  ?
Temporal Evaluation
  ?
Threshold Optimization
  ?
SHAP Explainability
  ?
FastAPI Scoring API
  ?
Streamlit Analyst Dashboard

?? Problem Statement

The objective is to build a fraud detection system that can:

Handle highly imbalanced fraud data
Generate fraud probabilities
Select an operational classification threshold
Evaluate performance on future time periods
Explain individual predictions
Provide an API for real-time application scoring
Provide an analyst interface for investigation
?? Machine Learning Pipeline
1. Exploratory Data Analysis

The dataset was analyzed for:

Class imbalance
Numerical feature distributions
Categorical variables
Sentinel values
Fraud rates across categories
Feature behavior

The dataset contains approximately 1 million applications with a fraud rate of approximately 1.1%.

2. Preprocessing

The preprocessing pipeline includes:

Stratified train/validation/test split
Sentinel-value handling
Missing-value indicators
Median imputation
One-hot encoding
Train-only preprocessing fitting

Dataset split:

Dataset    Percentage
Training    70%
Validation    15%
Test    15%

The final preprocessing pipeline produces 55 model features.

3. XGBoost Fraud Classifier

XGBoost was selected as the primary supervised model for the tabular classification problem.

The model handles:

Non-linear relationships
Feature interactions
Class imbalance
Large tabular datasets

Class imbalance was addressed using scale_pos_weight.

4. Probability Calibration

Model probabilities were calibrated using isotonic calibration.

Calibration was evaluated using:

PR-AUC
ROC-AUC
Brier Score

Final non-temporal test results:

Metric    Score
PR-AUC    0.1775
ROC-AUC    0.9037
Brier Score    0.00984

Because the dataset is highly imbalanced, PR-AUC is emphasized over accuracy.

5. Isolation Forest

Isolation Forest was evaluated as an unsupervised anomaly detection approach.

The experiment produced substantially weaker fraud discrimination than the supervised XGBoost model and did not provide useful complementary information for the final scoring pipeline.

Therefore, Isolation Forest was not included in the final fraud scoring system.

6. SHAP Explainability

SHAP is used to explain model predictions.

The system provides:

Global feature importance
Individual prediction explanations
Positive feature contributions
Negative feature contributions
Top contributing features

SHAP values describe model behavior and are not interpreted as causal relationships.

7. Temporal Evaluation

The model was evaluated chronologically to test performance on future periods.

Training    ? Months 0–4
Validation  ? Month 5
Future Test ? Months 6–7

Future temporal test:

Metric    Result
PR-AUC    ~0.189
ROC-AUC    ~0.892
Brier Score    ~0.0126

Feature distribution drift was also analyzed using Population Stability Index (PSI).

8. Threshold Optimization

A default threshold of 0.5 is not suitable for this highly imbalanced problem.

Multiple thresholds were evaluated using:

Precision
Recall
F1-score
False positives
False negatives
Relative fraud-review costs

The current operational threshold is:

0.09

Future temporal test at threshold 0.09:

Metric    Result
Precision    ~24.34%
Recall    ~27.07%
F1-score    ~25.63%

The threshold represents an operational trade-off and can be changed according to fraud-review capacity and business costs.

?? Fraud Case Investigation

Individual applications can be investigated using the model prediction and SHAP explanation.

For each case, the system provides:

Fraud Probability
       ?
Threshold
       ?
Risk Level
       ?
Model Decision
       ?
Top SHAP Factors
       ?
Application Features

This allows an analyst to understand which features contributed most strongly to a model prediction.

? FastAPI Fraud Scoring API

The trained model is exposed through a FastAPI service.

Application Features
        ?
Preprocessing Pipeline
        ?
Calibrated XGBoost
        ?
Fraud Probability
        ?
Threshold
        ?
Risk Level / Decision
API Endpoints
Endpoint    Purpose
GET /health    Check API and model status
POST /predict    Score a single application
POST /predict/batch    Score multiple applications
POST /predict/explain    Score and explain an application
Example Response
{
    "fraud_probability": 0.022,
    "threshold": 0.09,
    "risk_level": "LOW",
    "decision": "DO_NOT_FLAG"
}
? API Performance

Local inference benchmarks:

Metric    Result
Mean latency    ~14.45 ms
P50 latency    ~13.93 ms
P95 latency    ~20.32 ms
P99 latency    ~23.59 ms
Throughput    ~69 requests/sec

Batch inference:

Batch Size    Throughput
10    ~217 req/s
50    ~297 req/s
100    ~340 req/s
500    ~340 req/s

The explanation endpoint has higher latency because SHAP explanation generation adds computational overhead.

??? Streamlit Fraud Analyst Dashboard

A Streamlit dashboard was built on top of the FastAPI service.

Analyst Console

The Analyst Console provides:

Application case queue
Fraud probability
Risk level
Case status
Risk distribution
Case status analytics
SHAP explanations
Application details
Analyst workflow
Analyst Case Status
NEW
 ?
REVIEWING
 ?
CLEARED / ESCALATED

The model decision and analyst status are kept separate.

The model produces a risk signal, while the analyst controls the operational case status.

?? Test Application

The dashboard also contains a Test Application interface.

Application Features
        ?
Streamlit
        ?
FastAPI
        ?
Preprocessing
        ?
XGBoost
        ?
Fraud Probability
        ?
SHAP Explanation
        ?
Dashboard

This allows individual application inputs to be tested directly against the deployed inference pipeline.

??? Architecture
                    +-----------------------+
                    | Bank Account          |
                    | Application           |
                    +-----------+-----------+
                                |
                                v
                    +-----------------------+
                    | Preprocessing         |
                    |                       |
                    | Imputation            |
                    | Encoding              |
                    | Missing Indicators    |
                    +-----------+-----------+
                                |
                                v
                    +-----------------------+
                    | Calibrated XGBoost    |
                    +-----------+-----------+
                                |
                     +----------+----------+
                     |                     |
                     v                     v
              Fraud Probability          SHAP
                     |                Explanation
                     v
              Threshold 0.09
                     |
                     v
              +-------------+
              | FastAPI     |
              +------+------+
                     |
                     v
              +-------------+
              | Streamlit   |
              | Dashboard   |
              +------+------+
                     |
              +------+------+
              |             |
              v             v
          Case Queue    Investigation
??? Technology Stack
Machine Learning
Python
Pandas
NumPy
Scikit-learn
XGBoost
SHAP
Backend
FastAPI
Pydantic
Uvicorn
Dashboard
Streamlit
Development
Jupyter Notebook
Git
GitHub
?? Project Structure
adaptive-bank-fraud-detection/
¦
+-- api/
¦   +-- __init__.py
¦   +-- explainer.py
¦   +-- main.py
¦   +-- model_service.py
¦   +-- schemas.py
¦
+-- dashboard/
¦   +-- app.py
¦
+-- notebooks/
¦   +-- cleaning.ipynb
¦   +-- unique_values.txt
¦
+-- notes/
¦   +-- notes_pahse_1_Problem_&_Dataset.md
¦   +-- notes_phase_2_preprocessing_pipeline.md
¦   +-- notes_phase_3_model_training.md
¦   +-- notes_phase_4_hyperparameter_tuning.md
¦   +-- notes_phase_5_and_6_isolation_forest_and_shap.md
¦   +-- phase_7_month_wise_evaluation.md
¦   +-- phase_8_cost_sensitive_threshold_optimization.md
¦   +-- phase_9_explainibility_and_fruad_case_investigation.md
¦   +-- phase_10_real_time_fraud_scoring_api.md
¦   +-- phase_11_fraud_analyst_dashboard.md
¦
+-- benchmark.py
+-- benchmark_batch.py
+-- benchmark_explain.py
+-- features.md
+-- test_inference.py
+-- requirements.txt
+-- README.md
+-- .gitignore
?? Running Locally
1. Clone the repository
git clone <repository-url>
cd adaptive-bank-fraud-detection
2. Create virtual environment
python -m venv .venv
3. Activate environment
Windows PowerShell
.venv\Scripts\Activate.ps1
4. Install dependencies
pip install -r requirements.txt
5. Start FastAPI
uvicorn api.main:app --reload

API:

http://127.0.0.1:8000
6. Start Streamlit

Open another terminal:

streamlit run dashboard/app.py
?? Limitations & Scope
The original BAF dataset is not included in the repository.
Large trained model artifacts are excluded from Git.
The BAF dataset represents bank account/application fraud rather than a literal high-frequency transaction stream.
The current API provides application-level real-time scoring.
The current implementation is an ML engineering prototype rather than a production banking deployment.
Model predictions are risk signals and do not automatically determine final business decisions.
Production deployment, authentication, monitoring infrastructure, and model retraining pipelines are outside the current scope.
?? Project Status
Component    Status
Exploratory Data Analysis    ?
Preprocessing    ?
XGBoost Model    ?
Hyperparameter Tuning    ?
Probability Calibration    ?
Isolation Forest Experiment    ?
SHAP Explainability    ?
Temporal Evaluation    ?
Threshold Optimization    ?
Fraud Case Investigation    ?
FastAPI Scoring API    ?
Batch Inference    ?
Streamlit Analyst Dashboard    ?
????? Author

Mayank Asutkar

Computer Science & Engineering
Sardar Patel Institute of Technology, Mumbai
