from pathlib import Path
import pandas as pd

# FIX: Go 3 levels up from scripts/ -> api -> backend -> project root
ROOT = Path(__file__).resolve().parents[3]  
DATA_DIR = ROOT / "data"
OUT = DATA_DIR / "fake_news_dataset.csv"


def clean_text(text: str) -> str:
    """Simple text cleaner (you can extend with regex, stopwords, etc.)."""
    if not isinstance(text, str):
        return ""
    return " ".join(text.split())


def load_datasets():
    """Recursively load all CSVs under data/ that look like Fake/True datasets."""
    csv_files = list(DATA_DIR.rglob("*.csv"))
    frames = []

    for p in csv_files:
        try:
            df = pd.read_csv(p)
            print(f"Loaded {p.name}, shape={df.shape}")

            # --- Identify text columns ---
            if "text" in df.columns and "title" in df.columns:
                df["text_combined"] = df["title"].fillna("") + " " + df["text"].fillna("")
            elif "text" in df.columns:
                df["text_combined"] = df["text"].astype(str)
            elif "title" in df.columns:
                df["text_combined"] = df["title"].astype(str)
            elif "headline" in df.columns:
                df["text_combined"] = df["headline"].astype(str)
            elif "content" in df.columns:
                df["text_combined"] = df["content"].astype(str)
            else:
                df["text_combined"] = df.iloc[:, 0].astype(str)

            # --- Identify labels ---
            if "label" in df.columns:
                lab = df["label"]
            elif "truth" in df.columns:
                lab = df["truth"]
            elif "class" in df.columns:
                lab = df["class"]
            else:
                # Heuristic: infer from filename
                if "fake" in p.name.lower():
                    lab = 1
                elif "true" in p.name.lower():
                    lab = 0
                else:
                    print(f"⚠ Skipping {p.name}, no label info found")
                    continue

            df2 = df[["text_combined"]].copy()
            df2 = df2.rename(columns={"text_combined": "text"})
            df2["label"] = lab.astype(int) if hasattr(lab, "astype") else lab
            frames.append(df2)

        except Exception as e:
            print(f"❌ Could not load {p.name}: {e}")

    if not frames:
        raise FileNotFoundError(f"No suitable CSV files found under {DATA_DIR}")

    return pd.concat(frames, ignore_index=True)


def prepare_dataset():
    df = load_datasets()
    df["text"] = df["text"].astype(str).map(clean_text)
    df = df.drop_duplicates(subset=["text"])
    df.to_csv(OUT, index=False)
    print(f"✅ Saved combined dataset to {OUT}, shape={df.shape}")


if __name__ == "__main__":
    prepare_dataset()
