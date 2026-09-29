/**
 * Main Application Component for PhishGuard AI.
 * Coordinates UI components, API service calls, localStorage history, and navigation tabs.
 */

import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import UrlInput from './components/UrlInput';
import LoadingState from './components/LoadingState';
import RiskResult from './components/RiskResult';
import RiskIndicator from './components/RiskIndicator';
import FeatureSummary from './components/FeatureSummary';
import ErrorMessage from './components/ErrorMessage';
import RecentScans from './components/RecentScans';
import ScanComparison from './components/ScanComparison';
import PipelineVisualizer from './components/PipelineVisualizer';
import HowItWorks from './components/HowItWorks';
import ModelInsights from './components/ModelInsights';
import AboutSection from './components/AboutSection';
import { analyzeUrl } from './services/api';

const LOCAL_STORAGE_KEY = 'phishguard_scan_history';

function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [url, setUrl] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [compareScan, setCompareScan] = useState(null);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);
  const [isDemoMode, setIsDemoMode] = useState(false);

  // Load scan history from localStorage on initial render
  useEffect(() => {
    try {
      const savedHistory = localStorage.getItem(LOCAL_STORAGE_KEY);
      if (savedHistory) {
        setHistory(JSON.parse(savedHistory));
      }
    } catch (e) {
      console.warn('Could not read scan history from localStorage:', e);
    }
  }, []);

  // Save scan result to history (max 10 items, no sensitive tokens)
  const saveToHistory = (res) => {
    const newItem = {
      url: res.url,
      prediction: res.prediction,
      risk_level: res.risk_level,
      risk_score: res.risk_score,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      full_data: res,
    };

    setHistory((prevHistory) => {
      // Avoid duplicate consecutive entry
      const filtered = prevHistory.filter((item) => item.url !== res.url);
      const updated = [newItem, ...filtered].slice(0, 10);
      try {
        localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(updated));
      } catch (e) {
        console.warn('Could not save history to localStorage:', e);
      }
      return updated;
    });
  };

  const handleClearHistory = () => {
    setHistory([]);
    setCompareScan(null);
    try {
      localStorage.removeItem(LOCAL_STORAGE_KEY);
    } catch (e) {
      console.warn('Could not clear history from localStorage:', e);
    }
  };

  // Main scan execution handler calling backend POST /api/predict
  const handleScan = async (targetUrl) => {
    setIsAnalyzing(true);
    setError(null);
    setResult(null);
    setCompareScan(null);

    try {
      const data = await analyzeUrl(targetUrl);
      setResult(data);
      saveToHistory(data);
    } catch (err) {
      if (isDemoMode) {
        // Fallback for demo mode if backend is disconnected or offline during demo presentation
        const mockDemoData = {
          success: true,
          url: targetUrl,
          prediction: targetUrl.includes('secure') || targetUrl.includes('verify') || targetUrl.includes('@') ? 'likely_phishing' : 'likely_legitimate',
          risk_level: targetUrl.includes('secure') || targetUrl.includes('verify') ? 'high' : 'low',
          risk_score: targetUrl.includes('secure') || targetUrl.includes('verify') ? 85 : 12,
          confidence: 94.5,
          summary: targetUrl.includes('secure') || targetUrl.includes('verify')
            ? 'PhishGuard AI evaluated this link as HIGH RISK (85/100). Critical structural indicators were detected including suspicious domain keywords and prefix-suffix hyphens.'
            : 'PhishGuard AI evaluated this link as LOW RISK (12/100). Standard HTTPS protocol and standard domain length were verified.',
          risk_indicators: targetUrl.includes('secure') || targetUrl.includes('verify')
            ? [
                { name: 'Suspicious Domain Keywords', severity: 'HIGH', description: 'Domain contains sensitive authentication keywords (e.g., login, verify, secure).', detected: true },
                { name: 'Hyphenated Domain Structure', severity: 'MEDIUM', description: 'Domain contains hyphens (-) used to spoof trusted brands.', detected: true }
              ]
            : [],
          phishing_techniques: targetUrl.includes('secure') || targetUrl.includes('verify')
            ? [
                { technique: 'Credential-Themed URL', severity: 'high', description: 'Sensitive authentication terms found in URL.', evidence: 'Keywords: verify, login' }
              ]
            : [],
          trust_analysis: {
            https: targetUrl.startsWith('https'),
            domain_structure: 'Standard Domain Structure',
            trust_indicators: ['HTTPS protocol enabled'],
            warnings: targetUrl.startsWith('https') ? ['Note: HTTPS does not guarantee site safety'] : ['Insecure HTTP protocol']
          },
          heuristic_analysis: {
            url_structure: { scheme: targetUrl.startsWith('https') ? 'https' : 'http', hostname: 'example.com', path: '/login', query: '' },
            domain_analysis: { is_ip_address: false, subdomain_count: 0 }
          },
          analyzed_features: {
            url_length: { raw_value: targetUrl.length, extracted_feature: targetUrl.length > 54 ? 1 : -1, description: 'URL Length' },
            having_ip_address: { raw_value: 'No', extracted_feature: -1, description: 'IP Address' },
            https_token: { raw_value: targetUrl.startsWith('https') ? 'Yes' : 'No', extracted_feature: targetUrl.startsWith('https') ? -1 : 1, description: 'HTTPS Scheme' }
          },
          model: { name: 'Random Forest Classifier', feature_count: 30 }
        };
        setResult(mockDemoData);
        saveToHistory(mockDemoData);
      } else {
        setError(err.message || 'An unexpected error occurred during URL analysis.');
      }
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleRestoreScan = (scanData) => {
    setResult(scanData);
    setCompareScan(null);
    setUrl(scanData.url);
    setActiveTab('home');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleCompareScan = (pastScanData) => {
    setCompareScan(pastScanData);
    window.scrollTo({ top: 400, behavior: 'smooth' });
  };

  return (
    <div className="app-shell">
      {/* Navbar Header */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        isDemoMode={isDemoMode}
        setIsDemoMode={setIsDemoMode}
      />

      <main className="main-content">
        {activeTab === 'home' && (
          <>
            {/* Hero Section */}
            <section className="hero-section">
              <h1 className="hero-headline">Detect Phishing Before It Tricks You</h1>
              <p className="hero-subtitle">
                Analyze suspicious URLs using machine learning and receive an explainable risk assessment.
              </p>

              {/* URL Input Component */}
              <UrlInput
                url={url}
                setUrl={setUrl}
                onScan={handleScan}
                isAnalyzing={isAnalyzing}
              />
            </section>

            {/* Pipeline Visualizer (Requirement 11) */}
            {!isAnalyzing && !result && <PipelineVisualizer />}

            {/* Loading Animation */}
            {isAnalyzing && <LoadingState />}

            {/* Error Message */}
            {!isAnalyzing && error && <ErrorMessage message={error} />}

            {/* Comparison View Modal/Panel (Requirement 13) */}
            {compareScan && result && (
              <ScanComparison
                currentScan={result}
                compareScan={compareScan}
                onClose={() => setCompareScan(null)}
              />
            )}

            {/* Analysis Results */}
            {!isAnalyzing && result && (
              <section className="results-wrapper">
                <RiskResult result={result} />
                <RiskIndicator indicators={result.risk_indicators} />
                <FeatureSummary features={result.analyzed_features} />
              </section>
            )}

            {/* Client-Side Scan History (Requirement 12) */}
            <RecentScans
              history={history}
              onClearHistory={handleClearHistory}
              onRestoreScan={handleRestoreScan}
              onCompareScan={result ? handleCompareScan : null}
            />
          </>
        )}

        {activeTab === 'insights' && <ModelInsights />}
        {activeTab === 'how-it-works' && <HowItWorks />}
        {activeTab === 'about' && <AboutSection />}
      </main>

      {/* Footer */}
      <footer className="footer">
        <p>PhishGuard AI • PSN013 Real-Time AI Phishing Detection System</p>
      </footer>
    </div>
  );
}

export default App;
