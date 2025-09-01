# backend/api/scripts/train_fake_classifier.py
from pathlib import Path
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

BASE = Path(__file__).resolve().parents[2]   # points to project root
DATA_DIR = BASE / "data"
MODELS_DIR = BASE / "backend" / "api" / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

DATA_PATH = r"C:\Users\riyas\OneDrive\Desktop\anti_india_detector\data\Tweets.csv"
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"

df = pd.read_csv(DATA_PATH).dropna(subset=["text","label"])
texts = df["text"].tolist()
labels = df["label"].astype(int).tolist()

embedder = SentenceTransformer(EMBED_MODEL_NAME)
embeddings = embedder.encode(texts, show_progress_bar=True, convert_to_numpy=True)

X_train, X_test, y_train, y_test = train_test_split(embeddings, labels, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=200, n_jobs=-1, random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print(classification_report(y_test, y_pred))

joblib.dump(clf, MODELS_DIR / "fake_rf.joblib")
# save embedding model name so inference can load the same embedder
(MODELS_DIR / "embed_model_name.txt").write_text(EMBED_MODEL_NAME)
print("Saved fake_rf.joblib and embed_model_name.txt to", MODELS_DIR)
