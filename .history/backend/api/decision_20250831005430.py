# backend/api/decision.py
from pathlib import Path
import joblib
from sentence_transformers import SentenceTransformer
import numpy as np

# -------------------------
# Auto-detect model paths
# -------------------------
BASE_DIR = Path(__file__).resolve().parents[0]  # api folder
MODELS_DIR = BASE_DIR / "models"

RF_MODEL_PATH = MODELS_DIR / "fake_rf.joblib"
EMBED_MODEL_NAME_PATH = MODELS_DIR / "embed_model_name.txt"  # fixed spelling

# -------------------------
# Load RandomForest + Embedder
# -------------------------
try:
    rf_model = joblib.load(RF_MODEL_PATH)
except Exception as e:
    rf_model = None
    print(f"[WARN] Could not load RandomForest model: {e}")

try:
    embed_model_name = EMBED_MODEL_NAME_PATH.read_text().strip()
    embedder = SentenceTransformer(embed_model_name)
except Exception as e:
    embedder = None
    print(f"[WARN] Could not load embedder model: {e}")

# -------------------------
# Prediction Function
# -------------------------
def predict_fake(text: str) -> dict:
    """
    Predict whether given text is fake or not.
    Returns dict with label.
    """
    if rf_model is None or embedder is None:
        return {"error": "Models not loaded"}

    try:
        # Encode text using the same embedding model used for training
        emb = embedder.encode([text], convert_to_numpy=True)
        pred = rf_model.predict(emb)[0]
        return {"label": int(pred)}
    except Exception as e:
        return {"error": str(e)}

# -------------------------
# Backward Compatibility
# -------------------------
analyze_text = predict_fake
