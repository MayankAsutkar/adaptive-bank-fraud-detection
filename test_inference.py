# ============================================================
# PHASE 10 — STEP 3E
# Test model inference outside FastAPI
# ============================================================

import time
import pandas as pd
import numpy as np
from api.model_service import FraudModelService


# ============================================================
# LOAD MODEL
# ============================================================

start = time.perf_counter()

service = FraudModelService()

model_load_time = time.perf_counter() - start

print(f"\nModel load time: {model_load_time:.4f} seconds")


# ============================================================
# LOAD ONE REAL ROW
# ============================================================

df = pd.read_csv("datasets/Base.csv")

sample = df.iloc[0].drop("fraud_bool").to_dict()

actual_label = df.iloc[0]["fraud_bool"]


# ============================================================
# RUN INFERENCE
# ============================================================

start = time.perf_counter()

result = service.predict(sample)

inference_time = (time.perf_counter() - start) * 1000


# ============================================================
# DISPLAY RESULT
# ============================================================

print("\n" + "=" * 60)
print("FRAUD INFERENCE TEST")
print("=" * 60)

print(f"Actual label       : {actual_label}")
print(f"Fraud probability  : {result['fraud_probability']:.6f}")
print(f"Threshold          : {result['threshold']:.2f}")
print(f"Risk level         : {result['risk_level']}")
print(f"Decision            : {result['decision']}")
print(f"Inference time     : {inference_time:.3f} ms")

print("=" * 60)