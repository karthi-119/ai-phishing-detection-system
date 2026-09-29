"""
Automated unit test for FastAPI model insights endpoint.
Verifies GET /api/model/insights endpoint returns model info and top 10 feature importances.
"""

import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add backend directory to sys.path to enable app module imports
backend_path = Path(__file__).resolve().parent.parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.main import app

client = TestClient(app)


def test_model_insights_endpoint():
    """
    Test GET /api/model/insights returns HTTP 200 OK, feature count, top 10 features list, and model details.
    """
    response = client.get("/api/model/insights")
    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert data["model"] == "Random Forest Classifier"
    assert data["feature_count"] == 30
    assert "top_features" in data
    assert isinstance(data["top_features"], list)
    assert len(data["top_features"]) == 10

    first = data["top_features"][0]
    assert "feature" in first
    assert "importance" in first
    assert first["importance"] > 0
