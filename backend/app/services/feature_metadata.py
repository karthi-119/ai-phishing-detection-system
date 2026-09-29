"""
Feature Metadata Registry for AI Phishing Detection System.

Categorizes and documents all 30 features defined in the UCI Phishing Websites Dataset (ID: 327).
Distinguishes between:
1. URL-derived features (extracted statically directly from raw URL strings).
2. Webpage-derived features (require fetching/parsing HTML/JS/DOM content).
3. Domain/WHOIS-derived features (require external WHOIS or DNS database lookup).

To prevent Server-Side Request Forgery (SSRF) security risks and maintain fast real-time response,
webpage and domain-derived features utilize documented neutral fallback values (0 or 1).
"""

FEATURE_METADATA = {
    "having_ip_address": {
        "source": "URL-derived",
        "description": "Checks whether the hostname uses an IPv4 address or hex/octal IP instead of a domain name.",
        "values": {-1: "IP address present (Phishing)", 1: "Standard domain name (Legitimate)"}
    },
    "url_length": {
        "source": "URL-derived",
        "description": "Calculates total character length of the URL.",
        "values": {1: "< 54 chars (Legitimate)", 0: "54 - 75 chars (Suspicious)", -1: "> 75 chars (Phishing)"}
    },
    "shortining_service": {
        "source": "URL-derived",
        "description": "Detects whether the URL uses a known shortening service (e.g., bit.ly, tinyurl, t.co).",
        "values": {-1: "URL shortener detected (Phishing)", 1: "Standard domain (Legitimate)"}
    },
    "having_at_symbol": {
        "source": "URL-derived",
        "description": "Checks for presence of '@' symbol in URL.",
        "values": {-1: "'@' symbol present (Phishing)", 1: "No '@' symbol (Legitimate)"}
    },
    "double_slash_redirecting": {
        "source": "URL-derived",
        "description": "Checks for '//' redirection occurring after position 7 in URL.",
        "values": {-1: "Double slash redirection present (Phishing)", 1: "Clean protocol slash (Legitimate)"}
    },
    "prefix_suffix": {
        "source": "URL-derived",
        "description": "Checks for hyphens '-' separating domain prefixes or suffixes.",
        "values": {-1: "Hyphen in domain (Phishing)", 1: "No hyphen in domain (Legitimate)"}
    },
    "having_sub_domain": {
        "source": "URL-derived",
        "description": "Calculates the number of subdomain levels in the hostname.",
        "values": {1: "<= 1 subdomain (Legitimate)", 0: "2 subdomains (Suspicious)", -1: "> 2 subdomains (Phishing)"}
    },
    "sslfinal_state": {
        "source": "URL-derived",
        "description": "Checks HTTPS protocol scheme usage.",
        "values": {1: "HTTPS protocol used (Legitimate)", -1: "HTTP protocol / No SSL (Phishing)"}
    },
    "domain_registration_length": {
        "source": "Domain/WHOIS-derived",
        "fallback": -1,
        "description": "Domain registration period length from WHOIS database.",
        "values": {-1: "Short registration / Fallback", 1: "Long registration"}
    },
    "favicon": {
        "source": "Webpage-derived",
        "fallback": 1,
        "description": "Favicon icon loaded from external domain.",
        "values": {1: "Loaded from same domain / Fallback", -1: "Loaded from external domain"}
    },
    "port": {
        "source": "URL-derived",
        "description": "Detects explicit non-standard port numbers in host string (e.g., :8080).",
        "values": {-1: "Non-standard port open (Phishing)", 1: "Standard port / Unspecified (Legitimate)"}
    },
    "https_token": {
        "source": "URL-derived",
        "description": "Detects 'https' token inserted into domain name or path outside protocol scheme.",
        "values": {-1: "'https' token in domain (Phishing)", 1: "Clean protocol usage (Legitimate)"}
    },
    "request_url": {
        "source": "Webpage-derived",
        "fallback": 0,
        "description": "% of external request objects (img, video) in HTML.",
        "values": {1: "< 22% external", 0: "22% - 61% external / Fallback", -1: "> 61% external"}
    },
    "url_of_anchor": {
        "source": "Webpage-derived",
        "fallback": 0,
        "description": "% of anchor <a> tags pointing to different domains.",
        "values": {1: "< 31% external", 0: "31% - 67% external / Fallback", -1: "> 67% external"}
    },
    "links_in_tags": {
        "source": "Webpage-derived",
        "fallback": 0,
        "description": "% of links in <Meta>, <Script>, and <Link> tags pointing to external domains.",
        "values": {1: "< 17% external", 0: "17% - 81% external / Fallback", -1: "> 81% external"}
    },
    "sfh": {
        "source": "Webpage-derived",
        "fallback": -1,
        "description": "Server Form Handler action attribute status.",
        "values": {-1: "Empty/about:blank form handler / Fallback", 1: "Valid form handler"}
    },
    "submitting_to_email": {
        "source": "Webpage-derived",
        "fallback": 1,
        "description": "Form submission handler submitting directly to mailto: or email script.",
        "values": {-1: "Submits to email", 1: "Standard web submission / Fallback"}
    },
    "abnormal_url": {
        "source": "URL-derived",
        "description": "Checks whether hostname is missing or URL structure is malformed.",
        "values": {-1: "Abnormal URL structure (Phishing)", 1: "Standard URL structure (Legitimate)"}
    },
    "redirect": {
        "source": "URL-derived",
        "description": "Checks for URL redirection query parameters (e.g. redirect=, url=http).",
        "values": {-1: "Multiple redirects indicated (Phishing)", 0: "Single redirect (Suspicious)", 1: "No redirection (Legitimate)"}
    },
    "on_mouseover": {
        "source": "Webpage-derived",
        "fallback": 1,
        "description": "JavaScript mouseover altering status bar link text.",
        "values": {-1: "Status bar modified", 1: "Clean status bar / Fallback"}
    },
    "rightclick": {
        "source": "Webpage-derived",
        "fallback": 1,
        "description": "Disabled right-click context menu via JavaScript.",
        "values": {-1: "Right-click disabled", 1: "Right-click allowed / Fallback"}
    },
    "popupwindow": {
        "source": "Webpage-derived",
        "fallback": 1,
        "description": "Popup windows containing input fields.",
        "values": {-1: "Popup with input fields", 1: "No popup input / Fallback"}
    },
    "iframe": {
        "source": "Webpage-derived",
        "fallback": 1,
        "description": "Use of invisible <iframe> HTML elements.",
        "values": {-1: "Invisible iframe present", 1: "No invisible iframe / Fallback"}
    },
    "age_of_domain": {
        "source": "Domain/WHOIS-derived",
        "fallback": -1,
        "description": "Domain age in WHOIS database.",
        "values": {-1: "< 6 months age / Fallback", 1: ">= 6 months age"}
    },
    "dnsrecord": {
        "source": "Domain/WHOIS-derived",
        "fallback": 1,
        "description": "Existence of valid DNS host record.",
        "values": {-1: "No DNS record", 1: "DNS record exists / Fallback"}
    },
    "web_traffic": {
        "source": "Domain/WHOIS-derived",
        "fallback": 0,
        "description": "Alexa / SimilarWeb web traffic ranking.",
        "values": {1: "< 100,000 rank", 0: "> 100,000 rank / Fallback", -1: "No traffic / Unranked"}
    },
    "page_rank": {
        "source": "Domain/WHOIS-derived",
        "fallback": -1,
        "description": "PageRank authority score.",
        "values": {-1: "Low PageRank / Fallback", 1: "High PageRank"}
    },
    "google_index": {
        "source": "Domain/WHOIS-derived",
        "fallback": 1,
        "description": "Indexed status in Google search engine.",
        "values": {-1: "Not indexed", 1: "Indexed in Google / Fallback"}
    },
    "links_pointing_to_page": {
        "source": "Domain/WHOIS-derived",
        "fallback": 0,
        "description": "Number of external backlinks pointing to page.",
        "values": {1: "> 2 backlinks", 0: "1 - 2 backlinks / Fallback", -1: "0 backlinks"}
    },
    "statistical_report": {
        "source": "Domain/WHOIS-derived",
        "fallback": 1,
        "description": "Matches known phishing IP / domain blocklists.",
        "values": {-1: "Found on blocklist", 1: "Not on blocklist / Fallback"}
    }
}
