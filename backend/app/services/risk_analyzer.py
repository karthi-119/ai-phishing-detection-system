"""
Explainable Risk Analyzer Service for AI Phishing Detection System.

Analyzes extracted URL feature values (-1, 0, 1) and generates structured,
human-readable risk indicator objects with severity ratings (high, medium, low).
"""

from typing import List, Dict, Any


def analyze_risk_factors(feat_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Inspects feature dictionary and returns list of structured risk indicator objects.
    
    Args:
        feat_dict: Dictionary of extracted feature names and numeric values.
        
    Returns:
        List of dictionaries: {"name": str, "severity": "high"|"medium"|"low", "description": str, "detected": True}
    """
    indicators = []

    # 1. IP address in domain
    if feat_dict.get("having_ip_address") == -1:
        indicators.append({
            "name": "IP Address in URL",
            "severity": "high",
            "description": "The URL uses an IP address instead of a conventional domain name.",
            "detected": True
        })

    # 2. URL length
    if feat_dict.get("url_length") == -1:
        indicators.append({
            "name": "Excessive URL Length",
            "severity": "medium",
            "description": "The URL string is excessively long (> 75 characters).",
            "detected": True
        })
    elif feat_dict.get("url_length") == 0:
        indicators.append({
            "name": "Suspicious URL Length",
            "severity": "low",
            "description": "The URL length is suspicious (54 to 75 characters).",
            "detected": True
        })

    # 3. URL shortener
    if feat_dict.get("shortining_service") == -1:
        indicators.append({
            "name": "URL Shortening Service",
            "severity": "medium",
            "description": "The URL uses a known URL shortening service (e.g. bit.ly, tinyurl).",
            "detected": True
        })

    # 4. '@' symbol
    if feat_dict.get("having_at_symbol") == -1:
        indicators.append({
            "name": "@ Symbol in URL",
            "severity": "high",
            "description": "The URL contains an '@' symbol which can obscure the real destination host.",
            "detected": True
        })

    # 5. Double slash redirection
    if feat_dict.get("double_slash_redirecting") == -1:
        indicators.append({
            "name": "Double Slash Redirection",
            "severity": "high",
            "description": "The URL contains suspicious double-slash ('//') redirection after protocol scheme.",
            "detected": True
        })

    # 6. Prefix / Suffix hyphen
    if feat_dict.get("prefix_suffix") == -1:
        indicators.append({
            "name": "Domain Hyphen",
            "severity": "medium",
            "description": "Domain name contains a hyphen ('-') commonly used in brand spoofing.",
            "detected": True
        })

    # 7. Subdomains
    if feat_dict.get("having_sub_domain") == -1:
        indicators.append({
            "name": "Excessive Subdomains",
            "severity": "high",
            "description": "Hostname contains multiple subdomain levels (> 2 subdomains).",
            "detected": True
        })
    elif feat_dict.get("having_sub_domain") == 0:
        indicators.append({
            "name": "Suspicious Subdomain Pattern",
            "severity": "medium",
            "description": "Hostname contains a suspicious number of subdomains (2 subdomains).",
            "detected": True
        })

    # 8. SSL / HTTPS protocol state
    if feat_dict.get("sslfinal_state") == -1:
        indicators.append({
            "name": "Insecure HTTP Protocol",
            "severity": "medium",
            "description": "The URL uses non-secure HTTP protocol without SSL/TLS encryption.",
            "detected": True
        })

    # 9. Non-standard port
    if feat_dict.get("port") == -1:
        indicators.append({
            "name": "Non-Standard Port",
            "severity": "low",
            "description": "The URL specifies an explicit non-standard network port.",
            "detected": True
        })

    # 10. HTTPS token in domain
    if feat_dict.get("https_token") == -1:
        indicators.append({
            "name": "HTTPS Token Spoofing",
            "severity": "high",
            "description": "Domain or path contains 'https' token to trick users into trusting a non-SSL site.",
            "detected": True
        })

    # 11. Abnormal URL structure
    if feat_dict.get("abnormal_url") == -1:
        indicators.append({
            "name": "Abnormal URL Structure",
            "severity": "high",
            "description": "URL structure is abnormal or missing standard host components.",
            "detected": True
        })

    # 12. Redirect parameter
    if feat_dict.get("redirect") == -1:
        indicators.append({
            "name": "Redirection Query Parameters",
            "severity": "medium",
            "description": "URL query string contains explicit redirection parameters.",
            "detected": True
        })

    return indicators
