import os
import pandas as pd
from backend.api.utils.preprocess import clean_text

# Base data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")

# Function to recursively search for file
def find_file(filename, base_dir=DATA_DIR):
    for root, _, files in os.walk(base_dir):
        if filename in files:
            return os.path.join(root, filename)
    return None

def load_datasets():
    fake_path = find_file("Fake.csv")
    true_path = find_file("True.csv")

    if not fake_path or not true_path:
        raise FileNotFoundError(
            f"Could not find Fake.csv or True.csv in {DATA_DIR} or its subfolders."
        )

    fake_df = pd.read_csv(fake_path)
    true_df = pd.read_csv(true_path)

    # Add labels
    fake_df["label"] = 0
    true_df["label"] = 1

    # Merge
    df = pd.concat([fake_df, true_df], ignore_index=True)

    # Clean text column
    if "text" in df.columns:
        df["text"] = df["text"].apply(clean_text)
    elif "title" in df.columns:  # sometimes dataset has title instead
        df["title"] = df["title"].apply(clean_text)

    return df

if __name__ == "__main__":
    df = load_datasets()
    print(f"Dataset loaded with {len(df)} rows")
    print(df.head())
