# backend/api/scripts/train_fake_classifier.py

from pathlib import Path
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# -----------------------------
# Paths
# -----------------------------
BASE = Path(__file__).resolve().parents[2]  # project root
DATA_DIR = BASE / "data"
MODELS_DIR = BASE / "backend" / "api" / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

DATA_PATH = DATA_DIR / "Tweets.csv"  # CSV file
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv(DATA_PATH)

# Automatically detect label column if 'label' not present
label_column_candidates = ["label", "sentiment", "airline_sentiment", "target"]
label_col = None
for col in label_column_candidates:
    if col in df.columns:
        label_col = col
        break

if label_col is None:
    raise ValueError(f"No label column found. Columns available: {df.columns.tolist()}")

# Drop rows with missing text or label
df = df.dropna(subset=["text", label_col])

# Convert non-numeric labels to integers if necessary
if not pd.api.types.is_numeric_dtype(df[label_col]):
    unique_labels = df[label_col].unique()
    label_map = {label: idx for idx, label in enumerate(unique_labels)}
    df[label_col] = df[label_col].map(label_map)

texts = df["text"].tolist()
labels = df[label_col].astype(int).tolist()

# -----------------------------
# Generate embeddings
# -----------------------------
embedder = SentenceTransformer(EMBED_MODEL_NAME)
embeddings = embedder.encode(texts, show_progress_bar=True, convert_to_numpy=True)

# -----------------------------
# Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    embeddings, labels, test_size=0.2, random_state=42
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
print(classification_report(y_test, y_pred))

# -----------------------------
# Save model and embedding info
# -----------------------------
joblib.dump(clf, MODELS_DIR / "fake_rf.joblib")
(MODELS_DIR / "embed_model_name.txt").write_text(EMBED_MODEL_NAME)
print("Saved fake_rf.joblib and embed_model_name.txt to", MODELS_DIR)
