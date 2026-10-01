# ============================================================
# PHASE 10 — STEP 3
# File: api/model_service.py
# Purpose: Load artifacts and perform fraud inference
# ============================================================

import time
from pathlib import Path

import joblib
import pandas as pd
import numpy as np

import shap
# ============================================================
# CELL / CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PREPROCESSOR_PATH = PROJECT_ROOT / "notebooks" / "artifacts" / "preprocessor.pkl"
MODEL_PATH = PROJECT_ROOT / "notebooks" / "artifacts" / "calibrated_xgb.pkl"

DEFAULT_THRESHOLD = 0.09


# ============================================================
# RAW MODEL FEATURES
# ============================================================

CATEGORICAL_COLS = [
    "payment_type",
    "employment_status",
    "housing_status",
    "source",
    "device_os",
]

NUMERICAL_COLS = [
    "income",
    "name_email_similarity",
    "prev_address_months_count",
    "current_address_months_count",
    "customer_age",
    "days_since_request",
    "intended_balcon_amount",
    "zip_count_4w",
    "velocity_6h",
    "velocity_24h",
    "velocity_4w",
    "bank_branch_count_8w",
    "date_of_birth_distinct_emails_4w",
    "credit_risk_score",
    "email_is_free",
    "phone_home_valid",
    "phone_mobile_valid",
    "bank_months_count",
    "has_other_cards",
    "proposed_credit_limit",
    "foreign_request",
    "session_length_in_minutes",
    "keep_alive_session",
    "device_distinct_emails_8w",
    "month",
    "prev_address_months_count_missing",
    "current_address_months_count_missing",
    "bank_months_count_missing",
    "device_distinct_emails_8w_missing",
]

ALL_MODEL_INPUT_COLS = NUMERICAL_COLS + CATEGORICAL_COLS


# ============================================================
# MODEL SERVICE
# ============================================================

class FraudModelService:

    def __init__(self, threshold: float = DEFAULT_THRESHOLD):

        self.threshold = threshold

        print("Loading fraud detection artifacts...")

        start = time.perf_counter()

        self.preprocessor = joblib.load(PREPROCESSOR_PATH)
        self.model = joblib.load(MODEL_PATH)

        fitted_xgb = self.model.calibrated_classifiers_[0].estimator
        self.shap_explainer = shap.TreeExplainer(fitted_xgb)

        elapsed = time.perf_counter() - start

        print(f"Artifacts loaded in {elapsed:.4f} seconds")
        print(f"Threshold: {self.threshold}")


    # ========================================================
    # PREPROCESS RAW INPUT
    # ========================================================

    def preprocess(self, data: dict) -> pd.DataFrame:

        df = pd.DataFrame([data])

        # ----------------------------------------------------
        # Create missing indicators for sentinel values
        # ----------------------------------------------------

        sentinel_cols = [
            "prev_address_months_count",
            "current_address_months_count",
            "bank_months_count",
            "device_distinct_emails_8w",
        ]

        for col in sentinel_cols:
            df[col + "_missing"] = (
                df[col] == -1
            ).astype(int)

        # ----------------------------------------------------
        # Replace sentinel -1 with NaN
        # The saved preprocessor will impute these values.
        # ----------------------------------------------------

        for col in sentinel_cols:
            df[col] = df[col].replace(-1, np.nan)

        # ----------------------------------------------------
        # Keep exactly the features expected by the model
        # ----------------------------------------------------

        df = df[
            [
                "income",
                "name_email_similarity",
                "prev_address_months_count",
                "current_address_months_count",
                "customer_age",
                "days_since_request",
                "intended_balcon_amount",
                "payment_type",
                "zip_count_4w",
                "velocity_6h",
                "velocity_24h",
                "velocity_4w",
                "bank_branch_count_8w",
                "date_of_birth_distinct_emails_4w",
                "employment_status",
                "credit_risk_score",
                "email_is_free",
                "housing_status",
                "phone_home_valid",
                "phone_mobile_valid",
                "bank_months_count",
                "has_other_cards",
                "proposed_credit_limit",
                "foreign_request",
                "source",
                "session_length_in_minutes",
                "device_os",
                "keep_alive_session",
                "device_distinct_emails_8w",
                "month",
                "prev_address_months_count_missing",
                "current_address_months_count_missing",
                "bank_months_count_missing",
                "device_distinct_emails_8w_missing",
            ]
        ]

        return df


    # ========================================================
    # FRAUD PREDICTION
    # ========================================================

    def predict(self, data: dict) -> dict:

        start = time.perf_counter()

        # ----------------------------------------------------
        # Step 1: Raw input → DataFrame
        # ----------------------------------------------------

        df = self.preprocess(data)

        # ----------------------------------------------------
        # Step 2: Raw features → 55 processed features
        # ----------------------------------------------------

        X_processed = self.preprocessor.transform(df)

        # ----------------------------------------------------
        # Step 3: 55 features → calibrated probability
        # ----------------------------------------------------

        fraud_probability = float(
            self.model.predict_proba(X_processed)[0, 1]
        )

        # ----------------------------------------------------
        # Step 4: Apply operating threshold
        # ----------------------------------------------------

        is_fraud_alert = fraud_probability >= self.threshold

        if is_fraud_alert:
            risk_level = "HIGH"
            decision = "FLAG_FOR_INVESTIGATION"
        else:
            risk_level = "LOW"
            decision = "DO_NOT_FLAG"

        # ----------------------------------------------------
        # Latency measurement
        # ----------------------------------------------------

        latency_ms = (
            time.perf_counter() - start
        ) * 1000

        return {
            "fraud_probability": fraud_probability,
            "threshold": self.threshold,
            "risk_level": risk_level,
            "decision": decision,
            "latency_ms": latency_ms,
        }
        
        # ========================================================
    # BATCH FRAUD PREDICTION
    # ========================================================

    def predict_batch(self, data_list: list[dict]) -> list[dict]:

        start = time.perf_counter()

        # ----------------------------------------------------
        # Preprocess every request
        # ----------------------------------------------------

        dfs = [
            self.preprocess(data)
            for data in data_list
        ]

        # ----------------------------------------------------
        # Combine into one DataFrame
        # ----------------------------------------------------

        batch_df = pd.concat(
            dfs,
            ignore_index=True
        )

        # ----------------------------------------------------
        # Transform entire batch at once
        # ----------------------------------------------------

        X_processed = self.preprocessor.transform(batch_df)

        # ----------------------------------------------------
        # Predict entire batch at once
        # ----------------------------------------------------

        probabilities = self.model.predict_proba(
            X_processed
        )[:, 1]

        results = []

        for probability in probabilities:

            probability = float(probability)

            if probability >= self.threshold:
                risk_level = "HIGH"
                decision = "FLAG_FOR_INVESTIGATION"
            else:
                risk_level = "LOW"
                decision = "DO_NOT_FLAG"

            results.append({
                "fraud_probability": probability,
                "threshold": self.threshold,
                "risk_level": risk_level,
                "decision": decision,
            })

        elapsed_ms = (
            time.perf_counter() - start
        ) * 1000

        print(
            f"Batch size: {len(data_list)} | "
            f"Total inference time: {elapsed_ms:.3f} ms | "
            f"Per request: {elapsed_ms / len(data_list):.3f} ms"
        )

        return results
    
        # ========================================================
    # SHAP EXPLANATION
    # ========================================================

    def explain(self, data: dict, top_n: int = 5) -> dict:

        # ----------------------------------------------------
        # Preprocess input
        # ----------------------------------------------------

        df = self.preprocess(data)

        X_processed = self.preprocessor.transform(df)

        # ----------------------------------------------------
        # Fraud probability
        # ----------------------------------------------------

        fraud_probability = float(
            self.model.predict_proba(X_processed)[0, 1]
        )

        # ----------------------------------------------------
        # Get underlying XGBoost estimator
        # ----------------------------------------------------


        shap_values = self.shap_explainer.shap_values(
            X_processed
        )

        shap_values = shap_values[0]

        # ----------------------------------------------------
        # Feature names
        # ----------------------------------------------------

        feature_names = (
            self.preprocessor
            .get_feature_names_out()
        )

        # ----------------------------------------------------
        # Sort by absolute SHAP contribution
        # ----------------------------------------------------

        feature_importance = sorted(
            zip(feature_names, shap_values),
            key=lambda x: abs(x[1]),
            reverse=True
        )

        top_features = feature_importance[:top_n]

        # ----------------------------------------------------
        # Build explanation
        # ----------------------------------------------------

        factors = []

        for feature, shap_value in top_features:

            readable_name = feature

            if feature.startswith("num__"):
                readable_name = feature.replace(
                    "num__", ""
                )

            elif feature.startswith("cat__"):
                readable_name = feature.replace(
                    "cat__", ""
                )

            factors.append({
                "feature": readable_name,
                "shap_value": float(shap_value),
                "direction": (
                    "increases_fraud_score"
                    if shap_value > 0
                    else "decreases_fraud_score"
                ),
            })

        # ----------------------------------------------------
        # Decision
        # ----------------------------------------------------

        if fraud_probability >= self.threshold:
            risk_level = "HIGH"
            decision = "FLAG_FOR_INVESTIGATION"
        else:
            risk_level = "LOW"
            decision = "DO_NOT_FLAG"

        return {
            "fraud_probability": fraud_probability,
            "threshold": self.threshold,
            "risk_level": risk_level,
            "decision": decision,
            "factors": factors,
        }