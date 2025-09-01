# backend/api/utils/preprocess.py
from pathlib import Path
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure nltk data is available (quiet)
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

STOPWORDS = set(stopwords.words("english"))

def clean_text(text: str) -> str:
    """
    Simple cleaning: lowercase, remove urls, mentions, hashtags,
    non-alphanumeric chars, tokenise and remove stopwords.
    """
    if text is None:
        return ""
    text = str(text).lower()
    text = re.sub(r"http\S+|www\.\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#\w+", "", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    tokens = [t for t in word_tokenize(text) if t not in STOPWORDS and len(t) > 1]
    return " ".join(tokens)
