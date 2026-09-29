"""
Comprehensive Phase 10 Performance & Latency Measurement Script for PhishGuard AI.

Measures:
1. Model loading time from disk
2. Single prediction time (warm load)
3. 10 sequential full API predictions
4. 100 URL heuristic analyses
"""

import sys
import time
from pathlib import Path

# Add backend directory to sys.path
backend_path = Path(__file__).resolve().parent.parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.services.prediction_service import get_model_and_features, predict_url
from app.services.url_heuristics import analyze_url_heuristics

SAMPLE_URLS = [
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


def run_full_benchmark():
    print("=" * 75)
    print("PHISHGUARD AI PHASE 10 — COMPREHENSIVE PERFORMANCE MEASUREMENTS")
    print("=" * 75)

    # 1. Model Loading Time Measurement
    t0_load = time.perf_counter()
    model, feature_cols = get_model_and_features()
    t1_load = time.perf_counter()
    load_time_ms = (t1_load - t0_load) * 1000.0

    # 2. Single Prediction Time
    t0_single = time.perf_counter()
    res_single = predict_url("https://example.com")
    t1_single = time.perf_counter()
    single_time_ms = (t1_single - t0_single) * 1000.0
    assert res_single["success"] is True

    # 3. 10 Sequential Predictions
    seq_times = []
    for url in SAMPLE_URLS:
        t0_seq = time.perf_counter()
        res_seq = predict_url(url)
        t1_seq = time.perf_counter()
        seq_times.append((t1_seq - t0_seq) * 1000.0)
        assert res_seq["success"] is True

    total_10_ms = sum(seq_times)
    avg_10_ms = total_10_ms / len(seq_times)

    # 4. 100 URL Heuristic Analyses
    heur_times = []
    test_100 = [f"{SAMPLE_URLS[i % 10]}#item_{i}" for i in range(100)]
    t0_heur_total = time.perf_counter()
    for u in test_100:
        t0_h = time.perf_counter()
        h_res = analyze_url_heuristics(u)
        t1_h = time.perf_counter()
        heur_times.append((t1_h - t0_h) * 1000.0)
        assert "url_structure" in h_res

    t1_heur_total = time.perf_counter()
    heur_total_sec = t1_heur_total - t0_heur_total
    heur_avg_ms = sum(heur_times) / len(heur_times)

    print(f"1. Model Loading Time        : {load_time_ms:.2f} ms")
    print(f"2. Single Prediction Time     : {single_time_ms:.2f} ms")
    print(f"3. 10 Sequential Predictions  : Total {total_10_ms:.2f} ms | Avg {avg_10_ms:.2f} ms/request")
    print(f"4. 100 URL Heuristics         : Total {heur_total_sec:.3f} s | Avg {heur_avg_ms:.3f} ms/URL")
    print("=" * 75)


if __name__ == "__main__":
    run_full_benchmark()
