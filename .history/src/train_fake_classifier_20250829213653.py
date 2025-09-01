import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os
from preprocess import clean_text

os.makedirs("models", exist_ok=True)

df = pd.read_csv("../data/sample_data.csv")
df['clean'] = df['text'].apply(clean_text)

X = df['clean']
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer(max_features=2000, ngram_range=(1,2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

clf = LogisticRegression(max_iter=1000)
clf.fit(X_train_vec, y_train)

y_pred = clf.predict(X_test_vec)
print("Classification report:")
print(classification_report(y_test, y_pred))

joblib.dump(clf, "../models/fakeclf.joblib")
joblib.dump(vectorizer, "../models/vectorizer.joblib")
print("Saved models to ../models/")
