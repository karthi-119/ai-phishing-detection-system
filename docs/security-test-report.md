# PhishGuard AI - Security Test & Audit Report

**Date**: September 29, 2026  
**Project**: PSN013 – Real-Time AI Phishing Detection System  
**Product**: PhishGuard AI  
**Scope**: Server-Side Validation, SSRF Safety Audit, Model Consistency, API Integration, and Latency Performance Benchmarks  

---

## 1. Test Environment

| Environment Component | Specification / Version |
|---|---|
| **Operating System** | Windows 11 |
| **Python Runtime** | Python 3.14.5 |
| **Node.js Runtime** | Node.js v24.12.0 / npm 11.6.2 |
| **Backend Framework** | FastAPI 0.141.1 (Uvicorn 0.54.0) |
| **Frontend Framework** | React 19 / Vite 8.3.1 |
| **ML Framework** | Scikit-learn 1.9.1 / Pandas 3.0.6 |
| **Test Runner** | Pytest 9.1.1 (FastAPI TestClient) |

---

## 2. Server-Side URL Validation & Input Hardening

- **Module**: `backend/app/utils/url_validator.py`
- **Validation Rules Verified**:
  - **Empty Input Check**: Rejects empty strings and whitespace-only payloads (`HTTP 400 Bad Request`).
  - **Maximum Length Constraint**: Enforces `MAX_URL_LENGTH` (2,048 chars).
  - **Protocol Whitelisting**: Accepts strictly `http://` and `https://`. Rejects `ftp://`, `file://`, `javascript:`, `data:`, `mailto:`, and custom schemes (`HTTP 400 Bad Request`).
  - **Hostname Sanitization**: Verifies non-empty netloc with valid alphanumeric domain formatting.

---

## 3. SSRF Protection & Network Safety Audit

- **Codebase Audit Results**: Searched backend codebase for unneeded outbound network libraries (`requests`, `httpx`, `urllib.request`, `aiohttp`, `curl`, `subprocess`).
- **Outbound Request Ban**: Confirmed that **zero** code attempts to fetch, crawl, or download submitted URLs. Feature extraction operates 100% via static string parsing.
- **Forbidden Target Blocking**:
  - `http://localhost:8000` ➜ **Blocked** (`HTTP 400 Bad Request`)
  - `http://127.0.0.1/admin` ➜ **Blocked** (`HTTP 400 Bad Request`)
  - `http://192.168.1.1/router` ➜ **Blocked** (`HTTP 400 Bad Request`)
  - `http://169.254.169.254/latest/meta-data` (AWS Cloud Metadata) ➜ **Blocked** (`HTTP 400 Bad Request`)

---

## 4. Model & Feature Consistency Verification

- **Module**: `tests/test_model_consistency.py`
- **Test Items**:
  1. Serialized model (`ml/models/phishing_rf_model.pkl`) loads successfully.
  2. Feature column ordering (`ml/models/feature_columns.pkl`) contains exactly 30 features.
  3. Extracted feature DataFrames align 100% identically with model column order.
  4. Extracted features are 100% numeric with zero `NaN` or `null` values.
  5. Predicted output classes belong strictly to `{-1, 1}`.
  6. Prediction probabilities fall strictly within `[0.0, 1.0]` and sum to `1.0`.

---

## 5. API Test Suite Summary (30 Test Cases)

| Test Module | Total Tests | Passed | Failed | Status |
|---|---|---|---|---|
| `tests/test_health.py` | 2 | 2 | 0 | **PASSED** |
| `tests/test_model_consistency.py` | 3 | 3 | 0 | **PASSED** |
| `tests/test_prediction_api.py` | 16 | 16 | 0 | **PASSED** |
| `tests/test_url_feature_extractor.py` | 9 | 9 | 0 | **PASSED** |
| **TOTAL** | **30** | **30** | **0** | **100% PASS** |

---

## 6. Performance Benchmark Metrics

- **Script**: `tests/performance_test.py`
- **Workload**: 10 sequential predictions evaluated against test URLs.

| Performance Metric | Measured Latency (ms) |
|---|---|
| **Cold-Start Initial Request** | `3,083.04 ms` (includes initial model file I/O) |
| **Warm Average Latency** | `161.40 ms` (subsequent 9 requests) |
| **Minimum Latency** | `117.05 ms` |
| **Maximum Latency** | `3,083.04 ms` |
| **Overall Average Latency** | `451.36 ms` |

---

## 7. Known Limitations

1. **Static Analysis Focus**: Feature extraction relies on URL syntax and static metadata; it does not crawl external webpage HTML content to eliminate SSRF attack vectors.
2. **Probabilistic Nature**: Model outputs probabilistic risk scores ("likely_phishing" vs "likely_legitimate") rather than absolute guarantees.

---

## 8. Future Production Improvements

1. **Distributed Rate Limiting**: Implement Redis-backed sliding window rate limiting (e.g. 60 requests/minute per IP) for production deployments.
2. **Dynamic WHOIS / DNS Caching**: Integrate an isolated sandboxed microservice for WHOIS/DNS caching with strict timeout limits.
