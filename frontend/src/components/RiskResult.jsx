/**
 * RiskResult Component.
 * Displays overall phishing classification, AI Risk Score gauge (0-100),
 * risk level badge, confidence meter, summary text, and recommended security actions.
 */

import React from 'react';
import UrlBreakdown from './UrlBreakdown';
import PhishingTechniques from './PhishingTechniques';

function RiskResult({ result }) {
  if (!result) return null;

  const isPhishing = result.prediction === 'likely_phishing';
  const confidencePct = typeof result.confidence === 'number' ? result.confidence : 0;
  const riskScore = typeof result.risk_score === 'number' ? result.risk_score : 50;
  const riskLevel = (result.risk_level || 'low').toUpperCase();

  // Dynamic colors based on risk level
  const statusColor = isPhishing ? 'var(--color-phishing)' : 'var(--color-legitimate)';
  const riskBadgeClass = `risk-badge risk-${result.risk_level || 'low'}`;

  // Recommended Action Wording
  let actionText = '';
  if (riskLevel === 'CRITICAL' || riskLevel === 'HIGH') {
    actionText = 'Do not enter passwords, OTPs, banking information, or payment details on this website until its legitimacy is independently verified.';
  } else if (riskLevel === 'MEDIUM') {
    actionText = 'Exercise caution and verify the website through an official source before entering sensitive information.';
  } else {
    actionText = 'No major phishing-related indicators were detected. Continue following normal cybersecurity precautions.';
  }

  const trustAnalysis = result.trust_analysis || {};

  return (
    <div className="risk-result-wrapper" aria-live="assertive">
      <div className="card result-card">
        {/* Header Banner */}
        <div className="result-header">
          <div>
            <span className="section-label">AI Phishing Intelligence & Security Report</span>
            <h2 className="result-status" style={{ color: statusColor }}>
              {isPhishing ? '🚨 LIKELY PHISHING' : '✅ LIKELY LEGITIMATE'}
            </h2>
            <p className="analyzed-url-text">Target URL: <code>{result.url}</code></p>
          </div>

          <div className="score-and-badge">
            {/* AI Risk Score Gauge */}
            <div className="risk-score-box">
              <span className="score-label">AI RISK SCORE</span>
              <div className="score-number-row">
                <span className="score-large" style={{ color: statusColor }}>{riskScore}</span>
                <span className="score-max">/100</span>
              </div>
            </div>

            <div className={riskBadgeClass}>
              <span className="risk-level-label">RISK LEVEL</span>
              <span className="risk-level-value">{riskLevel}</span>
            </div>
          </div>
        </div>

        {/* Dynamic Security Summary Card */}
        <div className="summary-banner">
          <span className="summary-icon">💡</span>
          <div>
            <h4 className="summary-title">Security Intelligence Summary</h4>
            <p className="summary-text">{result.summary || 'URL features evaluated against Random Forest classifier and heuristic rules.'}</p>
          </div>
        </div>

        <div className="result-body">
          {/* Model Confidence Progress Gauge */}
          <div className="confidence-meter-box">
            <div className="confidence-label-row">
              <span>Model Confidence ({result.model?.name || 'Random Forest'})</span>
              <span className="confidence-value">{confidencePct.toFixed(1)}%</span>
            </div>

            <div className="confidence-track">
              <div
                className="confidence-fill"
                style={{
                  width: `${Math.min(100, Math.max(0, confidencePct))}%`,
                  backgroundColor: statusColor,
                }}
              ></div>
            </div>
          </div>

          {/* Trust Analysis Section (Requirement 6 & 9) */}
          <div className="trust-analysis-box">
            <h4 className="card-subtitle-sm">
              <span>🔒 Trust & Protocol Analysis</span>
              <span className="domain-struct-badge">{trustAnalysis.domain_structure || 'Standard Domain'}</span>
            </h4>
            <div className="trust-lists-grid">
              <div className="trust-list-col">
                <span className="col-title text-success">✓ Trust Indicators</span>
                <ul>
                  {trustAnalysis.trust_indicators && trustAnalysis.trust_indicators.length > 0 ? (
                    trustAnalysis.trust_indicators.map((ti, i) => <li key={i}>{ti}</li>)
                  ) : (
                    <li>No positive trust indicators observed</li>
                  )}
                </ul>
              </div>
              <div className="trust-list-col">
                <span className="col-title text-warning">⚠️ Warnings & Security Disclaimers</span>
                <ul>
                  {trustAnalysis.warnings && trustAnalysis.warnings.length > 0 ? (
                    trustAnalysis.warnings.map((warn, i) => <li key={i}>{warn}</li>)
                  ) : (
                    <li>No structural protocol warnings detected</li>
                  )}
                </ul>
              </div>
            </div>
          </div>

          {/* Recommended Action Card */}
          <div className={`action-card ${isPhishing ? 'action-danger' : 'action-safe'}`}>
            <div className="action-icon">{isPhishing ? '🛑' : '🛡️'}</div>
            <div>
              <h4 className="action-title">Recommended Action</h4>
              <p className="action-desc">{actionText}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Visual URL Breakdown Component (Requirement 10) */}
      <UrlBreakdown heuristicAnalysis={result.heuristic_analysis} />

      {/* Detected Phishing Attack Techniques (Requirement 3 & 9) */}
      <PhishingTechniques techniques={result.phishing_techniques} />
    </div>
  );
}

export default RiskResult;
