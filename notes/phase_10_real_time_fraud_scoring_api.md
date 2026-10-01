============================================================
PHASE 10 — REAL-TIME FRAUD SCORING API
============================================================

1. OBJECTIVE
------------------------------------------------------------
Phase 10 converts the trained fraud detection model into a
real-time inference service using FastAPI.

The API allows an external application/client to send raw
fraud-detection features and receive:

- Fraud probability
- Risk level
- Fraud decision
- SHAP-based explanation
- Batch predictions
- API health status

IMPORTANT:
This is real-time APPLICATION/ACCOUNT FRAUD SCORING.

The BAF dataset is not a literal high-frequency transaction
dataset, so the API should be described as real-time application
scoring rather than a true transaction-stream fraud engine.


2. PHASE 10 ARCHITECTURE
------------------------------------------------------------

                    CLIENT / FRONTEND
                           |
                           | HTTP
                           v
                    +-------------+
                    |   FastAPI   |
                    +------+------+
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
         /predict    /predict/batch  /predict/explain
             |             |             |
             +-------------+-------------+
                           |
                           v
                  FraudModelService
                           |
                           v
                  Raw Input Processing
                           |
                           v
                   Saved Preprocessor
                           |
                           v
                    55 Model Features
                           |
                           v
                  Calibrated XGBoost
                           |
                           v
                   Fraud Probability
                           |
                           v
                    Threshold = 0.09
                           |
                    +------+------+
                    |             |
                    v             v
                   LOW           HIGH
                    |             |
              DO_NOT_FLAG   FLAG_FOR_INVESTIGATION


3. WHY FASTAPI?
------------------------------------------------------------
FastAPI is used to expose the ML model through HTTP.

Instead of manually running:

    model.predict_proba(X)

inside a notebook, an application can send:

    POST /predict

and receive a structured JSON response.

Advantages:

- Request validation
- Response validation
- Automatic API documentation
- JSON request/response handling
- Easy frontend/backend integration
- High-performance web API framework
- Automatic Swagger UI documentation


4. PROJECT STRUCTURE
------------------------------------------------------------

FRAUD_TRANSACTION_DETECTION_SYSTEM/
|
+-- api/
|   +-- __init__.py
|   +-- main.py
|   +-- schemas.py
|   +-- model_service.py
|   +-- explainer.py
|
+-- notebooks/
|   +-- artifacts/
|       +-- preprocessor.pkl
|       +-- calibrated_xgb.pkl
|       +-- X_train_processed.npy
|       +-- X_val_processed.npy
|       +-- X_test_processed.npy
|       +-- y_train.npy
|       +-- y_val.npy
|       +-- y_test.npy
|       +-- ...
|
+-- benchmark.py
+-- benchmark_batch.py
+-- benchmark_explain.py


5. SAVED MODEL ARTIFACTS
------------------------------------------------------------
The API does NOT retrain the model.

It loads artifacts produced in previous phases.

Preprocessor:

    notebooks/artifacts/preprocessor.pkl

Model:

    notebooks/artifacts/calibrated_xgb.pkl

Pipeline:

    Training
       |
       v
    Save artifacts
       |
       v
    API startup
       |
       v
    Load artifacts
       |
       v
    Inference


6. ENVIRONMENT COMPATIBILITY
------------------------------------------------------------
The saved preprocessor was created using:

    scikit-learn 1.6.1

The original global environment had incompatible/newer versions,
which caused a serialization compatibility problem.

A project-specific virtual environment was therefore created:

    .venv

Important packages used by the API environment:

    scikit-learn 1.6.1
    numpy 2.5.3
    pandas 3.0.6
    xgboost 3.4.1
    joblib 1.6.0
    fastapi
    uvicorn

IMPORTANT LESSON:

Serialized ML artifacts such as .pkl files can depend on the
library versions used when they were created.

For production systems, dependency versions should be pinned.


7. FRAUD MODEL SERVICE
------------------------------------------------------------
FraudModelService is responsible for:

    Raw JSON
       |
       v
    DataFrame
       |
       v
    Sentinel processing
       |
       v
    Saved preprocessing pipeline
       |
       v
    Processed features
       |
       v
    Calibrated XGBoost
       |
       v
    Prediction


8. OPERATING THRESHOLD
------------------------------------------------------------
The API currently uses:

    DEFAULT_THRESHOLD = 0.09

This threshold comes from Phase 8 temporal cost-sensitive
threshold analysis.

Decision logic:

    fraud_probability >= 0.09
            |
            +----> HIGH
            |      FLAG_FOR_INVESTIGATION
            |
            +----> LOW
                   DO_NOT_FLAG

The threshold is a business operating point, not a universal
definition of fraud.


9. RAW FEATURE HANDLING
------------------------------------------------------------
The API receives the ORIGINAL RAW FEATURES.

The client does NOT need to manually perform:

- Missing-value processing
- Sentinel conversion
- One-hot encoding
- Feature transformation

Example:

    Client
       |
       | raw features
       v
    FastAPI
       |
       v
    preprocess()
       |
       v
    saved preprocessor
       |
       v
    model


10. SENTINEL VALUE HANDLING
------------------------------------------------------------
Four columns contain -1 as an unavailable/missing sentinel:

    prev_address_months_count
    current_address_months_count
    bank_months_count
    device_distinct_emails_8w

The API reproduces the Phase 2 preprocessing logic.

For every sentinel column:

STEP 1:
Create a missing indicator.

Example:

    prev_address_months_count_missing =
        prev_address_months_count == -1

STEP 2:
Replace -1 with NaN.

Example:

    prev_address_months_count = NaN

STEP 3:
The saved preprocessor handles the missing value through
its imputation pipeline.

This ensures inference preprocessing matches training.


11. WHY THE PREPROCESSING MUST MATCH TRAINING
------------------------------------------------------------
The model was trained using a specific preprocessing pipeline.

If API preprocessing differs from training preprocessing,
the model can receive features in a different representation.

Therefore:

    Training preprocessing
            =
    Production inference preprocessing

The API reuses the SAME saved preprocessor:

    preprocessor.pkl


12. MODEL INPUT
------------------------------------------------------------
The API receives 30 raw usable features.

The preprocessing pipeline converts them into:

    55 processed model features

The categorical variables are one-hot encoded.

Categorical columns:

    payment_type
    employment_status
    housing_status
    source
    device_os

Numerical columns include:

    income
    name_email_similarity
    customer_age
    credit_risk_score
    proposed_credit_limit
    velocity features
    address features
    device features
    temporal features
    missing indicators
    etc.


13. /HEALTH ENDPOINT
------------------------------------------------------------
Endpoint:

    GET /health

Purpose:

Check whether the API is running and whether the model
artifacts were successfully loaded.

Example response:

    {
        "status": "healthy",
        "model_loaded": true,
        "threshold": 0.09
    }

Successful result:

    HTTP 200


14. /PREDICT ENDPOINT
------------------------------------------------------------
Endpoint:

    POST /predict

Purpose:

Perform normal fraud prediction.

Pipeline:

    Raw JSON
       |
       v
    preprocess()
       |
       v
    preprocessor.transform()
       |
       v
    calibrated_xgb.predict_proba()
       |
       v
    fraud probability
       |
       v
    threshold comparison
       |
       v
    risk + decision


Example output:

    {
        "fraud_probability": 0.022186,
        "threshold": 0.09,
        "risk_level": "LOW",
        "decision": "DO_NOT_FLAG"
    }


15. /PREDICT/BATCH ENDPOINT
------------------------------------------------------------
Endpoint:

    POST /predict/batch

Purpose:

Predict multiple applications in one API request.

Instead of:

    request 1 -> model
    request 2 -> model
    request 3 -> model

the API:

    request 1
    request 2
    request 3
         |
         v
      DataFrame
         |
         v
    preprocess together
         |
         v
    model.predict_proba()
         |
         v
      results


Batch inference is more computationally efficient because the
model processes multiple observations together.


16. /PREDICT/EXPLAIN ENDPOINT
------------------------------------------------------------
Endpoint:

    POST /predict/explain

Purpose:

Return the fraud prediction together with the most important
SHAP factors for that individual prediction.

Pipeline:

    Raw Input
       |
       v
    Preprocessing
       |
       v
    Calibrated XGBoost
       |
       +----> Fraud Probability
       |
       v
    SHAP TreeExplainer
       |
       v
    SHAP Contributions
       |
       v
    Top 5 Features


17. SHAP EXPLAINER OPTIMIZATION
------------------------------------------------------------
Initially, the SHAP TreeExplainer was created inside every
/explain request.

That means:

    Request 1 -> create explainer -> calculate SHAP
    Request 2 -> create explainer -> calculate SHAP
    Request 3 -> create explainer -> calculate SHAP

This creates unnecessary repeated initialization overhead.

The implementation was changed so that the SHAP explainer is
created ONCE when FraudModelService starts.

API startup:

    Load model
       |
       v
    Get underlying XGBoost estimator
       |
       v
    Create TreeExplainer ONCE
       |
       v
    Store as:

        self.shap_explainer


Then requests reuse it:

    /predict/explain
          |
          v
    self.shap_explainer.shap_values()


18. SHAP INTERPRETATION
------------------------------------------------------------
For every individual prediction, SHAP provides feature
contributions.

Positive SHAP value:

    increases the model's fraud score

Negative SHAP value:

    decreases the model's fraud score

Example:

    housing_status_BA
    SHAP = +0.664

means:

    housing_status_BA pushed the model's output toward fraud
    for this particular case.

Example:

    has_other_cards
    SHAP = -1.245

means:

    has_other_cards pushed the model's output away from fraud
    for this particular case.

IMPORTANT:

SHAP explains MODEL BEHAVIOR.

It does NOT prove causality.

A positive SHAP value does NOT mean the feature causes fraud.


19. SUCCESSFUL EXPLAINABILITY TEST
------------------------------------------------------------
Test input produced:

    fraud_probability = 0.0221863516
    threshold = 0.09

Therefore:

    0.02218 < 0.09

Result:

    risk_level = LOW
    decision = DO_NOT_FLAG


Top SHAP factors:

    has_other_cards
        SHAP = -1.244907
        decreases_fraud_score

    zip_count_4w
        SHAP = -1.044683
        decreases_fraud_score

    intended_balcon_amount
        SHAP = -0.688104
        decreases_fraud_score

    housing_status_BA
        SHAP = +0.664093
        increases_fraud_score

    device_distinct_emails_8w
        SHAP = +0.560998
        increases_fraud_score


20. API VALIDATION
------------------------------------------------------------
FastAPI schemas are used to validate requests and responses.

FraudRequest:

    Represents one fraud-scoring request.

FraudResponse:

    Represents a standard prediction.

BatchFraudRequest:

    Represents multiple fraud requests.

BatchFraudResponse:

    Represents multiple predictions.

SHAPFactor:

    feature
    shap_value
    direction

FraudExplanationResponse:

    fraud_probability
    threshold
    risk_level
    decision
    factors


21. SWAGGER API DOCUMENTATION
------------------------------------------------------------
FastAPI automatically generates interactive API documentation.

Swagger allows testing endpoints directly from the browser.

Main endpoints:

    GET  /health

    POST /predict

    POST /predict/batch

    POST /predict/explain


Swagger also displays:

- Request schema
- Response schema
- Validation errors
- Example JSON
- Execute button
- HTTP status codes


22. ERROR HANDLING / VALIDATION
------------------------------------------------------------
The API uses schema validation.

Invalid request structures can result in:

    HTTP 422

Example:

    missing required field
    incorrect data type
    unexpected field

The FraudRequest schema uses:

    extra = "forbid"

Therefore unexpected input fields are rejected instead of being
silently ignored.


23. NORMAL PREDICTION BENCHMARK
------------------------------------------------------------
Individual inference benchmark:

    Requests = 1000

Results:

    Mean     = 14.451 ms
    P50      = 13.934 ms
    P95      = 20.322 ms
    P99      = 23.585 ms
    Min      = 9.802 ms
    Max      = 56.666 ms

Approximate throughput:

    69.20 requests/sec

IMPORTANT:

This is an inference-layer/API benchmark in the local
development environment, NOT a production load-test result.


24. BATCH INFERENCE BENCHMARK
------------------------------------------------------------
Batch size = 10

    Total       = 46.043 ms
    Per request = 4.604 ms
    Throughput  = 217.19 req/s


Batch size = 50

    Total       = 168.626 ms
    Per request = 3.373 ms
    Throughput  = 296.51 req/s


Batch size = 100

    Total       = 294.131 ms
    Per request = 2.941 ms
    Throughput  = 339.98 req/s


Batch size = 500

    Total       = 1471.674 ms
    Per request = 2.943 ms
    Throughput  = 339.75 req/s


Observation:

Throughput improved substantially when using batches.

Performance plateaued around:

    ~340 requests/sec

from batch sizes 100 to 500.


25. SHAP API BENCHMARK
------------------------------------------------------------
After moving the SHAP explainer initialization to API startup,
the /predict/explain endpoint was benchmarked.

Results:

    Requests = 100

    Mean = 31.543 ms
    P50  = 23.702 ms
    P95  = 89.808 ms
    P99  = 109.751 ms
    Min  = 18.535 ms
    Max  = 109.751 ms

Approximate throughput:

    31.70 requests/sec


26. PERFORMANCE COMPARISON
------------------------------------------------------------

Metric              /predict       /predict/explain

Mean                14.451 ms      31.543 ms
P50                 13.934 ms      23.702 ms
P95                 20.322 ms      89.808 ms
P99                 23.585 ms      109.751 ms
Throughput          69.20 req/s    31.70 req/s


Interpretation:

The SHAP endpoint is slower because it performs additional
explainability computation.

Normal prediction is the latency-sensitive endpoint.

SHAP explanation is intended more for:

- Fraud analyst investigation
- Model debugging
- Case investigation
- Explainable fraud decisions

Therefore the additional latency is expected.


27. WHY BATCH INFERENCE IS FASTER
------------------------------------------------------------
Individual inference repeatedly performs preprocessing and
model calls for one observation.

Batch inference allows the system to:

- Build one DataFrame
- Transform multiple observations together
- Call predict_proba() once
- Process multiple observations simultaneously

Therefore:

    larger batch
         |
         v
    lower per-request cost
         |
         v
    higher throughput


28. IMPORTANT DEPLOYMENT LESSONS
------------------------------------------------------------
1. Reuse trained artifacts instead of retraining during
   inference.

2. Keep inference preprocessing identical to training
   preprocessing.

3. Pin dependency versions for serialized ML artifacts.

4. Separate prediction and explainability endpoints.

5. Initialize expensive reusable objects at startup.

6. Benchmark P50/P95/P99 rather than reporting only average
   latency.

7. Batch inference can significantly increase throughput.

8. SHAP explanations are computationally more expensive than
   normal predictions.

9. The threshold is an operating/business decision and can be
   changed without retraining the model.

10. API benchmarks performed locally should not be presented as
    production capacity.


29. FINAL PHASE 10 STATUS
------------------------------------------------------------

                    PHASE 10 COMPLETE
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
       /health          /predict        /predict/batch
          |                |                |
          +----------------+----------------+
                           |
                           v
                    Calibrated XGBoost
                           |
                           v
                    Fraud Probability
                           |
                           v
                    Threshold = 0.09
                           |
                           v
                    Risk + Decision


                    +----------------+
                    | /predict/explain|
                    +--------+-------+
                             |
                             v
                         SHAP
                             |
                             v
                    Top Feature Factors


30. KEY RESULTS TO REMEMBER
------------------------------------------------------------

Model:
    Calibrated XGBoost

Operating threshold:
    0.09

Processed features:
    55

Normal API mean latency:
    14.451 ms

Normal API P95:
    20.322 ms

Normal API throughput:
    69.20 req/s

Batch throughput:
    ~340 req/s

SHAP API mean latency:
    31.543 ms

SHAP API P95:
    89.808 ms

SHAP API throughput:
    31.70 req/s

Endpoints:

    GET  /health
    POST /predict
    POST /predict/batch
    POST /predict/explain


============================================================
PHASE 10 CONCLUSION
============================================================

The trained fraud detection system has been converted into a
working FastAPI inference service.

The service accepts raw application-level fraud features,
reproduces the training preprocessing pipeline, generates
calibrated XGBoost fraud probabilities, applies the Phase 8
operating threshold of 0.09, and returns a risk decision.

The API additionally supports batch inference and individual
SHAP explanations.

The system was tested successfully through Swagger and
benchmarked for normal inference, batch inference, and SHAP
explanation latency.

Phase 10 therefore establishes the DEPLOYMENT / INFERENCE LAYER
of the fraud detection project.
============================================================