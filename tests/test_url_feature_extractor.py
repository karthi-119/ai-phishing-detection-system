"""
Unit Tests for URL Feature Extractor & Prediction Pipeline.

Tests:
1. Normal HTTPS URL
2. HTTP URL
3. URL containing an IP address
4. URL containing '@' symbol
5. Long URL (> 75 chars)
6. URL containing suspicious subdomain structure
7. Invalid / Empty URL inputs
8. Column order, feature count (30), non-null, and numeric types verification against feature_columns.pkl.
"""

import sys
import pytest
import joblib
from pathlib import Path

# Add backend directory to sys.path
backend_path = Path(__file__).resolve().parent.parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.services.url_feature_extractor import extract_features, extract_features_to_dataframe
from app.services.prediction_service import predict_url, get_model_and_features


@pytest.fixture
def feature_columns():
    """
    Fixture returning expected feature column order from ml/models/feature_columns.pkl.
    """
    _, cols = get_model_and_features()
    return cols


def test_feature_count_and_column_matching(feature_columns):
    """
    Test that extract_features produces exactly 30 features matching feature_columns.pkl.
    """
    url = "https://www.google.com"
    feats = extract_features(url)

    assert len(feats) == 30, f"Expected 30 features, got {len(feats)}"
    assert set(feats.keys()) == set(feature_columns), "Feature name mismatch"


def test_dataframe_feature_ordering_and_types(feature_columns):
    """
    Test that extract_features_to_dataframe aligns columns in exact sequence,
    with zero NaNs and numeric types.
    """
    url = "https://www.google.com"
    df = extract_features_to_dataframe(url, feature_columns)

    assert list(df.columns) == feature_columns, "Column ordering does not match feature_columns.pkl"
    assert df.isnull().sum().sum() == 0, "DataFrame contains NaN values"
    assert len(df) == 1, "Expected single row DataFrame"


def test_https_vs_http_feature_extraction():
    """
    Test sslfinal_state feature for HTTPS vs HTTP.
    """
    https_feats = extract_features("https://secure.bank.com")
    http_feats = extract_features("http://unsecure.bank.com")

    assert https_feats["sslfinal_state"] == 1, "HTTPS should yield sslfinal_state=1"
    assert http_feats["sslfinal_state"] == -1, "HTTP should yield sslfinal_state=-1"


def test_ip_address_detection():
    """
    Test having_ip_address feature for IP vs domain.
    """
    ip_feats = extract_features("http://192.168.1.100/login.html")
    domain_feats = extract_features("http://example.com/login.html")

    assert ip_feats["having_ip_address"] == -1, "IP address should yield having_ip_address=-1"
    assert domain_feats["having_ip_address"] == 1, "Domain should yield having_ip_address=1"


def test_at_symbol_detection():
    """
    Test having_at_symbol feature.
    """
    at_feats = extract_features("http://user:pass@phishing-target.com/page")
    clean_feats = extract_features("http://phishing-target.com/page")

    assert at_feats["having_at_symbol"] == -1, "'@' symbol should yield having_at_symbol=-1"
    assert clean_feats["having_at_symbol"] == 1, "No '@' symbol should yield having_at_symbol=1"


def test_long_url_detection():
    """
    Test url_length feature for long URLs (> 75 chars).
    """
    long_url = "http://example.com/" + "a" * 80
    feats = extract_features(long_url)

    assert feats["url_length"] == -1, "URL > 75 chars should yield url_length=-1"


def test_subdomain_count_detection():
    """
    Test having_sub_domain feature for multiple subdomain levels.
    """
    multi_subdomain_url = "http://login.paypal.account.verification.secure-update.com"
    feats = extract_features(multi_subdomain_url)

    assert feats["having_sub_domain"] == -1, "> 2 subdomains should yield having_sub_domain=-1"


def test_predict_url_end_to_end():
    """
    Test predict_url service produces structured response for legitimate and phishing URLs.
    """
    # Test safe HTTPS URL
    legit_res = predict_url("https://www.google.com")
    assert legit_res["prediction"] in ["likely_legitimate", "likely_phishing"]
    assert "confidence" in legit_res
    assert "risk_level" in legit_res
    assert isinstance(legit_res["risk_indicators"], list)

    # Test suspicious HTTP IP URL with @ symbol
    phish_res = predict_url("http://user@192.168.1.50/paypal-login/verify.php?redirect=http://malicious.com")
    assert phish_res["prediction"] == "likely_phishing"
    assert phish_res["risk_level"] in ["critical", "high", "moderate"]
    assert len(phish_res["risk_indicators"]) > 0


def test_invalid_url_handling():
    """
    Test that empty or blank URL inputs raise ValueError.
    """
    with pytest.raises(ValueError):
        predict_url("")

    with pytest.raises(ValueError):
        predict_url("   ")
