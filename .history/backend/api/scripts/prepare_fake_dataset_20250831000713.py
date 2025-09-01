from pathlib import Path
import pandas as pd
from backend.api.utils.preprocess import clean_text

ROOT = Path(__file__).resolve().parents[2]   # project root
DATA_DIR = ROOT / "data"
OUT = DATA_DIR / "fake_news_dataset.csv"

# Collect all candidate files (case-insensitive check)
all_files = {p.name.lower(): p for p in DATA_DIR.glob("*.csv")}
all_files.update({p.name.lower(): p for p in (DATA_DIR / "fake-and-real-news").glob("*.csv") if (DATA_DIR / "fake-and-real-news").exists()})
all_files.update({p.name.lower(): p for p in (DATA_DIR / "fake-news-detection").glob("*.csv") if (DATA_DIR / "fake-news-detection").exists()})

frames = []
for name in ["fake.csv", "true.csv", "data.csv"]:
    if name in all_files:
        p = all_files[name]
        try:
            df = pd.read_csv(p)
            print("Loaded", p, "shape:", df.shape)

            # Combine title/text/content/headline columns
            if "text" in df.columns and "title" in df.columns:
                df["text_combined"] = df["title"].fillna("") + " " + df["text"].fillna("")
            elif "title" in df.columns:
                df["text_combined"] = df["title"].astype(str)
            elif "headline" in df.columns:
                df["text_combined"] = df["headline"].astype(str)
            elif "content" in df.columns:
                df["text_combined"] = df["content"].astype(str)
            else:
                df["text_combined"] = df.iloc[:,0].astype(str)

            # Assign labels
            if "label" in df.columns:
                lab = df["label"]
            elif "truth" in df.columns:
                lab = df["truth"]
            elif "class" in df.columns:
                lab = df["class"]
            else:
                lab = 1 if "fake" in name else 0  # infer from filename

            df2 = df[["text_combined"]].copy()
            df2 = df2.rename(columns={"text_combined": "text"})
            df2["label"] = lab.astype(int) if hasattr(lab, "astype") else lab
            frames.append(df2)

        except Exception as e:
            print("Could not load", p, e)

if not frames:
    print("No input files found. Please place Fake.csv/True.csv in data/ or data/fake-and-real-news/")
else:
    combined = pd.concat(frames, ignore_index=True)
    combined["text"] = combined["text"].astype(str).map(clean_text)
    combined = combined.drop_duplicates(subset=["text"])
    combined.to_csv(OUT, index=False)
    print("✅ Saved combined fake dataset to", OUT, "shape:", combined.shape)
