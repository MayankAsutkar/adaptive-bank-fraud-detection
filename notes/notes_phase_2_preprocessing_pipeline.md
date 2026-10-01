# Phase 2 — Data Preprocessing & Feature Engineering

## 1. Train / Validation / Test Split

Used stratified 70/15/15 split:

* Train: 700,000
* Validation: 150,000
* Test: 150,000

Fraud rate remained approximately 1.10% in all splits.

```text
Train:      1.102857%
Validation: 1.103333%
Test:       1.102667%
```

Stratification preserves the original fraud/legitimate class distribution.

---

## 2. Sentinel Value Handling

The following columns use `-1` to represent unavailable information:

* `prev_address_months_count`
* `current_address_months_count`
* `bank_months_count`
* `device_distinct_emails_8w`

Processing:

1. Created missingness indicators.
2. Replaced `-1` with `NaN`.
3. Later imputed these values using training-set medians.

Missingness indicators:

* `prev_address_months_count_missing`
* `current_address_months_count_missing`
* `bank_months_count_missing`
* `device_distinct_emails_8w_missing`

Important:

* Do not replace all negative values globally.
* Some negative values in other columns are genuine values.

---

## 3. Genuine Negative Values

Negative values were retained for:

* `intended_balcon_amount`
* `velocity_6h`
* `credit_risk_score`
* `session_length_in_minutes`

These are not treated as missing/sentinel values.

---

## 4. Constant Feature Removal

Checked all training features for zero variance.

Removed:

* `device_fraud_count`

Reason:

* Constant value (`0`) for all observations.
* Provides no predictive information.

An accidental `income_bin` feature created during EDA was also removed because it was not intended to be a model feature.

---

## 5. Final Feature Set Before Encoding

After sentinel handling and constant-feature removal:

* 34 usable features
* 29 numerical features
* 5 categorical features

Categorical:

```text
payment_type
employment_status
housing_status
source
device_os
```

Numerical features include the original numerical/binary/temporal features plus the 4 missingness indicators.

---

## 6. Numerical Imputation

Used median imputation:

```python
SimpleImputer(strategy='median')
```

Important:

* Median was fitted **only on training data**.
* The same fitted imputer was applied to validation and test data.

Result:

```text
Train:      (700000, 29)
Validation: (150000, 29)
Test:       (150000, 29)
```

---

## 7. Categorical Encoding

Used one-hot encoding:

```python
OneHotEncoder(handle_unknown='ignore')
```

Result:

```text
26 encoded categorical features
```

`handle_unknown='ignore'` ensures unseen categories in validation/test/future API inputs do not cause errors.

---

## 8. Final Preprocessing Pipeline

Replaced the temporary manual preprocessing approach with a reusable `ColumnTransformer`:

```python
numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median'))
])

categorical_transformer = Pipeline([
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numerical_cols),
    ('cat', categorical_transformer, categorical_cols)
])
```

Fitted only on training data:

```python
X_train_processed = preprocessor.fit_transform(X_train)

X_val_processed = preprocessor.transform(X_val)
X_test_processed = preprocessor.transform(X_test)
```

---

## 9. Final Processed Dataset

Final dimensions:

```text
Train:      (700000, 55)
Validation: (150000, 55)
Test:       (150000, 55)
```

Feature composition:

```text
29 numerical
+
26 one-hot categorical
=
55 model features
```

Feature names were obtained using:

```python
feature_names = preprocessor.get_feature_names_out()
```

Examples:

```text
num__income
num__credit_risk_score
num__customer_age
num__prev_address_months_count_missing
cat__payment_type_AA
cat__employment_status_CC
cat__housing_status_BA
cat__source_INTERNET
cat__device_os_windows
```

---

## 10. Missing Value Verification

Verified the final processed matrices:

```text
Train NaN: 0
Val NaN:   0
Test NaN:  0
```

Therefore, preprocessing successfully removed all missing values.

---

## 11. Feature Engineering Decision

Considered creating:

```text
credit_income_ratio =
proposed_credit_limit / income
```

But `income` is normalized to approximately `0.1–0.9`, while `proposed_credit_limit` is approximately `190–2100`.

Therefore, a direct ratio would have arbitrary scale and was **not created**.

Decision:

* Keep `income` and `proposed_credit_limit` separately.
* Avoid unnecessary/artificial ratios.
* Let XGBoost learn interactions between features.
* Add engineered features later only when there is clear domain justification or validation evidence.

---

## Phase 2 Conclusion

* Data was split without leakage using stratification.
* Sentinel values were correctly converted to missing values.
* Missingness indicators were preserved.
* Constant features were removed.
* Numerical and categorical preprocessing was implemented.
* A reusable preprocessing pipeline was created.
* Final feature space contains **55 features**.
* No missing values remain after preprocessing.
* No unnecessary feature engineering was added.

### Phase 2 Status: COMPLETE ✅

### Next Phase

**Phase 3 — Baseline XGBoost Model**

1. Handle class imbalance.
2. Train baseline XGBoost.
3. Evaluate using PR-AUC and ROC-AUC.
4. Analyze precision, recall and F1.
5. Perform threshold analysis.
6. Tune the mode
