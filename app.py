"""CTI Demo Dashboard — FastAPI backend.

Endpoints:
    GET  /                  -> the single-page dashboard
    POST /api/phishing      -> {url} -> {label, prob, features}
    POST /api/intrusion     -> {features} -> {label, probs}
    POST /api/behavior      -> {features} -> {anomaly, score}
    GET  /api/metrics       -> training metrics (for the dashboard footer)
    GET  /api/sample/<kind> -> sample inputs (handy for live demo buttons)
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from ml.features import (INTRUSION_FEATURES, LOGIN_FEATURES, PHISH_FEATURES,
                         extract_url_features)

ROOT = Path(__file__).parent
MODELS_DIR = ROOT / "models"

app = FastAPI(title="AI in Threat Intelligence — Demo")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")


# ---------------------------------------------------------------------------
# Lazy-load models so the server starts even if training hasn't finished
# ---------------------------------------------------------------------------
_models: Dict[str, Any] = {}


def _load(name: str):
    if name in _models:
        return _models[name]
    path = MODELS_DIR / f"{name}.joblib"
    if not path.exists():
        raise HTTPException(status_code=503,
                            detail=f"Model '{name}' not trained yet. Run: python train_models.py")
    _models[name] = joblib.load(path)
    return _models[name]


# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------
class PhishingReq(BaseModel):
    url: str


class IntrusionReq(BaseModel):
    features: Dict[str, float]


class BehaviorReq(BaseModel):
    features: Dict[str, float]


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def index():
    return (ROOT / "static" / "index.html").read_text()


@app.post("/api/phishing")
def predict_phishing(req: PhishingReq):
    bundle = _load("phishing_rf")
    feats = extract_url_features(req.url)
    X = pd.DataFrame([[feats[c] for c in PHISH_FEATURES]], columns=PHISH_FEATURES)
    prob = float(bundle["model"].predict_proba(X)[0, 1])
    label = "malicious" if prob >= 0.5 else "benign"
    return {
        "url": req.url,
        "label": label,
        "malicious_probability": round(prob, 4),
        "features": feats,
    }


@app.post("/api/intrusion")
def predict_intrusion(req: IntrusionReq):
    bundle = _load("intrusion_rf")
    missing = [c for c in INTRUSION_FEATURES if c not in req.features]
    if missing:
        raise HTTPException(400, f"missing features: {missing}")
    X = pd.DataFrame([[req.features[c] for c in INTRUSION_FEATURES]],
                     columns=INTRUSION_FEATURES)
    model = bundle["model"]
    probs = model.predict_proba(X)[0]
    classes: List[str] = bundle["classes"]
    idx = int(np.argmax(probs))
    return {
        "label": classes[idx],
        "probabilities": {c: round(float(p), 4) for c, p in zip(classes, probs)},
    }


@app.post("/api/behavior")
def predict_behavior(req: BehaviorReq):
    bundle = _load("behavior_iforest")
    missing = [c for c in LOGIN_FEATURES if c not in req.features]
    if missing:
        raise HTTPException(400, f"missing features: {missing}")
    X = np.array([[req.features[c] for c in LOGIN_FEATURES]], dtype=float)
    Xs = bundle["scaler"].transform(X)
    model = bundle["model"]
    raw = int(model.predict(Xs)[0])              # -1 anomaly, 1 normal
    score = float(model.decision_function(Xs)[0])  # higher = more normal
    return {
        "anomaly": raw == -1,
        "anomaly_score": round(-score, 4),  # invert so higher = more suspicious
        "verdict": "ANOMALOUS — possible compromised account" if raw == -1 else "Normal",
    }


@app.get("/api/metrics")
def metrics():
    p = MODELS_DIR / "metrics.json"
    if not p.exists():
        return {"trained": False}
    return {"trained": True, **json.loads(p.read_text())}


@app.get("/api/sample/{kind}")
def sample(kind: str):
    if kind == "phishing":
        return {"examples": [
            "https://github.com/openai",
            "http://paypal-secure-login.xyz/verify?id=abc123def",
            "http://192.168.10.5/amazon/login.php",
            "http://bit.ly/3xKqZ9p",
            "https://www.wikipedia.org",
        ]}
    if kind == "intrusion":
        return {"examples": {
            "Normal HTTP session": dict(duration=5, src_bytes=320, dst_bytes=2100,
                wrong_fragment=0, urgent=0, count=4, srv_count=4,
                serror_rate=0.02, rerror_rate=0.02, same_srv_rate=0.9,
                diff_srv_rate=0.05, dst_host_count=20, dst_host_srv_count=18,
                dst_host_same_srv_rate=0.9, dst_host_serror_rate=0.02),
            "DoS flood": dict(duration=0, src_bytes=20, dst_bytes=0,
                wrong_fragment=1, urgent=0, count=210, srv_count=190,
                serror_rate=0.97, rerror_rate=0.03, same_srv_rate=0.98,
                diff_srv_rate=0.01, dst_host_count=255, dst_host_srv_count=255,
                dst_host_same_srv_rate=0.99, dst_host_serror_rate=0.97),
            "Port-scan probe": dict(duration=1, src_bytes=50, dst_bytes=10,
                wrong_fragment=0, urgent=0, count=85, srv_count=22,
                serror_rate=0.32, rerror_rate=0.6, same_srv_rate=0.2,
                diff_srv_rate=0.7, dst_host_count=120, dst_host_srv_count=22,
                dst_host_same_srv_rate=0.2, dst_host_serror_rate=0.3),
            "Privilege escalation (U2R)": dict(duration=60, src_bytes=400, dst_bytes=1500,
                wrong_fragment=0, urgent=2, count=1, srv_count=1,
                serror_rate=0.0, rerror_rate=0.0, same_srv_rate=1.0,
                diff_srv_rate=0.0, dst_host_count=5, dst_host_srv_count=5,
                dst_host_same_srv_rate=1.0, dst_host_serror_rate=0.0),
        }}
    if kind == "behavior":
        return {"examples": {
            "Typical workday login": dict(hour_of_day=10, is_weekend=0,
                country_distance_km=5, device_change=0, failed_attempts=0,
                session_duration_min=50, bytes_downloaded_mb=70,
                unusual_hour=0, vpn_used=0),
            "3am foreign login + new device": dict(hour_of_day=3, is_weekend=1,
                country_distance_km=8500, device_change=1, failed_attempts=4,
                session_duration_min=180, bytes_downloaded_mb=1200,
                unusual_hour=1, vpn_used=1),
            "Mass data exfiltration": dict(hour_of_day=2, is_weekend=1,
                country_distance_km=200, device_change=1, failed_attempts=2,
                session_duration_min=20, bytes_downloaded_mb=4500,
                unusual_hour=1, vpn_used=1),
            "Credential stuffing": dict(hour_of_day=4, is_weekend=0,
                country_distance_km=10000, device_change=1, failed_attempts=12,
                session_duration_min=2, bytes_downloaded_mb=0,
                unusual_hour=1, vpn_used=1),
        }}
    raise HTTPException(404, "unknown sample kind")


@app.get("/api/schema")
def schema():
    return {
        "phishing_features": PHISH_FEATURES,
        "intrusion_features": INTRUSION_FEATURES,
        "behavior_features": LOGIN_FEATURES,
    }
