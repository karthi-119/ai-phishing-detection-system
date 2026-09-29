"""
Phishing Technique Classifier Service for PhishGuard AI.

Classifies URL heuristics and feature extraction findings into structured
phishing techniques with severity levels, explanations, and evidence strings.
"""

from typing import Dict, Any, List


def classify_phishing_techniques(heuristics: Dict[str, Any], feat_dict: Dict[str, Any], url: str) -> List[Dict[str, Any]]:
    """
    Evaluates heuristic findings and raw feature extraction dictionary to identify
    specific phishing attack techniques present in the URL.
    
    Args:
        heuristics: Output dictionary from analyze_url_heuristics().
        feat_dict: Extracted 30-feature dictionary.
        url: Raw user-submitted URL string.
        
    Returns:
        List of technique objects containing technique, severity, description, and evidence.
    """
    techniques: List[Dict[str, Any]] = []

    domain_info = heuristics.get("domain_analysis", {})
    struct_info = heuristics.get("url_structure", {})
    kw_info = heuristics.get("keyword_analysis", {})
    obf_info = heuristics.get("obfuscation_analysis", {})
    redir_info = heuristics.get("redirect_analysis", {})

    # 1. IP-Based URL Technique
    if domain_info.get("is_ip_address"):
        techniques.append({
            "technique": "IP-Based URL",
            "severity": "high",
            "description": "The URL uses a raw IP address instead of a registered domain name to bypass domain reputation checks.",
            "evidence": f"Raw IP address used as host: {struct_info.get('hostname')}"
        })

    # 2. URL Shortening Technique
    if domain_info.get("is_shortener"):
        techniques.append({
            "technique": "URL Shortening",
            "severity": "high",
            "description": "The URL uses a public shortening service to hide the true destination domain from users.",
            "evidence": f"Known shortener domain: {struct_info.get('hostname')}"
        })

    # 3. URL Obfuscation Technique (@ symbol or encoded separators)
    if struct_info.get("has_at_symbol") or obf_info.get("has_encoded_separators"):
        evidence_list = []
        if struct_info.get("has_at_symbol"):
            evidence_list.append("@ symbol present before hostname")
        if obf_info.get("has_encoded_separators"):
            evidence_list.append("encoded separators in path/query")
        
        techniques.append({
            "technique": "URL Obfuscation",
            "severity": "high",
            "description": "The URL uses obfuscation techniques like user-info @ symbols or encoded path separators to mask the true destination.",
            "evidence": ", ".join(evidence_list)
        })

    # 4. Excessive Subdomains Technique
    sub_count = domain_info.get("subdomain_count", 0)
    if sub_count >= 3:
        techniques.append({
            "technique": "Excessive Subdomains",
            "severity": "medium",
            "description": "The URL contains multiple subdomain layers designed to mimic legitimate brand domain structures.",
            "evidence": f"{sub_count} subdomain levels detected in hostname"
        })

    # 5. Credential-Themed URL Technique
    cred_kws = kw_info.get("credential_keywords_found", [])
    if cred_kws:
        techniques.append({
            "technique": "Credential-Themed URL",
            "severity": "high" if any(k in ["login", "verify", "password", "bank"] for k in cred_kws) else "medium",
            "description": "The URL contains sensitive authentication or financial keywords commonly used in phishing lure links.",
            "evidence": f"Auth keywords found: {', '.join(cred_kws[:4])}"
        })

    # 6. Redirect Manipulation Technique
    redir_params = redir_info.get("detected_redirect_params", [])
    if redir_params:
        techniques.append({
            "technique": "Redirect Manipulation",
            "severity": "medium",
            "description": "The URL contains parameters commonly associated with open redirects, which can forward users to malicious sites.",
            "evidence": f"Redirect parameter keys: {', '.join(redir_params)}"
        })

    # 7. Suspicious Domain Structure (Hyphenated, Punycode, or Numeric-Heavy)
    domain_flags = []
    if domain_info.get("has_hyphen"):
        domain_flags.append("hyphenated domain")
    if domain_info.get("is_punycode"):
        domain_flags.append("punycode (xn--) IDN encoding")
    if domain_info.get("is_numeric_heavy"):
        domain_flags.append("numeric-heavy hostname")

    if domain_flags:
        techniques.append({
            "technique": "Suspicious Domain",
            "severity": "medium",
            "description": "The domain name exhibits typosquatting or brand spoofing characteristics.",
            "evidence": f"Domain features: {', '.join(domain_flags)}"
        })

    # 8. Missing HTTPS / Insecure Scheme Technique
    if struct_info.get("scheme") == "http":
        techniques.append({
            "technique": "Missing HTTPS",
            "severity": "medium",
            "description": "The URL uses unencrypted HTTP communication, making transmitted data susceptible to interception.",
            "evidence": "Insecure http:// scheme used instead of https://"
        })

    # 9. Suspicious Query Parameters / Obfuscated Encoding
    if obf_info.get("has_excessive_encoding") or obf_info.get("is_long_query"):
        techniques.append({
            "technique": "Suspicious Encoding",
            "severity": "low",
            "description": "The URL uses excessive percent encoding or a suspiciously long query string.",
            "evidence": f"Percent-encoding count: {obf_info.get('percent_encoding_count')}, long query: {obf_info.get('is_long_query')}"
        })

    # 10. Brand / Account-Themed Path Technique
    path_kws = kw_info.get("path_keywords_found", [])
    if path_kws and not any(t["technique"] == "Credential-Themed URL" for t in techniques):
        techniques.append({
            "technique": "Brand/Account-Themed Path",
            "severity": "medium",
            "description": "The URL path includes account or verification paths to simulate legitimate portal structures.",
            "evidence": f"Path terms: {', '.join(path_kws[:3])}"
        })

    return techniques
