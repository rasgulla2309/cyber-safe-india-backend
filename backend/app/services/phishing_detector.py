import re
from urllib.parse import urlparse


SUSPICIOUS_DOMAINS = [
    r"(^|\.)ngrok\.io$",
    r"(^|\.)trycloudflare\.com$",
    r"(^|\.)trycloudflare\.dev$",
    r"(^|\.)localhostrun\.com$",
    r"(^|\.)serveo\.net$",
    r"(^|\.)localtunnel\.me$",
    r"(^|\.)pagekite\.me$",
    r"(^|\.)surge\.sh$",
    r"(^|\.)000webhostapp\.com$",
    r"(^|\.)herokuapp\.com$",
    r"(^|\.)vercel\.app$",
    r"(^|\.)web\.app$",
    r"(^|\.)onrender\.com$",
    r"(^|\.)repl\.co$",
    r"(^|\.)railway\.app$",
    r"(^|\.)fly\.dev$",

    r"(^|\.)grabify\.link$",
    r"(^|\.)grabify\.me$",
    r"(^|\.)iplogger\.org$",
    r"(^|\.)iplogger\.com$",
    r"(^|\.)iplogger\.ru$",
    r"(^|\.)ipgrab\.me$",
    r"(^|\.)2no\.co$",
    r"(^|\.)yip\.sh$",
    r"(^|\.)bmwpo\.ly$",

    r"(^|\.)bit\.ly$",
    r"(^|\.)tinyurl\.com$",
    r"(^|\.)t\.co$",
    r"(^|\.)ow\.ly$",
    r"(^|\.)cutt\.ly$",
    r"(^|\.)rb\.gy$",
    r"(^|\.)shorturl\.at$",

    r"(phish|login|verify|secure|account|bank|update).*",
]

SUSPICIOUS_PATHS = [
    r"/(login|signin|verify|confirm|auth|account|secure|update)",
    r"/(bank|upi|paytm|gpay|google-pay|amazon-pay)",
]

IP_HOST_RE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
HIGH_RISK_SCORE = 70


def _compile(patterns):
    return [re.compile(p, re.IGNORECASE) for p in patterns]


DOMAINS_RX = _compile(SUSPICIOUS_DOMAINS)
PATHS_RX = _compile(SUSPICIOUS_PATHS)


def clean_domain(pattern: str) -> str:
    """
    Convert regex like (^|\\.)grabify\\.link$ → grabify.link
    """
    return (
        pattern
        .replace("(^|\\.)", "")
        .replace("\\.", ".")
        .replace("$", "")
    )


def analyze_url(url: str, reports: int = 0) -> dict:
    score = 0
    matches = []

    parsed = urlparse(url if "://" in url else "https://" + url)
    host = parsed.hostname or ""
    path = parsed.path or "/"
    host_l = host.lower()

    # 1️⃣ Suspicious domains
    for rx in DOMAINS_RX:
        if rx.search(host_l):
            domain = clean_domain(rx.pattern)
            matches.append(f"Known phishing service: {domain}")
            score += 40

    # 2️⃣ IP based URL
    if IP_HOST_RE.match(host_l):
        matches.append("Uses direct IP address instead of domain")
        score += 30

    # 3️⃣ Suspicious paths
    for rx in PATHS_RX:
        if rx.search(path.lower()):
            matches.append("Suspicious login / payment page detected")
            score += 20

    # 4️⃣ Keywords
    for kw in ["verify", "secure", "bank", "login", "account", "pay"]:
        if kw in host_l:
            matches.append(f"Sensitive keyword in domain: {kw}")
            score += 8

    # 5️⃣ Community reports boost
    if reports > 0:
        boost = min(40, reports * 10)
        score += boost
        matches.append(f"Reported by users: {reports} time(s)")

    if score > 100:
        score = 100

    # Risk level
    if score >= HIGH_RISK_SCORE:
        level = "🚫 High Risk"
    elif score >= 35:
        level = "⚠️ Suspected"
    elif score > 0:
        level = "🔎 Low Risk"
    else:
        level = "✅ Safe"

    explain = " | ".join(matches) if matches else "No suspicious patterns detected"

    return {
        "url": url,
        "host": host,
        "score": score,
        "risk_level": level,
        "matches": matches,
        "explain": explain
    }
