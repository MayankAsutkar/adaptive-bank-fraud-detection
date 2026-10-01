# ============================================================
# PHASE 10 — STEP 2
# File: api/schemas.py
# Purpose: API input/output validation using Pydantic
# ============================================================

from pydantic import BaseModel, ConfigDict


class FraudRequest(BaseModel):
    """
    Raw input schema for one fraud-scoring request.

    These are the original features used before preprocessing.
    """

    model_config = ConfigDict(extra="forbid")

    income: float
    name_email_similarity: float

    prev_address_months_count: float
    current_address_months_count: float

    customer_age: float
    days_since_request: float
    intended_balcon_amount: float

    payment_type: str

    zip_count_4w: float
    velocity_6h: float
    velocity_24h: float
    velocity_4w: float

    bank_branch_count_8w: float
    date_of_birth_distinct_emails_4w: float

    employment_status: str
    credit_risk_score: float

    email_is_free: int

    housing_status: str

    phone_home_valid: int
    phone_mobile_valid: int

    bank_months_count: float
    has_other_cards: int

    proposed_credit_limit: float

    foreign_request: int

    source: str

    session_length_in_minutes: float

    device_os: str

    keep_alive_session: int

    device_distinct_emails_8w: float

    month: int


class FraudResponse(BaseModel):
    """
    Response returned by the fraud scoring API.
    """

    fraud_probability: float
    threshold: float
    risk_level: str
    decision: str
    
class BatchFraudRequest(BaseModel):
    """
    Batch input containing multiple fraud-scoring requests.
    """

    requests: list[FraudRequest]


class BatchFraudResponse(BaseModel):
    """
    Batch prediction response.
    """

    predictions: list[FraudResponse]
    
    
# ============================================================
# PHASE 10 — STEP 9B
# SHAP explanation response schemas
# ============================================================

class SHAPFactor(BaseModel):
    """
    One feature's contribution to the model's fraud score.
    """

    feature: str
    shap_value: float
    direction: str


class FraudExplanationResponse(BaseModel):
    """
    Fraud prediction together with SHAP-based explanation.
    """

    fraud_probability: float
    threshold: float
    risk_level: str
    decision: str
    factors: list[SHAPFactor]