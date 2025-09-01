# backend/api/scripts/train_fake_classifier.py

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
# Load Tweets.csv only
# -----------------------------
DATA_PATH = DATA_DIR / "Tweets.csv"
if not DATA_PATH.exists():
    raise FileNotFoundError(f"{DATA_PATH} not found.")

df = pd.read_csv(DATA_PATH)
print(f"Loaded {DATA_PATH} with {len(df)} rows.")

# -----------------------------
# Check required columns
# -----------------------------
required_cols = ["text", "airline_sentiment"]
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Required column '{col}' not found in CSV.")

# -----------------------------
# Drop missing values
# -----------------------------
df = df.dropna(subset=required_cols)
print(f"After dropping missing values: {len(df)} rows.")

# -----------------------------
# Map labels to integers
# -----------------------------
label_map = {"negative": 0, "neutral": 1, "positive": 2}
df["label"] = df["airline_sentiment"].map(label_map)
print(f"Label distribution:\n{df['label'].value_counts()}")

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
labels = df["label"].tolist()

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
