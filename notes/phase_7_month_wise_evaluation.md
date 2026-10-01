PHASE 7 — TEMPORAL EVALUATION & TIME-BASED ROBUSTNESS

OBJECTIVE
Evaluate whether the fraud detection model remains effective on future time periods rather than only on a random train/test split.

A random split can contain observations from different months in both training and testing. Temporal evaluation better represents production deployment, where the model is trained on past data and applied to future data.


1. DATASET VERIFICATION

Dataset:
- Rows: 1,000,000
- Columns: 32
- Target: fraud_bool
- Months: 0–7
- Fraud cases: 11,029
- Overall fraud rate: 1.1029%


2. MONTHLY FRAUD DISTRIBUTION

Month    Samples    Fraud Count    Fraud Rate
0        132,440    1,500          1.133%
1        127,620    1,198          0.939%
2        136,979    1,198          0.875%
3        150,936    1,392          0.922%
4        127,691    1,452          1.137%
5        119,323    1,411          1.183%
6        108,168    1,450          1.341%
7         96,843    1,428          1.475%

Observation:
- Fraud rate generally increases toward the later months.
- Month 2 has the lowest fraud rate: 0.875%.
- Month 7 has the highest fraud rate: 1.475%.


3. CHRONOLOGICAL SPLIT

Train       → Months 0–4
Validation  → Month 5
Test        → Months 6–7

Train:
- Rows: 675,666
- Fraud rate: 0.998%

Validation:
- Rows: 119,323
- Fraud rate: 1.183%

Test:
- Rows: 205,011
- Fraud rate: 1.404%

Temporal structure:

Past                                      Future
Months 0–4          → Month 5 → Months 6–7
TRAIN                  VAL          TEST


4. CHRONOLOGICAL PREPROCESSING

Preprocessing was rebuilt specifically for the temporal split.

Important:
- Preprocessor was fitted ONLY on chronological training data (months 0–4).
- Validation and test data were transformed using the train-fitted preprocessor.
- This prevents preprocessing leakage from future periods.

Steps:
1. Remove fraud_bool
2. Remove constant device_fraud_count
3. Create missing indicators
4. Replace sentinel -1 values with NaN
5. Median imputation for numerical features
6. One-hot encoding for categorical features

Sentinel columns:
- prev_address_months_count
- current_address_months_count
- bank_months_count
- device_distinct_emails_8w

Processed shapes:
- Train: 675666 × 55
- Validation: 119323 × 55
- Test: 205011 × 55

NaN after preprocessing:
- Train: 0
- Validation: 0
- Test: 0


5. CHRONOLOGICAL XGBOOST

The same tuned XGBoost configuration from Phase 4 was used.

Configuration:
- n_estimators = 500
- max_depth = 4
- min_child_weight = 1
- learning_rate = 0.05
- subsample = 0.8
- colsample_bytree = 0.8
- reg_alpha = 0
- reg_lambda = 1.0
- objective = binary:logistic
- eval_metric = aucpr

Chronological training fraud rate:
- 0.9975%

scale_pos_weight:
- 99.2472

The model was trained only on months 0–4.


6. TEMPORAL MODEL PERFORMANCE

Chronological Validation — Month 5:
- PR-AUC: 0.191810
- ROC-AUC: 0.896511

Chronological Test — Months 6–7:
- PR-AUC: 0.194496
- ROC-AUC: 0.893650


Comparison with Phase 4:

                         PR-AUC      ROC-AUC
Random Validation       0.173801     0.896297
Random Test             0.178377     0.903192
Temporal Validation     0.191810     0.896511
Temporal Test           0.194496     0.893650


Interpretation:
- ROC-AUC decreased from 0.9032 to 0.8937 on the future test period.
- This represents a modest reduction in ranking performance.
- PR-AUC increased from 0.1784 to 0.1945.
- However, PR-AUC is sensitive to fraud prevalence.
- Future test fraud rate is 1.404%, compared with approximately 1.103% in the random test.
- Therefore, the increase in PR-AUC should not automatically be interpreted as improved model quality.


7. MONTHLY TEMPORAL PERFORMANCE

Month 6:
- Samples: 108,168
- Fraud rate: 1.341%
- PR-AUC: 0.183427
- ROC-AUC: 0.893400

Month 7:
- Samples: 96,843
- Fraud rate: 1.475%
- PR-AUC: 0.215184
- ROC-AUC: 0.897068

Observations:
- ROC-AUC remained stable from month 6 to month 7.
- PR-AUC increased from 0.1834 to 0.2152.
- No progressive performance degradation was observed.
- Month 7 also has higher fraud prevalence.


8. FEATURE DISTRIBUTION DRIFT — PSI

Population Stability Index (PSI) was used to compare:

Reference:
- Training period = Months 0–4

Future:
- Test period = Months 6–7

The month feature was excluded because its distribution is intentionally different due to the chronological split.

PSI interpretation:
- PSI < 0.10 → Low drift
- PSI 0.10–0.25 → Moderate drift
- PSI > 0.25 → High drift


HIGH DRIFT FEATURES

Feature                              PSI
velocity_4w                          3.738602
velocity_24h                         1.891704
velocity_6h                          1.088614
zip_count_4w                         0.491041
date_of_birth_distinct_emails_4w     0.454782
credit_risk_score                    0.261348


MODERATE DRIFT

prev_address_months_count            0.110974


LOW DRIFT

21 features had PSI < 0.10.


Drift summary:
- High drift: 6 features
- Moderate drift: 1 feature
- Low drift: 21 features


9. IMPORTANT DRIFT FINDING

Strong distribution shifts were observed in:
- velocity_4w
- velocity_24h
- velocity_6h
- zip_count_4w
- date_of_birth_distinct_emails_4w
- credit_risk_score

The strongest drift was observed in velocity-related features.

Despite this feature drift, future ROC-AUC remained around 0.89.


10. PREDICTION DISTRIBUTION DRIFT

Raw XGBoost prediction distributions:

Dataset                         Mean      Std       Median
Train (Months 0–4)              0.2373    0.2452    0.1382
Validation (Month 5)             0.2028    0.2307    0.1058
Test (Months 6–7)                0.1964    0.2355    0.0922

Upper tail:

Dataset                         P95       P99
Train                           0.7892    0.9323
Validation                      0.7455    0.9201
Test                            0.7541    0.9257

Main observation:
- Mean prediction decreased from 0.2373 to 0.1964.
- Median prediction decreased from 0.1382 to 0.0922.
- Upper-tail predictions remained relatively stable.
- Therefore, the model score distribution shifted somewhat downward, but there was no dramatic collapse.

Important:
- These are raw XGBoost scores.
- They should NOT be interpreted directly as calibrated fraud probabilities.


11. FINAL PHASE 7 CONCLUSION

The model demonstrates reasonable temporal robustness over the available future periods.

Evidence:
- Future test ROC-AUC = 0.8937
- Month 6 ROC-AUC = 0.8934
- Month 7 ROC-AUC = 0.8971
- No major performance collapse was observed.

However:
- Significant feature-distribution drift exists.
- 6 features show high PSI.
- 1 feature shows moderate PSI.
- The prediction distribution shifts somewhat downward.

Therefore:

The model maintains useful ranking performance despite substantial feature-distribution changes. However, production deployment would require continuous monitoring of feature distributions, prediction distributions, and future model performance.


12. LIMITATIONS

1. Only months 0–7 are available.
2. Future evaluation contains only months 6–7.
3. This demonstrates robustness over the available future period, not guaranteed long-term robustness.
4. PSI indicates distribution shift, but feature drift does not automatically prove concept drift.
5. PR-AUC comparisons across periods with different fraud prevalence must be interpreted carefully.
6. Threshold 0.50 was used only for diagnostics.
7. The final Phase 4 production-style model used isotonic calibration and threshold 0.12.
8. The Phase 7 temporal model evaluated here was raw XGBoost.


FINAL TAKEAWAY

Temporal Split:
Months 0–4 → Train
Month 5     → Validation
Months 6–7  → Test

Future Test:
PR-AUC  = 0.1945
ROC-AUC = 0.8937

Feature Drift:
High     = 6 features
Moderate = 1 feature
Low      = 21 features

Overall:
The model retains strong temporal ranking performance despite substantial
feature-distribution changes. Continuous drift and performance monitoring
would be required for a production deployment.