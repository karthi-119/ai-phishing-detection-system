"""
Trust Analyzer Service for PhishGuard AI.

Evaluates basic trust-related URL attributes strictly offline without making
network connections or verifying third-party domain reputation databases.
"""

from typing import Dict, Any, List


def analyze_trust_indicators(url: str, feat_dict: Dict[str, Any], heuristics: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates protocol, domain structure, and structural hygiene parameters to form
    a basic trust profile.
    
    Args:
        url: Raw user-submitted URL string.
        feat_dict: Extracted 30-feature dictionary.
        heuristics: Output dictionary from analyze_url_heuristics().
        
    Returns:
        Dictionary containing https (bool), domain_structure (str), trust_indicators (list),
        and warnings (list).
    """
    struct_info = heuristics.get("url_structure", {})
    domain_info = heuristics.get("domain_analysis", {})

    is_https = struct_info.get("scheme") == "https"
    is_ip = domain_info.get("is_ip_address", False)
    is_shortener = domain_info.get("is_shortener", False)
    subdomain_count = domain_info.get("subdomain_count", 0)
    has_hyphen = domain_info.get("has_hyphen", False)

    # Determine domain structure label
    if is_ip:
        domain_structure = "IP Address Hostname"
    elif is_shortener:
        domain_structure = "URL Shortening Service"
    elif subdomain_count >= 3:
        domain_structure = "Subdomain-Heavy Hostname"
    elif has_hyphen:
        domain_structure = "Hyphenated Domain Structure"
    else:
        domain_structure = "Standard Domain Structure"

    trust_indicators: List[str] = []
    warnings: List[str] = []

    # Protocol check
    if is_https:
        trust_indicators.append("HTTPS protocol scheme enabled")
        # Explicit mandatory disclaimer rule: HTTPS != Legitimate
        warnings.append("Note: HTTPS provides encryption but does NOT guarantee domain legitimacy or safety")
    else:
        warnings.append("Insecure HTTP protocol scheme used (data transmitted in plaintext)")

    # Domain structure checks
    if not is_ip:
        trust_indicators.append("Uses registered domain name instead of raw IP address")
    else:
        warnings.append("Raw IP address used as hostname (avoids domain registration checks)")

    if not is_shortener:
        trust_indicators.append("Direct destination URL (no URL shortening service detected)")
    else:
        warnings.append("URL shortener masks true target destination domain")

    if subdomain_count < 3:
        trust_indicators.append(f"Standard subdomain depth ({subdomain_count} subdomains)")
    else:
        warnings.append(f"Excessive subdomain depth ({subdomain_count} subdomains) may simulate trusted portals")

    if has_hyphen:
        warnings.append("Hyphenated domain structure is frequently observed in typosquatting lures")

    return {
        "https": is_https,
        "domain_structure": domain_structure,
        "trust_indicators": trust_indicators,
        "warnings": warnings
    }
