"""Train and persist all three demo models using real datasets.

Usage:
    python train_models.py

Datasets required (see README § 3):
    data/malicious_phish.csv        — malicious URL detection
    data/NSL-KDD/KDDTrain+.txt      — network intrusion classification

Outputs under ./models/:
    - phishing_rf.joblib       (RandomForestClassifier)
    - intrusion_rf.joblib      (RandomForestClassifier, multi-class)
    - behavior_iforest.joblib  (IsolationForest)
    - metrics.json             (printable summary for slides)
"""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, f1_score)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from ml.datasets import (build_intrusion_dataset, build_login_dataset,
                         build_phishing_dataset, sample_login_anomalies)
from ml.features import (INTRUSION_FEATURES, LOGIN_FEATURES, PHISH_FEATURES)

MODELS_DIR = Path(__file__).parent / "models"
MODELS_DIR.mkdir(exist_ok=True)


def train_phishing():
    print("[1/3] Training phishing URL classifier ...")
    df = build_phishing_dataset()
    X, y = df[PHISH_FEATURES], df["label"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)
    clf = RandomForestClassifier(n_estimators=200, random_state=0, n_jobs=-1)
    clf.fit(Xtr, ytr)
    pred = clf.predict(Xte)
    acc = accuracy_score(yte, pred)
    f1 = f1_score(yte, pred)
    print(f"   accuracy={acc:.3f}  f1={f1:.3f}")
    joblib.dump({"model": clf, "features": PHISH_FEATURES}, MODELS_DIR / "phishing_rf.joblib")
    return {"accuracy": round(acc, 4), "f1": round(f1, 4),
            "report": classification_report(yte, pred, output_dict=True),
            "confusion_matrix": confusion_matrix(yte, pred).tolist()}


def train_intrusion():
    print("[2/3] Training network intrusion classifier ...")
    df = build_intrusion_dataset()
    X, y = df[INTRUSION_FEATURES], df["label"]

    # Use stratified split; R2L/U2R are small but still split proportionally
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)

    # class_weight="balanced" compensates for the heavy R2L/U2R imbalance
    clf = RandomForestClassifier(
        n_estimators=300, random_state=0, n_jobs=-1,
        class_weight="balanced",
    )
    clf.fit(Xtr, ytr)
    pred = clf.predict(Xte)
    acc = accuracy_score(yte, pred)
    print(f"   accuracy={acc:.3f}")
    print(f"   per-class:\n{classification_report(yte, pred)}")
    joblib.dump({"model": clf, "features": INTRUSION_FEATURES,
                 "classes": clf.classes_.tolist()},
                MODELS_DIR / "intrusion_rf.joblib")
    return {"accuracy": round(acc, 4),
            "report": classification_report(yte, pred, output_dict=True),
            "labels": clf.classes_.tolist(),
            "confusion_matrix": confusion_matrix(yte, pred, labels=clf.classes_).tolist()}


def train_behavior():
    print("[3/3] Training behavioral anomaly detector ...")
    df = build_login_dataset()
    X = df[LOGIN_FEATURES].values
    scaler = StandardScaler().fit(X)
    Xs = scaler.transform(X)
    iso = IsolationForest(n_estimators=200, contamination=0.02, random_state=0)
    iso.fit(Xs)

    # quick eval on planted anomalies
    test_df = sample_login_anomalies()
    Xt = scaler.transform(test_df[LOGIN_FEATURES].values)
    raw = iso.predict(Xt)        # -1 = anomaly, 1 = normal
    pred = (raw == -1).astype(int)
    truth = test_df["label"].values
    acc = float(np.mean(pred == truth))
    print(f"   anomaly recall on planted set={acc:.3f}")
    joblib.dump({"model": iso, "scaler": scaler, "features": LOGIN_FEATURES},
                MODELS_DIR / "behavior_iforest.joblib")
    return {"planted_set_accuracy": round(acc, 4),
            "predictions": pred.tolist(), "truth": truth.tolist()}


def main():
    metrics = {
        "phishing": train_phishing(),
        "intrusion": train_intrusion(),
        "behavior": train_behavior(),
    }
    with open(MODELS_DIR / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2, default=str)
    print(f"\nAll models saved to {MODELS_DIR.resolve()}")


if __name__ == "__main__":
    main()
