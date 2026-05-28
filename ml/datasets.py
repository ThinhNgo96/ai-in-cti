"""Dataset loaders for real Kaggle data.

Data files expected under ./data/:
  - Phishing:   data/malicious_phish.csv   (sid321axn/malicious-urls, 651K rows)
  - Intrusion:  data/NSL-KDD/KDDTrain+.txt (hassan06/nslkdd, 125K rows)
  - Behavioral: synthetic — no public dataset matches our 9 login features.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .features import extract_url_features, PHISH_FEATURES, INTRUSION_FEATURES, LOGIN_FEATURES

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# Phishing URLs  (data/malicious_phish.csv)
#
# Columns: url, type
# type values: benign, phishing, defacement, malware
# We map to binary: benign → 0, everything else → 1 (malicious)
def build_phishing_dataset(
    max_per_class: int = 5000,
    seed: int = 42,
) -> pd.DataFrame:
    """Load raw URLs from malicious_phish.csv, extract 15 lexical features."""
    csv = DATA_DIR / "malicious_phish.csv"
    if not csv.exists():
        raise FileNotFoundError(
            f"Phishing dataset not found at {csv}.\n"
            "Download from: https://www.kaggle.com/datasets/sid321axn/malicious-urls\n"
            "Place the CSV at data/malicious_phish.csv"
        )

    print(f"   loading {csv} ...")
    raw = pd.read_csv(csv, low_memory=False)
    raw.columns = [c.strip().lower() for c in raw.columns]

    # Binary label: benign=0, phishing/defacement/malware=1
    raw["label"] = raw["type"].str.strip().str.lower().apply(
        lambda v: 0 if v == "benign" else 1
    )

    # Balance + sample
    rng = np.random.default_rng(seed)
    dfs = []
    for lbl in [0, 1]:
        subset = raw[raw["label"] == lbl]
        n = min(len(subset), max_per_class)
        idx = rng.choice(len(subset), size=n, replace=False)
        dfs.append(subset.iloc[idx])
    sampled = pd.concat(dfs, ignore_index=True)

    print(f"   extracting features from {len(sampled)} URLs ...")
    rows = []
    for _, row in sampled.iterrows():
        feats = extract_url_features(str(row["url"]))
        feats["label"] = int(row["label"])
        rows.append(feats)

    df = pd.DataFrame(rows)
    print(f"   malicious: {(df['label']==1).sum()} / benign: {(df['label']==0).sum()}")
    return df[PHISH_FEATURES + ["label"]]


# Network intrusion  (data/NSL-KDD/KDDTrain+.txt)
# Full NSL-KDD column headers (41 features + attack + difficulty)
NSL_KDD_COLUMNS = [
    "duration", "protocol_type", "service", "flag",
    "src_bytes", "dst_bytes", "land", "wrong_fragment", "urgent",
    "hot", "num_failed_logins", "logged_in",
    "num_compromised", "root_shell", "su_attempted", "num_root",
    "num_file_creations", "num_shells", "num_access_files",
    "num_outbound_cmds", "is_host_login", "is_guest_login",
    "count", "srv_count",
    "serror_rate", "srv_serror_rate", "rerror_rate", "srv_rerror_rate",
    "same_srv_rate", "diff_srv_rate", "srv_diff_host_rate",
    "dst_host_count", "dst_host_srv_count",
    "dst_host_same_srv_rate", "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate",
    "dst_host_serror_rate", "dst_host_srv_serror_rate",
    "dst_host_rerror_rate", "dst_host_srv_rerror_rate",
    "attack", "difficulty",
]

# NSL-KDD attack names → 5-class mapping
ATTACK_CATEGORY = {
    "normal": "Normal",
    # DoS
    "back": "DoS", "land": "DoS", "neptune": "DoS", "pod": "DoS",
    "smurf": "DoS", "teardrop": "DoS", "apache2": "DoS", "udpstorm": "DoS",
    "processtable": "DoS", "mailbomb": "DoS", "worm": "DoS",
    # Probe
    "ipsweep": "Probe", "nmap": "Probe", "portsweep": "Probe", "satan": "Probe",
    "mscan": "Probe", "saint": "Probe",
    # R2L
    "ftp_write": "R2L", "guess_passwd": "R2L", "imap": "R2L", "multihop": "R2L",
    "phf": "R2L", "spy": "R2L", "warezclient": "R2L", "warezmaster": "R2L",
    "sendmail": "R2L", "named": "R2L", "snmpgetattack": "R2L",
    "snmpguess": "R2L", "xlock": "R2L", "xsnoop": "R2L",
    "httptunnel": "R2L",
    # U2R
    "buffer_overflow": "U2R", "loadmodule": "U2R", "perl": "U2R",
    "rootkit": "U2R", "ps": "U2R", "sqlattack": "U2R", "xterm": "U2R",
}


def build_intrusion_dataset(
    max_per_class: int = 2000,
    seed: int = 7,
) -> pd.DataFrame:
    """Load NSL-KDD KDDTrain+.txt, map attacks to 5 categories,
    select the 15 features our model uses.

    R2L and U2R are rare in this dataset (995 and 52 respectively),
    so they are taken in full rather than subsampled.
    """
    txt = DATA_DIR / "NSL-KDD" / "KDDTrain+.txt"
    if not txt.exists():
        raise FileNotFoundError(
            f"NSL-KDD dataset not found at {txt}.\n"
            "Download from: https://www.kaggle.com/datasets/hassan06/nslkdd\n"
            "Extract into data/NSL-KDD/"
        )

    print(f"   loading {txt} ...")
    raw = pd.read_csv(txt, header=None, names=NSL_KDD_COLUMNS)

    # Map attack names to 5 categories
    raw["label"] = raw["attack"].str.strip().str.lower().map(ATTACK_CATEGORY)
    raw = raw.dropna(subset=["label"])

    # Balance + sample  (take all for rare classes)
    rng = np.random.default_rng(seed)
    dfs = []
    for cat in ["Normal", "DoS", "Probe", "R2L", "U2R"]:
        subset = raw[raw["label"] == cat]
        n = min(len(subset), max_per_class)
        if n == 0:
            print(f"   WARN: 0 samples for {cat}")
            continue
        if n < max_per_class:
            # Rare class — take all
            dfs.append(subset)
        else:
            idx = rng.choice(len(subset), size=n, replace=False)
            dfs.append(subset.iloc[idx])

    df = pd.concat(dfs, ignore_index=True)
    print(f"   intrusion samples per class:")
    for cat in ["Normal", "DoS", "Probe", "R2L", "U2R"]:
        print(f"      {cat}: {(df['label']==cat).sum()}")

    return df[INTRUSION_FEATURES + ["label"]]


# Behavioral / login-log dataset (synthetic — no public equivalent)
def build_login_dataset(n_normal: int = 5000, seed: int = 11) -> pd.DataFrame:
    """Only normal logins are used to train an unsupervised IsolationForest;
    we also generate a small held-out anomaly set for the live-demo evaluation.
    """
    rng = np.random.default_rng(seed)
    rows = []
    for _ in range(n_normal):
        hour = int(np.clip(rng.normal(13, 3), 0, 23))  # working hours
        rows.append({
            "hour_of_day": hour,
            "is_weekend": int(rng.random() < 0.2),
            "country_distance_km": float(abs(rng.normal(0, 30))),
            "device_change": int(rng.random() < 0.05),
            "failed_attempts": int(max(0, rng.normal(0, 0.4))),
            "session_duration_min": float(abs(rng.normal(45, 20))),
            "bytes_downloaded_mb": float(abs(rng.normal(80, 40))),
            "unusual_hour": int(hour < 6 or hour > 22),
            "vpn_used": int(rng.random() < 0.1),
            "label": 0,
        })
    return pd.DataFrame(rows)[LOGIN_FEATURES + ["label"]]


def sample_login_anomalies(seed: int = 99) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    anomalies = [
        # 3am login from another country, new device, multiple failures
        dict(hour_of_day=3, is_weekend=1, country_distance_km=8500,
             device_change=1, failed_attempts=4, session_duration_min=180,
             bytes_downloaded_mb=1200, unusual_hour=1, vpn_used=1, label=1),
        # Massive data exfiltration during weekend night
        dict(hour_of_day=2, is_weekend=1, country_distance_km=200,
             device_change=1, failed_attempts=2, session_duration_min=20,
             bytes_downloaded_mb=4500, unusual_hour=1, vpn_used=1, label=1),
        # Brute-force credential stuffing pattern
        dict(hour_of_day=4, is_weekend=0, country_distance_km=10000,
             device_change=1, failed_attempts=12, session_duration_min=2,
             bytes_downloaded_mb=0, unusual_hour=1, vpn_used=1, label=1),
    ]
    # plus a couple of true normals to show the model doesn't false-alarm
    normals = [
        dict(hour_of_day=10, is_weekend=0, country_distance_km=5,
             device_change=0, failed_attempts=0, session_duration_min=50,
             bytes_downloaded_mb=70, unusual_hour=0, vpn_used=0, label=0),
        dict(hour_of_day=15, is_weekend=0, country_distance_km=20,
             device_change=0, failed_attempts=1, session_duration_min=120,
             bytes_downloaded_mb=150, unusual_hour=0, vpn_used=0, label=0),
    ]
    return pd.DataFrame(anomalies + normals)[LOGIN_FEATURES + ["label"]]
