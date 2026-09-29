"""
Expanded API Integration & Security Test Suite for FastAPI Prediction Routes.

Tests 13 distinct cases:
VALID:
1. https://example.com
2. http://example.com

INVALID:
3. Empty URL string
4. Missing URL field
5. Malformed URL string
6. ftp:// protocol scheme
7. javascript: scheme
8. data: scheme
9. Excessively long URL (> 2048 chars)
10. Malformed hostname with spaces/invalid characters

SECURITY (SSRF Protection & Headers):
11. Localhost URL (http://localhost:8000)
12. Private IP URL (http://192.168.1.1)
13. Cloud metadata URL (http://169.254.169.254/latest/meta-data)
14. Security Headers Verification (X-Content-Type-Options, X-Frame-Options, Referrer-Policy)
"""

import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add backend directory to sys.path
backend_path = Path(__file__).resolve().parent.parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.main import app

# Create TestClient instance
client = TestClient(app)


# --- HEALTH & ROOT ENDPOINTS ---
def test_health_check_endpoint():
    """Test GET /api/health returns HTTP 200 and status ok."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] in ["healthy", "ok"]


def test_root_endpoint():
    """Test GET / returns API metadata and endpoints."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


# --- VALID URL TESTS ---
def test_valid_https_url():
    """1. Test valid HTTPS URL."""
    response = client.post("/api/predict", json={"url": "https://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["url"] == "https://example.com"
    assert data["prediction"] in ["likely_legitimate", "likely_phishing"]
    assert 0.0 <= data["confidence"] <= 100.0


def test_valid_http_url():
    """2. Test valid HTTP URL."""
    response = client.post("/api/predict", json={"url": "http://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


# --- INVALID URL TESTS ---
def test_empty_url_returns_400():
    """3. Test empty URL string returns HTTP 400."""
    response = client.post("/api/predict", json={"url": "   "})
    assert response.status_code == 400
    assert "detail" in response.json()


def test_missing_url_field_returns_422():
    """4. Test missing URL field in JSON payload returns HTTP 422."""
    response = client.post("/api/predict", json={})
    assert response.status_code == 422


def test_malformed_url_returns_400():
    """5. Test malformed URL returns HTTP 400."""
    response = client.post("/api/predict", json={"url": "http:///invalid_url"})
    assert response.status_code == 400


def test_ftp_scheme_returns_400():
    """6. Test ftp:// scheme returns HTTP 400."""
    response = client.post("/api/predict", json={"url": "ftp://files.example.com"})
    assert response.status_code == 400
    assert "Unsupported protocol" in response.json()["detail"]


def test_javascript_scheme_returns_400():
    """7. Test javascript: scheme returns HTTP 400."""
    response = client.post("/api/predict", json={"url": "javascript:alert(1)"})
    assert response.status_code == 400


def test_data_scheme_returns_400():
    """8. Test data: scheme returns HTTP 400."""
    response = client.post("/api/predict", json={"url": "data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=="})
    assert response.status_code == 400


def test_excessively_long_url_returns_400():
    """9. Test excessively long URL (> 2048 chars) returns HTTP 400."""
    long_url = "https://example.com/" + "a" * 2100
    response = client.post("/api/predict", json={"url": long_url})
    assert response.status_code == 400
    assert "exceeds maximum allowed length" in response.json()["detail"]


def test_malformed_hostname_returns_400():
    """10. Test hostname with spaces returns HTTP 400."""
    response = client.post("/api/predict", json={"url": "http://in valid domain.com"})
    assert response.status_code == 400


# --- SECURITY & SSRF PROTECTION TESTS ---
def test_localhost_url_returns_400():
    """11. Test localhost-style URL returns HTTP 400 (SSRF Protection)."""
    response = client.post("/api/predict", json={"url": "http://localhost:8000/admin"})
    assert response.status_code == 400
    assert "prohibited for security reasons" in response.json()["detail"]


def test_private_ip_url_returns_400():
    """12. Test private network IP returns HTTP 400 (SSRF Protection)."""
    response = client.post("/api/predict", json={"url": "http://192.168.1.1/router"})
    assert response.status_code == 400
    assert "prohibited for security reasons" in response.json()["detail"]


def test_cloud_metadata_url_returns_400():
    """13. Test AWS/GCP cloud metadata IP returns HTTP 400 (SSRF Protection)."""
    response = client.post("/api/predict", json={"url": "http://169.254.169.254/latest/meta-data"})
    assert response.status_code == 400
    assert "prohibited for security reasons" in response.json()["detail"]


def test_security_headers_present():
    """14. Test HTTP security headers are attached to API responses."""
    response = client.get("/api/health")
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("Referrer-Policy") == "no-referrer"
