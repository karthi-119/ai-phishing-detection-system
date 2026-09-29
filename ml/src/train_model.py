"""
Random Forest Model Training Script for AI Phishing Detection System.

Trains a Random Forest Classifier using ONLY the training dataset (ml/data/train.csv).
Serializes the trained model artifact and feature column list to ml/models/.
"""

import sys
from pathlib import Path
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

TARGET_COLUMN = "result"
MODEL_CONFIG = {
    "n_estimators": 200,
    "random_state": 42,
    "max_depth": None,
    "n_jobs": -1
}


def train_model():
    """
    Trains Random Forest classifier on ml/data/train.csv and saves model artifacts.
    """
    base_dir = Path(__file__).resolve().parent.parent
    train_path = base_dir / "data" / "train.csv"
    models_dir = base_dir / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    if not train_path.exists():
        print(f"Error: Training file not found at {train_path}. Run preprocessing.py first.")
        sys.exit(1)

    print("=" * 70)
    print("TRAINING RANDOM FOREST CLASSIFIER")
    print("=" * 70)

    # 1. Load training dataset
    df_train = pd.read_csv(train_path)
    X_train = df_train.drop(columns=[TARGET_COLUMN])
    y_train = df_train[TARGET_COLUMN]

    feature_columns = list(X_train.columns)
    print(f"Loaded training data: {X_train.shape[0]} samples, {len(feature_columns)} features.")
    print(f"Model Configuration: {MODEL_CONFIG}")

    # 2. Instantiate and train Random Forest Classifier
    rf_model = RandomForestClassifier(**MODEL_CONFIG)
    print("\nFitting Random Forest Classifier on training data...")
    rf_model.fit(X_train, y_train)
    print("Model training completed successfully!")

    # 3. Save Model Artifact & Feature Column Order (TASK 5)
    model_path = models_dir / "phishing_rf_model.pkl"
    feature_cols_path = models_dir / "feature_columns.pkl"

    joblib.dump(rf_model, model_path)
    joblib.dump(feature_columns, feature_cols_path)

    print(f"\nSaved trained model to           : {model_path}")
    print(f"Saved feature column order to   : {feature_cols_path}")
    return rf_model, feature_columns


if __name__ == "__main__":
    train_model()
