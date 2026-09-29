/**
 * ScanComparison Component.
 * Compares current URL scan metrics against a previously saved scan side-by-side.
 */

import React from 'react';

function ScanComparison({ currentScan, compareScan, onClose }) {
  if (!currentScan || !compareScan) return null;

  const getSubdomains = (scan) => scan?.heuristic_analysis?.domain_analysis?.subdomain_count ?? '-';
  const getUrlLen = (scan) => scan?.url?.length ?? '-';
  const getHttps = (scan) => (scan?.trust_analysis?.https ? '✓ HTTPS' : '⚠️ HTTP');

  return (
    <div className="card comparison-card">
      <div className="comparison-header">
        <h3 className="card-subtitle">
          <span className="subtitle-icon">⚖️</span> Scan Comparison: Current vs Previous
        </h3>
        <button type="button" className="btn-close-comparison" onClick={onClose}>
          ✕ Close Comparison
        </button>
      </div>

      <div className="table-responsive">
        <table className="comparison-table">
          <thead>
            <tr>
              <th>Metric / Property</th>
              <th>Current Scan</th>
              <th>Previous Scan</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Target URL</strong></td>
              <td className="url-cell" title={currentScan.url}>{currentScan.url}</td>
              <td className="url-cell" title={compareScan.url}>{compareScan.url}</td>
            </tr>
            <tr>
              <td><strong>Prediction</strong></td>
              <td>
                <span className={`status-pill ${currentScan.prediction === 'likely_phishing' ? 'pill-phishing' : 'pill-legitimate'}`}>
                  {currentScan.prediction === 'likely_phishing' ? 'Phishing' : 'Legitimate'}
                </span>
              </td>
              <td>
                <span className={`status-pill ${compareScan.prediction === 'likely_phishing' ? 'pill-phishing' : 'pill-legitimate'}`}>
                  {compareScan.prediction === 'likely_phishing' ? 'Phishing' : 'Legitimate'}
                </span>
              </td>
            </tr>
            <tr>
              <td><strong>AI Risk Score</strong></td>
              <td className="score-cell"><strong>{currentScan.risk_score ?? '-'}</strong>/100</td>
              <td className="score-cell"><strong>{compareScan.risk_score ?? '-'}</strong>/100</td>
            </tr>
            <tr>
              <td><strong>Risk Level</strong></td>
              <td>
                <span className={`risk-pill risk-pill-${currentScan.risk_level}`}>
                  {(currentScan.risk_level || 'low').toUpperCase()}
                </span>
              </td>
              <td>
                <span className={`risk-pill risk-pill-${compareScan.risk_level}`}>
                  {(compareScan.risk_level || 'low').toUpperCase()}
                </span>
              </td>
            </tr>
            <tr>
              <td><strong>Protocol</strong></td>
              <td>{getHttps(currentScan)}</td>
              <td>{getHttps(compareScan)}</td>
            </tr>
            <tr>
              <td><strong>URL Length</strong></td>
              <td>{getUrlLen(currentScan)} chars</td>
              <td>{getUrlLen(compareScan)} chars</td>
            </tr>
            <tr>
              <td><strong>Subdomains</strong></td>
              <td>{getSubdomains(currentScan)}</td>
              <td>{getSubdomains(compareScan)}</td>
            </tr>
            <tr>
              <td><strong>Risk Indicators</strong></td>
              <td>{currentScan.risk_indicators?.length ?? 0} Detected</td>
              <td>{compareScan.risk_indicators?.length ?? 0} Detected</td>
            </tr>
            <tr>
              <td><strong>Phishing Techniques</strong></td>
              <td>{currentScan.phishing_techniques?.length ?? 0} Techniques</td>
              <td>{compareScan.phishing_techniques?.length ?? 0} Techniques</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ScanComparison;
