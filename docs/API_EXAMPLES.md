# PhishGuard AI — REST API Documentation & Examples

This document provides sample request and response payloads for PhishGuard AI API endpoints.

---

## 1. POST /api/predict

Analyzes a target URL and returns an explainable security intelligence report.

### Request Payload
```json
{
  "url": "https://example.com"
}
```

### Response Payload (HTTP 200 OK)
```json
{
  "success": true,
  "url": "https://example.com",
  "prediction": "likely_legitimate",
  "risk_level": "low",
  "risk_score": 12,
  "confidence": 94.5,
  "summary": "LOW RISK URL based on available URL-level evidence. Standard HTTPS protocol and direct domain structure were confirmed.",
  "risk_indicators": [],
  "phishing_techniques": [],
  "heuristic_analysis": {
    "suspicious_patterns": [],
    "url_structure": {
      "scheme": "https",
      "hostname": "example.com",
      "path": "/",
      "query": "",
      "path_segment_count": 0,
      "query_param_count": 0,
      "subdomain_count": 0,
      "has_at_symbol": false
    },
    "domain_analysis": {
      "is_ip_address": false,
      "has_hyphen": false,
      "is_punycode": false,
      "is_shortener": false,
      "subdomain_count": 0
    }
  },
  "trust_analysis": {
    "https": true,
    "domain_structure": "Standard Domain Structure",
    "trust_indicators": [
      "HTTPS protocol scheme enabled",
      "Uses registered domain name instead of raw IP address",
      "Direct destination URL"
    ],
    "warnings": [
      "Note: HTTPS provides encryption but does NOT guarantee domain legitimacy or safety"
    ]
  },
  "analyzed_features": {
    "having_ip_address": { "raw_value": "No", "extracted_feature": -1, "description": "IP Address in Domain" },
    "url_length": { "raw_value": 19, "extracted_feature": -1, "description": "URL Length" },
    "https_token": { "raw_value": "Yes", "extracted_feature": -1, "description": "HTTPS Protocol Scheme" }
  },
  "model": {
    "name": "Random Forest Classifier",
    "algorithm": "Random Forest",
    "feature_count": 30
  },
  "limitations": [
    "Analysis is based on the submitted URL string and locally extracted features.",
    "The system does not browse, crawl, or execute the submitted website.",
    "A prediction is an AI-assisted risk assessment, not a guaranteed declaration of safety."
  ]
}
```

---

## 2. GET /api/model/insights

Returns model algorithm metadata and top 10 Gini feature importances.

### Response Payload (HTTP 200 OK)
```json
{
  "success": true,
  "model": "Random Forest Classifier",
  "dataset": "UCI Phishing Websites Dataset (ID: 327)",
  "feature_count": 30,
  "top_features": [
    { "feature": "sslfinal_state", "importance": 0.3285 },
    { "feature": "url_of_anchor", "importance": 0.2451 },
    { "feature": "web_traffic", "importance": 0.0754 },
    { "feature": "prefix_suffix", "importance": 0.0523 },
    { "feature": "having_sub_domain", "importance": 0.0489 },
    { "feature": "links_in_tags", "importance": 0.0312 },
    { "feature": "domain_registration_length", "importance": 0.0284 },
    { "feature": "request_url", "importance": 0.0241 },
    { "feature": "sfh", "importance": 0.0215 },
    { "feature": "age_of_domain", "importance": 0.0198 }
  ]
}
```

---

## 3. GET /api/health

Returns backend service availability and ML model readiness.

### Response Payload (HTTP 200 OK)
```json
{
  "status": "healthy",
  "service": "PhishGuard AI API",
  "model_loaded": true
}
```
