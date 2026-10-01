PHASE 9 — EXPLAINABILITY & FRAUD CASE INVESTIGATION

OBJECTIVE

The objective of Phase 9 is to make the fraud detection model interpretable for fraud analysts.

Instead of only producing a fraud probability, the system should explain:

- Why a case received its score
- Which features increased the fraud score
- Which features decreased the fraud score
- Why a case was flagged
- Why a fraud case was missed
- Why a legitimate case was incorrectly flagged

SHAP (SHapley Additive exPlanations) was used for model-level and individual-level explanations.

Important:
SHAP explains model behavior.
It does NOT establish causality or prove that a feature caused fraud.


1. PHASE 9 INPUTS

The following artifacts from previous phases were loaded:

- preprocessor.pkl
- calibrated_xgb.pkl
- X_val_processed.npy
- y_val.npy
- shap_values.npy
- fraud_shap.npy
- feature_names.txt
- project_results_through_phase_8.json

Loaded data:

- X_val_processed: (150000, 55)
- y_val: (150000,)
- SHAP values: (10000, 55)
- Feature names: 55

Important:

SHAP values were calculated only for the first 10,000 validation samples.

Therefore, SHAP-based TP/FP/FN comparisons are limited to those 10,000 samples.


2. GLOBAL SHAP FEATURE IMPORTANCE

Mean absolute SHAP values were calculated:

mean_abs_shap = mean(abs(SHAP))

Top features:

Rank    Feature                                      Mean |SHAP|

1       housing_status_BA                            0.511402
2       device_os_windows                            0.417484
3       phone_home_valid                             0.393635
4       keep_alive_session                           0.376641
5       has_other_cards                              0.343633
6       name_email_similarity                        0.324145
7       prev_address_months_count_missing            0.322524
8       current_address_months_count                 0.285160
9       income                                       0.273786
10      email_is_free                                0.260326
11      bank_branch_count_8w                         0.220051
12      intended_balcon_amount                       0.197063
13      credit_risk_score                             0.166055
14      velocity_4w                                  0.156407
15      days_since_request                            0.152509
16      zip_count_4w                                  0.135980
17      customer_age                                  0.135887
18      month                                         0.135569
19      bank_months_count                             0.130973
20      date_of_birth_distinct_emails_4w              0.116693

Interpretation:

Mean absolute SHAP measures the magnitude of a feature's influence on the model.

It does NOT indicate whether the feature increases or decreases fraud risk.


3. SHAP DIRECTION ANALYSIS

For each feature, the following were calculated:

- Mean SHAP
- Mean absolute SHAP
- Percentage of positive SHAP values
- Percentage of negative SHAP values
- Percentage of zero SHAP values

Examples:

housing_status_BA:
- Mean SHAP: -0.2503
- Mean |SHAP|: 0.5114
- Positive: 17.09%
- Negative: 82.91%

device_os_windows:
- Mean SHAP: -0.1278
- Mean |SHAP|: 0.4175
- Positive: 26.80%
- Negative: 73.20%

phone_home_valid:
- Mean SHAP: -0.0684
- Mean |SHAP|: 0.3936
- Positive: 58.73%
- Negative: 41.27%

Important:

A negative mean SHAP does not mean a feature is inherently protective.

SHAP contributions are instance-dependent and describe how the model moves its prediction for individual observations.


4. GLOBAL SHAP ARTIFACTS

Saved:

- artifacts/global_shap_importance.csv
- artifacts/shap_direction_analysis.csv


5. INDIVIDUAL CASE EXPLANATION

A reusable explain_case() function was created.

It produces:

- Fraud probability
- Threshold
- Alert decision
- SHAP contribution of every feature
- Top positive contributors
- Top negative contributors

Phase 8 F1-selected operating threshold:

0.09


6. FALSE NEGATIVE INVESTIGATION

At threshold 0.09 on the validation set:

- Fraud cases: 1,655
- False negatives: 1,036
- False-negative rate: 62.60%
- Fraud capture rate / recall: 37.40%

The highest-probability false negatives were close to the decision boundary.

Examples:

Validation Index     Probability

142450               0.089133
133139               0.088671
85838                0.088647
141771               0.088086
111350               0.087969

These cases are important because they are fraud cases that were close to being flagged.

A false negative is:

Actual fraud
+
Predicted as not fraud


7. FALSE POSITIVE INVESTIGATION

At threshold 0.09:

- Legitimate cases: 148,345
- False positives: 2,795
- False-positive rate: 1.88%

Highest-confidence false positives included:

Validation Index     Probability

135988               0.756410
29300                0.704301
80820                0.680059
60089                0.668948
61712                0.653138

These cases are particularly useful because the model assigned high fraud probabilities even though the actual label was legitimate.

A false positive is:

Actual legitimate
+
Predicted as fraud


8. TRUE POSITIVE INVESTIGATION

At threshold 0.09:

- Fraud cases: 1,655
- True positives: 619
- Fraud capture rate: 37.40%

Highest-confidence true positives:

Validation Index     Probability

122301               0.994575
93063                0.979660
118417               0.977023
100775               0.886133
99512                0.804399

The highest-confidence true positive had a fraud probability of 99.46%.


9. TP / FP / FN SHAP COMPARISON

SHAP comparison was performed using the first 10,000 validation rows.

Available cases:

- TP: 49
- FP: 184
- FN: 78

Top features by SHAP magnitude across these groups included:

- housing_status_BA
- device_os_windows
- phone_home_valid
- keep_alive_session
- name_email_similarity
- income
- current_address_months_count
- email_is_free
- bank_branch_count_8w
- credit_risk_score

Important observation:

Some features have strong SHAP influence in both true positives and false positives.

For example:

housing_status_BA:
- TP mean |SHAP| = 0.6764
- FP mean |SHAP| = 0.6899
- FN mean |SHAP| = 0.5564

device_os_windows:
- TP mean |SHAP| = 0.4512
- FP mean |SHAP| = 0.4524
- FN mean |SHAP| = 0.4404

This indicates that the model can use similar feature patterns when making both correct and incorrect predictions.

The comparison is a diagnostic sample, not a population-level SHAP analysis for all 150,000 validation rows.


10. REPRESENTATIVE TRUE POSITIVE

Validation index:

122301

Actual label:
- Fraud

Fraud probability:
- 0.994575

Threshold:
- 0.09

Decision:
- FLAGGED

Top factors increasing fraud score:

1. Proposed Credit Limit       +0.8889
2. Credit Risk Score            +0.7806
3. Housing Status = BA          +0.6673
4. Device OS = Windows          +0.4466
5. Income                        +0.4056

Top factors decreasing fraud score:

1. Velocity 24H                 -0.1006
2. Zip Count 4W                 -0.0506
3. Device Distinct Emails 8W   -0.0358
4. Customer Age                 -0.0273
5. Phone Mobile Valid           -0.0234


11. REPRESENTATIVE FALSE POSITIVE

Validation index:

135988

Actual label:
- Legitimate

Fraud probability:
- 0.756410

Threshold:
- 0.09

Decision:
- FLAGGED

Top factors increasing fraud score:

1. Proposed Credit Limit       +0.9908
2. Housing Status = BA          +0.6575
3. Credit Risk Score             +0.5273
4. Device OS = Windows           +0.4600
5. Income                         +0.4230

Top factors decreasing fraud score:

1. Name Email Similarity         -0.1386
2. Bank Months Count              -0.1292
3. Zip Count 4W                   -0.0554
4. Customer Age                   -0.0433
5. Device Distinct Emails 8W     -0.0365

Important observation:

The false positive has a feature pattern that the model strongly associates with fraud.

This demonstrates that the model can produce high fraud scores for legitimate cases.


12. REPRESENTATIVE FALSE NEGATIVE

Validation index:

142450

Actual label:
- Fraud

Fraud probability:
- 0.089133

Threshold:
- 0.09

Decision:
- NOT FLAGGED

Top factors increasing fraud score:

1. Credit Risk Score             +0.8168
2. Housing Status = BA           +0.6413
3. Foreign Request                +0.5925
4. Device OS = Windows            +0.4369
5. Income                          +0.4044

Top factors decreasing fraud score:

1. Prev Address Months Count Missing      -0.7023
2. Name Email Similarity                   -0.5259
3. Month                                    -0.2498
4. Bank Branch Count 8W                    -0.2398
5. Date of Birth Distinct Emails 4W       -0.2171

Important observation:

This case contains strong positive fraud signals, but strong negative contributions pull the final model score below the 0.09 threshold.

Therefore:

Probability = 8.9133%
Threshold = 9.0%

Result:

NOT FLAGGED


13. HUMAN-READABLE FEATURE NAMES

Technical processed feature names were converted into analyst-friendly names.

Examples:

num__credit_risk_score
→ Credit Risk Score

cat__housing_status_BA
→ Housing Status = BA

cat__device_os_windows
→ Device OS = Windows

num__name_email_similarity
→ Name Email Similarity

num__prev_address_months_count_missing
→ Prev Address Months Count = Missing


14. ANALYST-FRIENDLY RISK SUMMARY

A production-style explanation function was created.

Output structure:

- Fraud probability
- Risk level
- Decision
- Threshold
- Top risk factors
- Factors decreasing fraud score

Example:

Fraud Probability:
99.46%

Risk Level:
HIGH

Decision:
FLAG FOR INVESTIGATION

Threshold:
9.00%


Top Factors Increasing Fraud Score:

- Proposed Credit Limit
- Credit Risk Score
- Housing Status = BA
- Device OS = Windows
- Income


Factors Decreasing Fraud Score:

- Velocity 24H
- Zip Count 4W
- Device Distinct Emails 8W
- Customer Age
- Phone Mobile Valid


15. TERMINOLOGY NOTE

Negative SHAP contributors should preferably be described as:

"Factors decreasing the model's fraud score"

rather than:

"Protective factors"

because SHAP does not establish that these variables are actually protective or causal.


16. SAVED PHASE 9 ARTIFACTS

The following files were successfully created:

artifacts/global_shap_importance.csv

artifacts/shap_direction_analysis.csv

artifacts/fraud_case_investigation.csv

artifacts/analyst_fraud_explanation.json


17. PHASE 9 FINAL CONCLUSION

Phase 9 transformed the fraud classifier from a black-box prediction system into an interpretable fraud investigation system.

The system can now:

- Generate fraud probabilities
- Apply the selected operating threshold
- Identify flagged cases
- Explain individual predictions using SHAP
- Identify factors increasing the fraud score
- Identify factors decreasing the fraud score
- Investigate true positives
- Investigate false positives
- Investigate false negatives
- Produce human-readable explanations
- Save investigation reports for downstream applications

The analysis showed that:

- True positives can contain strong positive fraud signals.
- False positives can have very similar fraud-related feature patterns.
- False negatives can contain strong fraud signals that are offset by negative SHAP contributions.
- SHAP explanations describe model behavior rather than causality.
- Individual explanations are useful for analyst investigation and debugging.

FINAL PHASE 9 PIPELINE:

Application
    ↓
Preprocessing
    ↓
Calibrated XGBoost
    ↓
Fraud Probability
    ↓
Threshold = 0.09
    ↓
Alert / No Alert
    ↓
SHAP Explanation
    ↓
Top Risk Factors
    ↓
Top Factors Decreasing Fraud Score
    ↓
Analyst Investigation Report


PHASE STATUS:

Phase 1  → EDA                         ✓
Phase 2  → Preprocessing               ✓
Phase 3  → Baseline XGBoost            ✓
Phase 4  → Tuning + Calibration        ✓
Phase 5  → Isolation Forest            ✓
Phase 6  → SHAP                        ✓
Phase 7  → Temporal Evaluation         ✓
Phase 8  → Cost-Sensitive Threshold    ✓
Phase 9  → Explainability              ✓

NEXT:

Phase 10 — Real-Time Fraud Scoring / FastAPI