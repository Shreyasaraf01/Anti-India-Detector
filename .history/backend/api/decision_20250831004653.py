import os
import joblib

# Dynamically detect models folder relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Model file paths
RF_MODEL_PATH = os.path.join(MODELS_DIR, "fake_rf.joblib")
CLF_MODEL_PATH = os.path.join(MODELS_DIR, "fakeclf.joblib")
VECTORIZER_PATH = os.path.join(MODELS_DIR, "vectorizer.joblib")
EMBED_MODEL_PATH = os.path.join(MODELS_DIR, "embeded_model_name.txt")

# Load models
try:
    rf_model = joblib.load(RF_MODEL_PATH)
    clf_model = joblib.load(CLF_MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

    with open(EMBED_MODEL_PATH, "r", encoding="utf-8") as f:
        embed_model_name = f.read().strip()

except Exception as e:
    raise RuntimeError(f"❌ Failed to load models from {MODELS_DIR}: {e}")

# Example prediction function
def predict(text: str):
    """Run prediction using loaded models."""
    try:
        vectorized = vectorizer.transform([text])
        rf_pred = rf_model.predict(vectorized)[0]
        clf_pred = clf_model.predict(vectorized)[0]
        return {
            "RandomForest": int(rf_pred),
            "Classifier": int(clf_pred),
            "EmbeddingModel": embed_model_name
        }
    except Exception as e:
        return {"error": f"Prediction failed: {e}"}


if __name__ == "__main__":
    sample_text = "This is a test news article."
    result = predict(sample_text)
    print("✅ Prediction result:", result)
