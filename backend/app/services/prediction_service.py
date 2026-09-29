"""
Prediction Service for AI Phishing Detection System.

Handles URL validation, feature extraction, column alignment against feature_columns.pkl,
Random Forest model inference, advanced URL heuristics, phishing technique classification,
trust analysis, AI risk scoring (0-100), and explainable security intelligence summaries.
"""

from pathlib import Path
from typing import Dict, Any
import joblib
import pandas as pd
from app.services.url_feature_extractor import extract_features, extract_features_to_dataframe
from app.services.risk_analyzer import analyze_risk_factors
from app.services.risk_score import calculate_risk_score
from app.services.url_heuristics import analyze_url_heuristics
from app.services.phishing_techniques import classify_phishing_techniques
from app.services.trust_analyzer import analyze_trust_indicators
from app.services.security_summary import generate_security_summary

# Global cache for model and feature column ordering
_MODEL_CACHE = None
_FEATURE_COLS_CACHE = None


def get_model_and_features():
    """
    Loads and caches trained model and feature column order.
    """
    global _MODEL_CACHE, _FEATURE_COLS_CACHE

    if _MODEL_CACHE is None or _FEATURE_COLS_CACHE is None:
        # Base ML directory resolution
        base_dir = Path(__file__).resolve().parent.parent.parent.parent / "ml" / "models"
        model_path = base_dir / "phishing_rf_model.pkl"
        feature_cols_path = base_dir / "feature_columns.pkl"

        if not model_path.exists():
            raise FileNotFoundError(f"Trained model artifact not found at {model_path}.")
        if not feature_cols_path.exists():
            raise FileNotFoundError(f"Feature columns artifact not found at {feature_cols_path}.")

        _MODEL_CACHE = joblib.load(model_path)
        _FEATURE_COLS_CACHE = joblib.load(feature_cols_path)

    return _MODEL_CACHE, _FEATURE_COLS_CACHE


def predict_url(url: str) -> Dict[str, Any]:
    """
    Validates URL, extracts features, performs Random Forest inference,
    runs URL heuristics, classifies phishing techniques, calculates trust indicators,
    determines deterministic AI Risk Score (0-100), and returns enriched Phishing Intelligence response.
    
    Args:
        url: Raw user-entered URL string.
        
    Returns:
        Structured response dictionary matching Phase 9 API schema requirements.
    """
    if not url or not isinstance(url, str) or not url.strip():
        raise ValueError("Provided URL string is empty or blank.")

    url = url.strip()

    # 1. Load model and required feature ordering
    model, feature_columns = get_model_and_features()

    # 2. Extract feature dictionary and align DataFrame for Random Forest
    feat_dict = extract_features(url)
    X_df = extract_features_to_dataframe(url, feature_columns)

    # 3. Perform Random Forest inference
    pred_class = int(model.predict(X_df)[0])
    
    # 4. Confidence handling
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(X_df)[0]
        class_indices = {cls: idx for idx, cls in enumerate(model.classes_)}
        phishing_prob = float(probabilities[class_indices.get(-1, 0)])
        legitimate_prob = float(probabilities[class_indices.get(1, 1)])
        
        # Convert decimal probability to percentage (0.9145 -> 91.5)
        if pred_class == -1:
            confidence_pct = round(phishing_prob * 100, 1)
        else:
            confidence_pct = round(legitimate_prob * 100, 1)
    else:
        phishing_prob = 0.5 if pred_class == -1 else 0.1
        confidence_pct = None

    prediction = "likely_phishing" if pred_class == -1 else "likely_legitimate"

    # 5. Run Advanced URL Heuristic Engine
    heuristics = analyze_url_heuristics(url)

    # 6. Classify Phishing Attack Techniques
    phishing_techniques = classify_phishing_techniques(heuristics, feat_dict, url)

    # 7. Extract structured risk indicators
    risk_indicators = analyze_risk_factors(feat_dict)

    # 8. Conduct Trust Analysis
    trust_analysis = analyze_trust_indicators(url, feat_dict, heuristics)

    # 9. Calculate Deterministic AI Risk Score (0-100) and transparent risk level
    risk_score, risk_level = calculate_risk_score(
        phishing_prob, risk_indicators, phishing_techniques, heuristics
    )

    # 10. Generate Security Analysis Summary
    summary_text = generate_security_summary(
        prediction, risk_score, risk_level, phishing_techniques, risk_indicators, trust_analysis
    )

    # Standardized limitations list
    limitations = [
        "Analysis is based on the submitted URL string and locally extracted features.",
        "The system does not browse, crawl, or execute the submitted website.",
        "A prediction is an AI-assisted risk assessment, not a guaranteed declaration of safety."
    ]

    # Return Enriched Phase 9 Response Payload
    return {
        "success": True,
        "url": url,
        "prediction": prediction,
        "risk_level": risk_level,
        "risk_score": risk_score,
        "confidence": confidence_pct,
        "summary": summary_text,
        "risk_indicators": risk_indicators,
        "phishing_techniques": phishing_techniques,
        "heuristic_analysis": heuristics,
        "trust_analysis": trust_analysis,
        "analyzed_features": feat_dict,
        "model": {
            "name": "Random Forest Classifier",
            "algorithm": "Random Forest",
            "feature_count": len(feature_columns)
        },
        "limitations": limitations
    }
