# Phase 4 — Model Improvement & Tuning

## Objective

Improve the baseline XGBoost fraud detection model through controlled hyperparameter tuning, evaluate generalization, select an operating threshold, and calibrate the predicted probabilities.

**Primary metric:** PR-AUC
**Secondary metric:** ROC-AUC

The test set was kept untouched until final model evaluation.

---

## 4.1 Baseline Model

The baseline XGBoost model was configured as follows:

```python
XGBClassifier(
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

Because the fraud class represents only approximately 1.1% of the dataset, class weighting was applied:

```text
scale_pos_weight ≈ 89.7
```

### Baseline Validation Performance

```text
PR-AUC  = 0.159113
ROC-AUC = 0.885867
```

---

## 4.2 Hyperparameter Tuning

Hyperparameters were tuned systematically by changing one parameter group at a time while keeping the remaining configuration fixed.

### Experiment 1 — max_depth

Tested values:

```text
max_depth = 4, 6, 8
```

| max_depth | PR-AUC   | ROC-AUC  |
| --------- | -------- | -------- |
| 4         | 0.171206 | 0.895162 |
| 6         | 0.164468 | 0.886097 |
| 8         | 0.135719 | 0.864256 |

**Conclusion:** `max_depth=4` produced the highest validation PR-AUC among the tested values. Increasing tree depth reduced performance, indicating that deeper trees were not beneficial for this dataset.

---

### Experiment 2 — min_child_weight

With `max_depth=4`, the following values were tested:

```text
min_child_weight = 1, 5, 10
```

| min_child_weight | PR-AUC   | ROC-AUC  |
| ---------------- | -------- | -------- |
| 1                | 0.171206 | 0.895162 |
| 5                | 0.170136 | 0.895109 |
| 10               | 0.169408 | 0.894523 |

**Conclusion:** Increasing `min_child_weight` did not improve performance. `min_child_weight=1` was retained.

---

### Experiment 3 — Learning Rate and Number of Trees

| learning_rate | n_estimators | PR-AUC   | ROC-AUC  |
| ------------- | ------------ | -------- | -------- |
| 0.05          | 500          | 0.173801 | 0.896297 |
| 0.10          | 300          | 0.171206 | 0.895162 |
| 0.15          | 200          | 0.167234 | 0.893779 |

**Conclusion:** `learning_rate=0.05` with `n_estimators=500` produced the highest validation PR-AUC among the tested configurations.

---

### Experiment 4 — subsample

| subsample | PR-AUC   | ROC-AUC  |
| --------- | -------- | -------- |
| 0.6       | 0.172035 | 0.895541 |
| 0.8       | 0.173801 | 0.896297 |
| 1.0       | 0.171543 | 0.895215 |

**Conclusion:** `subsample=0.8` was retained.

---

### Experiment 5 — colsample_bytree

| colsample_bytree | PR-AUC   | ROC-AUC  |
| ---------------- | -------- | -------- |
| 0.6              | 0.173722 | 0.896134 |
| 0.8              | 0.173801 | 0.896297 |
| 1.0              | 0.171491 | 0.896309 |

**Conclusion:** `colsample_bytree=0.8` was retained based on the primary metric, PR-AUC.

The difference between 0.6 and 0.8 was very small, so no major performance advantage should be claimed.

---

### Experiment 6 — L1 Regularization

Tested `reg_alpha` values:

| reg_alpha | PR-AUC   | ROC-AUC  |
| --------- | -------- | -------- |
| 0         | 0.173801 | 0.896297 |
| 0.1       | 0.173406 | 0.896398 |
| 1.0       | 0.173294 | 0.896278 |

**Conclusion:** Additional L1 regularization did not improve PR-AUC. `reg_alpha=0` was retained.

---

### Experiment 7 — L2 Regularization

| reg_lambda | PR-AUC   | ROC-AUC  |
| ---------- | -------- | -------- |
| 0.5        | 0.172847 | 0.896375 |
| 1.0        | 0.173801 | 0.896297 |
| 5.0        | 0.172691 | 0.896660 |

**Conclusion:** `reg_lambda=1.0` was retained because PR-AUC was the primary evaluation metric.

---

## 4.3 Final Tuned XGBoost Configuration

```python
XGBClassifier(
    n_estimators=500,
    max_depth=4,
    min_child_weight=1,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0,
    reg_lambda=1.0,
    scale_pos_weight=scale_pos_weight,
    objective='binary:logistic',
    eval_metric='aucpr',
    random_state=42,
    n_jobs=-1
)
```

### Validation Performance

```text
PR-AUC  = 0.173801
ROC-AUC = 0.896297
```

Compared with the original baseline:

```text
Baseline PR-AUC = 0.159113
Tuned PR-AUC    = 0.173801
```

This represents approximately a **9.23% relative improvement in validation PR-AUC**.

---

## 4.4 Overfitting Check

The final tuned model was evaluated on both the training and validation sets.

| Metric  | Train    | Validation |
| ------- | -------- | ---------- |
| PR-AUC  | 0.205006 | 0.173801   |
| ROC-AUC | 0.928277 | 0.896297   |

There is a noticeable train-validation performance gap, indicating some degree of overfitting. However, validation performance remained strong and the model generalized well to the untouched test set.

---

## 4.5 Threshold Optimization — Uncalibrated Model

A classification threshold determines when the predicted fraud probability is converted into a fraud/review decision.

The default threshold of 0.5 was not assumed to be optimal.

A coarse threshold search followed by a fine-grained search was performed.

### Fine-Grained Results

| Threshold | Precision | Recall | F1     |
| --------- | --------- | ------ | ------ |
| 0.89      | 0.1819    | 0.3432 | 0.2378 |
| 0.90      | 0.1927    | 0.3178 | 0.2399 |
| 0.91      | 0.2063    | 0.2937 | 0.2423 |
| 0.92      | 0.2228    | 0.2640 | 0.2417 |
| 0.93      | 0.2428    | 0.2308 | 0.2367 |

The highest F1 among the tested thresholds occurred at:

```text
Threshold = 0.91
```

Validation performance:

```text
Precision = 20.63%
Recall    = 29.37%
F1        = 24.23%
Alerts    = 2,356
```

The threshold was selected based on F1 for model evaluation. In a real deployment, the final operating threshold should additionally consider false-positive cost, false-negative cost, and investigation capacity.

---

## 4.6 Final Uncalibrated Test Evaluation

Using the untouched test set and threshold `0.91`:

```text
PR-AUC    = 0.178377
ROC-AUC   = 0.903192
Precision = 0.213551
Recall    = 0.301088
F1        = 0.249875
```

### Confusion Matrix

```text
                 Predicted
                 Legit   Fraud
Actual Legit    146512   1834
Actual Fraud      1156    498
```

The model maintained similar performance on the test set, indicating reasonable generalization.

---

## 4.7 Probability Calibration

### Motivation

XGBoost can provide strong ranking performance while its raw probability estimates may not be well calibrated.

Calibration was therefore evaluated to determine whether predicted probabilities could be used more reliably in the later risk-scoring system.

Three models were compared:

1. Uncalibrated XGBoost
2. Sigmoid calibration
3. Isotonic calibration

### Calibration Results

| Model        | PR-AUC   | ROC-AUC  | Brier Score |
| ------------ | -------- | -------- | ----------- |
| Uncalibrated | 0.173801 | 0.896297 | 0.113403    |
| Sigmoid      | 0.173689 | 0.896451 | 0.010080    |
| Isotonic     | 0.173854 | 0.896411 | 0.009886    |

### Conclusion

Isotonic calibration was selected because it achieved the lowest Brier score while maintaining almost identical discrimination performance.

The purpose of calibration was **probability reliability**, not improving PR-AUC.

---

## 4.8 Threshold Optimization After Calibration

Calibration changes the probability scale, so the previous threshold of `0.91` could not be reused.

A new threshold search was performed using the calibrated validation probabilities.

A fine-grained search was performed between 0.05 and 0.15.

### F1-Optimal Calibrated Threshold

```text
Threshold = 0.12
```

Validation performance:

```text
Precision = 21.55%
Recall    = 28.64%
F1        = 24.59%
Alerts    = 2,200
```

Therefore, the final calibrated operating threshold was selected as:

```text
0.12
```

---

## 4.9 Final Calibrated Test Evaluation

The calibrated model was evaluated once on the untouched test set using the selected threshold of `0.12`.

### Test Performance

| Metric      | Result       |
| ----------- | ------------ |
| PR-AUC      | **0.177494** |
| ROC-AUC     | **0.903680** |
| Precision   | **21.49%**   |
| Recall      | **28.54%**   |
| F1          | **24.52%**   |
| Brier Score | **0.009840** |

### Confusion Matrix

```text
                 Predicted
                 Legit   Fraud
Actual Legit    146622   1724
Actual Fraud      1182    472
```

At the selected threshold:

```text
Fraud detected = 472 / 1654
Recall         = 28.54%

True positives = 472
False positives = 1724

Precision = 21.49%
```

---

## 4.10 Raw vs Calibrated Model

### Raw XGBoost

```text
PR-AUC    = 0.178377
ROC-AUC   = 0.903192
Precision = 21.36%
Recall    = 30.11%
F1        = 24.99%
```

### Calibrated XGBoost

```text
PR-AUC    = 0.177494
ROC-AUC   = 0.903680
Precision = 21.49%
Recall    = 28.54%
F1        = 24.52%
Brier     = 0.009840
```

### Interpretation

Calibration did not materially improve the classification/ranking metrics. Its main benefit was improving the reliability of predicted probabilities.

Therefore, the calibrated model is preferred for the later **risk-scoring component**, where probability quality is important.

---

# Phase 4 — Final Conclusion

The supervised fraud detection model was systematically improved through controlled hyperparameter tuning, threshold optimization, and probability calibration.

The final configuration uses:

```text
XGBoost
    ↓
Isotonic Calibration
    ↓
Calibrated Fraud Probability
    ↓
Threshold = 0.12
    ↓
Fraud / Review Decision
```

### Final Test Metrics

```text
PR-AUC     = 0.177494
ROC-AUC    = 0.903680
Precision  = 21.49%
Recall     = 28.54%
F1         = 24.52%
Brier      = 0.009840
```

The close validation and test performance indicates reasonable generalization to unseen data.

**Phase 4 is complete.**


### How I improved my fraud detection model

After building the baseline XGBoost model, my next step was to improve it systematically rather than randomly tuning hyperparameters.

The dataset was highly imbalanced, with only about **1.1% fraudulent applications**, so I used **PR-AUC as my primary metric** instead of accuracy, because accuracy can be misleading in highly imbalanced fraud problems.

I performed controlled experiments on parameters such as `max_depth`, `min_child_weight`, `learning_rate`, `n_estimators`, `subsample`, `colsample_bytree`, and regularization.

The baseline model achieved a validation **PR-AUC of 0.159**. After tuning, I obtained a validation PR-AUC of **0.174**, which was about a **9.2% relative improvement**.

The final XGBoost configuration used:

```text
n_estimators = 500
max_depth = 4
learning_rate = 0.05
subsample = 0.8
colsample_bytree = 0.8
min_child_weight = 1
```

I also checked for overfitting by comparing training and validation performance. The model had a train PR-AUC of about **0.205** versus **0.174** on validation, so there was some gap, but the model still generalized reasonably well.

Then I addressed another problem: **the raw XGBoost probabilities were not well calibrated**. Since I eventually wanted to use the probability as a fraud-risk score, I compared sigmoid and isotonic calibration.

Isotonic calibration reduced the Brier score substantially, from about **0.113 to 0.010**, while keeping ROC-AUC and PR-AUC almost unchanged.

Finally, I optimized the classification threshold on the validation set instead of blindly using 0.5. After calibration, the F1-optimal threshold among the tested values was **0.12**.

On the untouched test set, the final model achieved:

```text
PR-AUC    = 0.1775
ROC-AUC   = 0.9037
Precision = 21.49%
Recall    = 28.54%
F1        = 24.52%
Brier     = 0.00984
```

So the main idea was not just "I trained XGBoost." I built a **controlled model-development pipeline** involving tuning, overfitting checks, threshold optimization, and probability calibration while keeping the test set untouched until the final evaluation.



