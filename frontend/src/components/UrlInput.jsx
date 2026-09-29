/**
 * UrlInput Component.
 * Controlled input box for target URL entry with validation and clear button.
 */

import React, { useState } from 'react';

function UrlInput({ url, setUrl, onScan, isAnalyzing }) {
  const [inputError, setInputError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setInputError('');

    const trimmed = url.strip ? url.strip() : url.trim();

    if (!trimmed) {
      setInputError('Please enter a target URL to analyze.');
      return;
    }

    if (!trimmed.startsWith('http://') && !trimmed.startsWith('https://')) {
      // Auto-prefix http:// if omitted for user convenience or show friendly note
      if (!trimmed.includes('.')) {
        setInputError('Please enter a valid web domain or URL (e.g. https://example.com).');
        return;
      }
    }

    onScan(trimmed);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSubmit(e);
    }
  };

  const handleClear = () => {
    setUrl('');
    setInputError('');
  };

  return (
    <div className="url-input-container">
      <form onSubmit={handleSubmit} className="input-form">
        <div className="input-wrapper">
          <span className="search-icon">🌐</span>
          <input
            type="text"
            className="url-field"
            placeholder="Paste a suspicious URL here (e.g., https://example.com)..."
            value={url}
            onChange={(e) => {
              setUrl(e.target.value);
              if (inputError) setInputError('');
            }}
            onKeyDown={handleKeyDown}
            disabled={isAnalyzing}
            aria-label="URL to analyze"
          />
          {url && !isAnalyzing && (
            <button
              type="button"
              className="btn-clear"
              onClick={handleClear}
              aria-label="Clear input"
            >
              ✕
            </button>
          )}
        </div>

        <button
          type="submit"
          className="btn-scan"
          disabled={isAnalyzing || !url.trim()}
        >
          {isAnalyzing ? (
            <>
              <span className="spinner-sm"></span> Analyzing...
            </>
          ) : (
            'Analyze URL'
          )}
        </button>
      </form>

      {inputError && (
        <div className="input-validation-error">
          ⚠️ {inputError}
        </div>
      )}

      {/* Safe Demo Examples Selector (Requirement 14) */}
      <div className="demo-examples-row">
        <span className="demo-examples-label">Try Harmless Examples:</span>
        <button
          type="button"
          className="demo-example-pill"
          onClick={() => { setUrl('https://example.com'); setInputError(''); }}
        >
          https://example.com
        </button>
        <button
          type="button"
          className="demo-example-pill"
          onClick={() => { setUrl('https://www.example.org/login'); setInputError(''); }}
        >
          https://www.example.org/login
        </button>
        <button
          type="button"
          className="demo-example-pill"
          onClick={() => { setUrl('http://example.com/account'); setInputError(''); }}
        >
          http://example.com/account
        </button>
      </div>

      <p className="privacy-note">
        🔒 <strong>Privacy Note:</strong> URLs are analyzed by the local detection engine. Do not enter passwords or sensitive personal information.
      </p>
    </div>
  );
}

export default UrlInput;
