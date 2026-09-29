"""
100-URL Performance & Latency Benchmark Script for PhishGuard AI Phase 9.

Measures local performance of 100 URL predictions (feature extraction,
random forest inference, URL heuristics, technique classification, and trust analysis).
Reports total execution time and average latency per URL.
"""

import sys
import time
from pathlib import Path

# Add backend directory to sys.path
backend_path = Path(__file__).resolve().parent.parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.services.prediction_service import predict_url, get_model_and_features

# Base sample URLs generator to produce 100 distinct valid targets
BASE_SAMPLES = [
    "https://example.com",
    "http://192.168.1.1/login.php",
    "https://www.google.com/search?q=cybersecurity",
    "http://user@verify-account-security-update.org/bank/auth",
    "https://github.com/facebook/react/issues/100",
    "http://bit.ly/3xY8zQ",
    "https://a.b.c.d.subdomains.example-site.net/portal",
    "https://wikipedia.org/wiki/Phishing",
    "http://example-domain-typo-check.com/payment/confirm?redirect_url=http://malicious.com",
    "https://xn--e1afmkfd.xn--p1ai/signin"
]


def run_100_url_benchmark():
    print("=" * 70)
    print("PHISHGUARD AI PHASE 9 — 100 URL LOCAL PERFORMANCE BENCHMARK")
    print("=" * 70)

    # Warm up model and feature column caches
    get_model_and_features()

    # Generate list of 100 test URLs
    test_urls = []
    for i in range(10):
        for idx, base in enumerate(BASE_SAMPLES):
            test_urls.append(f"{base}#run_{i}_{idx}")

    latencies = []
    start_total = time.perf_counter()

    for idx, target_url in enumerate(test_urls):
        t0 = time.perf_counter()
        res = predict_url(target_url)
        t1 = time.perf_counter()
        elapsed_ms = (t1 - t0) * 1000.0
        latencies.append(elapsed_ms)
        assert res["success"] is True

    end_total = time.perf_counter()
    total_sec = end_total - start_total
    avg_ms = sum(latencies) / len(latencies)
    min_ms = min(latencies)
    max_ms = max(latencies)

    print(f"Total URLs Analyzed : {len(test_urls)}")
    print(f"Total Execution Time: {total_sec:.3f} seconds")
    print(f"Average Latency     : {avg_ms:.2f} ms per URL")
    print(f"Minimum Latency     : {min_ms:.2f} ms")
    print(f"Maximum Latency     : {max_ms:.2f} ms")
    print("=" * 70)


if __name__ == "__main__":
    run_100_url_benchmark()
