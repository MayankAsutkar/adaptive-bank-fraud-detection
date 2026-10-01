# ============================================================
# PHASE 10 — STEP 7
# File: benchmark.py
# Purpose: Measure fraud inference latency
# ============================================================

import time
import numpy as np
import pandas as pd

from api.model_service import FraudModelService


# ============================================================
# CONFIGURATION
# ============================================================

WARMUP_REQUESTS = 10
BENCHMARK_REQUESTS = 1000


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
      .iloc[:BENCHMARK_REQUESTS]
      .to_dict(orient="records")
)


# ============================================================
# WARM-UP
# ============================================================

print(f"\nRunning {WARMUP_REQUESTS} warm-up requests...")

for i in range(WARMUP_REQUESTS):
    service.predict(samples[i])


# ============================================================
# SINGLE-REQUEST LATENCY
# ============================================================

print(
    f"Running {BENCHMARK_REQUESTS} benchmark requests..."
)

latencies_ms = []

for sample in samples:

    start = time.perf_counter()

    service.predict(sample)

    elapsed_ms = (
        time.perf_counter() - start
    ) * 1000

    latencies_ms.append(elapsed_ms)


latencies_ms = np.array(latencies_ms)


# ============================================================
# LATENCY STATISTICS
# ============================================================

p50 = np.percentile(latencies_ms, 50)
p95 = np.percentile(latencies_ms, 95)
p99 = np.percentile(latencies_ms, 99)

mean_latency = np.mean(latencies_ms)
min_latency = np.min(latencies_ms)
max_latency = np.max(latencies_ms)


# ============================================================
# THROUGHPUT
# ============================================================

total_time_seconds = np.sum(latencies_ms) / 1000

throughput = (
    BENCHMARK_REQUESTS /
    total_time_seconds
)


# ============================================================
# RESULTS
# ============================================================

print("\n" + "=" * 60)
print("SINGLE-REQUEST LATENCY BENCHMARK")
print("=" * 60)

print(f"Requests          : {BENCHMARK_REQUESTS}")
print(f"Mean latency      : {mean_latency:.3f} ms")
print(f"P50 latency       : {p50:.3f} ms")
print(f"P95 latency       : {p95:.3f} ms")
print(f"P99 latency       : {p99:.3f} ms")
print(f"Minimum latency   : {min_latency:.3f} ms")
print(f"Maximum latency   : {max_latency:.3f} ms")
print(f"Throughput        : {throughput:.2f} requests/sec")

print("=" * 60)