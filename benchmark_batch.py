# ============================================================
# PHASE 10 — STEP 8
# File: benchmark_batch.py
# Purpose: Benchmark batch fraud inference
# ============================================================

import time
import numpy as np
import pandas as pd

from api.model_service import FraudModelService


# ============================================================
# CONFIGURATION
# ============================================================

BATCH_SIZES = [10, 50, 100, 500]


# ============================================================
# LOAD MODEL
# ============================================================

print("Loading model...")

service = FraudModelService()


# ============================================================
# LOAD REAL DATA
# ============================================================

df = pd.read_csv("datasets/Base.csv")

samples = (
    df.drop(columns=["fraud_bool"])
      .iloc[:500]
      .to_dict(orient="records")
)


# ============================================================
# WARM-UP
# ============================================================

print("\nRunning warm-up...")

service.predict_batch(samples[:10])


# ============================================================
# BATCH BENCHMARK
# ============================================================

results = []


for batch_size in BATCH_SIZES:

    batch = samples[:batch_size]

    start = time.perf_counter()

    predictions = service.predict_batch(batch)

    elapsed_ms = (
        time.perf_counter() - start
    ) * 1000

    per_request_ms = elapsed_ms / batch_size

    throughput = (
        batch_size / (elapsed_ms / 1000)
    )

    results.append({
        "batch_size": batch_size,
        "total_ms": elapsed_ms,
        "per_request_ms": per_request_ms,
        "throughput_req_sec": throughput,
        "predictions": len(predictions),
    })


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 75)
print("BATCH INFERENCE BENCHMARK")
print("=" * 75)

print(
    f"{'Batch':>10}"
    f"{'Total(ms)':>15}"
    f"{'Per Req(ms)':>18}"
    f"{'Throughput':>20}"
)

print("-" * 75)

for result in results:

    print(
        f"{result['batch_size']:>10}"
        f"{result['total_ms']:>15.3f}"
        f"{result['per_request_ms']:>18.3f}"
        f"{result['throughput_req_sec']:>20.2f}"
    )

print("=" * 75)