import os
import glob
import pandas as pd
from sklearn.utils import shuffle

# Base data directory (relative to this script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "..", "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "dataset.csv")


def find_file(filename, search_dir=DATA_DIR):
    """
    Recursively search for a file inside a directory and return its path.
    If multiple are found, return the first one.
    """
    matches = glob.glob(os.path.join(search_dir, "**", filename), recursive=True)
    return matches[0] if matches else None


def load_datasets():
    fake_path = find_file("Fake.csv")
    true_path = find_file("True.csv")

    if not fake_path or not true_path:
        raise FileNotFoundError(
            f"Could not find Fake.csv or True.csv in {DATA_DIR} or its subfolders."
        )

    print(f"Found Fake.csv at: {fake_path}")
    print(f"Found True.csv at: {true_path}")

    fake_df = pd.read_csv(fake_path)
    true_df = pd.read_csv(true_path)

    fake_df["label"] = 0  # Fake
    true_df["label"] = 1  # True

    return pd.concat([fake_df, true_df], axis=0)


def prepare_dataset():
    df = load_datasets()

    # Standardize text column name
    if "text" not in df.columns:
        # Try common column names
        for col in ["content", "article", "body", "Text"]:
            if col in df.columns:
                df.rename(columns={col: "text"}, inplace=True)
                break

    # Drop rows without text
    df = df.dropna(subset=["text"])

    # Shuffle dataset
    df = shuffle(df).reset_index(drop=True)

    # Save final dataset
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"✅ Dataset prepared and saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    prepare_dataset()
