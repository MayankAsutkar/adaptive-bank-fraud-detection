PHASE 5 & 6 — ANOMALY DETECTION AND EXPLAINABILITY

PHASE 5 — ISOLATION FOREST

Objective:
Evaluate whether unusual applications provide an additional fraud signal beyond XGBoost.

XGBoost learns known fraud patterns using fraud labels, while Isolation Forest detects unusual applications without using fraud labels.

Isolation Forest was trained on X_train_processed without using y_train.

Model:
IsolationForest(
    n_estimators=300,
    contamination='auto',
    random_state=42,
    n_jobs=-1
)

Anomaly scores were calculated as:
iso_val_score = -iso_model.score_samples(X_val_processed)

The negative sign is used because sklearn's score_samples gives lower values to more anomalous samples. Therefore, after inversion:
Higher score = More anomalous
Lower score = More normal

ISOLATION FOREST PERFORMANCE

Validation PR-AUC = 0.01295
Validation ROC-AUC = 0.53956

The validation fraud rate was approximately 1.10%, so Isolation Forest performed only slightly above the prevalence baseline.

Conclusion:
Isolation Forest was a weak standalone fraud detector.

ANOMALY SCORE DISTRIBUTION

Legitimate applications:
Mean anomaly score = 0.46447
Std = 0.02710

Fraudulent applications:
Mean anomaly score = 0.46867
Std = 0.02782

Fraudulent applications were slightly more anomalous on average, but the distributions overlapped heavily.

XGBOOST VS ISOLATION FOREST

Correlation between XGBoost predictions and Isolation Forest anomaly scores = 0.01949.

The two models produced largely different signals. However, low correlation does not automatically mean the anomaly signal is useful.

ANOMALY TAIL ANALYSIS

Overall fraud rate = 1.10%

Top 1% most anomalous applications:
Fraud rate = 2.33%

Top 2%:
Fraud rate = 1.80%

Top 5%:
Fraud rate = 1.56%

Top 10%:
Fraud rate = 1.53%

The most anomalous applications showed some fraud enrichment, but the improvement was modest.

XGBOOST + ISOLATION FOREST FUSION

XGBoost weight = 0.9, Isolation Forest weight = 0.1
PR-AUC = 0.16644
ROC-AUC = 0.84279

XGBoost weight = 0.8, Isolation Forest weight = 0.2
PR-AUC = 0.14727
ROC-AUC = 0.79342

XGBoost weight = 0.7, Isolation Forest weight = 0.3
PR-AUC = 0.12110
ROC-AUC = 0.75107

XGBoost weight = 0.6, Isolation Forest weight = 0.4
PR-AUC = 0.09179
ROC-AUC = 0.71261

XGBoost weight = 0.5, Isolation Forest weight = 0.5
PR-AUC = 0.06156
ROC-AUC = 0.67761

XGBoost-only validation PR-AUC = 0.17380.

Even the 90% XGBoost + 10% Isolation Forest combination reduced PR-AUC to 0.16644.

PHASE 5 CONCLUSION

Isolation Forest was evaluated as an independent anomaly detector but was not included in the final model because:

1. Standalone performance was weak.
2. Fraud and legitimate anomaly score distributions overlapped heavily.
3. Fusion with XGBoost reduced validation performance.

Therefore, the final supervised fraud detection system continues to use the calibrated XGBoost model without Isolation Forest fusion.


PHASE 6 — SHAP EXPLAINABILITY

Objective:
Understand why the XGBoost model predicts an application as fraudulent.

SHAP was used to provide both global and individual explanations.

SHAP SETUP

The fitted XGBoost estimator from the calibrated model was passed to SHAP TreeExplainer.

SHAP values were calculated for 10,000 validation samples.

SHAP output shape = (10000, 55)

This means 10,000 validation samples were explained across 55 processed features.

GLOBAL SHAP FEATURE IMPORTANCE

Mean absolute SHAP values were used to determine the overall importance of features.

Top features:

1. housing_status_BA
2. device_os_windows
3. phone_home_valid
4. keep_alive_session
5. has_other_cards
6. name_email_similarity
7. prev_address_months_count_missing
8. current_address_months_count
9. income
10. email_is_free
11. bank_branch_count_8w
12. intended_balcon_amount
13. credit_risk_score
14. velocity_4w
15. days_since_request

Important:
Mean absolute SHAP measures the magnitude of a feature's impact on the model prediction. It does not tell whether the feature increases or decreases fraud risk.

SHAP BEESWARM FINDINGS

housing_status_BA:
Associated with higher fraud risk.

device_os_windows:
Associated with higher fraud risk.

phone_home_valid:
Higher values generally push predictions toward lower risk.

keep_alive_session:
Higher values generally push predictions toward lower risk.

has_other_cards:
Generally associated with lower risk.

name_email_similarity:
Lower similarity is associated with higher fraud risk.

prev_address_months_count_missing:
Missing previous-address information increases risk.

income:
Higher income generally increases predicted risk.

credit_risk_score:
Higher values generally increase predicted risk.

velocity_4w:
Higher values generally increase predicted risk.

SHAP also captured nonlinear relationships that simple correlation analysis cannot fully describe.

INDIVIDUAL FRAUD CASE

One fraudulent validation sample was analyzed using SHAP.

Top SHAP contributions:

name_email_similarity:
Feature value = 0.0675
SHAP = +0.532
Effect = Increased fraud risk

housing_status_BA:
SHAP = -0.459
Effect = Decreased fraud risk

device_os_windows:
SHAP = -0.374
Effect = Decreased fraud risk

keep_alive_session:
Feature value = 0
SHAP = +0.347
Effect = Increased fraud risk

email_is_free:
SHAP = -0.343
Effect = Decreased fraud risk

phone_home_valid:
Feature value = 0
SHAP = +0.270
Effect = Increased fraud risk

velocity_4w:
Feature value = 4110.23
SHAP = +0.266
Effect = Increased fraud risk

customer_age:
Feature value = 20
SHAP = -0.224
Effect = Decreased fraud risk

current_address_months_count:
Feature value = 49
SHAP = +0.213
Effect = Increased fraud risk

bank_months_count:
Feature value = 31
SHAP = +0.199
Effect = Increased fraud risk

The strongest individual positive contributor for this case was low name-email similarity.

SHAP WATERFALL

The waterfall plot showed how individual features moved the prediction away from the model's baseline.

Important:
The waterfall explanation used the raw XGBoost output, not the calibrated fraud probability.

Therefore, a raw model output greater than 1 should NOT be interpreted as a probability greater than 100%.

SHAP VS EDA

Several SHAP findings were consistent with the earlier EDA:

Low name-email similarity -> Higher fraud risk
Housing status BA -> High importance
Windows device OS -> High importance
Higher income -> Higher predicted risk
Higher credit risk score -> Higher predicted risk
Velocity features -> Important
Missing address information -> Important

This consistency indicates that several important relationships discovered during EDA were also learned by the XGBoost model.

Important limitation:
SHAP explains model behavior and feature contribution. It does NOT establish causality.

FINAL STATUS

Phase 5:
Isolation Forest evaluated.
Standalone performance measured.
Anomaly tail analysis performed.
Fusion with XGBoost tested.
Isolation Forest rejected from final model.

Phase 6:
Global SHAP analysis completed.
SHAP feature importance completed.
SHAP beeswarm analysis completed.
Individual fraud case explained.
SHAP waterfall analyzed.
SHAP findings compared with EDA.

Phase 5 and Phase 6 are COMPLETE.