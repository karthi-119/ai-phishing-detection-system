/**
 * RiskIndicator Component.
 * Displays visual cards for each empirical risk indicator returned by the backend,
 * featuring severity badges (HIGH, MEDIUM, LOW) and detailed descriptions.
 */

import React from 'react';

function RiskIndicator({ indicators }) {
  const hasIndicators = Array.isArray(indicators) && indicators.length > 0;

  return (
    <div className="card indicators-card">
      <h3 className="card-subtitle">
        <span className="subtitle-icon">⚠️</span> Security Indicators ({hasIndicators ? indicators.length : 0})
      </h3>

      {hasIndicators ? (
        <div className="indicators-grid">
          {indicators.map((ind, idx) => {
            // Support both object and plain string fallback formats
            const name = typeof ind === 'object' ? ind.name : ind;
            const severity = (typeof ind === 'object' ? ind.severity : 'medium').toLowerCase();
            const desc = typeof ind === 'object' ? ind.description : '';

            const severityBadgeClass = `severity-tag sev-${severity}`;
            const icon = severity === 'high' ? '🔴' : severity === 'medium' ? '🟠' : '🟡';

            return (
              <div key={idx} className="indicator-card-item">
                <div className="indicator-card-header">
                  <span className="indicator-card-title">
                    <span className="indicator-icon">{icon}</span> {name}
                  </span>
                  <span className={severityBadgeClass}>{severity.toUpperCase()}</span>
                </div>
                {desc && <p className="indicator-card-desc">{desc}</p>}
              </div>
            );
          })}
        </div>
      ) : (
        <div className="no-indicators-box">
          <span className="check-icon">🟢</span>
          <span className="no-indicators-text">No major phishing-related URL indicators were detected.</span>
        </div>
      )}
    </div>
  );
}

export default RiskIndicator;
