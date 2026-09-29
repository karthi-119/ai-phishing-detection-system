/**
 * API Service module for PhishGuard AI frontend.
 * Communicates with FastAPI backend POST /api/predict and GET /api/model/insights endpoints.
 */

const API_BASE_URL = 'http://localhost:8000';

/**
 * Sends URL to backend API for phishing analysis and risk assessment.
 * 
 * @param {string} url - Target URL string to analyze.
 * @returns {Promise<Object>} Backend prediction response object.
 */
export async function analyzeUrl(url) {
  if (!url || typeof url !== 'string' || !url.trim()) {
    throw new Error('Please enter a valid URL.');
  }

  const endpoint = `${API_BASE_URL}/api/predict`;

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: url.trim() }),
    });

    const data = await response.json();

    if (!response.ok) {
      const errorMsg = data.detail || data.error || 'URL analysis failed. Please try again.';
      throw new Error(errorMsg);
    }

    return data;
  } catch (err) {
    if (err.name === 'TypeError' && err.message.includes('Fetch')) {
      throw new Error('Unable to connect to PhishGuard AI server. Please verify FastAPI backend is running on http://localhost:8000.');
    }
    throw err;
  }
}

/**
 * Fetches trained model insights and feature importances from backend.
 * 
 * @returns {Promise<Object>} Model insights JSON object.
 */
export async function getModelInsights() {
  const endpoint = `${API_BASE_URL}/api/model/insights`;

  try {
    const response = await fetch(endpoint);
    if (!response.ok) {
      throw new Error('Failed to load model insights from backend.');
    }
    return await response.json();
  } catch (err) {
    console.warn('Could not fetch model insights:', err);
    return null;
  }
}
