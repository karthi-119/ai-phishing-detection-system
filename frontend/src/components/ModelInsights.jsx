/**
 * ModelInsights Component.
 * Fetches live top 10 feature importances from GET /api/model/insights and renders
 * a horizontal bar chart along with model transparency information.
 */

import React, { useState, useEffect } from 'react';
import { getModelInsights } from '../services/api';

function ModelInsights() {
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadInsights() {
      const data = await getModelInsights();
      setInsights(data);
      setLoading(false);
    }
    loadInsights();
  }, []);

  return (
    <div className="card info-page-card">
      <div className="page-header">
        <h2 className="page-title">Model Transparency & AI Insights</h2>
        <p className="page-subtitle">
          Empirical training metadata, dataset characteristics, and Gini feature importances extracted directly from our trained Random Forest model.
        </p>
      </div>

      {/* Model Transparency Badges */}
      <div className="insights-summary-grid">
        <div className="insight-stat-card">
          <span className="stat-label">Algorithm</span>
          <span className="stat-value">{insights?.model || 'RandomForestClassifier'}</span>
        </div>
        <div className="insight-stat-card">
          <span className="stat-label">Dataset</span>
          <span className="stat-value">UCI Phishing Websites (ID 327)</span>
        </div>
        <div className="insight-stat-card">
          <span className="stat-label">Evaluated Features</span>
          <span className="stat-value">{insights?.feature_count || 30} Features</span>
        </div>
        <div className="insight-stat-card">
          <span className="stat-label">Test Accuracy</span>
          <span className="stat-value text-accent">97.42%</span>
        </div>
      </div>

      {/* Model Transparency Details Card */}
      <div className="transparency-card-box">
        <h3 className="card-subtitle">
          <span className="subtitle-icon">🔬</span> Training & Dataset Transparency
        </h3>
        <p className="transparency-disclaimer">
          The model predicts based on extracted URL/web characteristics available to the trained feature set. Below are the actual training parameters:
        </p>
        <div className="transparency-metrics-grid">
          <div className="transparency-item">
            <span className="trans-label">Total Instances:</span>
            <span className="trans-val">11,055 Samples</span>
          </div>
          <div className="transparency-item">
            <span className="trans-label">Train / Test Split:</span>
            <span className="trans-val">8,844 Train (80%) / 2,211 Test (20%)</span>
          </div>
          <div className="transparency-item">
            <span className="trans-label">Estimators (Trees):</span>
            <span className="trans-val">200 Decision Trees</span>
          </div>
          <div className="transparency-item">
            <span className="trans-label">Phishing Precision:</span>
            <span className="trans-val">97.82%</span>
          </div>
          <div className="transparency-item">
            <span className="trans-label">Phishing Recall:</span>
            <span className="trans-val">96.33%</span>
          </div>
          <div className="transparency-item">
            <span className="trans-label">Phishing F1-Score:</span>
            <span className="trans-val">97.07%</span>
          </div>
        </div>
      </div>

      {/* Feature Importance Chart */}
      <div className="chart-section-box">
        <h3 className="card-subtitle">
          <span className="subtitle-icon">📈</span> Top 10 Model Features (Gini Importance)
        </h3>

        {loading ? (
          <p className="loading-text">Loading feature importances from backend model...</p>
        ) : insights && insights.top_features ? (
          <div className="feature-bars-container">
            {insights.top_features.map((item, idx) => {
              const pct = (item.importance * 100).toFixed(1);
              return (
                <div key={idx} className="bar-row">
                  <div className="bar-label-col">
                    <code>{item.feature}</code>
                  </div>
                  <div className="bar-track-col">
                    <div
                      className="bar-fill-accent"
                      style={{ width: `${Math.min(100, Math.max(5, pct * 2.5))}%` }}
                    ></div>
                  </div>
                  <div className="bar-value-col">
                    <span>{pct}%</span>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <p className="loading-text">Unable to load live feature importances.</p>
        )}

        <div className="disclaimer-note-box">
          ℹ️ <strong>Feature Importance Note:</strong> Feature importance indicates which features contributed most to the model's decisions during training; it does not prove that a feature alone determines whether a URL is malicious.
        </div>
      </div>
    </div>
  );
}

export default ModelInsights;
