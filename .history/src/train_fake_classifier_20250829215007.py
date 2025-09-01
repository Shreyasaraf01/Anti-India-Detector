import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os
from preprocess import clean_text

# Get absolute project root (where this script is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(MODELS_DIR, exist_ok=True)

# Load dataset safely
data_path = os.path.join(DATA_DIR, "sample_data.csv")
df = pd.read_csv(data_path)

# Preprocess
df['clean'] = df['text'].apply(clean_text)

X = df['clean']
y = df['label']

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer(max_features=2000, ngram_range=(1,2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Logistic Regression Classifier
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train_vec, y_train)

# Evaluate
y_pred = clf.predict(X_test_vec)
print("Classification report:")
print(classification_report(y_test, y_pred))

# Save model + vectorizer
clf_path = os.path.join(MODELS_DIR, "fakeclf.joblib")
vec_path = os.path.join(MODELS_DIR, "vectorizer.joblib")

joblib.dump(clf, clf_path)
joblib.dump(vectorizer, vec_path)

print(f"✅ Models saved in: {MODELS_DIR}")
