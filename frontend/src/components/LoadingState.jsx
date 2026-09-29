/**
 * LoadingState Component.
 * Displays animated radar scanner with dynamic stage-based status messages during API inference.
 */

import React, { useState, useEffect } from 'react';

const STAGES = [
  'Analyzing URL syntax & protocol...',
  'Extracting 30 lexical & domain features...',
  'Evaluating Random Forest AI classifier...',
  'Inspecting suspicious heuristic patterns...',
  'Generating explainable security report...'
];

function LoadingState() {
  const [currentStageIdx, setCurrentStageIdx] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentStageIdx((prev) => (prev + 1) % STAGES.length);
    }, 400);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="loading-container" aria-live="polite">
      <div className="radar-spinner">
        <div className="radar-sweep"></div>
        <div className="radar-dot"></div>
      </div>
      <h3 className="loading-title">{STAGES[currentStageIdx]}</h3>
      <p className="loading-subtitle">
        PhishGuard AI Detection Engine • Non-intrusive offline inspection in progress
      </p>
    </div>
  );
}

export default LoadingState;
