# PhishGuard AI - Frontend Web Application

**PhishGuard AI** is a modern, responsive web application for real-time URL phishing detection and explainable risk factor analysis.

---

## 🛠️ Technology Stack

- **Framework**: React 19 (scaffolded via Vite)
- **Styling**: Modern CSS (Cybersecurity Dark Mode design system, glassmorphism, responsive CSS grid)
- **API Client**: Standard Fetch API communicating with REST endpoints
- **Development Server**: Vite dev server (`http://localhost:5173`)

---

## 📁 Frontend Directory Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/         # Reusable UI components
│   │   ├── Navbar.jsx          # Header navigation & PhishGuard AI branding
│   │   ├── UrlInput.jsx        # Controlled input form & validation
│   │   ├── LoadingState.jsx    # Radar scanner animation loader
│   │   ├── RiskResult.jsx      # Result card, status badge, risk level & confidence meter
│   │   ├── RiskIndicator.jsx   # List of empirical risk indicators
│   │   ├── FeatureSummary.jsx  # Card grid of key URL feature characteristics
│   │   ├── ErrorMessage.jsx    # User-friendly error alert cards
│   │   ├── RecentScans.jsx     # Client-side localStorage history (last 5 scans)
│   │   ├── HowItWorks.jsx      # 4-step workflow diagram page
│   │   └── AboutSection.jsx    # Project background & disclaimer page
│   │
│   ├── services/
│   │   └── api.js              # REST API client sending POST http://localhost:8000/api/predict
│   │
│   ├── App.jsx             # Main application layout & state coordinator
│   ├── main.jsx            # DOM mounting entrypoint
│   └── index.css           # Cybersecurity design system stylesheet
├── package.json            # Node.js dependencies
└── README.md               # Frontend documentation (this file)
```

---

## ⚙️ Backend Dependency

The frontend requires the **FastAPI backend** running locally on port `8000`.

- **API Endpoint**: `POST http://localhost:8000/api/predict`
- **Health Check**: `GET http://localhost:8000/api/health`

---

## 🚦 Quick Start Instructions

### 1. Install Dependencies
```bash
npm install
```

### 2. Start Development Server
```bash
npm run dev
```

- Open your browser at: `http://localhost:5173`
- Ensure FastAPI backend server is active at `http://localhost:8000`.

---

## 🔒 Security Notice

- The application performs **non-invasive static URL feature analysis** via the backend API.
- The frontend **never** automatically visits, opens, downloads files, or executes JavaScript from submitted URLs.
