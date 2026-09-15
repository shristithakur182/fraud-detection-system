import streamlit as st
import requests

# 1. Page Config
st.set_page_config(
    page_title="Fraud Detector",
    page_icon="🛡️",
    layout="centered"
)

# 2. Injected Custom Dark Mode & Component Styling
st.markdown("""
    <style>
    /* Dark Background & Text Rules */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
        max-width: 680px;
        margin: 0 auto;
    }

    /* Headings */
    h1, h2, h3, h4 {
        color: #f0f6fc !important;
        font-weight: 600;
    }

    /* Custom Input Fields */
    .stNumberInput input {
        background-color: #161b22 !important;
        color: #f0f6fc !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }

    /* Primary Action Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: #ffffff !important;
        border: none;
        border-radius: 8px;
        height: 3.2em;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
        transform: translateY(-1px);
    }

    /* Metric Cards */
    [data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. App Title & Subtitle
st.title("🛡️ Transaction Risk Evaluator")
st.caption("Neural Network-powered real-time fraud assessment service.")

# 4. Preset Selector
preset = st.segmented_control(
    "Sample Payload Preset",
    options=["Legitimate", "Fraudulent", "Custom"],
    default="Legitimate"
)

if preset == "Legitimate":
    default_time, default_amount, default_v1, default_v14, default_v17 = 80000.0, 45.50, -0.45, 0.25, -0.15
elif preset == "Fraudulent":
    default_time, default_amount, default_v1, default_v14, default_v17 = 406.0, 529.00, -2.31, -4.28, -2.83
else:
    default_time, default_amount, default_v1, default_v14, default_v17 = 0.0, 100.00, 0.0, 0.0, 0.0

st.divider()

# 5. Form Input Grid
col1, col2 = st.columns(2)

with col1:
    amount = st.number_input("Amount ($)", value=default_amount, step=10.0)
    time = st.number_input("Time (Sec)", value=default_time, step=100.0)
    v1 = st.number_input("PCA V1", value=default_v1, format="%.2f")

with col2:
    v14 = st.number_input("PCA V14", value=default_v14, format="%.2f")
    v17 = st.number_input("PCA V17", value=default_v17, format="%.2f")

st.markdown("<br>", unsafe_allow_html=True)

# 6. Primary Action Button & Prediction Callout
if st.button("Evaluate Risk Score"):
    payload = {
        "Time": time, "V1": v1, "V2": 0.0, "V3": 0.0, "V4": 0.0, "V5": 0.0, "V6": 0.0,
        "V7": 0.0, "V8": 0.0, "V9": 0.0, "V10": 0.0, "V11": 0.0, "V12": 0.0, "V13": 0.0,
        "V14": v14, "V15": 0.0, "V16": 0.0, "V17": v17, "V18": 0.0, "V19": 0.0,
        "V20": 0.0, "V21": 0.0, "V22": 0.0, "V23": 0.0, "V24": 0.0, "V25": 0.0,
        "V26": 0.0, "V27": 0.0, "V28": 0.0, "Amount": amount
    }

    try:
        res = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=3)
        if res.status_code == 200:
            data = res.json()
            prob = data["fraud_probability"]
            is_fraud = data["is_fraud"]

            st.divider()
            
            # Formatted Metrics Display
            m1, m2 = st.columns(2)
            m1.metric("Risk Level", f"{prob * 100:.1f}%")
            m2.metric("Decision", "FLAGGED" if is_fraud else "APPROVED")

            st.progress(prob)

            if is_fraud:
                st.error("🚨 High risk of fraud detected. Transaction suspended.")
            else:
                st.success("✅ Transaction safe. Approved for processing.")
        else:
            st.error("Backend server returned an error.")
    except Exception:
        st.error("Cannot connect to FastAPI backend. Make sure Uvicorn is running.")