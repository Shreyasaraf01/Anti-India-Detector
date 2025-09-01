import os
import joblib

# -------------------------
# Auto-detect model paths
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Files
RF_MODEL_PATH = os.path.join(MODELS_DIR, "fake_rf.joblib")
CLF_MODEL_PATH = os.path.join(MODELS_DIR, "fakeclf.joblib")
VECTORIZER_PATH = os.path.join(MODELS_DIR, "vectorizer.joblib")
EMBED_MODEL_NAME_PATH = os.path.join(MODELS_DIR, "embeded_model_name.txt")

# -------------------------
# Load models + vectorizer
# -------------------------
try:
    rf_model = joblib.load(RF_MODEL_PATH)
except Exception as e:
    rf_model = None
    print(f"[WARN] Could not load RandomForest model: {e}")

try:
    clf_model = joblib.load(CLF_MODEL_PATH)
except Exception as e:
    clf_model = None
    print(f"[WARN] Could not load classifier model: {e}")

try:
    vectorizer = joblib.load(VECTORIZER_PATH)
except Exception as e:
    vectorizer = None
    print(f"[WARN] Could not load vectorizer: {e}")

try:
    with open(EMBED_MODEL_NAME_PATH, "r", encoding="utf-8") as f:
        embed_model_name = f.read().strip()
except Exception as e:
    embed_model_name = None
    print(f"[WARN] Could not load embed model name: {e}")

# -------------------------
# Prediction Function
# -------------------------
def predict_fake(text: str) -> dict:
    """
    Predict whether given text is fake or not.
    Returns dict with label + probability.
    """
    if vectorizer is None or (rf_model is None and clf_model is None):
        return {"error": "Models not loaded"}

    # Transform input text
    X = vectorizer.transform([text])

    # Prefer RF model if available, else fallback
    model = rf_model if rf_model is not None else clf_model

    try:
        prediction = model.predict(X)[0]
        probability = max(model.predict_proba(X)[0])
        return {"label": str(prediction), "probability": float(probability)}
    except Exception as e:
        return {"error": str(e)}

# -------------------------
# Backward Compatibility
# -------------------------
# Some older code still calls `analyze_text`
analyze_text = predict_fake
