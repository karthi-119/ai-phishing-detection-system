/**
 * PipelineVisualizer Component.
 * Visualizes the 7-stage cybersecurity detection pipeline workflow:
 * URL Input -> URL Validation -> Feature Extractor -> Random Forest -> Heuristics -> Risk Intelligence -> Explainable Result.
 */

import React from 'react';

function PipelineVisualizer() {
  const steps = [
    { num: 1, icon: '🌐', title: 'URL Input', desc: 'Raw Target String' },
    { num: 2, icon: '🛡️', title: 'URL Validation', desc: 'SSRF & Syntax Guard' },
    { num: 3, icon: '📊', title: '30-Feature Extractor', desc: 'Lexical & Host Extraction' },
    { num: 4, icon: '🤖', title: 'Random Forest', desc: 'ML Inference Model' },
    { num: 5, icon: '🔬', title: 'Heuristic Engine', desc: 'Pattern & Obfuscation' },
    { num: 6, icon: '🎯', title: 'Risk Intelligence', desc: 'Deterministic 0-100 Score' },
    { num: 7, icon: '📝', title: 'Explainable Result', desc: 'Security Report' }
  ];

  return (
    <div className="card pipeline-card">
      <h3 className="card-subtitle">
        <span className="subtitle-icon">⚙️</span> PhishGuard AI Detection Pipeline
      </h3>
      <p className="section-help-text">
        Multi-layered analysis architecture combining machine learning inference with offline heuristic security rules.
      </p>

      <div className="pipeline-steps-wrapper">
        {steps.map((step, idx) => (
          <React.Fragment key={idx}>
            <div className="pipeline-step-box">
              <div className="step-badge">{step.num}</div>
              <div className="pipeline-step-icon">{step.icon}</div>
              <div className="pipeline-step-title">{step.title}</div>
              <div className="pipeline-step-desc">{step.desc}</div>
            </div>
            {idx < steps.length - 1 && <div className="pipeline-connector-arrow">➔</div>}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}

export default PipelineVisualizer;
