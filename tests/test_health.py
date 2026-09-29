"""
Automated unit test for FastAPI backend health check endpoint.
Verifies GET /api/health endpoint status code and response payload.
"""

import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add backend directory to sys.path to enable app module imports
backend_path = Path(__file__).resolve().parent.parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.main import app

# Create TestClient instance
client = TestClient(app)


def test_health_check_endpoint():
    """
    Test GET /api/health returns HTTP 200 OK and expected JSON payload.
    """
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True


def test_root_welcome_endpoint():
    """
    Test GET / returns HTTP 200 OK and root API information.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
