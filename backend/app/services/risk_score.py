"""
AI Risk Scoring Engine for AI Phishing Detection System.

Computes a deterministic integer AI Risk Score (0-100) combining:
1. Model evidence (Random Forest prediction probability)
2. URL structural heuristic evidence
3. Phishing technique severity boosts

Categorizes score into 4 transparent risk levels:
- 0–29   ➜ LOW
- 30–59  ➜ MEDIUM
- 60–79  ➜ HIGH
- 80–100 ➜ CRITICAL
"""

from typing import Tuple, List, Dict, Any


def calculate_risk_score(
    phishing_prob: float,
    indicators: List[Dict[str, Any]],
    phishing_techniques: List[Dict[str, Any]] = None,
    heuristics: Dict[str, Any] = None
) -> Tuple[int, str]:
    """
    Calculates deterministic AI Risk Score (0-100) and transparent risk level.
    
    Args:
        phishing_prob: Phishing probability output from model predict_proba (0.0 to 1.0).
        indicators: List of detected structured risk indicator dictionaries.
        phishing_techniques: List of detected phishing technique dictionaries.
        heuristics: Output dictionary from analyze_url_heuristics().
        
    Returns:
        Tuple of (risk_score: int, risk_level: str)
    """
    phishing_techniques = phishing_techniques or []
    heuristics = heuristics or {}

    # 1. Base ML Probability score (max 65 points)
    ml_contribution = phishing_prob * 65.0

    # 2. Risk Indicators contribution (max 20 points)
    high_ind_count = sum(1 for ind in indicators if ind.get("severity") == "high")
    med_ind_count = sum(1 for ind in indicators if ind.get("severity") == "medium")
    indicator_contribution = min(20.0, (high_ind_count * 8.0) + (med_ind_count * 4.0))

    # 3. Phishing Techniques contribution (max 20 points)
    high_tech_count = sum(1 for t in phishing_techniques if t.get("severity") == "high")
    med_tech_count = sum(1 for t in phishing_techniques if t.get("severity") == "medium")
    tech_contribution = min(20.0, (high_tech_count * 9.0) + (med_tech_count * 4.5))

    # Total raw score sum
    raw_score = int(round(ml_contribution + indicator_contribution + tech_contribution))

    # Reasonable caps:
    # A single weak indicator/technique without ML support cannot trigger High/Critical
    has_high_severity = (high_ind_count > 0) or (high_tech_count > 0)
    if not has_high_severity and phishing_prob < 0.50:
        raw_score = min(59, raw_score)

    # Clamp bounded score strictly between 0 and 100
    risk_score = max(0, min(100, raw_score))

    # Transparent Risk Level mapping
    if risk_score >= 80 or (phishing_prob >= 0.75 and has_high_severity):
        risk_level = "critical"
        risk_score = max(80, risk_score)
    elif risk_score >= 60 or (phishing_prob >= 0.50) or has_high_severity:
        risk_level = "high"
        risk_score = max(60, min(79, risk_score))
    elif risk_score >= 30 or len(indicators) > 0 or len(phishing_techniques) > 0:
        risk_level = "medium"
        risk_score = max(30, min(59, risk_score))
    else:
        risk_level = "low"
        risk_score = min(29, risk_score)

    return risk_score, risk_level
