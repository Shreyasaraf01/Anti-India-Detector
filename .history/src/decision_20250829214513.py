import joblib
from preprocess import clean_text
from transformers import pipeline
import re

# load saved models
clf = joblib.load("../models/fakeclf.joblib")
vectorizer = joblib.load("../models/vectorizer.joblib")

# sentiment pipeline (downloads a small model first time)
sentiment_pipe = pipeline("sentiment-analysis")  

# keywords related to India (we look for these words)
KEYWORDS = ['india','bharat','government','govt','army','modi','pm','citizen','nation']

def analyze_text(text):
    text = str(text)
    cleaned = clean_text(text)
    # classifier probability of label=1 (suspicious)
    vec = vectorizer.transform([cleaned])
    fake_prob = float(clf.predict_proba(vec)[0][1])

    # sentiment from transformers
    sent = sentiment_pipe(text)[0]   # {'label': 'POSITIVE'/'NEGATIVE', 'score': 0.99}
    sent_label = sent['label']
    sent_score = float(sent['score'])

    # keyword hits
    hits = [k for k in KEYWORDS if k in text.lower()]

    # decision rules (simple)
    suspicious = False
    # rule 1: classifier says very likely
    if fake_prob > 0.6:
        suspicious = True
    # rule 2: negative sentiment + India keywords
    if sent_label == 'NEGATIVE' and len(hits) > 0:
        suspicious = True
    # rule 3: moderate classifier prob + negative sentiment
    if fake_prob > 0.45 and sent_label == 'NEGATIVE':
        suspicious = True

    # confidence (simple mix)
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

# quick test (only run if this file is executed directly)
if __name__ == "__main__":
    examples = [
        "This article tries to make people hate India with lies",
        "I love India, so many beautiful places!"
    ]
    for ex in examples:
        print(analyze_text(ex))
