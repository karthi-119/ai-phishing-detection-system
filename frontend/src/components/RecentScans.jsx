/**
 * RecentScans Component.
 * Manages client-side scan history stored in localStorage (last 5 scans).
 * Features a "View Analysis" button to restore selected analysis results locally.
 */

import React from 'react';

function RecentScans({ history, onClearHistory, onRestoreScan, onCompareScan }) {
  if (!history || history.length === 0) return null;

  return (
    <div className="card history-card">
      <div className="history-header">
        <h3 className="card-subtitle">
          <span className="subtitle-icon">🕒</span> Recent Scans (Last {history.length} of 10)
        </h3>
        <button
          type="button"
          className="btn-text-danger"
          onClick={onClearHistory}
        >
          Clear History
        </button>
      </div>

      <div className="table-responsive">
        <table className="history-table">
          <thead>
            <tr>
              <th>Target URL</th>
              <th>Prediction</th>
              <th>AI Risk Score</th>
              <th>Risk Level</th>
              <th>Time</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {history.map((item, idx) => {
              const isPhishing = item.prediction === 'likely_phishing';
              return (
                <tr key={idx} className="history-row">
                  <td className="url-cell" title={item.url}>
                    {item.url}
                  </td>
                  <td>
                    <span className={`status-pill ${isPhishing ? 'pill-phishing' : 'pill-legitimate'}`}>
                      {isPhishing ? 'Phishing' : 'Legitimate'}
                    </span>
                  </td>
                  <td className="score-cell">
                    <strong>{item.risk_score ?? '-'}</strong>/100
                  </td>
                  <td>
                    <span className={`risk-pill risk-pill-${item.risk_level}`}>
                      {(item.risk_level || 'low').toUpperCase()}
                    </span>
                  </td>
                  <td className="time-cell">{item.time}</td>
                  <td className="actions-cell">
                    <button
                      type="button"
                      className="btn-action-restore"
                      onClick={() => onRestoreScan(item.full_data || item)}
                      title="Inspect analysis report"
                    >
                      View Analysis
                    </button>
                    {onCompareScan && (
                      <button
                        type="button"
                        className="btn-action-compare"
                        onClick={() => onCompareScan(item.full_data || item)}
                        title="Compare against current scan"
                      >
                        Compare
                      </button>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default RecentScans;
