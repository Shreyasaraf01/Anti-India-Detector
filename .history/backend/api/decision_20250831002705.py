# backend/api/decision.py
from pathlib import Path
import joblib
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from backend.api.utils.preprocess import clean_text

ROOT = Path(__file__).resolve().parents[1]   # backend/api
MODELS_DIR = ROOT / "models"

RF_PATH = MODELS_DIR / "fake_rf.joblib"
EMBED_NAME_PATH = MODELS_DIR / "embed_model_name.txt"

if not RF_PATH.exists():
    raise FileNotFoundError(f"{RF_PATH} not found. Train fake classifier first.")

embed_name = EMBED_NAME_PATH.read_text().strip() if EMBED_NAME_PATH.exists() else "all-MiniLM-L6-v2"

print("Loading models: RF:", RF_PATH, "embedder:", embed_name)
rf = joblib.load(RF_PATH)
embedder = SentenceTransformer(embed_name)

# sentiment pipeline
sentiment_pipe = pipeline("sentiment-analysis")

KEYWORDS = ['india','bharat','government','govt','army','modi','pm','citizen','nation','hindustan']

def analyze_text(text: str):
    text = str(text)
    cleaned = clean_text(text)

    emb = embedder.encode([text], convert_to_numpy=True)
    fake_prob = float(rf.predict_proba(emb)[0][1])

    sent = sentiment_pipe(text)[0]
    sent_label = sent['label']
    sent_score = float(sent['score'])

    hits = [k for k in KEYWORDS if k in text.lower()]

    suspicious = False
    if fake_prob > 0.6:
        suspicious = True
    if sent_label == 'NEGATIVE' and len(hits) > 0:
        suspicious = True
    if fake_prob > 0.45 and sent_label == 'NEGATIVE':
        suspicious = True

    conf = min(1.0, 0.6*fake_prob + 0.4*(1.0 if sent_label=='NEGATIVE' else 0.0))

    return {
        "text": text,
        "cleaned": cleaned,
        "fake_prob": round(fake_prob,3),
        "sentiment": sent_label,
        "sentiment_score": round(sent_score,3),
        "keywords": hits,
        "suspicious": suspicious,
        "confidence": round(conf,3)
    }
