/**
 * ErrorMessage Component.
 * Displays user-friendly error alerts for network or validation failures.
 */

import React from 'react';

function ErrorMessage({ message }) {
  if (!message) return null;

  return (
    <div className="card error-card" aria-live="assertive">
      <div className="error-icon">⚠️</div>
      <div className="error-content">
        <h4 className="error-title">Analysis Failed</h4>
        <p className="error-message-text">{message}</p>
      </div>
    </div>
  );
}

export default ErrorMessage;
