"""
Automated Integration Test Suite for Phase 9 Advanced Phishing Intelligence.

Tests 12 distinct URL analysis cases:
1. Normal HTTPS URL
2. HTTP URL
3. IP-based URL
4. URL containing @
5. Very long URL
6. Excessive subdomains
7. URL with suspicious redirect parameter
8. URL with credential-themed path
9. URL with encoded characters
10. URL with punycode indicator
11. URL with multiple suspicious indicators
12. Clean URL with no major indicators
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Add backend directory to sys.path
backend_path = Path(__file__).resolve().parent.parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.main import app
from app.services.prediction_service import predict_url
from app.services.url_heuristics import analyze_url_heuristics
from app.services.phishing_techniques import classify_phishing_techniques

client = TestClient(app)


def test_1_normal_https_url():
    res = predict_url("https://example.com")
    assert res["success"] is True
    assert res["prediction"] == "likely_legitimate"
    assert res["risk_level"] in ["low", "medium"]
    assert res["trust_analysis"]["https"] is True
    assert isinstance(res["phishing_techniques"], list)


def test_2_http_url():
    res = predict_url("http://example.com")
    assert res["success"] is True
    assert res["trust_analysis"]["https"] is False
    techniques = [t["technique"] for t in res["phishing_techniques"]]
    assert "Missing HTTPS" in techniques


def test_3_ip_based_url():
    res = predict_url("http://8.8.8.8/login.php")
    assert res["success"] is True
    assert res["heuristic_analysis"]["domain_analysis"]["is_ip_address"] is True
    techniques = [t["technique"] for t in res["phishing_techniques"]]
    assert "IP-Based URL" in techniques


def test_4_url_with_at_symbol():
    res = predict_url("http://user:pass@example.com/login")
    assert res["success"] is True
    assert res["heuristic_analysis"]["url_structure"]["has_at_symbol"] is True
    techniques = [t["technique"] for t in res["phishing_techniques"]]
    assert "URL Obfuscation" in techniques


def test_5_very_long_url():
    long_url = "https://example.com/" + "security/verify/login/" * 10
    res = predict_url(long_url)
    assert res["success"] is True
    assert res["heuristic_analysis"]["url_structure"]["url_length"] > 120
    assert any("Excessive URL length" in p for p in res["heuristic_analysis"]["suspicious_patterns"])


def test_6_excessive_subdomains():
    res = predict_url("https://a.b.c.d.e.example.com/portal")
    assert res["success"] is True
    assert res["heuristic_analysis"]["domain_analysis"]["subdomain_count"] >= 3
    techniques = [t["technique"] for t in res["phishing_techniques"]]
    assert "Excessive Subdomains" in techniques


def test_7_suspicious_redirect_parameter():
    res = predict_url("https://example.com/auth?redirect_url=http://malicious-site.com")
    assert res["success"] is True
    assert res["heuristic_analysis"]["redirect_analysis"]["has_redirect_param"] is True
    techniques = [t["technique"] for t in res["phishing_techniques"]]
    assert "Redirect Manipulation" in techniques


def test_8_credential_themed_path():
    res = predict_url("https://example.com/account/verification/password-reset")
    assert res["success"] is True
    kws = res["heuristic_analysis"]["keyword_analysis"]["credential_keywords_found"]
    assert "verify" in kws or "account" in kws or "password" in kws
    techniques = [t["technique"] for t in res["phishing_techniques"]]
    assert "Credential-Themed URL" in techniques or "Brand/Account-Themed Path" in techniques


def test_9_encoded_characters():
    res = predict_url("https://example.com/login%2fverify%3fuser%3dadmin")
    assert res["success"] is True
    assert res["heuristic_analysis"]["obfuscation_analysis"]["has_encoded_separators"] is True
    techniques = [t["technique"] for t in res["phishing_techniques"]]
    assert "Suspicious Encoding" in techniques or "URL Obfuscation" in techniques


def test_10_punycode_indicator():
    res = predict_url("https://xn--e1afmkfd.xn--p1ai/login")
    assert res["success"] is True
    assert res["heuristic_analysis"]["domain_analysis"]["is_punycode"] is True
    techniques = [t["technique"] for t in res["phishing_techniques"]]
    assert "Suspicious Domain" in techniques


def test_11_multiple_suspicious_indicators():
    multi_url = "http://user@xn--e1afmkfd.com/account/login.php?redirect=http://phish.com"
    res = predict_url(multi_url)
    assert res["success"] is True
    assert res["risk_level"] in ["high", "critical"]
    assert res["risk_score"] >= 60
    assert len(res["phishing_techniques"]) >= 2


def test_12_clean_url_no_major_indicators():
    res = predict_url("https://www.wikipedia.org/wiki/Main_Page")
    assert res["success"] is True
    assert res["prediction"] == "likely_legitimate"
    assert res["risk_level"] == "low"
    assert res["risk_score"] < 30
    assert len(res["phishing_techniques"]) == 0
