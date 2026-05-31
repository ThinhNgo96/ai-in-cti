"""Feature extraction helpers shared by training and live prediction.

Keeping extractors here (instead of inside the training script) means the
FastAPI server can re-use the *exact same* logic at inference time.
"""
from __future__ import annotations

import math
import re
from urllib.parse import urlparse


# 1) Phishing URL features
SUSPICIOUS_KEYWORDS = (
    "login", "verify", "secure", "account", "update", "bank", "free",
    "bonus", "gift", "confirm", "signin", "wallet", "paypal", "support",
)
SHORTENERS = ("bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd")
PHISH_FEATURES = [
    "num_dots", "num_hyphens", "num_at", "num_question", "num_equals",
    "num_digits", "num_subdomains", "has_ip", "is_shortener",
    "suspicious_kw_count", "tld_suspicious",
]
SUSPICIOUS_TLDS = {"zip", "mov", "xyz", "top", "tk", "ml", "ga", "cf", "gq", "click", "country"}


def extract_url_features(url: str) -> dict:
    url = (url or "").strip()
    if "://" not in url:
        url = "http://" + url
    try:
        parsed = urlparse(url)
        host = parsed.hostname or ""
        path = parsed.path or ""
        scheme = parsed.scheme
    except Exception:
        # Fallback for malformed/invalid URLs (e.g. invalid IPv6 URLs with brackets)
        scheme = "http"
        host = ""
        path = ""
        if "://" in url:
            try:
                rest = url.split("://", 1)[1]
                if "/" in rest:
                    host, path_part = rest.split("/", 1)
                    path = "/" + path_part
                else:
                    host = rest
            except Exception:
                pass

    digits = sum(c.isdigit() for c in url)
    tld = host.rsplit(".", 1)[-1].lower() if "." in host else ""
    has_ip = bool(re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host))
    return {
        "url_length": len(url),
        "hostname_length": len(host),
        "path_length": len(path),
        "num_dots": url.count("."),
        "num_hyphens": url.count("-"),
        "num_at": url.count("@"),
        "num_question": url.count("?"),
        "num_equals": url.count("="),
        "num_digits": digits,
        "num_subdomains": max(host.count(".") - 1, 0),
        "has_ip": int(has_ip),
        "has_https": int(scheme == "https"),
        "is_shortener": int(any(s in host for s in SHORTENERS)),
        "suspicious_kw_count": sum(kw in url.lower() for kw in SUSPICIOUS_KEYWORDS),
        "tld_suspicious": int(tld in SUSPICIOUS_TLDS),
    }


# 2) Network intrusion features (NSL-KDD inspired, simplified)
INTRUSION_FEATURES = [
    "duration", "src_bytes", "dst_bytes", "wrong_fragment", "urgent",
    "count", "srv_count", "serror_rate", "rerror_rate", "same_srv_rate",
    "diff_srv_rate", "dst_host_count", "dst_host_srv_count",
    "dst_host_same_srv_rate", "dst_host_serror_rate",
]
INTRUSION_CLASSES = ("Normal", "DoS", "Probe", "R2L", "U2R")


# 3) Behavioral / login-log features
LOGIN_FEATURES = [
    "hour_of_day", "is_weekend", "country_distance_km", "device_change",
    "failed_attempts", "session_duration_min", "bytes_downloaded_mb",
    "unusual_hour", "vpn_used",
]


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))
