/**
 * AboutSection Component.
 * Explains project background, technology stack, and essential security disclaimers.
 */

import React from 'react';

function AboutSection() {
  return (
    <div className="card info-page-card">
      <div className="page-header">
        <h2 className="page-title">About PhishGuard AI</h2>
        <p className="page-subtitle">
          College Hackathon Prototype for PSN013 – Real-Time AI Phishing Detection System.
        </p>
      </div>

      <div className="about-content">
        <p>
          <strong>PhishGuard AI</strong> is an AI-assisted phishing detection prototype built to inspect web links in real time.
          Using a <strong>Random Forest Classifier</strong> trained on the UCI Phishing Websites Dataset (11,055 samples),
          the system evaluates 30 structural, domain, and protocol signals to detect zero-day phishing attempts before users fall victim.
        </p>

        <div className="tech-badge-container">
          <span className="tech-pill">React + Vite</span>
          <span className="tech-pill">FastAPI</span>
          <span className="tech-pill">Python 3.14</span>
          <span className="tech-pill">Scikit-learn</span>
          <span className="tech-pill">Random Forest (97.42% Acc)</span>
          <span className="tech-pill">REST API</span>
        </div>

        <div className="disclaimer-banner">
          <div className="disclaimer-icon">⚠️</div>
          <div>
            <h4 className="disclaimer-title">Important System Disclaimer</h4>
            <p className="disclaimer-text">
              The system provides an automated machine-learning risk assessment and should not be treated as a guarantee that a website is 100% safe or malicious. Always exercise standard cyber hygiene and verify link destinations independently.
            </p>
          </div>
        </div>

        <details className="limitations-accordion">
          <summary className="accordion-header">
            <span>⚙️ System Limitations & Detection Boundaries</span>
            <span className="accordion-icon">▼</span>
          </summary>
          <div className="accordion-content">
            <ul>
              <li><strong>No Dynamic Content Inspection:</strong> The model evaluates structural and domain parameters; it does not execute client-side JavaScript or analyze rendered page screenshots.</li>
              <li><strong>Zero-Day Domain Heuristics:</strong> Brand-new domains may trigger domain age indicators even if legitimate, or evade detection if hosted on reputable CDNs.</li>
              <li><strong>Offline Analysis:</strong> Analysis is non-intrusive and static to prevent server-side request forgery (SSRF) and avoid exposing server IPs to suspicious destinations.</li>
            </ul>
          </div>
        </details>
      </div>
    </div>
  );
}

export default AboutSection;
