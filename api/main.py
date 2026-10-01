# ============================================================
# PHASE 10 — STEP 4
# File: api/main.py
# Purpose: FastAPI application and HTTP endpoints
# ============================================================

from fastapi import FastAPI

from api.model_service import FraudModelService
from api.schemas import FraudRequest, FraudResponse

from api.schemas import (
    FraudRequest,
    FraudResponse,
    BatchFraudRequest,
    BatchFraudResponse,
    FraudExplanationResponse,
)

import shap

# ============================================================
# CREATE FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Fraud Detection API",
    description="Real-time fraud scoring using calibrated XGBoost",
    version="1.0.0",
)


# ============================================================
# LOAD MODEL ONCE AT SERVER STARTUP
# ============================================================

model_service = FraudModelService()


# ============================================================
# HEALTH ENDPOINT
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": True,
        "threshold": model_service.threshold,
    }


# ============================================================
# FRAUD PREDICTION ENDPOINT
# ============================================================

@app.post("/predict", response_model=FraudResponse)
def predict(request: FraudRequest):

    result = model_service.predict(
        request.model_dump()
    )

    return FraudResponse(
        fraud_probability=result["fraud_probability"],
        threshold=result["threshold"],
        risk_level=result["risk_level"],
        decision=result["decision"],
    )
    
# ============================================================
# SHAP EXPLANATION ENDPOINT
# ============================================================

@app.post(
    "/predict/explain",
    response_model=FraudExplanationResponse
)
def predict_explain(request: FraudRequest):

    result = model_service.explain(
        request.model_dump()
    )

    return FraudExplanationResponse(
        fraud_probability=result["fraud_probability"],
        threshold=result["threshold"],
        risk_level=result["risk_level"],
        decision=result["decision"],
        factors=result["factors"],
    )

# ============================================================
# BATCH FRAUD PREDICTION ENDPOINT
# ============================================================

@app.post(
    "/predict/batch",
    response_model=BatchFraudResponse
)
def predict_batch(request: BatchFraudRequest):

    data_list = [
        item.model_dump()
        for item in request.requests
    ]

    results = model_service.predict_batch(
        data_list
    )

    return BatchFraudResponse(
        predictions=results
    )