# AI in Cyber Threat Intelligence — Demo & Presentation

A self-contained demo + slide deck for a **10–15 min** Information Security & Assurance presentation on **AI in Threat Intelligence**.

It implements three live ML-powered detectors that map directly onto the talk:

| Tab in dashboard | Slide section it illustrates | Model |
|---|---|---|
| **Malicious URL Detector** | Phishing Detection & Prevention | RandomForest (supervised) |
| **Network Intrusion Classifier** | Proactive Threat Detection | RandomForest, multi-class (Normal / DoS / Probe / R2L / U2R) |
| **Behavioral Anomaly Detector** | Behavioral Analytics | IsolationForest (unsupervised) |

> Phishing and intrusion models are trained on **real public datasets** (651K URLs + 125K NSL-KDD flows). The behavioral anomaly detector uses synthetic data (no public dataset matches our 9 login features).
---

## 1 · Project layout

```
threatIntel/
├── app.py                  FastAPI server + dashboard
├── train_models.py         Trains & saves the 3 models
├── requirements.txt
├── ml/
│   ├── features.py         Feature extractors (URL, flow, login)
│   └── datasets.py         Dataset loaders (real + synthetic)
├── data/                   Downloaded Kaggle datasets
│   ├── malicious_phish.csv   651K URLs (benign/phishing/defacement/malware)
│   └── NSL-KDD/              NSL-KDD intrusion dataset
│       └── KDDTrain+.txt     125K network flows
├── static/
│   └── index.html          Tailwind + Chart.js single-page UI
├── models/                 Created after training
│   ├── phishing_rf.joblib
│   ├── intrusion_rf.joblib
│   ├── behavior_iforest.joblib
│   └── metrics.json
```

> **Note**: Both `data/` and `models/` directories are untracked and excluded in `.gitignore` to prevent committing massive dataset CSVs and large binary weights (joblib) to version control.

---
## 2 · Setup (one-time)

Requires **Python 3.13** (3.10+ works, but examples here use 3.13).

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 3 · Download real Kaggle datasets

The phishing and intrusion models require real datasets.

| Dataset | Kaggle link | Size | Local path |
|---|---|---|---|
| **Malicious URLs** | [sid321axn/malicious-urls](https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset) | 651K URLs | `data/malicious_phish.csv` |
| **NSL-KDD** (intrusion) | [hassan06/nslkdd](https://www.kaggle.com/datasets/hassan06/nslkdd) | 125K flows | `data/NSL-KDD/KDDTrain+.txt` |
| Behavioral logins | *(synthetic — no public equivalent)* | — | generated at train time |

Download from the Kaggle links above and place into the `data/` directory as shown.

---

## 4 · Train the three models

```bash
python train_models.py
```

With **real** data (~2 minutes, most time spent on URL feature extraction):
```
[1/3] Training phishing URL classifier ...
   loading data/malicious_phish.csv ...
   extracting features from 10000 URLs ...
   malicious: 5000 / benign: 5000
   accuracy=0.965  f1=0.962
[2/3] Training network intrusion classifier ...
   loading data/NSL-KDD/KDDTrain+.txt ...
   intrusion samples per class:
      Normal: 2000
      DoS: 2000
      Probe: 2000
      R2L: 995
      U2R: 52
   accuracy=0.993
[3/3] Training behavioral anomaly detector ...
   anomaly recall on planted set=0.800
```

> Real-data accuracy (~96% URLs, ~99% intrusion) matches published benchmarks (Sahingoz et al. 2019, Tavallaee et al. 2009).

---

## 5 · Run the dashboard

```bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

Open <http://127.0.0.1:8000>.

You get four tabs:

- **Malicious URL Detector** — type any URL, get a live malicious probability + the 15 extracted features.
- **Network Intrusion Classifier** — pick a scenario (Normal / DoS / Probe / U2R), get a bar chart of class probabilities.
- **Behavioral Anomaly Detector** — pick a login event, get an anomaly verdict + a running anomaly-score line chart.
- **Model Metrics** — auto-rendered accuracy cards + the intrusion confusion matrix.

---

## 6 · Tech stack

- **Python 3.13**, scikit-learn 1.5, pandas, NumPy
- **FastAPI + Uvicorn** for the API (async, OpenAPI docs at `/docs`)
- **Tailwind CSS + Chart.js** via CDN — no Node build step required
- **Marp** for the slides

---

## 7 · License

Educational use. Cite this repo if reused for coursework.
