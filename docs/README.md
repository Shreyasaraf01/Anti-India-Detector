Anti-India Campaign Detector

A machine learning–powered web application that detects potential anti-India campaigns in online content (tweets, posts, or articles).

The system combines sentiment analysis, keyword checks, and a fake news classifier to decide whether a given text is normal or suspicious.

🚀 Features

Input Text Analysis: Paste any tweet, post, or news article.

Preprocessing: Text is cleaned (stopwords, URLs, mentions, hashtags removed).

Classification:

Trained RandomForest model on multilingual political/fake news datasets.

Uses SentenceTransformer embeddings (all-MiniLM-L6-v2).

Prediction Output:

Label → Normal or Likely Misinformation / Anti-India Campaign

Confidence score (percentage).

Interactive Visuals:

Pie Chart → Confidence vs. Uncertainty

Word Cloud → Frequent words in text

Frontend: Modern React.js interface

Backend: Django REST API serving ML predictions

⚙️ How It Works

User Input: Text (tweet/news/article) entered on the web page.

API Call: Sent to Django endpoint /api/analyze/.

Preprocessing:

Lowercase, remove URLs, hashtags, mentions.

Tokenization + stopword removal.

Embedding: Convert text into vector using SentenceTransformer.

Prediction: RandomForest model classifies text as real/normal or fake/suspicious.

Response: Returns label + confidence score to frontend.

Visualization: Pie chart and word cloud generated dynamically.

📊 Example

Input:

This propaganda article is spreading lies about India.


Output:

Label → Likely Misinformation

Confidence → 78.4%

Pie chart → 78% confidence vs. 22% uncertainty

Word Cloud → ["propaganda", "lies", "India"]

📂 Dataset

The model was trained on:

Fake news samples

Political tweets

Sentiment-labeled tweets

Multilingual Twitter data

Training file: indian_news_500.csv

🧑‍💻 Installation
Backend (Django + Python)
# Clone repo
git clone https://github.com/your-username/Anti-India-Detector.git
cd Anti-India-Detector/backend

# Setup virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Run Django server
python manage.py runserver

Frontend (React)
cd ../frontend

# Install dependencies
npm install

# Run development server
npm start

Frontend will be available at:
👉 http://localhost:3000

Backend will run at:
👉 http://127.0.0.1:8000

🛠️ Training the Model

To retrain the fake news classifier:
cd backend
python train_fake_classifier.py

This will:

Clean the dataset

Generate embeddings

Train a RandomForest model

Save files in backend/api/models/

📌 Tech Stack

Backend: Django, Python, NumPy, Pandas, Scikit-learn, SentenceTransformers

Frontend: React.js, Recharts, HTML, CSS

ML: RandomForest Classifier, MiniLM embeddings

Dataset: Fake/real political tweets & news articles