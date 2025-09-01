# backend/api/scripts/prepare_fake_dataset.py
from pathlib import Path
import pandas as pd
from backend.api.utils.preprocess import clean_text

ROOT = Path(__file__).resolve().parents[2]   # project root
DATA_DIR = ROOT / "data"
OUT = DATA_DIR / "fake_news_dataset.csv"

# Attempt to load common filenames (adjust names if different)
candidates = [
    DATA_DIR / "Fake.csv",
    DATA_DIR / "True.csv",
    DATA_DIR / "fake-news-detection" / "data.csv",   # other dataset
    DATA_DIR / "fake-and-real-news-dataset.zip"      # ignored if zipped
]

frames = []
for p in candidates:
    if p.exists():
        try:
            df = pd.read_csv(p)
            print("Loaded", p.name, "shape:", df.shape)
            # Heuristics: try to locate text/title columns and label
            if "text" in df.columns and "title" in df.columns:
                df["text_combined"] = df["title"].fillna("") + " " + df["text"].fillna("")
            elif "title" in df.columns:
                df["text_combined"] = df["title"].astype(str)
            elif "headline" in df.columns:
                df["text_combined"] = df["headline"].astype(str)
            elif "content" in df.columns:
                df["text_combined"] = df["content"].astype(str)
            else:
                # fallback to first column
                df["text_combined"] = df.iloc[:,0].astype(str)

            # Determine label: if dataset contains "label"/"truth" etc.
            if "label" in df.columns:
                lab = df["label"]
            elif "truth" in df.columns:
                lab = df["truth"]
            elif "class" in df.columns:
                lab = df["class"]
            else:
                # If this is Fake/True pair, infer label by filename
                lab = 1 if "Fake" in p.name else 0

            df2 = df[["text_combined"]].copy()
            df2 = df2.rename(columns={"text_combined":"text"})
            df2["label"] = lab.astype(int) if hasattr(lab, "astype") else lab
            frames.append(df2)
        except Exception as e:
            print("Could not load", p, e)

if not frames:
    print("No input files found. Please place Fake.csv/True.csv etc in data/")
else:
    combined = pd.concat(frames, ignore_index=True)
    combined["text"] = combined["text"].astype(str).map(clean_text)
    combined = combined.drop_duplicates(subset=["text"])
    combined.to_csv(OUT, index=False)
    print("Saved combined fake dataset to", OUT, "shape:", combined.shape)
