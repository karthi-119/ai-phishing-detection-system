"""
Performance Benchmark Test Script for AI Phishing Detection System.

Measures latency (minimum, maximum, average) across 10 sequential URL prediction requests.
"""

import sys
import time
from pathlib import Path
from fastapi.testclient import TestClient

# Add backend directory to sys.path
backend_path = Path(__file__).resolve().parent.parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.main import app

client = TestClient(app)

BENCHMARK_URLS = [
    "https://example.com",
    "https://www.google.com",
    "https://github.com",
    "http://example-domain-check.org",
    "https://wikipedia.org",
    "http://test-subdomain.example-site.net/login.php",
    "https://mozilla.org/en-US/",
    "http://another-test-domain.com",
    "https://stackover-flow.com/questions",
    "http://bit.ly/3xY8zQ"
]


def run_performance_benchmark():
    """
    Executes 10 sequential prediction requests and calculates latency statistics.
    """
    print("=" * 70)
    print("RUNNING LATENCY PERFORMANCE BENCHMARK (10 SEQUENTIAL PREDICTIONS)")
    print("=" * 70)

    durations = []

    for idx, url in enumerate(BENCHMARK_URLS, 1):
        start = time.perf_counter()
        response = client.post("/api/predict", json={"url": url})
        elapsed_ms = (time.perf_counter() - start) * 1000.0

        assert response.status_code == 200, f"Request {idx} failed with status {response.status_code}"
        durations.append(elapsed_ms)

        prediction = response.json()["prediction"]
        print(f"Request {idx:2d}: {url:<52} -> {prediction:<18} ({elapsed_ms:6.2f} ms)")

    min_ms = min(durations)
    max_ms = max(durations)
    avg_ms = sum(durations) / len(durations)

    print("\n--- BENCHMARK RESULTS ---")
    print(f"Total Requests : {len(durations)}")
    print(f"Minimum Latency: {min_ms:.2f} ms")
    print(f"Maximum Latency: {max_ms:.2f} ms")
    print(f"Average Latency: {avg_ms:.2f} ms")
    print("=" * 70)

    return {
        "count": len(durations),
        "min_ms": round(min_ms, 2),
        "max_ms": round(max_ms, 2),
        "avg_ms": round(avg_ms, 2)
    }


if __name__ == "__main__":
    run_performance_benchmark()
