# backend/api/decision.py
from pathlib import Path
import joblib
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from backend.api.utils.preprocess import clean_text

# --- Path setup ---
ROOT = Path(__file__).resolve().parents[1]   # backend/api
POSSIBLE_MODEL_DIRS = [
    ROOT / "models",                       # backend/api/models ✅
    ROOT.parent / "models",                # backend/models
    ROOT.parent / "fake_news" / "models",  # backend/fake_news/models
]

def find_file(filename: str) -> Path:
    """Search for filename in POSSIBLE_MODEL_DIRS and return the first match."""
    for d in POSSIBLE_MODEL_DIRS:
        candidate = d / filename
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        f"❌ Could not find {filename} in any of: {[str(d) for d in POSSIBLE_MODEL_DIRS]}"
    )

# --- Load models ---
RF_PATH = find_file("fake_rf.joblib")
EMBED_NAME_PATH = find_file("embed_model_name.txt")

embed_name = EMBED_NAME_PATH.read_text().strip() if EMBED_NAME_PATH.exists() else "all-MiniLM-L6-v2"

print("Loading models: RF:", RF_PATH, "embedder:", embed_name)
rf = joblib.load(RF_PATH)
embedder = SentenceTransformer(embed_name)

# Sentiment pipeline
sentiment_pipe = pipeline("sentiment-analysis")

KEYWORDS = [
    'india', 'bharat', 'government', 'govt',
    'army', 'modi', 'pm', 'citizen',
    'nation', 'hindustan'
]

def analyze_text(text: str):
    text = str(text)
    cleaned = clean_text(text)

    # Sentence embedding
    emb = embedder.encode([text], convert_to_numpy=True)
    fake_prob = float(rf.predict_proba(emb)[0][1])

    # Sentiment analysis
    sent = sentiment_pipe(text)[0]
    sent_label = sent['label']
    sent_score = float(sent['score'])

    # Keyword hits
    hits = [k for k in KEYWORDS if k in text.lower()]

    # Suspicion rules
    suspicious = False
    if fake_prob > 0.6:
        suspicious = True
    if sent_label == 'NEGATIVE' and len(hits) > 0:
        suspicious = True
    if fake_prob > 0.45 and sent_label == 'NEGATIVE':
        suspicious = True

    # Confidence score
    conf = min(
        1.0,
        0.6 * fake_prob + 0.4 * (1.0 if sent_label == 'NEGATIVE' else 0.0)
    )

    return {
        "text": text,
        "cleaned": cleaned,
        "fake_prob": round(fake_prob, 3),
        "sentiment": sent_label,
        "sentiment_score": round(sent_score, 3),
        "keywords": hits,
        "suspicious": suspicious,
        "confidence": round(conf, 3)
    }
