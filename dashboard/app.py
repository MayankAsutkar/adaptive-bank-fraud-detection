# Cell 1 — Imports

import streamlit as st
import requests
import pandas as pd


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Fraud Detection Analyst Console",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"


# ============================================================
# SESSION STATE
# ============================================================

if "selected_case" not in st.session_state:
    st.session_state["selected_case"] = None

if "case_results" not in st.session_state:
    st.session_state["case_results"] = {}

if "case_statuses" not in st.session_state:
    st.session_state["case_statuses"] = {}


# ============================================================
# CASE DATA
# ============================================================

cases = [
    {
        "case_id": "CASE-1001",
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
        "month": 7,
    },
    {
        "case_id": "CASE-1002",
        "income": 0.35,
        "name_email_similarity": 0.01,
        "prev_address_months_count": -1,
        "current_address_months_count": 2,
        "customer_age": 21,
        "days_since_request": 0.001,
        "intended_balcon_amount": 5000.0,
        "payment_type": "AC",
        "zip_count_4w": 25,
        "velocity_6h": 8000.0,
        "velocity_24h": 15000.0,
        "velocity_4w": 40000.0,
        "bank_branch_count_8w": 0,
        "date_of_birth_distinct_emails_4w": 8,
        "employment_status": "CC",
        "credit_risk_score": 40,
        "email_is_free": 1,
        "housing_status": "BA",
        "phone_home_valid": 0,
        "phone_mobile_valid": 1,
        "bank_months_count": -1,
        "has_other_cards": 0,
        "proposed_credit_limit": 15000.0,
        "foreign_request": 1,
        "source": "INTERNET",
        "session_length_in_minutes": 1.5,
        "device_os": "windows",
        "keep_alive_session": 1,
        "device_distinct_emails_8w": 15,
        "month": 7,
    },
    {
        "case_id": "CASE-1003",
        "income": 0.72,
        "name_email_similarity": 0.91,
        "prev_address_months_count": 36,
        "current_address_months_count": 120,
        "customer_age": 38,
        "days_since_request": 2.5,
        "intended_balcon_amount": 50.0,
        "payment_type": "AB",
        "zip_count_4w": 2,
        "velocity_6h": 50.0,
        "velocity_24h": 120.0,
        "velocity_4w": 500.0,
        "bank_branch_count_8w": 5,
        "date_of_birth_distinct_emails_4w": 1,
        "employment_status": "CA",
        "credit_risk_score": 180,
        "email_is_free": 0,
        "housing_status": "BE",
        "phone_home_valid": 1,
        "phone_mobile_valid": 1,
        "bank_months_count": 48,
        "has_other_cards": 1,
        "proposed_credit_limit": 1500.0,
        "foreign_request": 0,
        "source": "INTERNET",
        "session_length_in_minutes": 12.0,
        "device_os": "linux",
        "keep_alive_session": 1,
        "device_distinct_emails_8w": 1,
        "month": 6,
    },
    {
        "case_id": "CASE-1004",
        "income": 0.48,
        "name_email_similarity": 0.35,
        "prev_address_months_count": 8,
        "current_address_months_count": 30,
        "customer_age": 29,
        "days_since_request": 0.5,
        "intended_balcon_amount": 300.0,
        "payment_type": "AA",
        "zip_count_4w": 8,
        "velocity_6h": 700.0,
        "velocity_24h": 1800.0,
        "velocity_4w": 6500.0,
        "bank_branch_count_8w": 2,
        "date_of_birth_distinct_emails_4w": 3,
        "employment_status": "CA",
        "credit_risk_score": 105,
        "email_is_free": 1,
        "housing_status": "BA",
        "phone_home_valid": 1,
        "phone_mobile_valid": 1,
        "bank_months_count": 10,
        "has_other_cards": 0,
        "proposed_credit_limit": 4000.0,
        "foreign_request": 0,
        "source": "INTERNET",
        "session_length_in_minutes": 6.0,
        "device_os": "windows",
        "keep_alive_session": 1,
        "device_distinct_emails_8w": 4,
        "month": 6,
    },
    {
        "case_id": "CASE-1005",
        "income": 0.55,
        "name_email_similarity": 0.22,
        "prev_address_months_count": -1,
        "current_address_months_count": 15,
        "customer_age": 26,
        "days_since_request": 0.15,
        "intended_balcon_amount": 800.0,
        "payment_type": "AC",
        "zip_count_4w": 12,
        "velocity_6h": 1500.0,
        "velocity_24h": 4000.0,
        "velocity_4w": 12000.0,
        "bank_branch_count_8w": 1,
        "date_of_birth_distinct_emails_4w": 4,
        "employment_status": "CF",
        "credit_risk_score": 90,
        "email_is_free": 1,
        "housing_status": "BA",
        "phone_home_valid": 0,
        "phone_mobile_valid": 1,
        "bank_months_count": -1,
        "has_other_cards": 1,
        "proposed_credit_limit": 5000.0,
        "foreign_request": 1,
        "source": "TELEAPP",
        "session_length_in_minutes": 4.0,
        "device_os": "windows",
        "keep_alive_session": 0,
        "device_distinct_emails_8w": 6,
        "month": 7,
    },
]


# ============================================================
# HELPERS
# ============================================================

def score_case(case):
    """Send a case to the FastAPI explanation endpoint."""

    payload = {
        key: value
        for key, value in case.items()
        if key != "case_id"
    }

    try:
        response = requests.post(
            f"{API_URL}/predict/explain",
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return None


def get_risk_display(risk):
    if risk == "HIGH":
        return "🔴 HIGH"

    if risk == "MEDIUM":
        return "🟠 MEDIUM"

    return "🟢 LOW"


def get_case_status(case_id):
    return st.session_state["case_statuses"].get(
        case_id,
        "NEW"
    )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🕵️ Fraud Intelligence")

page = st.sidebar.radio(
    "Navigation",
    [
        "🕵️ Analyst Console",
        "🔍 Test Application"
    ]
)


# ============================================================
# API HEALTH
# ============================================================

try:
    health_response = requests.get(
        f"{API_URL}/health",
        timeout=5
    )

    if health_response.status_code == 200:
        health_data = health_response.json()

        st.sidebar.success("🟢 API Online")

        st.sidebar.caption(
            f"Model Loaded: {health_data.get('model_loaded', False)}"
        )

        st.sidebar.caption(
            f"Threshold: {health_data.get('threshold', 0.09):.2%}"
        )

    else:
        st.sidebar.error("🔴 API Error")

except requests.exceptions.RequestException:
    st.sidebar.error("🔴 API Offline")
    st.sidebar.caption("Start FastAPI before using scoring.")


# ============================================================
# ANALYST CONSOLE
# ============================================================

if page == "🕵️ Analyst Console":

    st.title("🕵️ Fraud Detection Analyst Console")

    st.caption(
        "Bank account/application fraud risk investigation dashboard"
    )

    st.divider()

    # ========================================================
    # PORTFOLIO ANALYTICS
    # ========================================================

    st.subheader("📊 Portfolio Analytics")

    total_cases = len(cases)

    scored_cases = len(
        st.session_state["case_results"]
    )

    high_risk_cases = sum(
        1
        for result in st.session_state["case_results"].values()
        if result.get("risk_level") == "HIGH"
    )

    reviewing_cases = sum(
        1
        for case in cases
        if get_case_status(case["case_id"]) == "REVIEWING"
    )

    escalated_cases = sum(
        1
        for case in cases
        if get_case_status(case["case_id"]) == "ESCALATED"
    )

    cleared_cases = sum(
        1
        for case in cases
        if get_case_status(case["case_id"]) == "CLEARED"
    )

    new_cases = sum(
        1
        for case in cases
        if get_case_status(case["case_id"]) == "NEW"
    )

    scored_probabilities = [
        result["fraud_probability"]
        for result in st.session_state["case_results"].values()
        if "fraud_probability" in result
    ]

    average_probability = (
        sum(scored_probabilities) /
        len(scored_probabilities)
        if scored_probabilities
        else 0.0
    )

    # ========================================================
    # KPI ROW 1
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Applications",
            total_cases
        )

    with col2:
        st.metric(
            "High-Risk Cases",
            high_risk_cases
        )

    with col3:
        st.metric(
            "Scored Cases",
            scored_cases
        )

    with col4:
        st.metric(
            "Avg Fraud Probability",
            f"{average_probability:.2%}"
        )

    # ========================================================
    # KPI ROW 2
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "New",
            new_cases
        )

    with col2:
        st.metric(
            "Reviewing",
            reviewing_cases
        )

    with col3:
        st.metric(
            "Escalated",
            escalated_cases
        )

    with col4:
        st.metric(
            "Cleared",
            cleared_cases
        )

    st.divider()

    # ========================================================
    # CHARTS
    # ========================================================

    chart_col1, chart_col2 = st.columns(2)

    # --------------------------------------------------------
    # Risk Distribution
    # --------------------------------------------------------

    with chart_col1:

        st.subheader("⚠️ Risk Distribution")

        risk_counts = {
            "LOW": 0,
            "MEDIUM": 0,
            "HIGH": 0
        }

        for result in st.session_state["case_results"].values():

            risk = result.get("risk_level")

            if risk in risk_counts:
                risk_counts[risk] += 1

        risk_df = pd.DataFrame(
            {
                "Risk Level": list(risk_counts.keys()),
                "Applications": list(risk_counts.values())
            }
        )

        st.bar_chart(
            risk_df.set_index("Risk Level")
        )

    # --------------------------------------------------------
    # Status Distribution
    # --------------------------------------------------------

    with chart_col2:

        st.subheader("📋 Case Status Distribution")

        status_counts = {
            "NEW": 0,
            "REVIEWING": 0,
            "ESCALATED": 0,
            "CLEARED": 0
        }

        for case in cases:

            status = get_case_status(
                case["case_id"]
            )

            if status in status_counts:
                status_counts[status] += 1

        status_df = pd.DataFrame(
            {
                "Status": list(status_counts.keys()),
                "Cases": list(status_counts.values())
            }
        )

        st.bar_chart(
            status_df.set_index("Status")
        )

    st.caption(
        "Analytics are based on cases currently loaded in the dashboard. "
        "Fraud probabilities are available only for cases that have been scored."
    )

    st.divider()

    # ========================================================
    # CASE QUEUE
    # ========================================================

    st.subheader("📋 Case Queue")

    queue_header = st.columns(
        [2, 2, 2, 2, 1]
    )

    queue_header[0].markdown("**Case ID**")
    queue_header[1].markdown("**Fraud Probability**")
    queue_header[2].markdown("**Risk**")
    queue_header[3].markdown("**Status**")
    queue_header[4].markdown("**Action**")

    for case in cases:

        case_id = case["case_id"]

        result = st.session_state["case_results"].get(
            case_id
        )

        status = get_case_status(case_id)

        if result:

            probability = result.get(
                "fraud_probability",
                0.0
            )

            risk = result.get(
                "risk_level",
                "LOW"
            )

            probability_text = f"{probability:.2%}"
            risk_text = get_risk_display(risk)

        else:

            probability_text = "Not scored"
            risk_text = "—"

        row = st.columns(
            [2, 2, 2, 2, 1]
        )

        row[0].write(case_id)
        row[1].write(probability_text)
        row[2].write(risk_text)
        row[3].write(status)

        if row[4].button(
            "Open",
            key=f"open_{case_id}"
        ):

            st.session_state["selected_case"] = case_id

            st.rerun()

    # ========================================================
    # SELECTED CASE
    # ========================================================

    selected_case_id = st.session_state["selected_case"]

    if selected_case_id is not None:

        selected_case = next(
            (
                case
                for case in cases
                if case["case_id"] == selected_case_id
            ),
            None
        )

        if selected_case is not None:

            st.divider()

            st.subheader(
                f"🔎 Case Details — {selected_case_id}"
            )

            # ------------------------------------------------
            # Score case automatically
            # ------------------------------------------------

            if selected_case_id not in st.session_state["case_results"]:

                with st.spinner(
                    "Running fraud detection model..."
                ):

                    result = score_case(
                        selected_case
                    )

                if result is not None:

                    st.session_state["case_results"][
                        selected_case_id
                    ] = result

                    st.rerun()

            result = st.session_state["case_results"].get(
                selected_case_id
            )

            if result:

                probability = result.get(
                    "fraud_probability",
                    0.0
                )

                threshold = result.get(
                    "threshold",
                    0.09
                )

                risk_level = result.get(
                    "risk_level",
                    "LOW"
                )

                decision = result.get(
                    "decision",
                    "DO_NOT_FLAG"
                )

                # ============================================
                # MODEL ASSESSMENT
                # ============================================

                st.markdown("### 🤖 Model Assessment")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Fraud Probability",
                        f"{probability:.2%}"
                    )

                with col2:
                    st.metric(
                        "Threshold",
                        f"{threshold:.2%}"
                    )

                with col3:
                    st.metric(
                        "Risk Level",
                        risk_level
                    )

                with col4:
                    st.metric(
                        "Model Decision",
                        decision
                    )

                # ============================================
                # ANALYST WORKFLOW
                # ============================================

                st.markdown("### 👨‍💼 Analyst Workflow")

                current_status = get_case_status(
                    selected_case_id
                )

                st.write(
                    f"Current analyst status: **{current_status}**"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    if st.button(
                        "🔍 Start Review",
                        use_container_width=True
                    ):

                        st.session_state["case_statuses"][
                            selected_case_id
                        ] = "REVIEWING"

                        st.rerun()

                with col2:

                    if st.button(
                        "✅ Clear Case",
                        use_container_width=True
                    ):

                        st.session_state["case_statuses"][
                            selected_case_id
                        ] = "CLEARED"

                        st.rerun()

                with col3:

                    if st.button(
                        "🚨 Escalate",
                        use_container_width=True
                    ):

                        st.session_state["case_statuses"][
                            selected_case_id
                        ] = "ESCALATED"

                        st.rerun()

                # ============================================
                # MODEL INTERPRETATION
                # ============================================

                st.markdown("### 🧠 Model Explanation")

                st.info(
                    "The model output is a risk signal for analyst "
                    "investigation. The analyst status is separate "
                    "from the model decision."
                )

                factors = result.get(
                    "factors",
                    []
                )

                if factors:

                    positive_factors = [
                        factor
                        for factor in factors
                        if factor.get("direction")
                        == "increases_fraud_score"
                    ]

                    negative_factors = [
                        factor
                        for factor in factors
                        if factor.get("direction")
                        == "decreases_fraud_score"
                    ]

                    col1, col2 = st.columns(2)

                    with col1:

                        st.markdown(
                            "#### 🔴 Factors Increasing Fraud Score"
                        )

                        if positive_factors:

                            for factor in positive_factors:

                                st.write(
                                    f"**{factor['feature']}**  "
                                    f"`+{factor['shap_value']:.4f}`"
                                )

                        else:

                            st.write(
                                "No major positive factors."
                            )

                    with col2:

                        st.markdown(
                            "#### 🟢 Factors Decreasing Fraud Score"
                        )

                        if negative_factors:

                            for factor in negative_factors:

                                st.write(
                                    f"**{factor['feature']}**  "
                                    f"`{factor['shap_value']:.4f}`"
                                )

                        else:

                            st.write(
                                "No major negative factors."
                            )

                # ============================================
                # APPLICATION DETAILS
                # ============================================

                st.markdown("### 📄 Application Details")

                application_data = {
                    key: value
                    for key, value in selected_case.items()
                    if key != "case_id"
                }

                details_df = pd.DataFrame(
                    list(application_data.items()),
                    columns=[
                        "Feature",
                        "Value"
                    ]
                )

                st.dataframe(
                    details_df,
                    use_container_width=True,
                    hide_index=True
                )


# ============================================================
# TEST APPLICATION
# ============================================================

elif page == "🔍 Test Application":

    st.title("🔍 Test Application")

    st.caption(
        "Submit a raw application to the FastAPI fraud detection service."
    )

    st.divider()

    # ========================================================
    # INPUT FORM
    # ========================================================

    with st.form("fraud_test_form"):

        st.subheader("Applicant Information")

        col1, col2, col3 = st.columns(3)

        with col1:

            income = st.number_input(
                "Income",
                value=0.6
            )

            customer_age = st.number_input(
                "Customer Age",
                min_value=0,
                value=24
            )

            employment_status = st.selectbox(
                "Employment Status",
                ["CA", "CB", "CC", "CD", "CE", "CF"]
            )

            housing_status = st.selectbox(
                "Housing Status",
                ["BA", "BB", "BC", "BD", "BE", "BF"]
            )

            payment_type = st.selectbox(
                "Payment Type",
                ["AA", "AB", "AC", "AD"]
            )

        with col2:

            name_email_similarity = st.number_input(
                "Name-Email Similarity",
                min_value=0.0,
                max_value=1.0,
                value=0.08
            )

            credit_risk_score = st.number_input(
                "Credit Risk Score",
                value=150.0
            )

            proposed_credit_limit = st.number_input(
                "Proposed Credit Limit",
                value=1000.0
            )

            foreign_request = st.selectbox(
                "Foreign Request",
                [0, 1]
            )

            source = st.selectbox(
                "Source",
                ["INTERNET", "TELEAPP"]
            )

        with col3:

            email_is_free = st.selectbox(
                "Email Is Free",
                [0, 1]
            )

            phone_home_valid = st.selectbox(
                "Phone Home Valid",
                [0, 1]
            )

            phone_mobile_valid = st.selectbox(
                "Phone Mobile Valid",
                [0, 1]
            )

            has_other_cards = st.selectbox(
                "Has Other Cards",
                [0, 1]
            )

            device_os = st.selectbox(
                "Device OS",
                [
                    "windows",
                    "linux",
                    "macintosh",
                    "x11",
                    "other"
                ]
            )

        st.subheader("Address & Banking")

        col1, col2, col3 = st.columns(3)

        with col1:

            prev_address_months_count = st.number_input(
                "Previous Address Months",
                value=-1.0
            )

            current_address_months_count = st.number_input(
                "Current Address Months",
                value=49.0
            )

            bank_months_count = st.number_input(
                "Bank Months Count",
                value=12.0
            )

            bank_branch_count_8w = st.number_input(
                "Bank Branch Count 8W",
                value=3.0
            )

        with col2:

            zip_count_4w = st.number_input(
                "ZIP Count 4W",
                value=5.0
            )

            date_of_birth_distinct_emails_4w = st.number_input(
                "DOB Distinct Emails 4W",
                value=1.0
            )

            device_distinct_emails_8w = st.number_input(
                "Device Distinct Emails 8W",
                value=2.0
            )

            intended_balcon_amount = st.number_input(
                "Intended Balance Amount",
                value=100.0
            )

        with col3:

            days_since_request = st.number_input(
                "Days Since Request",
                value=0.02
            )

            session_length_in_minutes = st.number_input(
                "Session Length",
                value=5.0
            )

            month = st.number_input(
                "Month",
                min_value=0,
                max_value=12,
                value=7
            )

        st.subheader("Velocity Features")

        col1, col2, col3 = st.columns(3)

        with col1:

            velocity_6h = st.number_input(
                "Velocity 6H",
                value=1000.0
            )

        with col2:

            velocity_24h = st.number_input(
                "Velocity 24H",
                value=2000.0
            )

        with col3:

            velocity_4w = st.number_input(
                "Velocity 4W",
                value=5000.0
            )

        st.subheader("Session & Device")

        col1, col2 = st.columns(2)

        with col1:

            keep_alive_session = st.selectbox(
                "Keep Alive Session",
                [0, 1]
            )

        with col2:

            submitted = st.form_submit_button(
                "🚀 Score Application",
                use_container_width=True
            )

    # ========================================================
    # SEND REQUEST
    # ========================================================

    if submitted:

        payload = {
            "income": income,
            "name_email_similarity": name_email_similarity,
            "prev_address_months_count": prev_address_months_count,
            "current_address_months_count": current_address_months_count,
            "customer_age": customer_age,
            "days_since_request": days_since_request,
            "intended_balcon_amount": intended_balcon_amount,
            "payment_type": payment_type,
            "zip_count_4w": zip_count_4w,
            "velocity_6h": velocity_6h,
            "velocity_24h": velocity_24h,
            "velocity_4w": velocity_4w,
            "bank_branch_count_8w": bank_branch_count_8w,
            "date_of_birth_distinct_emails_4w":
                date_of_birth_distinct_emails_4w,
            "employment_status": employment_status,
            "credit_risk_score": credit_risk_score,
            "email_is_free": email_is_free,
            "housing_status": housing_status,
            "phone_home_valid": phone_home_valid,
            "phone_mobile_valid": phone_mobile_valid,
            "bank_months_count": bank_months_count,
            "has_other_cards": has_other_cards,
            "proposed_credit_limit": proposed_credit_limit,
            "foreign_request": foreign_request,
            "source": source,
            "session_length_in_minutes":
                session_length_in_minutes,
            "device_os": device_os,
            "keep_alive_session": keep_alive_session,
            "device_distinct_emails_8w":
                device_distinct_emails_8w,
            "month": month,
        }

        try:

            with st.spinner(
                "Running fraud detection model..."
            ):

                response = requests.post(
                    f"{API_URL}/predict/explain",
                    json=payload,
                    timeout=30
                )

            if response.status_code == 200:

                result = response.json()

                st.success(
                    "Application scored successfully."
                )

                st.divider()

                st.subheader("🎯 Model Result")

                col1, col2, col3, col4 = st.columns(4)

                with col1:

                    st.metric(
                        "Fraud Probability",
                        f"{result['fraud_probability']:.2%}"
                    )

                with col2:

                    st.metric(
                        "Threshold",
                        f"{result['threshold']:.2%}"
                    )

                with col3:

                    st.metric(
                        "Risk Level",
                        result["risk_level"]
                    )

                with col4:

                    st.metric(
                        "Decision",
                        result["decision"]
                    )

                # ============================================
                # SHAP
                # ============================================

                st.subheader("🧠 SHAP Explanation")

                factors = result.get(
                    "factors",
                    []
                )

                if factors:

                    shap_df = pd.DataFrame(
                        factors
                    )

                    shap_df = shap_df[
                        [
                            "feature",
                            "shap_value",
                            "direction"
                        ]
                    ]

                    shap_df.columns = [
                        "Feature",
                        "SHAP Value",
                        "Direction"
                    ]

                    st.dataframe(
                        shap_df,
                        use_container_width=True,
                        hide_index=True
                    )

                else:

                    st.info(
                        "No SHAP explanation returned."
                    )

            else:

                st.error(
                    f"API returned status "
                    f"{response.status_code}"
                )

                try:
                    st.json(response.json())

                except Exception:
                    st.text(response.text)

        except requests.exceptions.RequestException as e:

            st.error(
                f"Could not connect to FastAPI: {e}"
            )