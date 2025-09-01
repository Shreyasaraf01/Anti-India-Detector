import os
import joblib
from preprocess import clean_text
from transformers import pipeline
import nltk
import warnings

# Suppress nltk warnings/logs
warnings.filterwarnings("ignore", category=UserWarning, module="nltk")
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

# Get project root (parent of "src")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Load saved models safely
clf = joblib.load(os.path.join(MODELS_DIR, "fakeclf.joblib"))
vectorizer = joblib.load(os.path.join(MODELS_DIR, "vectorizer.joblib"))

# Sentiment pipeline (HuggingFace Transformers)
sentiment_pipe = pipeline("sentiment-analysis")

# Keywords related to India
KEYWORDS = ['india','bharat','government','govt','army','modi','pm','citizen','nation']

def analyze_text(text):
    text = str(text)
    cleaned = clean_text(text)

    # Classifier probability
    vec = vectorizer.transform([cleaned])
    fake_prob = float(clf.predict_proba(vec)[0][1])

    # Sentiment
    sent = sentiment_pipe(text)[0]   # {'label': 'POSITIVE'/'NEGATIVE', 'score': 0.99}
    sent_label = sent['label']
    sent_score = float(sent['score'])

    # Keyword hits
    hits = [k for k in KEYWORDS if k in text.lower()]

    # Decision rules
    suspicious = False
    if fake_prob > 0.6:
        suspicious = True
    if sent_label == 'NEGATIVE' and len(hits) > 0:
        suspicious = True
    if fake_prob > 0.45 and sent_label == 'NEGATIVE':
        suspicious = True

    # Confidence (simple mix)
    conf = min(1.0, 0.6*fake_prob + 0.4*(1.0 if sent_label=='NEGATIVE' else 0.0))

    return {
        'text': text,
        'cleaned': cleaned,
        'fake_prob': fake_prob,
        'sentiment': sent_label,
        'sentiment_score': sent_score,
        'keywords': hits,
        'suspicious': suspicious,
        'confidence': round(conf, 3)
    }

# Quick test
if __name__ == "__main__":
    examples = [
        "This article tries to make people hate India with lies",
        "I love India, so many beautiful places!"
    ]
    for ex in examples:
        print(analyze_text(ex))
