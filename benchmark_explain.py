import requests
import time
import statistics


URL = "http://127.0.0.1:8000/predict/explain"

payload = {
    "income": 0.6,
    "name_email_similarity": 0.08,
    "prev_address_months_count": -1,
    "current_address_months_count": 49,
    "customer_age": 24,
    "days_since_request": 0.02,
    "intended_balcon_amount": 100.0,
    "payment_type": "AA",
    "zip_count_4w": 5,
    "velocity_6h": 1000.0,
    "velocity_24h": 2000.0,
    "velocity_4w": 5000.0,
    "bank_branch_count_8w": 3,
    "date_of_birth_distinct_emails_4w": 1,
    "employment_status": "CA",
    "credit_risk_score": 150,
    "email_is_free": 1,
    "housing_status": "BA",
    "phone_home_valid": 0,
    "phone_mobile_valid": 1,
    "bank_months_count": 12,
    "has_other_cards": 1,
    "proposed_credit_limit": 1000.0,
    "foreign_request": 1,
    "source": "INTERNET",
    "session_length_in_minutes": 5.0,
    "device_os": "windows",
    "keep_alive_session": 0,
    "device_distinct_emails_8w": 2,
    "month": 7
}


# Warm-up
for _ in range(10):
    requests.post(URL, json=payload)


latencies = []

for _ in range(100):
    start = time.perf_counter()

    response = requests.post(URL, json=payload)

    elapsed_ms = (time.perf_counter() - start) * 1000

    if response.status_code != 200:
        print("Request failed:", response.status_code)
        print(response.text)
        break

    latencies.append(elapsed_ms)


latencies.sort()

print("\n========== SHAP API BENCHMARK ==========")

print(f"Requests: {len(latencies)}")
print(f"Mean:     {statistics.mean(latencies):.3f} ms")
print(f"P50:      {latencies[int(0.50 * len(latencies))]:.3f} ms")
print(f"P95:      {latencies[int(0.95 * len(latencies))]:.3f} ms")
print(f"P99:      {latencies[int(0.99 * len(latencies))]:.3f} ms")
print(f"Min:      {min(latencies):.3f} ms")
print(f"Max:      {max(latencies):.3f} ms")

print(
    f"Throughput: "
    f"{1000 / statistics.mean(latencies):.2f} requests/sec"
)