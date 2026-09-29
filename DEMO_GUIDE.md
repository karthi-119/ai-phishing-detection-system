# PhishGuard AI — 3 to 5 Minute Hackathon Demonstration Guide

This guide provides a step-by-step presentation flow for demonstrating **PhishGuard AI** to hackathon evaluators.

---

## ⏱️ Presentation Timeline (3–5 Minutes)

### 1. Introduction & Problem Statement (0:00 – 0:45)
- **Speaker**: "Hello everyone! Today we are presenting **PhishGuard AI**, an AI-powered real-time phishing detection system for PSN013."
- **Key Point**: "Traditional static blacklists fail to detect zero-day phishing links. Attackers continuously create lookalike URLs targeting login portals and personal credentials. PhishGuard AI solves this by inspecting raw URL structures offline using Machine Learning and an Advanced Heuristic Engine."

### 2. Live Scanner Demonstration (0:45 – 2:00)
- **Action**: Open [http://localhost:5173](http://localhost:5173).
- **Step 1**: Click the harmless demo example pill: `https://www.example.org/login`.
- **Step 2**: Click **"Analyze URL"**.
- **Step 3**: Point out the dynamic scanning stages (`Analyzing URL syntax...` ➔ `Extracting 30 features...` ➔ `Evaluating Random Forest AI...`).
- **Step 4**: Explain the result:
  - **AI Risk Score**: `15 / 100` (LOW RISK)
  - **Explainable Security Report**: Direct HTTPS scheme and standard domain structure confirmed.
  - **Visual URL Breakdown**: Highlight decomposed `Protocol`, `Domain Hostname`, and `Resource Path`.

### 3. Suspicious / High Risk Link Inspection (2:00 – 3:15)
- **Step 1**: Enter a suspicious test pattern into the input box:
  `http://user@paypal-verify-account.com/login.php?redirect_url=http://malicious.com`
- **Step 2**: Click **"Analyze URL"**.
- **Step 3**: Show the resulting report:
  - **AI Risk Score**: `85 / 100` (CRITICAL / HIGH RISK)
  - **Phishing Attack Techniques**: Highlight detected cards (`IP-Based URL`, `URL Obfuscation`, `Credential-Themed URL`, `Redirect Manipulation`).
  - **Trust & Protocol Analysis**: Point out warnings (`Insecure HTTP scheme`, `Open redirect parameter`).

### 4. Model Transparency & Security Architecture (3:15 – 4:15)
- **Step 1**: Click the **"Model Insights"** tab in the top navigation.
- **Step 2**: Show actual dataset metrics:
  - Dataset: **UCI Phishing Websites (11,055 samples)**
  - Algorithm: **Random Forest Classifier (97.42% accuracy)**
  - Interactive **Gini Feature Importance** horizontal bar chart (`sslfinal_state`, `url_of_anchor`, `web_traffic`).
- **Step 3**: Click **"How It Works"** to review the 7-stage detection pipeline.

### 5. API Documentation & Conclusion (4:15 – 5:00)
- **Step 1**: Open Interactive Swagger API Docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
- **Step 2**: Mention **Security & SSRF Safeguards**:
  - Offline analysis only (server **never** fetches external websites or executes page JavaScript).
  - Submitted links are displayed in non-clickable code blocks for user safety.
- **Closing**: "Thank you! PhishGuard AI delivers instant, transparent, and explainable phishing detection."

---

## 💡 Harmless Demo Example URLs

| Demo Category | Target URL String | Expected Risk Level |
| :--- | :--- | :--- |
| **Legitimate Site** | `https://example.com` | LOW (Score: 0–29) |
| **Standard Portal** | `https://www.example.org/login` | LOW (Score: 0–29) |
| **Account Path** | `http://example.com/account` | MEDIUM (Score: 30–59) |
| **Suspicious Pattern** | `http://user@verify-secure-login.org/auth` | CRITICAL (Score: 80–100) |
