# api_app/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from collections import Counter
import pandas as pd
import re
import sys
import os
from pathlib import Path

# -------------------------
# Path and data setup
# -------------------------
BASE_DIR = Path(__file__).resolve().parents[2] # Adjust the path to go up to the project root
DATA_DIR = BASE_DIR / "data"
news_path = DATA_DIR / "indian_news_500.csv"

# Load and clean data once when the server starts
try:
    df = pd.read_csv(news_path)
    df["label"] = df["label"].map({"FAKE": 1, "REAL": 0, "fake": 1, "real": 0, 1: 1, 0: 0})
    df = df.dropna(subset=["text", "label"])
    df = df[df["text"].str.len() > 10]
    df = df[df["label"].isin([0, 1])]

except FileNotFoundError:
    df = pd.DataFrame(columns=["text", "label"])
    print(f"Error: File not found at {news_path}. Stats and word cloud will be empty.")


# -------------------------
# Helper function for text cleaning
# -------------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|@\w+|#\w+", "", text)  # remove URLs, mentions, hashtags
    text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
    text = re.sub(r"\d+", "", text)      # remove numbers
    text = re.sub(r"\s+", " ", text)     # remove extra spaces
    return text.strip()


# -------------------------
# API Endpoints
# -------------------------
@api_view(["GET"])
def stats_view(request):
    """
    Returns the count of flagged vs. normal content.
    """
    flagged_count = df[df['label'] == 1].shape[0]
    normal_count = df[df['label'] == 0].shape[0]

    return Response({
        "flagged": flagged_count,
        "normal": normal_count
    })


@api_view(["GET"])
def wordcloud_view(request):
    """
    Generates a word cloud from frequent negative terms in flagged content.
    """
    # 1. Filter for flagged content and apply text cleaning
    flagged_df = df[df['label'] == 1]
    flagged_texts = flagged_df['text'].apply(clean_text).tolist()

    # 2. Get word frequencies
    stop_words = {"a", "the", "is", "in", "of", "and", "to", "for", "with", "that", "on", "it", "its", "had", "was", "has", "are", "by", "from"}
    
    all_words = []
    for text in flagged_texts:
        all_words.extend([word for word in text.split() if word not in stop_words and len(word) > 2])

    word_freqs = Counter(all_words).most_common(50)  # Get top 50 terms

    # 3. Format for word cloud
    wordcloud_data = {
        "words": {text: value for text, value in word_freqs}
    }
    
    return Response(wordcloud_data)


@api_view(["POST"])
def analyze_view(request):
    """
    Analyzes a given text using the trained model.
    (Assumes 'predict_fake' function is correctly implemented elsewhere)
    """
    text = request.data.get("text", "")
    if not text:
        return Response({"error": "text is required"}, status=400)
    
    # You need to ensure the `predict_fake` function is imported and works correctly
    # with your `sentence_transformers` and `RandomForestClassifier` models.
    try:
        from api.decision import predict_fake # Assumes decision.py is in the same directory
        result = predict_fake(text)
        return Response(result)
    except ImportError:
        return Response({"error": "Prediction model not found. Check decision.py."}, status=500)