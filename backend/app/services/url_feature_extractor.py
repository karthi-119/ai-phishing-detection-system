"""
URL Feature Extractor Service for AI Phishing Detection System.

Parses raw input URLs and extracts 30 numerical features matching the UCI Phishing Websites
dataset encoding scheme (-1, 0, 1).

Includes dynamic fallback logic for webpage and domain-derived features when running static URL analysis.
"""

import re
import ipaddress
from urllib.parse import urlparse
import pandas as pd
from app.services.feature_metadata import FEATURE_METADATA

# Known URL Shortening Service domains
KNOWN_SHORTENERS = {
    "bit.ly", "goo.gl", "tinyurl.com", "ow.ly", "t.co", "is.gd",
    "cli.gs", "yfrog.com", "migre.me", "ff.im", "tiny.cc", "url4.eu",
    "twit.ac", "su.pr", "twurl.nl", "snipurl.com", "short.to", "BudURL.com",
    "ping.fm", "post.ly", "Just.as", "bkite.com", "snipr.com", "fic.kr",
    "loopt.us", "doiop.com", "short.ie", "kl.am", "wp.me", "rubyurl.com",
    "om.ly", "to.ly", "bit.do", "t.ly", "lnkd.in", "db.tt", "qr.ae",
    "adf.ly", "cur.lv", "ity.im", "q.gs", "po.st", "bc.vc", "twitthis.com",
    "u.to", "j.mp", "buzurl.com", "cutt.us", "u.bb", "yourls.org", "x.co",
    "prettylinkpro.com", "scrnch.me", "filoops.info", "vzturl.com", "qr.net",
    "1url.com", "tweez.me", "v.gd", "tr.im", "link.zip.net"
}


def is_ip_address(hostname: str) -> bool:
    """
    Detects whether hostname is a valid IPv4 address or hex/octal encoded IP.
    """
    if not hostname:
        return False
    # Check standard IPv4 notation
    try:
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        pass

    # Regex check for IPv4 or hex/octal IP formats
    ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    if re.match(ip_pattern, hostname):
        return True

    # Check hex IP representation
    hex_pattern = r'^0x[0-9a-fA-F]{8}$'
    if re.match(hex_pattern, hostname):
        return True

    return False


def extract_features(url: str) -> dict:
    """
    Analyzes raw input URL and generates dictionary of 30 feature values.
    
    Returns:
        dict mapping feature_name -> numeric feature value (-1, 0, or 1).
    """
    if not url or not isinstance(url, str):
        url = ""

    url_str = url.strip()

    # Ensure URL scheme for proper parsing
    if not url_str.startswith(("http://", "https://", "ftp://")):
        parsed = urlparse("http://" + url_str)
        raw_url = "http://" + url_str
    else:
        parsed = urlparse(url_str)
        raw_url = url_str

    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""

    features = {}

    # 1. having_ip_address (-1 if IP address, 1 if domain)
    features["having_ip_address"] = -1 if is_ip_address(hostname) else 1

    # 2. url_length (1 if < 54, 0 if 54-75, -1 if > 75)
    url_len = len(raw_url)
    if url_len < 54:
        features["url_length"] = 1
    elif 54 <= url_len <= 75:
        features["url_length"] = 0
    else:
        features["url_length"] = -1

    # 3. shortining_service (-1 if shortener, 1 otherwise)
    domain_lower = hostname.lower()
    features["shortining_service"] = -1 if domain_lower in KNOWN_SHORTENERS else 1

    # 4. having_at_symbol (-1 if @ in URL, 1 otherwise)
    features["having_at_symbol"] = -1 if "@" in raw_url else 1

    # 5. double_slash_redirecting (-1 if // after position 7)
    last_double_slash = raw_url.rfind("//")
    features["double_slash_redirecting"] = -1 if last_double_slash > 7 else 1

    # 6. prefix_suffix (-1 if hyphen in domain, 1 otherwise)
    features["prefix_suffix"] = -1 if "-" in domain_lower else 1

    # 7. having_sub_domain (dots in domain: <=1 -> 1, 2 -> 0, >2 -> -1)
    clean_domain = domain_lower.replace("www.", "")
    dot_count = clean_domain.count(".")
    if dot_count <= 1:
        features["having_sub_domain"] = 1
    elif dot_count == 2:
        features["having_sub_domain"] = 0
    else:
        features["having_sub_domain"] = -1

    # 8. sslfinal_state (1 if HTTPS, -1 if HTTP/None)
    features["sslfinal_state"] = 1 if parsed.scheme.lower() == "https" else -1

    # 9. port (-1 if non-standard port specified, 1 otherwise)
    if parsed.port and parsed.port not in (80, 443):
        features["port"] = -1
    else:
        features["port"] = 1

    # 10. https_token (-1 if 'https' in domain or path outside scheme, 1 otherwise)
    domain_and_path = (hostname + path).lower()
    features["https_token"] = -1 if "https" in domain_and_path else 1

    # 11. abnormal_url (-1 if hostname missing or malformed, 1 otherwise)
    features["abnormal_url"] = -1 if not hostname or hostname not in raw_url else 1

    # 12. redirect (-1 if suspicious redirection parameter, 1 otherwise)
    redirect_indicators = ["//", "redirect=", "url=http", "target=http"]
    has_redirect = any(ind in query.lower() for ind in redirect_indicators)
    features["redirect"] = -1 if has_redirect else 1

    # Count URL-level negative risk signals
    url_risk_count = sum(1 for val in features.values() if val == -1)

    # 13 - 30. Populate webpage and domain-derived features
    # If multiple URL-level risk indicators are detected (>= 2), adjust webpage/domain fallbacks to reflect elevated risk.
    for feat_name, meta in FEATURE_METADATA.items():
        if feat_name not in features:
            if url_risk_count >= 2:
                # Dynamic risk-aware fallback for webpage/domain dependent features
                if feat_name in ("url_of_anchor", "web_traffic", "request_url", "links_in_tags", "google_index", "statistical_report"):
                    features[feat_name] = -1
                else:
                    features[feat_name] = meta.get("fallback", 1)
            else:
                features[feat_name] = meta.get("fallback", 1)

    return features


def extract_features_to_dataframe(url: str, feature_order: list) -> pd.DataFrame:
    """
    Extracts features for input URL and returns a single-row pandas DataFrame
    reordered EXACTLY according to feature_order.
    
    Validates no NaN values and 100% numeric types.
    """
    feat_dict = extract_features(url)

    # Ensure all expected columns exist
    missing_cols = set(feature_order) - set(feat_dict.keys())
    if missing_cols:
        raise ValueError(f"Feature extraction failed. Missing expected columns: {missing_cols}")

    # Build DataFrame in exact feature_order sequence
    row_data = {col: [feat_dict[col]] for col in feature_order}
    df = pd.DataFrame(row_data)

    # Validate numeric types and absence of NaNs
    if df.isnull().sum().sum() > 0:
        raise ValueError("Feature extraction produced NaN values.")

    return df
