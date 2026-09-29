# AI Phishing Detection API - Backend Service

This service provides a RESTful FastAPI backend and ML inference pipeline for real-time URL phishing detection and explainable risk analysis.

---

## 📂 Backend Project Structure

```
backend/
├── app/
│   ├── __init__.py      # Package initialization marker
│   ├── main.py          # FastAPI app entry point & CORS middleware
│   ├── routes/          # API route definitions
│   │   ├── __init__.py  # Package initialization marker
│   │   ├── health.py    # GET /api/health endpoint
│   │   └── predict.py   # POST /api/predict endpoint
│   ├── services/        # Business logic & ML inference services
│   │   ├── __init__.py           # Package initialization marker
│   │   ├── url_feature_extractor.py # Real-time 30-feature URL extractor
│   │   ├── feature_metadata.py     # Categorization & fallback registry
│   │   ├── prediction_service.py   # Random Forest inference & percentage confidence
│   │   └── risk_analyzer.py        # Explainable risk factor generator
│   └── utils/           # Utility functions
├── requirements.txt     # Python backend dependencies
└── README.md            # Backend documentation (this file)
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API Root Welcome & Metadata |
| `GET` | `/api/health` | Health Check Endpoint |
| `POST` | `/api/predict` | Real-Time Phishing Prediction & Risk Analysis |

---

## 📩 Request & Response Examples (`POST /api/predict`)

### 1. Request Payload Example
```json
POST /api/predict
Content-Type: application/json

{
  "url": "https://example.com"
}
```

### 2. Success Response Example (Legitimate URL)
```json
{
  "success": true,
  "url": "https://example.com",
  "prediction": "likely_legitimate",
  "risk_level": "low",
  "confidence": 91.5,
  "risk_indicators": [],
  "analyzed_features": {
    "having_ip_address": 1,
    "url_length": 1,
    "shortining_service": 1,
    "having_at_symbol": 1,
    "sslfinal_state": 1
  },
  "message": "No major phishing indicators were detected."
}
```

### 3. Success Response Example (Phishing URL)
```json
{
  "success": true,
  "url": "http://login.paypal.account.verification.secure-update.com",
  "prediction": "likely_phishing",
  "risk_level": "high",
  "confidence": 100.0,
  "risk_indicators": [
    "URL length is suspicious (54-75 characters).",
    "Domain name contains a hyphen ('-') commonly used in brand spoofing.",
    "Hostname contains multiple subdomain levels (> 2 subdomains).",
    "URL uses non-secure HTTP protocol without SSL/TLS encryption."
  ],
  "analyzed_features": {
    "having_ip_address": 1,
    "prefix_suffix": -1,
    "having_sub_domain": -1,
    "sslfinal_state": -1
  },
  "message": "Multiple phishing-related indicators were detected."
}
```

### 4. Error Response Examples

#### A. Invalid Protocol (HTTP 400 Bad Request)
```json
{
  "detail": "Unsupported protocol 'ftp://'. Only 'http://' and 'https://' URLs are accepted."
}
```

#### B. Forbidden Target / SSRF Protection (HTTP 400 Bad Request)
```json
{
  "detail": "Analysis of internal/private network targets or metadata endpoints is prohibited for security reasons."
}
```

---

## 🛡️ Security Limitations & SSRF Protection

1. **No External Browsing**: The API does **not** automatically visit, execute JS, download files, or follow HTTP redirects from user-submitted URLs.
2. **Localhost & Internal IP Blocking**: Requests targeting `localhost`, `127.0.0.1`, `0.0.0.0`, `169.254.169.254` (cloud metadata endpoints), or `192.168.x.x` are rejected with HTTP 400.
3. **CORS Restrictions**: Configured specifically for local frontend origin `http://localhost:5173`.

---

## 🚀 Virtual Environment & Execution

### 1. Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Run API Server
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- **Interactive Swagger Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 3. Run Automated Tests
```bash
pytest ../tests/
```
