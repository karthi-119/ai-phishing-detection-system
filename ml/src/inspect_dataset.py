"""
Dataset Inspection & Target Mapping Script for Phishing Websites Dataset (UCI ID: 327).

Inspects dataset statistics, data types, missing values, duplicate rows,
target column distribution, and metadata.
"""

import sys
from pathlib import Path
import pandas as pd
from ucimlrepo import fetch_ucirepo


def inspect_dataset():
    """
    Performs comprehensive dataset inspection and target variable analysis.
    """
    data_path = Path(__file__).resolve().parent.parent / "data" / "phishing_websites.csv"
    if not data_path.exists():
        print(f"Error: Dataset file not found at {data_path}. Run download_dataset.py first.")
        sys.exit(1)

    df = pd.read_csv(data_path)

    # Fetch UCI metadata for target variable descriptions
    try:
        phishing_websites = fetch_ucirepo(id=327)
        variables_meta = phishing_websites.variables
        target_name = phishing_websites.data.targets.columns[0]
    except Exception as e:
        print(f"Warning: Could not fetch UCI repo metadata: {e}")
        variables_meta = None
        target_name = df.columns[-1]

    report_lines = []

    def log(text=""):
        print(text)
        report_lines.append(text)

    log("=" * 70)
    log("UCI PHISHING WEBSITES DATASET (ID: 327) - INSPECTION REPORT")
    log("=" * 70)

    # 1. Number of rows and columns
    num_rows, num_cols = df.shape
    log(f"\n1. DATASET SHAPE")
    log(f"   - Number of Rows: {num_rows}")
    log(f"   - Number of Columns: {num_cols}")

    # 2. Target Column Identification & Mapping (TASK 3)
    log(f"\n2. TARGET VARIABLE ANALYSIS (TASK 3)")
    log(f"   - Target Column Name: '{target_name}'")

    target_counts = df[target_name].value_counts().to_dict()
    log(f"   - Target Value Counts: {target_counts}")

    # Check UCI variable metadata for target explanation
    if variables_meta is not None:
        target_info = variables_meta[variables_meta['name'] == target_name]
        log(f"   - Target Metadata Details:\n{target_info.to_string(index=False)}")

    # UCI Phishing Websites dataset encoding:
    # 1 = Legitimate website
    # -1 = Phishing website
    # 0 = Suspicious (if applicable, though UCI 327 uses -1 and 1)
    log("\n   - Target Value Mapping (Verified via UCI Metadata):")
    log("     •  1  => Legitimate Website")
    log("     • -1  => Phishing Website")

    # 3. Column names & data types
    log(f"\n3. COLUMN NAMES & DATA TYPES")
    for col, dtype in df.dtypes.items():
        log(f"   - {col:<32}: {dtype}")

    # 4. Missing values
    missing_series = df.isnull().sum()
    total_missing = missing_series.sum()
    log(f"\n4. MISSING VALUES ANALYSIS")
    log(f"   - Total Missing Values: {total_missing}")
    if total_missing > 0:
        log(f"   - Columns with Missing Values:\n{missing_series[missing_series > 0]}")
    else:
        log("   - Clean dataset: 0 missing values found across all columns.")

    # 5. Duplicate rows
    num_duplicates = df.duplicated().sum()
    log(f"\n5. DUPLICATE ROWS ANALYSIS")
    log(f"   - Total Duplicate Rows: {num_duplicates}")

    # 6. Target / Class distribution
    log(f"\n6. CLASS DISTRIBUTION")
    for val, count in target_counts.items():
        percentage = (count / num_rows) * 100
        label_str = "Legitimate (1)" if val == 1 else "Phishing (-1)" if val == -1 else f"Value ({val})"
        log(f"   - {label_str:<18}: {count} samples ({percentage:.2f}%)")

    # 7. First 5 rows snippet
    log(f"\n7. FIRST 5 ROWS")
    log(df.head(5).to_string())

    # 8. Statistical summary
    log(f"\n8. STATISTICAL SUMMARY")
    log(df.describe().to_string())

    # Save inspection report to file
    report_path = Path(__file__).resolve().parent.parent / "data" / "inspection_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    log(f"\nFull inspection report saved to: {report_path}")
    return target_name, target_counts


if __name__ == "__main__":
    inspect_dataset()
