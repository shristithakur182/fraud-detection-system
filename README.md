# 💳 Credit Card Fraud Detection System

An end-to-end, real-time transaction risk screening application built using an **Artificial Neural Network (ANN)** binary classifier, served via **FastAPI**, and visualized through an interactive **Streamlit** dashboard.

---

## 🌟 Key Features

* **High-Precision Thresholding:** Implements a strict `0.85` probability classification threshold tuned for imbalanced fraud datasets.
* **RESTful API Backend:** High-performance inference engine built with **FastAPI** and validated via **Pydantic**.
* **Interactive Web UI:** Clean, dark-themed dashboard built with **Streamlit** for real-time risk evaluation and preset testing.
* **Feature Normalization:** Standardized feature scaling via `StandardScaler` to ensure balanced model weights.

---

## 🏗️ System Architecture

```text
       ┌────────────────────────┐
       │   Streamlit Frontend   │
       │        (app.py)        │
       └───────────┬────────────┘
                   │
           HTTP POST /predict
                   │
                   ▼
       ┌────────────────────────┐
       │    FastAPI Backend     │
       │   (backend/main.py)    │
       └───────────┬────────────┘
                   │
          Preprocess & Scale
                   │
                   ▼
       ┌────────────────────────┐
       │   ANN Keras Model      │
       │   (fraud_model.h5)     │
       └────────────────────────┘