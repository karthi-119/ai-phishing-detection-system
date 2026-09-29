/**
 * UrlBreakdown Component.
 * Visually decomposes a target URL into color-coded structural components:
 * Protocol | Domain | Path | Query String.
 * Submitted URLs are strictly displayed as code/text blocks (NOT clickable) for SSRF safety.
 */

import React from 'react';

function UrlBreakdown({ heuristicAnalysis }) {
  if (!heuristicAnalysis || !heuristicAnalysis.url_structure) return null;

  const { scheme, hostname, path, query } = heuristicAnalysis.url_structure;

  return (
    <div className="card breakdown-card">
      <h3 className="card-subtitle">
        <span className="subtitle-icon">🧩</span> Visual URL Breakdown
      </h3>
      <p className="section-help-text">
        Non-intrusive lexical decomposition of protocol, hostname, path, and query parameters.
      </p>

      <div className="url-segments-container">
        {/* Scheme / Protocol */}
        <div className="segment-box segment-scheme">
          <span className="segment-label">Protocol</span>
          <code className="segment-val">{scheme ? `${scheme}://` : 'http://'}</code>
        </div>

        {/* Hostname / Domain */}
        <div className="segment-box segment-domain">
          <span className="segment-label">Domain Hostname</span>
          <code className="segment-val">{hostname || 'unknown-domain'}</code>
        </div>

        {/* Path */}
        {path && path !== '/' && (
          <div className="segment-box segment-path">
            <span className="segment-label">Resource Path</span>
            <code className="segment-val">{path}</code>
          </div>
        )}

        {/* Query Parameters */}
        {query && (
          <div className="segment-box segment-query">
            <span className="segment-label">Query Parameters</span>
            <code className="segment-val">?{query}</code>
          </div>
        )}
      </div>
    </div>
  );
}

export default UrlBreakdown;
