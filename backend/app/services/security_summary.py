"""
Security Summary Generator for PhishGuard AI.

Synthesizes Random Forest inference, URL heuristics, detected phishing techniques,
and trust analysis into a clear, dynamic human-readable security assessment summary.
"""

from typing import Dict, Any, List


def generate_security_summary(
    prediction: str,
    risk_score: int,
    risk_level: str,
    phishing_techniques: List[Dict[str, Any]],
    risk_indicators: List[Dict[str, Any]],
    trust_analysis: Dict[str, Any]
) -> str:
    """
    Generates a dynamic human-readable security explanation summarizing empirical findings.
    
    Args:
        prediction: ML prediction string ('likely_phishing' or 'likely_legitimate').
        risk_score: AI Risk Score integer (0-100).
        risk_level: Transparent risk level string ('low', 'medium', 'high', 'critical').
        phishing_techniques: List of detected phishing technique dictionaries.
        risk_indicators: List of extracted risk indicator dictionaries.
        trust_analysis: Trust analysis dictionary.
        
    Returns:
        Concise, human-readable security summary string.
    """
    tech_names = [t["technique"] for t in phishing_techniques]
    is_phishing = prediction == "likely_phishing"
    is_https = trust_analysis.get("https", False)

    summary_parts: List[str] = []

    # 1. Headline Sentence
    if risk_level == "critical":
        summary_parts.append(f"CRITICAL RISK URL DETECTED (AI Risk Score: {risk_score}/100).")
    elif risk_level == "high":
        summary_parts.append(f"HIGH RISK URL DETECTED (AI Risk Score: {risk_score}/100).")
    elif risk_level == "medium":
        summary_parts.append(f"MODERATE RISK URL DETECTED (AI Risk Score: {risk_score}/100).")
    else:
        summary_parts.append(f"LOW RISK URL based on available URL-level evidence (AI Risk Score: {risk_score}/100).")

    # 2. Key Findings & Techniques Summary
    if tech_names:
        techniques_str = ", ".join(tech_names[:3])
        if len(tech_names) > 3:
            techniques_str += f", and {len(tech_names) - 3} other technique(s)"
        summary_parts.append(f"Analysis flagged active threat patterns including: {techniques_str}.")
    elif is_phishing:
        summary_parts.append("The Random Forest classifier flagged structural features matching trained phishing models.")
    else:
        summary_parts.append("No major suspicious URL indicators or phishing techniques were detected.")

    # 3. Protocol & Contextual Advice
    if not is_https:
        summary_parts.append("The URL uses unencrypted HTTP; avoid entering sensitive credentials.")
    elif is_phishing or risk_level in ["high", "critical"]:
        summary_parts.append("Although HTTPS encryption is present, attackers frequently use HTTPS on phishing sites. Exercise extreme caution.")
    elif risk_level == "low":
        summary_parts.append("Standard HTTPS encryption and direct domain structure were confirmed.")

    return " ".join(summary_parts)
