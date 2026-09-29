/**
 * FeatureSummary Component.
 * Groups URL feature characteristics into 3 logical categories:
 * 1. URL Structure
 * 2. Domain Characteristics
 * 3. Security & Protocol
 */

import React from 'react';

function FeatureSummary({ features }) {
  if (!features) return null;

  const categories = [
    {
      title: '🌐 URL Structure',
      items: [
        {
          label: 'URL Length',
          value: features.url_length === 1 ? 'Normal (<54 chars)' : features.url_length === 0 ? 'Suspicious (54-75)' : 'Excessive (>75 chars)',
          status: features.url_length === 1 ? 'good' : features.url_length === 0 ? 'warning' : 'bad'
        },
        {
          label: '@ Symbol',
          value: features.having_at_symbol === -1 ? 'Detected (@ Present)' : 'Not Detected',
          status: features.having_at_symbol === -1 ? 'bad' : 'good'
        },
        {
          label: 'Double Slash',
          value: features.double_slash_redirecting === -1 ? 'Redirection Detected' : 'Clean',
          status: features.double_slash_redirecting === -1 ? 'bad' : 'good'
        },
        {
          label: 'URL Redirection',
          value: features.redirect === -1 ? 'Redirection Parameters Found' : 'Clean',
          status: features.redirect === -1 ? 'bad' : 'good'
        }
      ]
    },
    {
      title: '🏢 Domain Characteristics',
      items: [
        {
          label: 'IP Address',
          value: features.having_ip_address === -1 ? 'IP Address Detected' : 'Not Detected (Domain Used)',
          status: features.having_ip_address === -1 ? 'bad' : 'good'
        },
        {
          label: 'Subdomain Count',
          value: features.having_sub_domain === 1 ? 'Normal (<=1)' : features.having_sub_domain === 0 ? 'Suspicious (2)' : 'Excessive (>2 subdomains)',
          status: features.having_sub_domain === 1 ? 'good' : features.having_sub_domain === 0 ? 'warning' : 'bad'
        },
        {
          label: 'Domain Hyphen',
          value: features.prefix_suffix === -1 ? 'Hyphen in Domain (-)' : 'Clean Domain',
          status: features.prefix_suffix === -1 ? 'bad' : 'good'
        },
        {
          label: 'URL Shortener',
          value: features.shortining_service === -1 ? 'Shortener Service Detected' : 'Not Detected',
          status: features.shortining_service === -1 ? 'bad' : 'good'
        }
      ]
    },
    {
      title: '🔒 Security & Protocol',
      items: [
        {
          label: 'HTTPS / SSL',
          value: features.sslfinal_state === 1 ? 'Secure (HTTPS Protocol)' : 'Insecure (HTTP Protocol)',
          status: features.sslfinal_state === 1 ? 'good' : 'bad'
        },
        {
          label: 'Network Port',
          value: features.port === -1 ? 'Non-Standard Port Open' : 'Standard Port (80/443)',
          status: features.port === -1 ? 'bad' : 'good'
        }
      ]
    }
  ];

  return (
    <div className="card feature-summary-card">
      <h3 className="card-subtitle">
        <span className="subtitle-icon">📊</span> URL Feature Analysis
      </h3>

      <div className="grouped-features-wrapper">
        {categories.map((cat, idx) => (
          <div key={idx} className="feature-category-block">
            <h4 className="category-title">{cat.title}</h4>
            <div className="features-grid">
              {cat.items.map((item, itemIdx) => (
                <div key={itemIdx} className={`feature-card feat-status-${item.status}`}>
                  <span className="feature-card-label">{item.label}</span>
                  <span className="feature-card-value">{item.value}</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default FeatureSummary;
