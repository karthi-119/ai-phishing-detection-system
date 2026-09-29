"""
Model Evaluation Script for AI Phishing Detection System.

Evaluates trained Random Forest model using ONLY ml/data/test.csv.
Computes Accuracy, Precision, Recall, F1-Score, and Confusion Matrix.
Generates evaluation artifacts:
- ml/outputs/evaluation/confusion_matrix.png
- ml/outputs/evaluation/feature_importance.csv
- ml/outputs/evaluation/feature_importance.png (Top 10 features)
- ml/models/model_metadata.json
"""

import sys
import json
from datetime import datetime
from pathlib import Path
import pandas as pd
import numpy as np
import joblib

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

TARGET_COLUMN = "result"


def evaluate_model():
    """
    Evaluates saved model on test.csv and exports evaluation metrics and charts.
    """
    base_dir = Path(__file__).resolve().parent.parent
    test_path = base_dir / "data" / "test.csv"
    train_path = base_dir / "data" / "train.csv"
    model_path = base_dir / "models" / "phishing_rf_model.pkl"
    feature_cols_path = base_dir / "models" / "feature_columns.pkl"
    eval_dir = base_dir / "outputs" / "evaluation"
    eval_dir.mkdir(parents=True, exist_ok=True)

    if not model_path.exists():
        print(f"Error: Trained model not found at {model_path}. Run train_model.py first.")
        sys.exit(1)
    if not test_path.exists():
        print(f"Error: Test data not found at {test_path}. Run preprocessing.py first.")
        sys.exit(1)

    print("=" * 70)
    print("EVALUATING MODEL PERFORMANCE ON TEST DATASET")
    print("=" * 70)

    # 1. Load Model, Feature Columns, and Test Data
    rf_model = joblib.load(model_path)
    feature_columns = joblib.load(feature_cols_path)

    df_test = pd.read_csv(test_path)
    df_train = pd.read_csv(train_path)

    X_test = df_test[feature_columns]
    y_test = df_test[TARGET_COLUMN]

    print(f"Loaded Test Dataset: {X_test.shape[0]} samples, {X_test.shape[1]} features.")

    # 2. Generate Model Predictions
    y_pred = rf_model.predict(X_test)

    # 3. Calculate Performance Metrics (TASK 3)
    # Using pos_label=1 (Legitimate) / -1 (Phishing), weighted average for multiclass/binary summary
    accuracy = float(accuracy_score(y_test, y_pred))
    precision = float(precision_score(y_test, y_pred, pos_label=-1))  # Phishing precision
    recall = float(recall_score(y_test, y_pred, pos_label=-1))        # Phishing recall
    f1 = float(f1_score(y_test, y_pred, pos_label=-1))                # Phishing F1

    macro_precision = float(precision_score(y_test, y_pred, average='macro'))
    macro_recall = float(recall_score(y_test, y_pred, average='macro'))
    macro_f1 = float(f1_score(y_test, y_pred, average='macro'))

    cm = confusion_matrix(y_test, y_pred, labels=[-1, 1])

    print("\n--- MEASURED PERFORMANCE METRICS (TEST SET) ---")
    print(f"Accuracy               : {accuracy:.4f} ({accuracy * 100:.2f}%)")
    print(f"Precision (Phishing -1): {precision:.4f} ({precision * 100:.2f}%)")
    print(f"Recall (Phishing -1)   : {recall:.4f} ({recall * 100:.2f}%)")
    print(f"F1-Score (Phishing -1) : {f1:.4f} ({f1 * 100:.2f}%)")
    print(f"Macro F1-Score         : {macro_f1:.4f} ({macro_f1 * 100:.2f}%)")

    print("\n--- CLASSIFICATION REPORT ---")
    class_report_str = classification_report(y_test, y_pred, target_names=['Phishing (-1)', 'Legitimate (1)'])
    print(class_report_str)

    print("\n--- CONFUSION MATRIX ---")
    print("Labels: [-1: Phishing, 1: Legitimate]")
    print(cm)

    # 4. Save Confusion Matrix Plot
    plt.figure(figsize=(7, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Blues',
        xticklabels=['Phishing (-1)', 'Legitimate (1)'],
        yticklabels=['Phishing (-1)', 'Legitimate (1)']
    )
    plt.title('Confusion Matrix - Random Forest Classifier', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.ylabel('Actual True Label', fontsize=12)
    plt.tight_layout()
    cm_path = eval_dir / "confusion_matrix.png"
    plt.savefig(cm_path, dpi=300)
    plt.close()

    # 5. Extract Feature Importance (TASK 4)
    importances = rf_model.feature_importances_
    fi_df = pd.DataFrame({
        'Feature': feature_columns,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False).reset_index(drop=True)

    # Save feature importance table to CSV
    fi_csv_path = eval_dir / "feature_importance.csv"
    fi_df.to_csv(fi_csv_path, index=False)

    print("\n--- TOP 10 IMPORTANT FEATURES ---")
    print(fi_df.head(10).to_string(index=False))

    # Save Top 10 Feature Importance Bar Plot
    top10_fi = fi_df.head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(
        x='Importance',
        y='Feature',
        data=top10_fi,
        hue='Feature',
        palette='viridis',
        legend=False
    )
    plt.title('Top 10 Most Important Features (Random Forest)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Gini Importance', fontsize=12)
    plt.ylabel('Feature Name', fontsize=12)
    plt.tight_layout()
    fi_img_path = eval_dir / "feature_importance.png"
    plt.savefig(fi_img_path, dpi=300)
    plt.close()

    # 6. Save Model Metadata (TASK 6)
    metadata = {
        "model_name": "Phishing_URL_RandomForest_v1",
        "algorithm": "RandomForestClassifier",
        "dataset_name": "UCI Phishing Websites Dataset (ID 327)",
        "number_of_training_samples": int(len(df_train)),
        "number_of_test_samples": int(len(df_test)),
        "number_of_features": int(len(feature_columns)),
        "random_state": 42,
        "n_estimators": 200,
        "metrics": {
            "accuracy": round(accuracy, 4),
            "phishing_precision": round(precision, 4),
            "phishing_recall": round(recall, 4),
            "phishing_f1_score": round(f1, 4),
            "macro_f1_score": round(macro_f1, 4)
        },
        "training_timestamp": datetime.now().isoformat()
    }

    metadata_path = base_dir / "models" / "model_metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    print(f"\nSaved confusion matrix plot to : {cm_path}")
    print(f"Saved feature importances CSV to: {fi_csv_path}")
    print(f"Saved feature importances plot to: {fi_img_path}")
    print(f"Saved model metadata JSON to   : {metadata_path}")

    return metadata, fi_df


if __name__ == "__main__":
    evaluate_model()
