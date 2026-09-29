"""
Explainable AI Summary Service for AI Phishing Detection System.

Generates concise, non-exaggerated human-readable summary sentences based strictly
on actual model classification and detected empirical risk indicators.
"""

from typing import List, Dict, Any


def generate_explanation(prediction: str, indicators: List[Dict[str, Any]]) -> str:
    """
    Generates concise explanation string based on prediction and indicators.
    
    Args:
        prediction: 'likely_phishing' or 'likely_legitimate'
        indicators: List of structured indicator objects.
        
    Returns:
        Summary explanation string.
    """
    if not indicators or len(indicators) == 0:
        if prediction == "likely_phishing":
            return "Structural patterns in the URL align with known phishing characteristics."
        return "No major phishing-related URL indicators were detected by the current model."

    names = [ind.get("name", "") for ind in indicators if ind.get("name")]
    high_count = sum(1 for ind in indicators if ind.get("severity") == "high")

    if prediction == "likely_phishing":
        if high_count >= 2:
            return f"Critical risk detected: Multiple severe indicators found ({', '.join(names[:2])})."
        elif len(names) >= 2:
            return f"Several characteristics associated with phishing were detected, including {names[0].lower()} and {names[1].lower()}."
        else:
            return f"Phishing indicators detected: {names[0]}."
    else:
        if len(names) > 0:
            return f"Minor URL signals noted ({names[0]}), but overall model evaluation remains likely legitimate."
        return "No major phishing-related URL indicators were detected by the current model."
