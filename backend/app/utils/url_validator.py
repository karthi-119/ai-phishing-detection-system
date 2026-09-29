"""
Robust Server-Side URL Validation and Sanitization Utility.

Ensures strict URL validation, protocol whitelisting, length constraints,
and SSRF security checks prior to feature extraction or model inference.
"""

from urllib.parse import urlparse
import re
from app.config import MAX_URL_LENGTH

# Whitelisted schemes allowed for analysis
ALLOWED_SCHEMES = {"http", "https"}

# Forbidden hostnames and private/cloud-metadata targets (SSRF Protection)
FORBIDDEN_HOSTS = {
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "::1",
    "169.254.169.254",  # AWS/GCP Metadata endpoint
    "metadata.google.internal"
}


def validate_and_normalize_url(url: str) -> str:
    """
    Validates, sanitizes, and normalizes a target URL.
    
    Args:
        url: Raw user-submitted URL string.
        
    Returns:
        Normalized URL string.
        
    Raises:
        ValueError: If URL violates validation or SSRF security rules.
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL parameter cannot be empty or blank.")

    cleaned_url = url.strip()

    # 1. Reject empty or whitespace-only strings
    if not cleaned_url:
        raise ValueError("URL parameter cannot be empty or blank.")

    # 2. Reject excessively long URLs
    if len(cleaned_url) > MAX_URL_LENGTH:
        raise ValueError(f"URL exceeds maximum allowed length of {MAX_URL_LENGTH} characters.")

    # 3. Detect and extract scheme explicitly
    if "://" in cleaned_url:
        scheme = cleaned_url.split("://", 1)[0].lower()
        raw_to_parse = cleaned_url
    elif ":" in cleaned_url and not cleaned_url.startswith("http"):
        scheme = cleaned_url.split(":", 1)[0].lower()
        raw_to_parse = cleaned_url
    else:
        scheme = "http"
        raw_to_parse = "http://" + cleaned_url

    # Enforce protocol scheme whitelist (Task 1)
    if scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported protocol '{scheme}'. Only 'http://' and 'https://' URLs are accepted.")

    # 4. Parse URL structure
    try:
        parsed = urlparse(raw_to_parse)
    except Exception as e:
        raise ValueError(f"Malformed URL structure: {str(e)}")

    hostname = (parsed.hostname or "").lower()

    # 5. Reject missing hostname
    if not hostname:
        raise ValueError("URL is missing a valid domain name or hostname.")

    # 6. Hostname structure validation (alphanumeric, hyphens, dots)
    if not re.match(r'^[a-zA-Z0-9\.\-_]+$', hostname):
        raise ValueError("Hostname contains invalid or malformed characters.")

    # 7. SSRF Security Check: Reject localhost, loopback, private IPs & cloud metadata
    if hostname in FORBIDDEN_HOSTS or hostname.startswith("127.") or hostname.startswith("192.168.") or hostname.startswith("10."):
        raise ValueError("Analysis of internal/private network targets or metadata endpoints is prohibited for security reasons.")

    return raw_to_parse
