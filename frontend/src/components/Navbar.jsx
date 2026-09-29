/**
 * Navbar Component for PhishGuard AI.
 * Displays logo branding, AI badge, navigation links, and Demo Mode toggle.
 */

import React from 'react';

function Navbar({ activeTab, setActiveTab, isDemoMode, setIsDemoMode }) {
  return (
    <nav className="navbar">
      <div className="navbar-brand" onClick={() => setActiveTab('home')}>
        <div className="shield-icon">🛡️</div>
        <div>
          <span className="brand-name">PhishGuard <span className="brand-accent">AI</span></span>
          <span className="brand-badge">AI-Powered Phishing Detection</span>
        </div>
      </div>

      <div className="navbar-links">
        <button
          className={`nav-link ${activeTab === 'home' ? 'active' : ''}`}
          onClick={() => setActiveTab('home')}
        >
          Home
        </button>
        <button
          className={`nav-link ${activeTab === 'insights' ? 'active' : ''}`}
          onClick={() => setActiveTab('insights')}
        >
          Model Insights
        </button>
        <button
          className={`nav-link ${activeTab === 'how-it-works' ? 'active' : ''}`}
          onClick={() => setActiveTab('how-it-works')}
        >
          How It Works
        </button>
        <button
          className={`nav-link ${activeTab === 'about' ? 'active' : ''}`}
          onClick={() => setActiveTab('about')}
        >
          About
        </button>

        {/* Demo Mode Toggle (Task 16) */}
        <button
          className={`demo-mode-btn ${isDemoMode ? 'demo-active' : ''}`}
          onClick={() => setIsDemoMode(!isDemoMode)}
          title="Toggle Development Demo Mode"
        >
          {isDemoMode ? '🧪 DEMO MODE (ON)' : '⚡ LIVE API MODE'}
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
