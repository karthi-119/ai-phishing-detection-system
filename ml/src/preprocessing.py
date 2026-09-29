"""
Reusable Preprocessing Pipeline for AI Phishing Detection System.

Handles:
1. Loading raw dataset.
2. Feature/target separation.
3. Numeric type validation and missing value checks.
4. Stratified 80/20 train/test split (random_state=42).
5. Saving processed train.csv and test.csv without data leakage.
"""

import sys
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

# Target column name defined in UCI dataset ID 327
TARGET_COLUMN = "result"
RANDOM_STATE = 42
TEST_SIZE = 0.20


def load_raw_dataset(csv_path: Path) -> pd.DataFrame:
    """
    Loads raw CSV dataset from local storage.
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found at {csv_path}. Run download_dataset.py first.")
    df = pd.read_csv(csv_path)
    return df


def preprocess_data(df: pd.DataFrame, target_col: str = TARGET_COLUMN):
    """
    Preprocesses dataset:
    - Validates target column presence
    - Validates numeric conversions
    - Checks missing values
    - Separates features (X) and target (y)
    - Performs stratified train/test split (80/20) with random_state=42
    
    Data Leakage Prevention:
    - Splitting is performed FIRST before any potential feature scaling or transformations.
    - Test set remains isolated and untouched.
    """
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in dataset columns.")

    # 1. Check & handle missing values
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        print(f"Warning: Found {missing_count} missing values. Imputing with median.")
        df = df.fillna(df.median())
    else:
        print("Dataset check: No missing values found.")

    # 2. Ensure all feature columns are numeric
    feature_cols = [c for c in df.columns if c != target_col]
    for col in feature_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Re-check nulls after numeric conversion
    if df.isnull().sum().sum() > 0:
        df = df.fillna(0)

    # 3. Separate features (X) and target (y)
    X = df[feature_cols]
    y = df[target_col]

    # Validate target values (-1 = phishing, 1 = legitimate)
    unique_targets = set(y.unique())
    print(f"Target variable unique values: {sorted(list(unique_targets))}")

    # 4. Stratified Train/Test Split (80% train / 20% test)
    # Stratification ensures target class proportions (-1 vs 1) are identical in train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )

    print("\n--- Stratified Train/Test Split Summary ---")
    print(f"Training Set Shape : {X_train.shape} (Target distribution: {dict(y_train.value_counts())})")
    print(f"Testing Set Shape  : {X_test.shape} (Target distribution: {dict(y_test.value_counts())})")

    # Combine X and y into clean DataFrames for saving
    train_df = pd.concat([X_train, y_train], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)

    return train_df, test_df


def save_processed_splits(train_df: pd.DataFrame, test_df: pd.DataFrame, data_dir: Path):
    """
    Saves train.csv and test.csv to dataset directory.
    """
    data_dir.mkdir(parents=True, exist_ok=True)

    train_path = data_dir / "train.csv"
    test_path = data_dir / "test.csv"

    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)

    print(f"\nSaved processed training set to : {train_path} ({len(train_df)} rows)")
    print(f"Saved processed testing set to  : {test_path} ({len(test_df)} rows)")
    return train_path, test_path


def run_pipeline():
    """
    Runs the complete preprocessing pipeline.
    """
    data_dir = Path(__file__).resolve().parent.parent / "data"
    raw_csv = data_dir / "phishing_websites.csv"

    print(f"Loading raw dataset from {raw_csv}...")
    df = load_raw_dataset(raw_csv)

    train_df, test_df = preprocess_data(df)
    save_processed_splits(train_df, test_df, data_dir)


if __name__ == "__main__":
    run_pipeline()
