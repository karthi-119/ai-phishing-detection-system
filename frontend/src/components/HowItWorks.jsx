/**
 * HowItWorks Component.
 * Illustrates the 5-step processing pipeline and visual flow diagram.
 */

import React from 'react';

function HowItWorks() {
  return (
    <div className="card info-page-card">
      <div className="page-header">
        <h2 className="page-title">How PhishGuard AI Works</h2>
        <p className="page-subtitle">
          An end-to-end explainable AI security pipeline evaluating URL structure, lexical characteristics, and protocol security signals in real time.
        </p>
      </div>

      {/* 5-Step Visual Pipeline Flow (Task 11) */}
      <div className="pipeline-flow">
        <div className="flow-step">
          <div className="step-number">1</div>
          <div className="step-icon">🌐</div>
          <h4>URL Input</h4>
          <p>User submits a target web address for security inspection.</p>
        </div>
        <div className="flow-arrow">➔</div>

        <div className="flow-step">
          <div className="step-number">2</div>
          <div className="step-icon">⚙️</div>
          <h4>Feature Extraction</h4>
          <p>30 lexical, domain, and protocol signals are extracted from the URL string.</p>
        </div>
        <div className="flow-arrow">➔</div>

        <div className="flow-step">
          <div className="step-number">3</div>
          <div className="step-icon">🌲</div>
          <h4>Machine Learning</h4>
          <p>Random Forest classifier evaluates features against trained 97.42% accurate model.</p>
        </div>
        <div className="flow-arrow">➔</div>

        <div className="flow-step">
          <div className="step-number">4</div>
          <div className="step-icon">⚡</div>
          <h4>Risk Analysis</h4>
          <p>Calculates AI Risk Score (0-100) and maps risk levels (LOW, MEDIUM, HIGH, CRITICAL).</p>
        </div>
        <div className="flow-arrow">➔</div>

        <div className="flow-step">
          <div className="step-number">5</div>
          <div className="step-icon">📊</div>
          <h4>Explainable Result</h4>
          <p>Generates structured security indicators and actionable recommendations.</p>
        </div>
      </div>

      <div className="workflow-details-grid">
        <div className="detail-card">
          <h3>🔍 Lexical & Domain Signals</h3>
          <p>
            Analyzes IP address usage, domain hyphens, subdomain depth, URL shorteners,
            `@` symbols, non-standard network ports, and redirection query parameters.
          </p>
        </div>

        <div className="detail-card">
          <h3>🛡️ SSRF Safety & Static Parsing</h3>
          <p>
            The backend engine performs non-invasive static URL analysis without automatically
            crawling or executing remote JavaScript, ensuring zero SSRF security risk.
          </p>
        </div>
      </div>
    </div>
  );
}

export default HowItWorks;
