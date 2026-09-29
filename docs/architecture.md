# PhishGuard AI — System Architecture & Security Specification

This document details the multi-layered system architecture, data flow, ML model inference pipeline, and security boundaries of **PhishGuard AI**.

---

## 🏗️ Architectural Overview

PhishGuard AI follows a decoupled client-server architecture:

```
[ User Browser (React Web UI) ]
             │
             │ HTTP REST (JSON)
             ▼
[ FastAPI Backend API Engine (Port 8000) ]
   ├── 1. Server-Side URL Validator & SSRF Guard
   ├── 2. 30-Feature Lexical & Host Extractor
   ├── 3. Random Forest Model Inference Engine (.pkl)
   ├── 4. Advanced URL Heuristic Engine
   ├── 5. Phishing Attack Technique Classifier
   ├── 6. Trust & Protocol Analyzer
   └── 7. Explainable Security Summary Generator
```

---

## 🛡️ Security Boundaries & SSRF Guarding

### 1. Offline String Analysis Policy
- The backend treats user-submitted URLs strictly as **untrusted input data**.
- The server **never** initiates outbound HTTP requests, resolves external DNS records, follows HTTP redirects, downloads page content, or executes client-side JavaScript.
- Analysis operates 100% locally on the URL string.

### 2. SSRF (Server-Side Request Forgery) Protection
- `url_validator.py` enforces protocol scheme whitelisting (`http://` and `https://` only).
- Blacklists loopback addresses (`127.0.0.1`, `localhost`), private network ranges (`10.x.x.x`, `172.16-31.x.x`, `192.168.x.x`), and cloud provider metadata endpoints (`169.254.169.254`).

### 3. Frontend Non-Clickable Code Blocks
- Submitted URLs in the React UI are displayed strictly inside non-clickable `<code>` elements without `href` anchors to protect users from accidental navigation.

---

## 🤖 ML Inference Pipeline

1. **Input**: Raw target URL string (max 2,048 chars).
2. **Feature Extraction**: Extracts 30 structural features mapped to integer encodings (`-1` = Phishing, `0` = Suspicious, `1` = Legitimate).
3. **Model Prediction**: Evaluated against pre-trained Random Forest Classifier (`phishing_rf_model.pkl`).
4. **Scoring Engine**: Combines ML output probability with heuristic severity boosts to generate a deterministic **0–100 AI Risk Score**.
