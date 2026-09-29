"""
Model & Feature Consistency Test Suite.

Verifies:
1. Trained model artifact loads successfully.
2. Feature column list loads and contains exactly 30 features.
3. Feature extractor output aligns perfectly with feature column sequence.
4. Extracted values are 100% numeric with zero NaN or null values.
5. Model prediction output belongs strictly to expected set {-1, 1}.
6. Model probabilities fall strictly within [0.0, 1.0].
"""

import sys
from pathlib import Path
import joblib
import pandas as pd
import numpy as np

# Add backend directory to sys.path
backend_path = Path(__file__).resolve().parent.parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.services.prediction_service import get_model_and_features
from app.services.url_feature_extractor import extract_features, extract_features_to_dataframe

EXPECTED_FEATURE_COUNT = 30
VALID_PREDICTED_CLASSES = {-1, 1}


def test_model_and_features_load():
    """
    Test that Random Forest model and feature column list load cleanly.
    """
    model, feature_cols = get_model_and_features()

    assert model is not None, "Model artifact failed to load"
    assert isinstance(feature_cols, list), "Feature columns must be a list"
    assert len(feature_cols) == EXPECTED_FEATURE_COUNT, f"Expected {EXPECTED_FEATURE_COUNT} features, found {len(feature_cols)}"


def test_feature_alignment_and_numeric_types():
    """
    Test feature extraction DataFrame aligns with model feature columns with zero NaNs.
    """
    model, feature_cols = get_model_and_features()
    test_url = "https://www.google.com"

    df = extract_features_to_dataframe(test_url, feature_cols)

    assert list(df.columns) == feature_cols, "Feature column sequence mismatch"
    assert df.isnull().sum().sum() == 0, "Extracted DataFrame contains NaN values"

    # Verify all columns are numeric
    for col in df.columns:
        assert pd.api.types.is_numeric_dtype(df[col]), f"Column '{col}' is not numeric"


def test_model_inference_consistency():
    """
    Test model inference returns valid class prediction and probability bounds [0.0, 1.0].
    """
    model, feature_cols = get_model_and_features()
    sample_urls = [
        "https://www.google.com",
        "http://suspicious-target-paypal-update.com/login",
        "http://user@192.168.1.1/test"
    ]

    for url in sample_urls:
        df = extract_features_to_dataframe(url, feature_cols)
        
        # Test class prediction
        pred = model.predict(df)[0]
        assert pred in VALID_PREDICTED_CLASSES, f"Unexpected prediction class {pred} for URL {url}"

        # Test probability prediction
        probs = model.predict_proba(df)[0]
        assert len(probs) == 2, "Expected 2 probability classes"
        for p in probs:
            assert 0.0 <= p <= 1.0, f"Probability {p} out of bounds [0.0, 1.0]"
        assert abs(sum(probs) - 1.0) < 1e-5, f"Probabilities do not sum to 1.0: {probs}"
