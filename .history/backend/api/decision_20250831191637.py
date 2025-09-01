# backend/api/decision.py
from pathlib import Path
import joblib
from sentence_transformers import SentenceTransformer
import numpy as np
import os # <-- Add this import

# -------------------------
# Auto-detect model paths
# -------------------------
# Traverse up the directory tree to find the project root
# and then navigate down to the models directory.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODELS_DIR = PROJECT_ROOT / "backend" / "api" / "models"

RF_MODEL_PATH = MODELS_DIR / "fake_rf.joblib"
EMBED_MODEL_NAME_PATH = MODELS_DIR / "embed_model_name.txt"

# -------------------------
# Load RandomForest + Embedder
# -------------------------
rf_model = None
try:
    if RF_MODEL_PATH.exists():
        rf_model = joblib.load(RF_MODEL_PATH)
    else:
        raise FileNotFoundError(f"Model file not found at: {RF_MODEL_PATH}")
except Exception as e:
    print(f"[WARN] Could not load RandomForest model: {e}")

embedder = None
try:
    if EMBED_MODEL_NAME_PATH.exists():
        embed_model_name = EMBED_MODEL_NAME_PATH.read_text().strip()
        embedder = SentenceTransformer(embed_model_name)
    else:
        raise FileNotFoundError(f"Embedder name file not found at: {EMBED_MODEL_NAME_PATH}")
except Exception as e:
    print(f"[WARN] Could not load embedder model: {e}")

# -------------------------
# Prediction Function
# -------------------------
def predict_fake(text: str) -> dict:
    """
    Predict whether given text is fake or real.
    """
    if rf_model is None or embedder is None:
        return {"error": "Prediction model not found. Check decision.py."}

    try:
        emb = embedder.encode([text], convert_to_numpy=True)
        pred = rf_model.predict(emb)[0]
        prob = max(rf_model.predict_proba(emb)[0])

        label_map = {0: "real", 1: "fake"}
        label_name = label_map.get(pred, str(pred))

        return {
            "label": label_name,
            "probability": round(prob * 100, 2)
        }
    except Exception as e:
        return {"error": f"An error occurred during prediction: {str(e)}"}

# -------------------------
# Backward Compatibility
# -------------------------
analyze_text = predict_fake