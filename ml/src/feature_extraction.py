"""
URL Feature Extraction Module for Phishing Detection System.

This module will extract lexical, structural, and domain features from raw URLs, including:
- URL length, path length, query parameter length
- Character counts: dots, hyphens, underscores, slashes, '@' symbols, digits
- IP address detection in domain string
- HTTPS protocol usage
- Character entropy and suspicious keyword indicators
"""


def extract_url_features(url: str) -> dict:
    """
    Placeholder function to extract feature dictionary from a single URL string.
    To be implemented in Step 3 during feature engineering.
    """
    raise NotImplementedError("Feature extraction logic will be implemented in Step 3.")
