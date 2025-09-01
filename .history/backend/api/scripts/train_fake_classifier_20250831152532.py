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
# Load Fake and True datasets
# -----------------------------
fake_path = DATA_DIR / "Fake.csv"
true_path = DATA_DIR / "True.csv"
df_fake = pd.read_csv(fake_path)
df_true = pd.read_csv(true_path)

# Add labels
df_fake["label"] = 1  # Fake/Anti-India
df_true["label"] = 0  # Real/Normal

# Combine
df = pd.concat([df_fake, df_true], ignore_index=True)

# -----------------------------
# Optionally merge fake_news_dataset.csv if present
# -----------------------------
extra_path = DATA_DIR / "fake_news_dataset.csv"
if extra_path.exists():
    df_extra = pd.read_csv(extra_path)
    # Try to auto-detect columns
    text_col = None
    label_col = None
    for col in df_extra.columns:
        if "text" in col.lower():
            text_col = col
        if "label" in col.lower() or "target" in col.lower():
            label_col = col
    if text_col and label_col:
        # Map labels to 0/1 if needed
        df_extra[label_col] = df_extra[label_col].map({"FAKE": 1, "REAL": 0, "fake": 1, "real": 0, 1: 1, 0: 0})
        df_extra = df_extra.rename(columns={text_col: "text", label_col: "label"})
        df = pd.concat([df, df_extra[["text", "label"]]], ignore_index=True)
        print(f"Merged {extra_path} with {len(df_extra)} rows.")

print(f"Total samples after merging: {len(df)}")

# -----------------------------
# Drop missing values
# -----------------------------
df = df.dropna(subset=["text", "label"])
print(f"After dropping missing values: {len(df)} rows.")

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