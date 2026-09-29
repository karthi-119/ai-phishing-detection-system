/**
 * PhishingTechniques Component.
 * Displays classified phishing attack techniques present in the analyzed URL.
 */

import React from 'react';

function PhishingTechniques({ techniques }) {
  if (!techniques || !Array.isArray(techniques) || techniques.length === 0) {
    return (
      <div className="card techniques-card">
        <h3 className="card-subtitle">
          <span className="subtitle-icon">🏷️</span> Detected Phishing Techniques
        </h3>
        <div className="no-techniques-box">
          <span className="no-tech-icon">🛡️</span>
          <div>
            <h4 className="no-tech-title">No Active Phishing Techniques Detected</h4>
            <p className="no-tech-desc">
              The URL string does not exhibit known attack pattern signatures such as IP hostnames, URL shorteners, open redirects, or credential harvesting keywords.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="card techniques-card">
      <h3 className="card-subtitle">
        <span className="subtitle-icon">🏷️</span> Detected Phishing Techniques ({techniques.length})
      </h3>
      <p className="section-help-text">
        Categorized threat patterns identified through URL pattern analysis.
      </p>

      <div className="techniques-grid">
        {techniques.map((item, idx) => {
          const sev = (item.severity || 'low').toLowerCase();
          return (
            <div key={idx} className={`technique-card tech-sev-${sev}`}>
              <div className="tech-card-header">
                <span className="tech-name">{item.technique}</span>
                <span className={`severity-badge severity-${sev}`}>
                  {sev === 'high' ? '🔴 HIGH' : sev === 'medium' ? '🟠 MEDIUM' : '🟡 LOW'}
                </span>
              </div>
              <p className="tech-desc">{item.description}</p>
              <div className="tech-evidence-box">
                <span className="evidence-tag">Evidence:</span> <code>{item.evidence}</code>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default PhishingTechniques;
