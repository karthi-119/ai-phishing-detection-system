"""
Exploratory Data Analysis (EDA) Script for AI Phishing Detection System.

Analyzes training dataset (ml/data/train.csv) and generates visualizations:
1. Class distribution bar chart (class_distribution.png)
2. Feature correlation heatmap (correlation_heatmap.png)
3. Target correlation ranking bar chart (feature_importance_eda.png)
4. Important feature distributions (feature_distributions.png)
5. Target distribution pie chart (target_distribution.png)

Outputs saved to ml/outputs/eda/ directory.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for headless rendering
import matplotlib.pyplot as plt
import seaborn as sns

TARGET_COLUMN = "result"


def perform_eda():
    """
    Executes EDA on training dataset and saves plots to ml/outputs/eda/.
    """
    # 1. Load Training Data
    base_dir = Path(__file__).resolve().parent.parent
    train_path = base_dir / "data" / "train.csv"
    output_dir = base_dir / "outputs" / "eda"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not train_path.exists():
        print(f"Error: Training file not found at {train_path}. Run preprocessing.py first.")
        sys.exit(1)

    df_train = pd.read_csv(train_path)

    print("=" * 70)
    print("EXPLORATORY DATA ANALYSIS (TRAINING DATASET)")
    print("=" * 70)

    # Print basic statistics
    print(f"\n1. Dataset Shape: {df_train.shape} ({df_train.shape[0]} rows, {df_train.shape[1]} cols)")
    feature_cols = [c for c in df_train.columns if c != TARGET_COLUMN]
    print(f"2. Feature Count: {len(feature_cols)}")
    print(f"3. Feature Names:\n   {feature_cols}")

    target_counts = df_train[TARGET_COLUMN].value_counts().to_dict()
    print(f"\n4. Target Distribution: {target_counts}")
    print(f"   - Legitimate (1) : {target_counts.get(1, 0)} samples ({target_counts.get(1, 0)/len(df_train)*100:.2f}%)")
    print(f"   - Phishing (-1)  : {target_counts.get(-1, 0)} samples ({target_counts.get(-1, 0)/len(df_train)*100:.2f}%)")

    print("\n5. Descriptive Statistics:")
    print(df_train.describe().T[['mean', 'std', 'min', '50%', 'max']].to_string())

    # Compute correlation with target
    correlations = df_train.corr()[TARGET_COLUMN].drop(TARGET_COLUMN).sort_values(ascending=False)
    print("\n6. Top 10 Positive Correlations with Target (Legitimate):")
    print(correlations.head(10).to_string())
    print("\n7. Top 10 Negative Correlations with Target (Phishing):")
    print(correlations.tail(10).to_string())

    # --- PLOT 1: Class Distribution Bar Chart ---
    plt.figure(figsize=(7, 5))
    ax = sns.barplot(
        x=['Phishing (-1)', 'Legitimate (1)'],
        y=[target_counts.get(-1, 0), target_counts.get(1, 0)],
        palette=['#ef4444', '#10b981']
    )
    plt.title('Target Class Distribution (Training Dataset)', fontsize=14, fontweight='bold', pad=15)
    plt.ylabel('Number of Samples', fontsize=12)
    plt.xlabel('Class Label', fontsize=12)
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height()):,}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 8), textcoords='offset points', fontweight='bold')
    plt.tight_layout()
    plot1_path = output_dir / "class_distribution.png"
    plt.savefig(plot1_path, dpi=300)
    plt.close()

    # --- PLOT 2: Feature Correlation Heatmap ---
    plt.figure(figsize=(16, 14))
    sns.heatmap(df_train.corr(), annot=False, cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5)
    plt.title('Feature Correlation Heatmap', fontsize=16, fontweight='bold', pad=15)
    plt.tight_layout()
    plot2_path = output_dir / "correlation_heatmap.png"
    plt.savefig(plot2_path, dpi=300)
    plt.close()

    # --- PLOT 3: Target Correlation Ranking (Feature Importance EDA) ---
    plt.figure(figsize=(10, 10))
    colors = ['#10b981' if v > 0 else '#ef4444' for v in correlations.values]
    sns.barplot(x=correlations.values, y=correlations.index, palette=colors)
    plt.title('Feature Correlation with Target (Result)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Pearson Correlation Coefficient', fontsize=12)
    plt.axvline(0, color='gray', linestyle='--', linewidth=1)
    plt.tight_layout()
    plot3_path = output_dir / "feature_importance_eda.png"
    plt.savefig(plot3_path, dpi=300)
    plt.close()

    # --- PLOT 4: Top 4 Correlated Feature Distributions ---
    top_features = correlations.abs().sort_values(ascending=False).head(4).index
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    for idx, feat in enumerate(top_features):
        sns.countplot(data=df_train, x=feat, hue=TARGET_COLUMN, ax=axes[idx], palette={1: '#10b981', -1: '#ef4444'})
        axes[idx].set_title(f'Distribution: {feat}', fontsize=12, fontweight='bold')
        axes[idx].set_xlabel('Feature Value', fontsize=10)
        axes[idx].set_ylabel('Count', fontsize=10)
        axes[idx].legend(title='Target', labels=['Phishing (-1)', 'Legitimate (1)'])
    plt.tight_layout()
    plot4_path = output_dir / "feature_distributions.png"
    plt.savefig(plot4_path, dpi=300)
    plt.close()

    # --- PLOT 5: Target Distribution Pie Chart ---
    plt.figure(figsize=(6, 6))
    plt.pie(
        [target_counts.get(1, 0), target_counts.get(-1, 0)],
        labels=['Legitimate (1)', 'Phishing (-1)'],
        autopct='%1.1f%%',
        colors=['#10b981', '#ef4444'],
        startangle=140,
        explode=(0.03, 0.03)
    )
    plt.title('Target Class Balance Ratio', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plot5_path = output_dir / "target_distribution.png"
    plt.savefig(plot5_path, dpi=300)
    plt.close()

    print(f"\nSaved all 5 EDA visualization plots inside: {output_dir}")


if __name__ == "__main__":
    perform_eda()
