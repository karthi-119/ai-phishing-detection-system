"""
Dataset Acquisition Script for Phishing Websites Dataset (UCI ID: 327).

Downloads the official UCI Phishing Websites dataset using ucimlrepo
and saves it locally to ml/data/phishing_websites.csv.
"""

import sys
from pathlib import Path
import pandas as pd
from ucimlrepo import fetch_ucirepo


def download_uci_dataset():
    """
    Downloads UCI Dataset ID 327 ('Phishing Websites') and saves as CSV.
    """
    print("Fetching UCI Phishing Websites dataset (ID: 327)...")

    try:
        phishing_websites = fetch_ucirepo(id=327)
    except Exception as e:
        print(f"Error fetching dataset from UCI repository: {e}")
        sys.exit(1)

    # Extract features (X) and targets (y)
    X = phishing_websites.data.features
    y = phishing_websites.data.targets

    print(f"Features shape: {X.shape}")
    print(f"Targets shape: {y.shape}")

    # Combine features and target into a single pandas DataFrame
    df = pd.concat([X, y], axis=1)

    # Ensure output directory exists
    output_dir = Path(__file__).resolve().parent.parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "phishing_websites.csv"
    df.to_csv(csv_path, index=False)

    print(f"Dataset successfully saved to: {csv_path}")
    print(f"Total Rows: {len(df)}, Total Columns: {len(df.columns)}")
    return df, phishing_websites.metadata


if __name__ == "__main__":
    download_uci_dataset()
