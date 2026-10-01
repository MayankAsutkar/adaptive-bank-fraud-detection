```text
============================================================
PHASE 11 — FRAUD ANALYST DASHBOARD & INVESTIGATION WORKFLOW
============================================================

OBJECTIVE
------------------------------------------------------------

Phase 11 converts the fraud detection ML + FastAPI backend into
an analyst-facing application.

The goal is NOT to train another model.

The goal is to provide a practical interface where a fraud analyst
can:

1. View incoming application cases.
2. Select a case for investigation.
3. Send the case to the FastAPI fraud model.
4. View fraud probability.
5. View the model threshold.
6. View model risk level and model decision.
7. Inspect SHAP explanations.
8. Review the original application features.
9. Change the analyst-controlled case status.
10. View portfolio-level analytics.
11. Test arbitrary applications through a separate testing interface.

The dashboard is implemented using Streamlit.

The backend remains FastAPI.

The trained model and preprocessing artifacts remain unchanged.


============================================================
1. PHASE 11 ARCHITECTURE
============================================================

The Phase 11 architecture is:

                    ┌─────────────────────────┐
                    │      Fraud Analyst      │
                    │                         │
                    │   Streamlit Dashboard   │
                    └────────────┬────────────┘
                                 │
                                 │ HTTP
                                 ▼
                    ┌─────────────────────────┐
                    │        FastAPI          │
                    │                         │
                    │ /health                 │
                    │ /predict               │
                    │ /predict/batch         │
                    │ /predict/explain       │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Model Service         │
                    │                         │
                    │ Preprocessor            │
                    │ Calibrated XGBoost      │
                    │ SHAP Explainer          │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ Fraud Risk Result       │
                    │                         │
                    │ Probability             │
                    │ Threshold               │
                    │ Risk Level              │
                    │ Decision                │
                    │ SHAP Factors            │
                    └─────────────────────────┘


The important separation is:

Streamlit
    ↓
User interface

FastAPI
    ↓
Inference service

Model Service
    ↓
Machine learning logic

Artifacts
    ↓
Trained model + preprocessing


============================================================
2. WHY STREAMLIT WAS USED
============================================================

Streamlit provides a fast way to build a data/ML application
interface using Python.

It is useful for this project because the dashboard needs to:

- display model outputs
- display tables
- display metrics
- display charts
- accept application inputs
- communicate with the FastAPI backend
- display SHAP explanations
- support analyst workflow

The dashboard does not contain the actual ML model.

Instead:

Streamlit → FastAPI → Model

This separation is important because the model-serving logic
should not be tightly coupled to the UI.


============================================================
3. DASHBOARD STRUCTURE
============================================================

Directory:

dashboard/
└── app.py


The dashboard contains two major sections:

1. Analyst Console
2. Test Application


Navigation:

    🕵️ Analyst Console
    🔍 Test Application


============================================================
4. ANALYST CONSOLE
============================================================

The Analyst Console represents the operational interface for a
fraud analyst.

The analyst is not the customer.

The analyst receives applications/cases that need investigation
and uses the model output as a decision-support signal.


Main workflow:

    Case Queue
        ↓
    Open Case
        ↓
    Model Scoring
        ↓
    Fraud Probability
        ↓
    Risk Level
        ↓
    SHAP Explanation
        ↓
    Application Details
        ↓
    Analyst Review
        ↓
    Analyst Status


============================================================
5. CASE QUEUE
============================================================

The dashboard contains multiple synthetic application cases.

Current cases:

CASE-1001
CASE-1002
CASE-1003
CASE-1004
CASE-1005


These cases contain the original application features used by the
fraud model.

Examples:

- income
- name_email_similarity
- customer_age
- payment_type
- credit_risk_score
- housing_status
- proposed_credit_limit
- foreign_request
- source
- device_os
- velocity features
- address history
- banking history


IMPORTANT:

These dashboard cases are synthetic feature combinations.

They should NOT be presented as real customer records.

Their purpose is to demonstrate the complete investigation workflow.


============================================================
6. CASE SELECTION
============================================================

The analyst can click:

    Open

for a case.

The selected case is stored in Streamlit session state.

Example:

    st.session_state["selected_case"]


This allows the selected case to persist across Streamlit reruns.


============================================================
7. STREAMLIT SESSION STATE
============================================================

The dashboard uses session state for temporary application state.

Important variables:

    selected_case

Stores the currently selected case.

Example:

    st.session_state["selected_case"] = None


case_results

Stores API results for cases that have already been scored.

Example:

    st.session_state["case_results"] = {}


case_statuses

Stores analyst-controlled workflow status.

Example:

    st.session_state["case_statuses"] = {}


The three concepts are different:

selected_case
    ↓
Which case is currently open?

case_results
    ↓
What did the ML model return?

case_statuses
    ↓
What has the analyst done with the case?


============================================================
8. AUTOMATIC CASE SCORING
============================================================

When an analyst opens a case, the dashboard sends the application
features to:

    POST /predict/explain


The helper function is conceptually:

    score_case(case)

The case ID is removed from the payload because it is a dashboard
identifier and is not a model feature.

The remaining 30 raw application features are sent to FastAPI.


Workflow:

    CASE-1001
         ↓
    Extract features
         ↓
    POST /predict/explain
         ↓
    FastAPI
         ↓
    preprocessing
         ↓
    calibrated XGBoost
         ↓
    SHAP
         ↓
    JSON response
         ↓
    Streamlit


============================================================
9. MODEL ASSESSMENT
============================================================

After scoring a case, the dashboard displays:

    Fraud Probability
    Threshold
    Risk Level
    Model Decision


Example structure:

    Fraud Probability     2.22%
    Threshold             9.00%
    Risk Level            LOW
    Model Decision        DO_NOT_FLAG


The probability represents the model's estimated fraud probability.

The threshold is the operating threshold used by the system.

The model decision compares the probability against the threshold.


============================================================
10. MODEL DECISION VS ANALYST DECISION
============================================================

This is one of the most important design principles in Phase 11.

The model output is NOT the same thing as the analyst's final
workflow decision.

Model:

    fraud_probability
    threshold
    risk_level
    decision


Analyst:

    NEW
    REVIEWING
    CLEARED
    ESCALATED


Therefore:

    Model Decision ≠ Analyst Status


Example:

Model:

    fraud_probability = 0.15
    threshold = 0.09
    decision = FLAG


The analyst could then:

    REVIEWING

or

    ESCALATED

depending on the investigation.

This prevents the dashboard from pretending that the ML model
automatically makes the final banking decision.


============================================================
11. ANALYST WORKFLOW
============================================================

Each case starts with:

    NEW


The analyst can select:

    🔍 Start Review

which changes:

    NEW
      ↓
    REVIEWING


The analyst can then:

    ✅ Clear Case

or:

    🚨 Escalate


Possible workflow:

    NEW
     │
     ▼
    REVIEWING
     │
     ├───────────────┐
     ▼               ▼
  CLEARED         ESCALATED


The model does not directly modify these statuses.

They are controlled by the analyst.


============================================================
12. RISK LEVEL
============================================================

The dashboard displays:

    LOW
    MEDIUM
    HIGH


These values come from the FastAPI response.

The dashboard should not independently calculate a different risk
classification.

The API is the source of truth for model inference.


============================================================
13. SHAP EXPLANATION
============================================================

The dashboard displays SHAP-based model explanations.

SHAP explains how individual features contributed to the model's
prediction for a particular case.


The dashboard separates factors into:

    Factors Increasing Fraud Score

and:

    Factors Decreasing Fraud Score


Example:

    housing_status_BA
        +0.6641

means that this feature contributed positively toward the model's
fraud score for that particular prediction.


Example:

    has_other_cards
        -1.2449

means that this feature contributed negatively toward the model's
fraud score for that prediction.


IMPORTANT:

SHAP values explain model behavior.

They do NOT establish causality.

Therefore:

    "The model increased the fraud score because..."

is more appropriate than:

    "This feature caused the application to be fraudulent."


============================================================
14. SHAP FACTOR STRUCTURE
============================================================

The API returns factors containing:

    feature
    shap_value
    direction


Example:

    {
        "feature": "housing_status_BA",
        "shap_value": 0.6641,
        "direction": "increases_fraud_score"
    }


Possible directions:

    increases_fraud_score

    decreases_fraud_score


The dashboard separates them into two groups.


============================================================
15. APPLICATION DETAILS
============================================================

After the model explanation, the dashboard displays the original
application features.

Examples:

    income
    customer_age
    credit_risk_score
    payment_type
    housing_status
    proposed_credit_limit
    foreign_request
    device_os
    velocity_6h
    velocity_24h
    velocity_4w
    etc.


The details are displayed in a table.

This allows the analyst to inspect the underlying application
rather than seeing only the model probability.


============================================================
16. DASHBOARD KPI ANALYTICS
============================================================

Phase 11.10 adds portfolio-level dashboard analytics.

The dashboard displays:

    Total Applications
    High-Risk Cases
    Scored Cases
    Average Fraud Probability
    New
    Reviewing
    Escalated
    Cleared


These metrics are calculated from the dashboard session state.


============================================================
17. TOTAL APPLICATIONS
============================================================

Total Applications represents the number of cases currently loaded
into the dashboard.

Current demonstration setup:

    5 cases


This is dashboard data, not a production application database.


============================================================
18. SCORED CASES
============================================================

Scored Cases represents the number of cases for which the FastAPI
model has actually been called during the dashboard session.

For example:

    Total Cases = 5
    Scored Cases = 2


means only two cases have been opened/scored so far.


============================================================
19. HIGH-RISK CASES
============================================================

High-Risk Cases counts scored cases whose API result contains:

    risk_level = HIGH


Unscored cases should not be treated as low-risk.

They simply do not have a model result yet.


============================================================
20. AVERAGE FRAUD PROBABILITY
============================================================

Average Fraud Probability is calculated only from scored cases.

Conceptually:

    average_probability =
        sum(scored probabilities)
        /
        number of scored cases


If no cases have been scored:

    average_probability = 0


This is important because unscored cases do not have a probability.


============================================================
21. RISK DISTRIBUTION
============================================================

The dashboard contains a risk distribution chart.

Categories:

    LOW
    MEDIUM
    HIGH


The chart counts scored cases in each category.

Example:

    LOW       3
    MEDIUM    1
    HIGH      1


The chart is generated from actual model results stored in:

    st.session_state["case_results"]


Therefore the chart changes as more cases are scored.


============================================================
22. CASE STATUS DISTRIBUTION
============================================================

The dashboard also displays analyst workflow status.

Categories:

    NEW
    REVIEWING
    ESCALATED
    CLEARED


Example:

    NEW          2
    REVIEWING    1
    ESCALATED    1
    CLEARED      1


This is different from risk distribution.

Risk distribution:

    Model output


Status distribution:

    Analyst workflow


============================================================
23. WHY RISK AND STATUS MUST BE SEPARATE
============================================================

Consider:

    Model:
        HIGH risk

    Analyst:
        REVIEWING


This means:

    The model considers the application high risk,
    but the analyst is still investigating it.


Another example:

    Model:
        LOW risk

    Analyst:
        REVIEWING


This can happen because the analyst may have additional information
that is not available to the model.

Therefore, the dashboard correctly separates:

    ML assessment

from:

    Human investigation workflow.


============================================================
24. TEST APPLICATION
============================================================

The second dashboard section is:

    🔍 Test Application


This is not the operational case queue.

It is a testing/simulation interface.

It allows the developer or analyst to manually enter application
features and send them to the model.


Workflow:

    Enter features
         ↓
    Submit
         ↓
    POST /predict/explain
         ↓
    FastAPI
         ↓
    Model
         ↓
    Probability + SHAP
         ↓
    Display result


============================================================
25. TEST APPLICATION INPUTS
============================================================

The Test Application accepts the raw model inputs.

Major groups include:

Applicant information:

    income
    customer_age
    employment_status
    housing_status
    payment_type
    name_email_similarity


Credit:

    credit_risk_score
    proposed_credit_limit


Identity/contact:

    email_is_free
    phone_home_valid
    phone_mobile_valid


Address:

    prev_address_months_count
    current_address_months_count


Banking:

    bank_months_count
    bank_branch_count_8w
    has_other_cards


Velocity:

    velocity_6h
    velocity_24h
    velocity_4w


Device/session:

    device_os
    device_distinct_emails_8w
    keep_alive_session
    session_length_in_minutes


Other:

    foreign_request
    source
    month
    days_since_request
    intended_balcon_amount
    zip_count_4w
    date_of_birth_distinct_emails_4w


============================================================
26. RAW INPUT → MODEL PIPELINE
============================================================

The dashboard sends raw features.

The dashboard does NOT perform preprocessing itself.

The backend handles preprocessing.

Pipeline:

    Raw Application
          ↓
    FastAPI schema validation
          ↓
    Model Service
          ↓
    Sentinel handling
          ↓
    Missing indicators
          ↓
    Preprocessor
          ↓
    Calibrated XGBoost
          ↓
    Probability
          ↓
    Threshold
          ↓
    Decision
          ↓
    SHAP explanation


This maintains a clean separation between frontend and model logic.


============================================================
27. SENTINEL VALUES
============================================================

Some application features use:

    -1

to indicate unavailable information.

The dashboard simply sends these values.

The model service handles them.

For example:

    prev_address_months_count = -1


The backend converts the sentinel representation into the
appropriate preprocessing representation.

This means the dashboard does not need to duplicate the ML
preprocessing logic.


============================================================
28. API HEALTH INDICATOR
============================================================

The sidebar checks:

    GET /health


The dashboard displays:

    🟢 API Online

or:

    🔴 API Offline


It also displays:

    Model Loaded
    Threshold


This gives the analyst/developer an immediate indication of whether
the inference backend is available.


============================================================
29. API ENDPOINTS USED BY PHASE 11
============================================================

The FastAPI backend exposes:

    GET /health

    POST /predict

    POST /predict/batch

    POST /predict/explain


Phase 11 primarily uses:

    /health

and:

    /predict/explain


because the analyst dashboard needs both:

    prediction

and:

    explanation.


============================================================
30. WHY /predict/explain IS USED
============================================================

The basic endpoint:

    /predict

returns the prediction.

The analyst dashboard needs more information.

Therefore:

    /predict/explain

returns:

    fraud_probability
    threshold
    risk_level
    decision
    SHAP factors


This avoids making a separate model request just to obtain the
explanation.


============================================================
31. ERROR HANDLING
============================================================

The dashboard handles API failures.

Example:

    requests.exceptions.RequestException


If FastAPI is unavailable, the dashboard displays an error instead
of crashing silently.


The Test Application also checks the HTTP response status.

For example:

    200
        → successful prediction

Other status codes:

    → display API error


============================================================
32. STREAMLIT RERUN BEHAVIOR
============================================================

Streamlit reruns the script when widgets are interacted with.

Therefore session state is essential.

Without session state:

    selected case
    model results
    analyst status

could be lost during reruns.


The dashboard uses:

    st.session_state


to preserve these values within the Streamlit session.


============================================================
33. PHASE 11 DATA FLOW
============================================================

Complete analyst workflow:

    1. Analyst opens dashboard.

    2. Dashboard checks FastAPI /health.

    3. Analyst sees case queue.

    4. Analyst selects CASE-XXXX.

    5. Dashboard sends raw application features.

    6. FastAPI validates the request.

    7. Model service preprocesses the application.

    8. Calibrated XGBoost generates probability.

    9. Threshold is applied.

   10. SHAP explanation is generated.

   11. API returns result.

   12. Dashboard displays:
          - probability
          - threshold
          - risk
          - model decision

   13. Dashboard displays SHAP factors.

   14. Analyst inspects application features.

   15. Analyst changes workflow status.

   16. Dashboard analytics update.


============================================================
34. MODEL OUTPUT VS BUSINESS WORKFLOW
============================================================

The project deliberately separates:

                MACHINE LEARNING
                      │
                      ▼
             Fraud Probability
                      │
                      ▼
                  Threshold
                      │
                      ▼
              Model Decision
                      │
                      │
                      ▼
               ANALYST REVIEW
                      │
             ┌────────┴────────┐
             ▼                 ▼
          CLEARED           ESCALATED


This is more realistic than implementing:

    model says fraud
        ↓
    automatically reject customer


The ML model acts as a decision-support component.


============================================================
35. WHAT PHASE 11 DOES NOT DO
============================================================

Phase 11 does NOT:

- retrain the model
- modify XGBoost
- modify calibration
- change the threshold
- perform database persistence
- implement authentication
- implement role-based access
- deploy to cloud
- provide a production customer-facing application
- automatically reject applications
- claim synthetic cases are real customers


These belong to later production/deployment work if required.


============================================================
36. REAL-TIME INTERPRETATION
============================================================

The project can demonstrate real-time APPLICATION scoring:

    Application submitted
          ↓
    API request
          ↓
    Model inference
          ↓
    Risk result


However, the BAF dataset represents bank-account/application fraud
rather than a literal high-frequency transaction stream.

Therefore the dashboard should be described accurately as:

    "real-time fraud risk scoring for bank account/application
     submissions"

rather than claiming it is a production transaction-streaming
system.


============================================================
37. PHASE 11 TECHNOLOGY STACK
============================================================

Frontend / Dashboard:

    Streamlit


Backend:

    FastAPI


Inference server:

    Uvicorn


Machine Learning:

    XGBoost


Calibration:

    Isotonic calibration


Explainability:

    SHAP


Data processing:

    pandas
    NumPy


Model persistence:

    joblib / serialized artifacts


Communication:

    HTTP REST API


Visualization:

    Streamlit charts


============================================================
38. PHASE 11 FILE STRUCTURE
============================================================

Relevant project structure:

FRAUD_TRANSACTION_DETECTION_SYSTEM/
│
├── api/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   ├── model_service.py
│   └── explainer.py
│
├── dashboard/
│   └── app.py
│
├── notebooks/
│   └── artifacts/
│       ├── preprocessor.pkl
│       ├── calibrated_xgb.pkl
│       ├── feature_names...
│       └── other model artifacts
│
└── .venv/


============================================================
39. HOW TO RUN PHASE 11
============================================================

Terminal 1:

    cd C:\Users\mayan\Documents\projects\
    FRAUD_TRANSACTION_DETECTION_SYSTEM

Activate environment:

    .venv\Scripts\activate


Start FastAPI:

    uvicorn api.main:app --reload


Expected:

    http://127.0.0.1:8000


Terminal 2:

    cd C:\Users\mayan\Documents\projects\
    FRAUD_TRANSACTION_DETECTION_SYSTEM

Activate environment:

    .venv\Scripts\activate


Start dashboard:

    streamlit run dashboard/app.py


The dashboard opens in the browser.


============================================================
40. PHASE 11 TESTING CHECKLIST
============================================================

API:

    [✓] /health works
    [✓] /predict works
    [✓] /predict/batch works
    [✓] /predict/explain works


Dashboard:

    [✓] Dashboard starts
    [✓] Sidebar navigation works
    [✓] API health appears
    [✓] Case queue appears
    [✓] Case can be opened
    [✓] Case is scored
    [✓] Probability displayed
    [✓] Threshold displayed
    [✓] Risk displayed
    [✓] Model decision displayed
    [✓] SHAP factors displayed
    [✓] Application details displayed
    [✓] Start Review works
    [✓] Clear Case works
    [✓] Escalate works
    [✓] Multiple cases supported
    [✓] Portfolio analytics displayed
    [✓] Risk chart displayed
    [✓] Status chart displayed
    [✓] Test Application works


============================================================
41. IMPORTANT DESIGN DECISIONS
============================================================

DECISION 1:

Keep the ML model inside FastAPI rather than Streamlit.

Reason:

    Separates UI from inference.


DECISION 2:

Use the saved calibrated model.

Reason:

    Dashboard must use the finalized model rather than retraining
    or creating another model.


DECISION 3:

Use /predict/explain for analyst investigations.

Reason:

    Analysts need explanations in addition to probability.


DECISION 4:

Keep analyst status separate from model decision.

Reason:

    ML output is a risk signal, not the complete human workflow.


DECISION 5:

Keep synthetic cases clearly identifiable as demonstrations.

Reason:

    Avoid representing fabricated applications as real banking data.


DECISION 6:

Calculate dashboard analytics dynamically.

Reason:

    Metrics should reflect the current dashboard session rather
    than hard-coded numbers.


============================================================
42. PHASE 11 PERFORMANCE CONTEXT
============================================================

The backend benchmark from Phase 10 showed approximately:

Single prediction:

    Mean ≈ 14.45 ms
    P50  ≈ 13.93 ms
    P95  ≈ 20.32 ms
    P99  ≈ 23.59 ms


Batch inference:

    Batch 10:
        ≈ 4.60 ms/request

    Batch 50:
        ≈ 3.37 ms/request

    Batch 100:
        ≈ 2.94 ms/request

    Batch 500:
        ≈ 2.94 ms/request


SHAP endpoint:

    Mean ≈ 31.54 ms
    P50  ≈ 23.70 ms
    P95  ≈ 89.81 ms
    P99  ≈ 109.75 ms


Therefore the standard prediction endpoint is considerably faster
than the explanation endpoint.

This is acceptable because SHAP is mainly used for analyst
investigation rather than every high-volume scoring request.


============================================================
43. PHASE 11 OUTPUT
============================================================

At the end of Phase 11, the project has evolved from:

    ML Notebook
        ↓
    Trained Fraud Model


into:

    ML Model
        ↓
    FastAPI Inference Service
        ↓
    Analyst Dashboard
        ↓
    Case Investigation Workflow
        ↓
    Explainable Fraud Risk Assessment


This creates an end-to-end prototype rather than only an ML
notebook.


============================================================
44. PHASE 11 FINAL ARCHITECTURE
============================================================

                         USER
                          │
                          ▼
              ┌──────────────────────┐
              │ Streamlit Dashboard  │
              │                      │
              │ Analyst Console      │
              │ Test Application     │
              │ Analytics            │
              └──────────┬───────────┘
                         │
                         │ REST
                         ▼
              ┌──────────────────────┐
              │      FastAPI         │
              │                      │
              │ /health              │
              │ /predict             │
              │ /predict/batch       │
              │ /predict/explain     │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   Model Service      │
              │                      │
              │ Preprocessor         │
              │ Calibrated XGBoost   │
              │ SHAP Explainer       │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │     Artifacts        │
              │                      │
              │ preprocessor.pkl     │
              │ calibrated_xgb.pkl   │
              └──────────────────────┘


============================================================
45. PHASE 11 COMPLETION STATUS
============================================================

PHASE 11 — DASHBOARD & ANALYST WORKFLOW

    11.1  Streamlit setup                         ✓
    11.2  Analyst Console                         ✓
    11.3  FastAPI integration                     ✓
    11.4  Case queue                              ✓
    11.5  Real model scoring                      ✓
    11.6  SHAP investigation                      ✓
    11.7  Application details                     ✓
    11.8  Analyst workflow statuses               ✓
    11.9  Multiple cases                          ✓
    11.10 Dashboard analytics                     ✓


FINAL STATUS:

    PHASE 11 COMPLETE


============================================================
46. TRANSITION TO PHASE 12
============================================================

After Phase 11:

    Phase 1–9
        ↓
    ML development + validation + explainability
        ↓
    Phase 10
        ↓
    FastAPI inference service
        ↓
    Phase 11
        ↓
    Analyst dashboard
        ↓
    Phase 12
        ↓
    Production hardening + deployment


Phase 12 will focus on making the existing system more
production-ready rather than changing the ML methodology.

Main Phase 12 areas:

    12.1 API production hardening
    12.2 Configuration and environment variables
    12.3 Structured logging
    12.4 Automated testing
    12.5 Dockerization
    12.6 Deployment
    12.7 Final documentation
    12.8 Final end-to-end system review


============================================================
END OF PHASE 11
============================================================
```
