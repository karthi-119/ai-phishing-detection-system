"""
Advanced URL Heuristic Engine for PhishGuard AI.

Performs offline, static string inspection of target URLs to detect
suspicious URL structure, domain characteristics, phishing/credential terms,
obfuscation indicators, and redirect parameters without outbound network calls.
"""

import re
import urllib.parse
from typing import Dict, Any, List

# Target keywords associated with credential theft and account verification
CREDENTIAL_KEYWORDS = [
    "login", "signin", "verify", "verification", "account", "secure",
    "update", "password", "banking", "wallet", "payment", "recovery",
    "authentication", "confirm"
]

# Query parameters commonly used for open redirect manipulation
REDIRECT_PARAMS = [
    "redirect", "redirect_url", "return", "return_url", "next",
    "continue", "target", "destination", "url"
]

# Known URL shortener domains
SHORTENER_DOMAINS = [
    "bit.ly", "goo.gl", "tinyurl.com", "ow.ly", "t.co", "is.gd",
    "buff.ly", "adf.ly", "bit.do", "mcaf.ee", "su.pr"
]


def analyze_url_heuristics(url: str) -> Dict[str, Any]:
    """
    Analyzes target URL string for suspicious structural, lexical, domain,
    obfuscation, and redirect characteristics.
    
    Args:
        url: Raw user-submitted URL string.
        
    Returns:
        Dictionary containing url_structure, domain_analysis, detected_patterns,
        obfuscation_indicators, and redirect_analysis.
    """
    if not url or not isinstance(url, str):
        url = ""

    parsed = urllib.parse.urlparse(url)
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    # Strip port if present
    hostname = netloc.split(":")[0] if ":" in netloc else netloc
    path = parsed.path
    query = parsed.query

    # Parse query parameters into dictionary
    query_params = urllib.parse.parse_qs(query)
    param_keys = [k.lower() for k in query_params.keys()]

    # 1. URL Structure Analysis
    url_length = len(url)
    path_segments = [seg for seg in path.split("/") if seg]
    path_segment_count = len(path_segments)
    query_param_count = len(query_params)
    has_at_symbol = "@" in url
    has_double_slash_in_path = "//" in path
    has_suspicious_chars = bool(re.search(r'[@~`$<>{}\\]', url))

    # Subdomain count
    domain_parts = hostname.split(".")
    # Remove www prefix if evaluating subdomains
    effective_parts = [p for p in domain_parts if p != "www"]
    subdomain_count = max(0, len(effective_parts) - 2) if len(effective_parts) > 2 else 0

    # 2. Domain Characteristics
    is_ip_address = bool(re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', hostname))
    has_hyphen = "-" in hostname
    is_punycode = "xn--" in hostname.lower()
    is_shortener = hostname.lower() in SHORTENER_DOMAINS

    # Numeric ratio of hostname
    digits_in_hostname = sum(c.isdigit() for c in hostname)
    hostname_alpha_len = len(re.sub(r'[\.\:-]', '', hostname))
    numeric_ratio = (digits_in_hostname / hostname_alpha_len) if hostname_alpha_len > 0 else 0.0
    is_numeric_heavy = numeric_ratio > 0.40 and not is_ip_address

    # 3. Credential & Auth Keyword Detection
    url_lower = url.lower()
    found_credential_keywords = [kw for kw in CREDENTIAL_KEYWORDS if kw in url_lower]

    # Path credential keywords
    path_lower = path.lower()
    found_path_keywords = [kw for kw in CREDENTIAL_KEYWORDS if kw in path_lower]

    # 4. Obfuscation Detection
    percent_encodings = re.findall(r'%[0-9a-fA-F]{2}', url)
    percent_encoding_count = len(percent_encodings)
    has_excessive_encoding = percent_encoding_count > 3
    has_encoded_separators = bool(re.search(r'%(2f|5c|23|3f|3a)', url, re.IGNORECASE))
    is_long_query = len(query) > 50

    # 5. Redirect Parameter Detection
    detected_redirect_params = [p for p in param_keys if p in REDIRECT_PARAMS]
    has_redirect_param = len(detected_redirect_params) > 0

    # Consolidate suspicious patterns summary
    suspicious_patterns: List[str] = []
    if is_ip_address:
        suspicious_patterns.append("IP Address used as hostname")
    if is_shortener:
        suspicious_patterns.append("Known URL Shortening Service used")
    if is_punycode:
        suspicious_patterns.append("Punycode / IDN Internationalized Domain detected")
    if has_at_symbol:
        suspicious_patterns.append("@ symbol present in URL")
    if url_length > 75:
        suspicious_patterns.append(f"Excessive URL length ({url_length} characters)")
    if subdomain_count >= 3:
        suspicious_patterns.append(f"High subdomain depth ({subdomain_count} subdomains)")
    if found_credential_keywords:
        suspicious_patterns.append(f"Credential/Auth keywords present ({', '.join(found_credential_keywords[:3])})")
    if has_redirect_param:
        suspicious_patterns.append(f"Open redirect parameter detected ({', '.join(detected_redirect_params)})")
    if has_encoded_separators or has_excessive_encoding:
        suspicious_patterns.append("URL percent encoding / obfuscation present")

    return {
        "suspicious_patterns": suspicious_patterns,
        "url_structure": {
            "url_length": url_length,
            "scheme": scheme,
            "hostname": hostname,
            "path": path,
            "query": query,
            "path_segment_count": path_segment_count,
            "query_param_count": query_param_count,
            "subdomain_count": subdomain_count,
            "has_at_symbol": has_at_symbol,
            "has_double_slash_in_path": has_double_slash_in_path,
            "has_suspicious_chars": has_suspicious_chars
        },
        "domain_analysis": {
            "is_ip_address": is_ip_address,
            "has_hyphen": has_hyphen,
            "is_punycode": is_punycode,
            "is_shortener": is_shortener,
            "is_numeric_heavy": is_numeric_heavy,
            "subdomain_count": subdomain_count,
            "hostname_length": len(hostname)
        },
        "keyword_analysis": {
            "credential_keywords_found": found_credential_keywords,
            "path_keywords_found": found_path_keywords
        },
        "obfuscation_analysis": {
            "percent_encoding_count": percent_encoding_count,
            "has_excessive_encoding": has_excessive_encoding,
            "has_encoded_separators": has_encoded_separators,
            "is_long_query": is_long_query
        },
        "redirect_analysis": {
            "has_redirect_param": has_redirect_param,
            "detected_redirect_params": detected_redirect_params
        }
    }
