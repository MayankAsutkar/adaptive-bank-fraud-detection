# Phase 3 — Baseline Fraud Detection Model

## Objective

Build a baseline supervised fraud detection model using **XGBoost** before performing hyperparameter tuning or adding other detection methods.

The baseline is used to:

* Establish initial model performance.
* Understand the effect of class imbalance.
* Evaluate fraud detection at different probability thresholds.
* Identify important features.
* Provide a reference point for future model improvements.

---

# 1. Class Imbalance

The dataset contains approximately:

* Legitimate: 98.9%
* Fraud: 1.1%

Overall fraud rate:

```text
1.1029%
```

Therefore, fraud is a highly imbalanced minority class.

### Why this matters

A model could achieve very high accuracy by predicting most/all observations as legitimate while detecting very little fraud.

Therefore, **accuracy is not an appropriate primary metric** for this problem.

Important metrics:

* PR-AUC → primary
* ROC-AUC → secondary
* Precision
* Recall
* F1-score
* Confusion matrix

---

# 2. Class Weighting

For XGBoost, class imbalance was handled using:

```python
scale_pos_weight = number_of_legitimate / number_of_fraud
```

Implementation:

```python
neg = (y_train == 0).sum()
pos = (y_train == 1).sum()

scale_pos_weight = neg / pos
```

The resulting value is approximately:

```text
~89.7
```

This reflects the approximate ratio:

```text
90 legitimate : 1 fraud
```

### Why `scale_pos_weight`?

It increases the importance of the minority fraud class during model training.

It does **not**:

* create synthetic fraud observations,
* duplicate fraud rows,
* change the validation/test distribution.

It only changes the training loss weighting.

---

# 3. Baseline XGBoost

Initial model:

```python
model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=scale_pos_weight,
    objective='binary:logistic',
    eval_metric='aucpr',
    random_state=42,
    n_jobs=-1
)
```

### Parameter reasoning

* `n_estimators=300`

  * Number of boosting trees.
  * Used as a reasonable baseline rather than a tuned value.

* `max_depth=6`

  * Controls tree complexity.
  * Moderate depth provides enough capacity while avoiding an unnecessarily complex baseline.

* `learning_rate=0.1`

  * Controls the contribution of each boosting iteration.

* `subsample=0.8`

  * Uses 80% of training observations per boosting iteration.

* `colsample_bytree=0.8`

  * Uses 80% of features for each tree.

* `scale_pos_weight`

  * Addresses the strong fraud/legitimate class imbalance.

* `objective='binary:logistic'`

  * Binary classification with fraud as the positive class.

* `eval_metric='aucpr'`

  * PR-AUC is especially relevant because fraud is rare.

* `random_state=42`

  * Ensures reproducibility.

* `n_jobs=-1`

  * Uses available CPU cores.

### Important

These parameters were **not considered final/tuned hyperparameters**.

They were used only to establish a baseline.

---

# 4. Fraud Probability

The model generates a probability of belonging to the fraud class:

```python
y_val_prob = model.predict_proba(X_val_processed)[:, 1]
```

The output is a continuous score between 0 and 1.

Example:

```text
0.02 → relatively low fraud score
0.70 → relatively high fraud score
0.95 → very high fraud score
```

The probability is later converted into a binary decision using a threshold.

---

# 5. ROC-AUC

Validation ROC-AUC:

```text
0.8859
```

ROC-AUC measures the model's ability to rank fraudulent cases above legitimate cases across different classification thresholds.

A value of approximately 0.886 indicates that the baseline has meaningful discrimination between the two classes.

ROC-AUC does **not** mean that 88.6% of predictions are correct.

---

# 6. PR-AUC

Validation PR-AUC:

```text
0.1591
```

The dataset's fraud prevalence is approximately:

```text
0.011
```

Therefore, the model's PR-AUC is substantially above the approximate random-classifier baseline represented by the positive-class prevalence.

PR-AUC was treated as the **primary evaluation metric** because the positive fraud class is highly rare.

### Why PR-AUC is important

Precision-recall performance focuses directly on the minority/fraud class.

ROC-AUC can remain relatively high even when a model produces many false positives in a highly imbalanced dataset.

---

# 7. Default Threshold Analysis

Initially evaluated the default threshold:

```text
threshold = 0.5
```

Decision rule:

```text
P(fraud) >= 0.5 → fraud
P(fraud) < 0.5  → legitimate
```

Validation confusion matrix:

```text
[[131841  16504]
 [   517   1138]]
```

Therefore:

```text
TN = 131,841
FP = 16,504
FN = 517
TP = 1,138
```

### Fraud-class metrics at threshold 0.5

```text
Precision = 6.45%
Recall    = 68.76%
F1        = 11.79%
```

### Interpretation

The model detects a substantial portion of fraud:

```text
Recall ≈ 68.8%
```

but generates many false-positive alerts:

```text
FP = 16,504
```

Therefore, the default threshold of 0.5 is not automatically suitable for deployment.

---

# 8. Threshold Analysis

Because XGBoost produces continuous fraud probabilities, different thresholds were evaluated.

Thresholds tested:

```text
0.05 → 0.95
```

For every threshold we calculated:

* Precision
* Recall
* F1
* Number of predicted fraud cases
* Number of actual fraud cases detected

### Selected results

| Threshold | Precision | Recall |    F1 | Alerts | Fraud Detected |
| --------: | --------: | -----: | ----: | -----: | -------------: |
|      0.50 |     6.45% | 68.76% | 0.118 | 17,642 |          1,138 |
|      0.60 |     7.96% | 62.18% | 0.141 | 12,929 |          1,029 |
|      0.70 |    10.12% | 54.20% | 0.171 |  8,862 |            897 |
|      0.80 |    13.62% | 43.63% | 0.208 |  5,300 |            722 |
|      0.85 |    16.35% | 36.13% | 0.225 |  3,657 |            598 |
|      0.90 |    20.39% | 26.22% | 0.229 |  2,129 |            434 |
|      0.95 |    32.03% | 13.90% | 0.194 |    718 |            230 |

---

# 9. Precision–Recall Trade-off

The threshold analysis showed a clear relationship:

```text
Threshold increases
        ↓
Precision generally increases
        ↓
Recall generally decreases
```

Lower threshold:

```text
More cases flagged
→ More fraud detected
→ More false positives
```

Higher threshold:

```text
Fewer cases flagged
→ Fewer false positives
→ More fraud missed
```

Therefore, there is no universally correct threshold.

---

# 10. F1-Based Threshold

Among the tested thresholds, the maximum F1 occurred at:

```text
Threshold = 0.90
```

Results:

```text
Precision = 20.39%
Recall    = 26.22%
F1        = 22.94%
```

However, **0.90 was not selected as the final production threshold**.

### Reason

F1 treats precision and recall equally.

A real fraud detection system may have different costs for:

* False Positive → legitimate customer incorrectly flagged.
* False Negative → fraudulent application incorrectly accepted.

Therefore, the final threshold should eventually be selected based on the system's operational/business requirements rather than F1 alone.

---

# 11. Operational Threshold Analysis

The threshold analysis also considered the number of cases that would be flagged.

For example:

### Threshold = 0.50

```text
17,642 cases flagged
1,138 fraud cases detected
```

### Threshold = 0.90

```text
2,129 cases flagged
434 fraud cases detected
```

Increasing the threshold therefore substantially reduces the number of alerts, but also reduces the number of fraud cases detected.

This is important for a practical fraud detection system because a model must consider both:

* fraud detection capability,
* investigation/alert workload.

---

# 12. Feature Importance

XGBoost feature importance was extracted using:

```python
feature_importance = pd.DataFrame({
    'feature': feature_names,
    'importance': model.feature_importances_
})
```

Top features from the baseline:

| Rank | Feature                     | Importance |
| ---: | --------------------------- | ---------: |
|    1 | `housing_status_BA`         |     0.1261 |
|    2 | `device_os_windows`         |     0.0760 |
|    3 | `prev_address_missing`*     |     0.0530 |
|    4 | `has_other_cards`           |     0.0529 |
|    5 | `phone_home_valid`          |     0.0495 |
|    6 | `keep_alive_session`        |     0.0479 |
|    7 | `email_is_free`             |     0.0322 |
|    8 | `employment_status_CA`      |     0.0252 |
|    9 | `housing_status_BE`         |     0.0251 |
|   10 | `device_distinct_emails_8w` |     0.0247 |

*The initial baseline output contained duplicate/old missingness indicators. This was identified as a preprocessing issue after restarting the notebook.

The old indicators were removed and the preprocessing pipeline was corrected to retain only the four intended descriptive missingness indicators.

### Important interpretation

Feature importance does **not** mean:

```text
"feature X causes fraud"
```

or:

```text
"feature X contributes exactly X% of fraud"
```

It represents how useful the feature was to the trained XGBoost trees according to the selected feature-importance measure.

It also does not provide the same type of explanation as SHAP.

---

# 13. Zero-Importance Features

The initial baseline showed zero importance for:

```text
device_distinct_emails_8w_missing
housing_status_BG
```

These were **not automatically removed**.

Reason:

A feature having zero importance in one baseline model does not prove that it is useless.

Feature usage can change after:

* hyperparameter tuning,
* different tree structures,
* different regularization,
* model changes.

Therefore, feature removal should be based on stronger evidence rather than a single baseline importance result.

---

# 14. Preprocessing Issue Identified During Phase 3

After restarting the notebook, duplicate missingness indicators were discovered:

```text
Old:
prev_address_missing
current_address_missing
bank_months_missing
device_emails_missing
```

and:

```text
Intended:
prev_address_months_count_missing
current_address_months_count_missing
bank_months_count_missing
device_distinct_emails_8w_missing
```

The old four indicators were removed.

The sentinel preprocessing was corrected to create only the descriptive indicators.

Final intended missingness indicators:

```text
prev_address_months_count_missing
current_address_months_count_missing
bank_months_count_missing
device_distinct_emails_8w_missing
```

This ensures that the model does not receive duplicate representations of the same missingness information.

---

# 15. Why XGBoost Was Used

XGBoost was selected as the first supervised model because the dataset contains:

* numerical features,
* categorical features after encoding,
* nonlinear relationships,
* feature interactions,
* highly imbalanced target classes.

Tree-based boosting can naturally capture nonlinear relationships and interactions without requiring feature scaling.

Therefore:

```text
StandardScaler → not required for XGBoost
```

The model can learn interactions such as:

```text
customer characteristics
        +
device information
        +
identity signals
        +
behavioral signals
        ↓
fraud prediction
```

---

# 16. What Was Considered but Not Done Yet

### No hyperparameter tuning yet

The baseline parameters were intentionally kept fixed.

Tuning will be performed later to determine whether the model can improve beyond:

```text
ROC-AUC = 0.8859
PR-AUC  = 0.1591
```

### No final threshold selected

Threshold `0.90` gave the highest F1 among the tested thresholds, but it is not considered the final production threshold.

### No synthetic oversampling

We used:

```text
scale_pos_weight
```

rather than immediately applying SMOTE or another oversampling technique.

This keeps the baseline simple and provides a clean reference point.

### No anomaly model yet

XGBoost is currently the supervised component.

An unsupervised model such as **Isolation Forest** can be introduced later to provide an independent anomaly signal.

---

# Phase 3 Baseline Summary

```text
Dataset fraud rate       ≈ 1.1029%

Model                    XGBoost
Class imbalance          scale_pos_weight ≈ 89.7

Validation ROC-AUC       0.8859
Validation PR-AUC        0.1591

Threshold = 0.50
Precision                6.45%
Recall                   68.76%
F1                       11.79%

Best tested F1 threshold
Threshold                0.90
Precision                20.39%
Recall                   26.22%
F1                       22.94%
```

## Phase 3 Conclusion

The baseline XGBoost model demonstrates meaningful ability to distinguish fraudulent from legitimate applications.

However, the default 0.5 threshold generates a large number of false-positive alerts. Increasing the threshold improves precision but reduces fraud recall.

Therefore, **threshold selection should be treated as a separate decision from model training** and should eventually be based on operational/business costs.

The baseline also provides a reference point for evaluating future model improvements.

### Phase 3 Status

**Baseline XGBoost: COMPLETE ✅**

### Next Phase

**Phase 4 — Model Improvement & Tuning**

1. Hyperparameter tuning.
2. Optimize primarily for PR-AUC.
3. Compare tuned model against baseline.
4. Re-evaluate threshold after tuning.
5. Analyze whether calibration is needed.
6. Select the final supervised model.
7. Later introduce an anomaly-detection component such as Isolation Forest.
