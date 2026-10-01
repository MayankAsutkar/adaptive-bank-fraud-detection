# Phase 1 — EDA

## Dataset

* 1,000,000 records.
* Overall fraud rate: **1.1029%**.
* No standard NaN values.

## 1. Negative / Sentinel Values

### Sentinel `-1` → treat as unavailable

* `prev_address_months_count`
* `current_address_months_count`
* `bank_months_count`
* `device_distinct_emails_8w`

Important:

* Do **not** globally replace negative values with NaN.
* Create missingness indicators during preprocessing.
* Missing previous-address and bank-history information shows higher fraud rates.

### Genuine negative values → retain

* `intended_balcon_amount`
* `credit_risk_score`
* `velocity_6h`
* `session_length_in_minutes`

Negative `intended_balcon_amount` is associated with higher fraud.

## 2. Numerical EDA

Notable relationships with fraud:

* `name_email_similarity`: lower values → higher fraud.
* `income`: higher values → higher fraud.
* `customer_age`: higher age → higher fraud.
* `credit_risk_score`: high values → substantially higher fraud.
* `intended_balcon_amount`: negative ranges → generally higher fraud.
* Behavioral features (`days_since_request`, velocity features, session length)
  show mostly **non-linear** relationships.

Several numerical features are highly right-skewed, especially:

* `days_since_request`
* `bank_branch_count_8w`
* `session_length_in_minutes`
* `intended_balcon_amount`

## 3. Categorical EDA

Overall fraud rate: **1.1029%**

Meaningful differences:

* `payment_type`: `AC` → **1.670%**
* `employment_status`: `CC` → **2.468%**
* `housing_status`: `BA` → **3.747%**
* `device_os`: `windows` → **2.469%**

`source` shows little practical difference and is highly imbalanced:

* `INTERNET` ≈ 99.3% of records.

Rare categories should be interpreted cautiously.

## 4. Correlation

Highest Pearson correlations with fraud:

* `credit_risk_score`: **0.0706**
* `proposed_credit_limit`: **0.0689**
* `customer_age`: **0.0630**
* `prev_address_missing`: **0.0481**
* `income`: **0.0451**

Key conclusion:

* Most linear correlations are weak.
* Low correlation does **not** mean a feature is useless because fraud
  relationships can be non-linear.
* Do not remove features based only on Pearson correlation.

## 5. Temporal Analysis

`month` shows a temporal pattern:

* Lowest fraud rate: month 2 → **0.875%**
* Highest fraud rate: month 7 → **1.475%**
* Fraud rate generally increases toward later months.

Keep `month` as a potentially useful feature.

## Phase 1 Conclusion

The dataset contains useful numerical, categorical, behavioral and temporal
signals. Many relationships are non-linear, supporting the use of
tree-based models.

### Next Phase

**Data Preprocessing & Feature Engineering**

1. Train/validation/test split
2. Handle sentinel values
3. Create missingness indicators
4. Encode categorical features
5. Check constant/near-constant features
6. Feature engineering
7. Build preprocessing pipeline
