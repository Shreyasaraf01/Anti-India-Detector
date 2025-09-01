from pathlib import Path
import pandas as pd
import re
from sentence_transformers import SentenceTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# -----------------------------
# Paths
# -----------------------------
BASE = Path(__file__).resolve().parents[3]  # project root
DATA_DIR = BASE / "data"
MODELS_DIR = BASE / "backend" / "api" / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Load indian_news_500.csv
# -----------------------------
news_path = DATA_DIR / "indian_news_500.csv"
df = pd.read_csv(news_path)

# Map labels to 0/1 if needed
df["label"] = df["label"].map({"FAKE": 1, "REAL": 0, "fake": 1, "real": 0, 1: 1, 0: 0})

print(f"Total samples loaded: {len(df)}")
print("Label distribution:\n", df["label"].value_counts())

# -----------------------------
# Drop missing or short texts
# -----------------------------
df = df.dropna(subset=["text", "label"])
df = df[df["text"].str.len() > 10]  # Remove very short texts
df = df[df["label"].isin([0, 1])]   # Ensure only 0/1 labels
print(f"After cleaning: {len(df)} rows.")

# -----------------------------
# Clean text
# -----------------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)  # remove URLs
    text = re.sub(r"@\w+", "", text)     # remove mentions
    text = re.sub(r"#\w+", "", text)     # remove hashtags
    text = re.sub(r"\s+", " ", text)     # remove extra spaces
    return text.strip()

df["text"] = df["text"].apply(clean_text)

texts = df["text"].tolist()
labels = df["label"].astype(int).tolist()

# -----------------------------
# Generate embeddings
# -----------------------------
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
embedder = SentenceTransformer(EMBED_MODEL_NAME)
embeddings = embedder.encode(texts, show_progress_bar=True, convert_to_numpy=True)

# -----------------------------
# Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    embeddings, labels, test_size=0.2, random_state=42, stratify=labels
)

# -----------------------------
# Train classifier
# -----------------------------
clf = RandomForestClassifier(n_estimators=200, n_jobs=-1, random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

# -----------------------------
# Evaluation
# -----------------------------
print(classification_report(y_test, y_pred, zero_division=0))

# -----------------------------
# Save model and embedding info
# -----------------------------
joblib.dump(clf, MODELS_DIR / "fake_rf.joblib")
(MODELS_DIR / "embed_model_name.txt").write_text(EMBED_MODEL_NAME)
print("Saved fake_rf.joblib and embed_model_name.txt to", MODELS_DIR)