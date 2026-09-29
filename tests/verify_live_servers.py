"""
Verification script to test live running FastAPI backend and verify frontend integration endpoints.
"""

import urllib.request
import urllib.parse
import json
import sys


def verify_live_endpoints():
    print("=" * 70)
    print("VERIFYING LIVE PHISHGUARD AI BACKEND AT http://127.0.0.1:8000")
    print("=" * 70)

    # 1. Health check
    health_url = "http://127.0.0.1:8000/api/health"
    try:
        with urllib.request.urlopen(health_url) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"[PASS] GET /api/health -> Status {resp.status} | Data: {data}")
            assert data["status"] == "healthy"
            assert data["model_loaded"] is True
    except Exception as e:
        print(f"[FAIL] GET /api/health failed: {e}")
        sys.exit(1)

    # 2. Swagger docs check
    docs_url = "http://127.0.0.1:8000/docs"
    try:
        with urllib.request.urlopen(docs_url) as resp:
            print(f"[PASS] GET /docs -> Status {resp.status} OK (Swagger UI Available)")
    except Exception as e:
        print(f"[FAIL] GET /docs failed: {e}")
        sys.exit(1)

    # 3. Predict API check
    predict_url = "http://127.0.0.1:8000/api/predict"
    payload = json.dumps({"url": "https://example.com"}).encode('utf-8')
    req = urllib.request.Request(predict_url, data=payload, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"[PASS] POST /api/predict -> Status {resp.status} OK")
            print(f"       Prediction : {data.get('prediction')}")
            print(f"       Risk Score : {data.get('risk_score')}/100")
            print(f"       Risk Level : {data.get('risk_level')}")
            print(f"       Summary    : {data.get('summary')[:80]}...")
            assert data["success"] is True
            assert "prediction" in data
            assert "risk_score" in data
            assert "phishing_techniques" in data
            assert "heuristic_analysis" in data
            assert "trust_analysis" in data
    except Exception as e:
        print(f"[FAIL] POST /api/predict failed: {e}")
        sys.exit(1)

    # 4. Model Insights API check
    insights_url = "http://127.0.0.1:8000/api/model/insights"
    try:
        with urllib.request.urlopen(insights_url) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"[PASS] GET /api/model/insights -> Status {resp.status} OK | Top Features: {len(data.get('top_features', []))}")
            assert data["success"] is True
    except Exception as e:
        print(f"[FAIL] GET /api/model/insights failed: {e}")
        sys.exit(1)

    print("=" * 70)
    print("ALL LIVE ENDPOINT VERIFICATIONS PASSED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    verify_live_endpoints()
