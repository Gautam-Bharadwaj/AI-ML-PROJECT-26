import pandas as pd
import os
import sys

sys.path.append(os.getcwd())

from src.preprocess import preprocess_dataframe

def start_pipeline(raw_csv, processed_csv):
    if not os.path.exists(raw_csv):
        print(f"File not found: {raw_csv}")
        return

    print(f"Loading data from {raw_csv}...")
    df = pd.read_csv(raw_csv)

    df = df.dropna(subset=['clause_text']).drop_duplicates(subset=['clause_text'])

    df = preprocess_dataframe(df, text_col='clause_text')

    os.makedirs(os.path.dirname(processed_csv), exist_ok=True)

    print(f"Saving to {processed_csv}...")
    df.to_csv(processed_csv, index=False)
    print("Done! Data is ready for ML training.")

if __name__ == "__main__":
    RAW = "data/raw/legal_docs_modified.csv"
    OUT = "data/processed/cleaned_legal_clauses.csv"
    start_pipeline(RAW, OUT)
