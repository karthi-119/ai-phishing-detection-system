"""
Dataset Validation & Quality Assurance Script.

Verifies integrity, non-null properties, column alignment, target value mapping,
and class distribution consistency between train.csv and test.csv.
"""

import sys
import io
from pathlib import Path
import pandas as pd

# Ensure UTF-8 output encoding for console safety
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

EXPECTED_FEATURE_COUNT = 30
EXPECTED_TOTAL_COLUMNS = 31
TARGET_COLUMN = "result"
VALID_TARGET_VALUES = {-1, 1}


def validate_dataset_files():
    """
    Validates train.csv and test.csv dataset files.
    """
    data_dir = Path(__file__).resolve().parent.parent / "data"
    train_path = data_dir / "train.csv"
    test_path = data_dir / "test.csv"

    print("=" * 70)
    print("RUNNING DATASET QUALITY CHECKS & VALIDATION")
    print("=" * 70)

    # 1. Verify file existence
    errors = []
    if not train_path.exists():
        errors.append(f"Missing train dataset: {train_path}")
    if not test_path.exists():
        errors.append(f"Missing test dataset: {test_path}")

    if errors:
        for err in errors:
            print(f"[FAIL] {err}")
        sys.exit(1)

    print("[PASS] Check 1: Both train.csv and test.csv files exist.")

    # 2. Load datasets
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    print(f"   - Training dataset shape : {train_df.shape}")
    print(f"   - Testing dataset shape  : {test_df.shape}")

    # 3. Column Count & Alignment Verification
    if len(train_df.columns) != EXPECTED_TOTAL_COLUMNS:
        errors.append(f"Expected {EXPECTED_TOTAL_COLUMNS} columns in train.csv, found {len(train_df.columns)}")
    if len(test_df.columns) != EXPECTED_TOTAL_COLUMNS:
        errors.append(f"Expected {EXPECTED_TOTAL_COLUMNS} columns in test.csv, found {len(test_df.columns)}")
    if list(train_df.columns) != list(test_df.columns):
        errors.append("Column alignment mismatch between train.csv and test.csv.")

    if TARGET_COLUMN not in train_df.columns:
        errors.append(f"Target column '{TARGET_COLUMN}' missing from train.csv.")

    if not errors:
        print(f"[PASS] Check 2: Exactly {EXPECTED_TOTAL_COLUMNS} columns ({EXPECTED_FEATURE_COUNT} features + 1 target '{TARGET_COLUMN}') present and aligned.")

    # 4. Null & Missing Value Check
    train_nulls = train_df.isnull().sum().sum()
    test_nulls = test_df.isnull().sum().sum()

    if train_nulls > 0:
        errors.append(f"Found {train_nulls} null values in train.csv.")
    if test_nulls > 0:
        errors.append(f"Found {test_nulls} null values in test.csv.")

    if not errors:
        print("[PASS] Check 3: Zero missing or null values found in train and test datasets.")

    # 5. Target Label Validity Check
    train_targets = set(train_df[TARGET_COLUMN].unique())
    test_targets = set(test_df[TARGET_COLUMN].unique())

    if not train_targets.issubset(VALID_TARGET_VALUES):
        errors.append(f"Unexpected target values in train.csv: {train_targets - VALID_TARGET_VALUES}")
    if not test_targets.issubset(VALID_TARGET_VALUES):
        errors.append(f"Unexpected target values in test.csv: {test_targets - VALID_TARGET_VALUES}")

    if not errors:
        print(f"[PASS] Check 4: Target values belong strictly to valid set {VALID_TARGET_VALUES} (-1=Phishing, 1=Legitimate).")

    # 6. Stratified Class Ratio Check
    train_dist = train_df[TARGET_COLUMN].value_counts(normalize=True).to_dict()
    test_dist = test_df[TARGET_COLUMN].value_counts(normalize=True).to_dict()

    print(f"\n   - Train Class Ratios : Legitimate (1): {train_dist.get(1, 0)*100:.2f}%, Phishing (-1): {train_dist.get(-1, 0)*100:.2f}%")
    print(f"   - Test Class Ratios  : Legitimate (1): {test_dist.get(1, 0)*100:.2f}%, Phishing (-1): {test_dist.get(-1, 0)*100:.2f}%")

    ratio_diff = abs(train_dist.get(1, 0) - test_dist.get(1, 0))
    if ratio_diff > 0.01:
        errors.append(f"Class ratio mismatch between train and test splits ({ratio_diff:.4f} difference).")

    if not errors:
        print("[PASS] Check 5: Stratified train/test class distributions match closely.")

    # Final Summary
    if errors:
        print("\n[FAIL] DATA VALIDATION FAILED WITH ERRORS:")
        for err in errors:
            print(f"   - {err}")
        sys.exit(1)
    else:
        print("\n[SUCCESS] ALL DATA QUALITY CHECKS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    validate_dataset_files()
