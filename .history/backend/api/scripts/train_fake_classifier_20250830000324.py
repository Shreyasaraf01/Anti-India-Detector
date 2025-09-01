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

# Find all CSVs in data/
csv_files = list(DATA_DIR.glob("*.csv"))
if not csv_files:
    raise FileNotFoundError(f"No CSV files found in {DATA_DIR}")

# -----------------------------
# Load and combine CSVs
# -----------------------------
df_list = []
for csv_file in csv_files:
    temp_df = pd.read_csv(csv_file)
    df_list.append(temp_df)

df = pd.concat(df_list, ignore_index=True)
print(f"Combined {len(csv_files)} CSVs. Total rows: {len(df)}")

# -----------------------------
# Detect label column
# -----------------------------
label_candidates = ["label", "sentiment", "airline_sentiment", "target"]
label_col = None
for col in label_candidates:
    if col in df.columns:
        label_col = col
        break

if label_col is None:
    raise ValueError(f"No label column found. Columns available: {df.columns.tolist()}")

# -----------------------------
# Prepare dataset
# -----------------------------
if "text" not in df.columns:
    raise ValueError(f"No 'text' column found in CSVs. Columns available: {df.columns.tolist()}")

# Drop missing values
df = df.dropna(subset=["text", label_col])

# Map non-numeric labels to integers
if not pd.api.types.is_numeric_dtype(df[label_col]):
    unique_labels = df[label_col].unique()
    label_map = {label: idx for idx, label in enumerate(unique_labels)}
    df[label_col] = df[label_col].map(label_map)

texts = df["text"].tolist()
labels = df[label_col].astype(int).tolist()

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
