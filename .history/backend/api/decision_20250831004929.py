import os
import joblib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Automatically detect models directory relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

if not os.path.exists(MODELS_DIR):
    logger.warning(f"Models directory not found at: {MODELS_DIR}")

# Dictionary to hold loaded objects
_loaded_objects = {}

# Supported model extensions
MODEL_EXTENSIONS = (".joblib", ".pkl")

def _load_models():
    """
    Load all model/vectorizer files from the models directory into memory.
    """
    if not os.path.exists(MODELS_DIR):
        raise FileNotFoundError(f"Models directory not found: {MODELS_DIR}")

    for file_name in os.listdir(MODELS_DIR):
        file_path = os.path.join(MODELS_DIR, file_name)

        # Load only supported model files
        if file_name.endswith(MODEL_EXTENSIONS):
            try:
                _loaded_objects[file_name] = joblib.load(file_path)
                logger.info(f"Loaded: {file_name}")
            except Exception as e:
                logger.error(f"Failed to load {file_name}: {e}")

        # Text-based configs (like embedded_model_name.txt)
        elif file_name.endswith(".txt"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    _loaded_objects[file_name] = f.read().strip()
                logger.info(f"Loaded text config: {file_name}")
            except Exception as e:
                logger.error(f"Failed to read {file_name}: {e}")

# Load models immediately when module is imported
_load_models()

def get_model(name: str):
    """
    Retrieve a loaded object (model/vectorizer/config) by filename.
    Example:
        model = get_model("fake_rf.joblib")
    """
    if name not in _loaded_objects:
        raise KeyError(f"Object '{name}' not found in loaded models. Available: {list(_loaded_objects.keys())}")
    return _loaded_objects[name]

def predict_fake(text: str) -> str:
    """
    Example prediction function using the available models.
    Modify this to fit your pipeline.
    """
    try:
        vectorizer = get_model("vectorizer.joblib")
        clf = get_model("fake_rf.joblib")  # or fakeclf.joblib depending on what you want

        features = vectorizer.transform([text])
        prediction = clf.predict(features)[0]
        return "Fake" if prediction == 1 else "Real"

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return "Error during prediction"
