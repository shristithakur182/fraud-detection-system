import joblib
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Initialize FastAPI application
app = FastAPI(
    title="Credit Card Fraud Detection API",
    description="Backend service powered by an Artificial Neural Network (ANN) to detect credit card fraud.",
    version="1.0.0"
)

# Load saved model and scaler into memory on server startup
try:
    model = tf.keras.models.load_model('credit_card_ann_model.keras')
    scaler = joblib.load('scaler.pkl')
    print("SUCCESS: Model and Scaler loaded successfully!")
except Exception as e:
    print(f"ERROR: Failed to load model files: {e}")
    model = None
    scaler = None


# Define Pydantic schema to validate the incoming 30 features
class TransactionData(BaseModel):
    Time: float
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float
    Amount: float


@app.get("/")
def root():
    """Health check endpoint to verify backend service status."""
    return {
        "status": "online",
        "message": "Credit Card Fraud Detection API is running smoothly!"
    }


@app.post("/predict")
def predict_fraud(transaction: TransactionData):
    """
    Accepts raw transaction details, normalizes features via StandardScaler,
    and returns fraud probability and classification based on a 0.85 threshold.
    """
    if model is None or scaler is None:
        raise HTTPException(
            status_code=500, 
            detail="Model or Scaler not loaded on server. Please check file paths."
        )

    try:
        # 1. Extract inputs into a 2D array matching the model's training order
        features = np.array([[
            transaction.Time, transaction.V1, transaction.V2, transaction.V3, transaction.V4,
            transaction.V5, transaction.V6, transaction.V7, transaction.V8, transaction.V9,
            transaction.V10, transaction.V11, transaction.V12, transaction.V13, transaction.V14,
            transaction.V15, transaction.V16, transaction.V17, transaction.V18, transaction.V19,
            transaction.V20, transaction.V21, transaction.V22, transaction.V23, transaction.V24,
            transaction.V25, transaction.V26, transaction.V27, transaction.V28, transaction.Amount
        ]])

        # 2. Scale features using saved StandardScaler
        scaled_features = scaler.transform(features)

        # 3. Generate raw probability score from ANN model
        raw_prediction = model.predict(scaled_features, verbose=0)
        fraud_probability = float(raw_prediction[0][0])

        # 4. Apply optimized classification threshold (0.85)
        threshold = 0.85
        is_fraud = fraud_probability >= threshold

        return {
            "fraud_probability": round(fraud_probability, 4),
            "is_fraud": is_fraud,
            "threshold_used": threshold,
            "decision": "FRAUD DETECTED" if is_fraud else "LEGITIMATE TRANSACTION"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction Error: {str(e)}")