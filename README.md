# Wind Turbine Gearbox Predictive Maintenance

<div align="center">

**Anomaly Detection & Remaining Useful Life Prediction via SCADA Time-Series Data**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![TensorFlow 2.x](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)](https://tensorflow.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.1+-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)
[![Kaggle Dataset](https://img.shields.io/badge/Dataset-Kaggle-20BEFF?style=flat-square&logo=kaggle&logoColor=white)](https://www.kaggle.com/datasets/aiwithcagri/wind-turbine-gearbox-anomaly-detection-5year-scada/data)

<br/>

*Mechatronics Engineering — Undergraduate Thesis Project*  
**Fırat University, Department of Mechatronics Engineering**

</div>

---

## Overview

This project presents an end-to-end predictive maintenance pipeline for wind turbine gearboxes using five years of real-world SCADA sensor data. The system combines classical machine learning, unsupervised anomaly detection, deep learning sequence models, and hybrid ensemble methods — culminating in a Remaining Useful Life (RUL) regression module that enables early fault warning up to 72 hours in advance.

The pipeline spans six sequential notebooks, each building on the outputs of the previous, and is designed to run natively on **Kaggle GPU environments** with zero local setup.

---

## Table of Contents

- [Dataset](#dataset)
- [Project Architecture](#project-architecture)
- [Notebook Descriptions](#notebook-descriptions)
- [Methods & Techniques](#methods--techniques)
- [Results](#results)
- [Getting Started](#getting-started)
- [Dependencies](#dependencies)
- [Citation](#citation)
- [License](#license)

---

## Dataset

| Property | Value |
|----------|-------|
| **Source** | [Kaggle — Wind Turbine Gearbox Anomaly Detection (5-Year SCADA)](https://www.kaggle.com/datasets/aiwithcagri/wind-turbine-gearbox-anomaly-detection-5year-scada/data) |
| **Format** | CSV (time-series, SCADA) |
| **Duration** | 5 years of continuous operation |
| **Labels** | Binary anomaly labels |
| **Features** | Gearbox temperature sensors, power output, wind speed, RPM, vibration proxies |

### Quick Download

```bash
pip install kaggle
mkdir -p ~/.kaggle && cp kaggle.json ~/.kaggle/ && chmod 600 ~/.kaggle/kaggle.json
kaggle datasets download -d aiwithcagri/wind-turbine-gearbox-anomaly-detection-5year-scada
unzip wind-turbine-gearbox-anomaly-detection-5year-scada.zip -d data/
```

> **On Kaggle:** Dataset path is automatically set to `/kaggle/input/wind-turbine-gearbox-anomaly-detection-5year-scada/`

---

## Project Architecture

```
turbine-gearbox-predictive-maintenance/
│
├── 01_EDA_Feature_Engineering/
│   ├── notebook.ipynb          # Exploratory analysis & feature construction
│   └── results/README.md       # Expected outputs
│
├── 02_Classical_ML_Baselines/
│   ├── notebook.ipynb          # RF · XGBoost · LightGBM · Logistic Regression
│   └── results/README.md
│
├── 03_Anomaly_Detection_Unsupervised/
│   ├── notebook.ipynb          # Isolation Forest · OC-SVM · LOF · Autoencoder
│   └── results/README.md
│
├── 04_TimeSeries_DeepLearning/
│   ├── notebook.ipynb          # LSTM · TCN · Transformer Encoder
│   └── results/README.md
│
├── 05_Hybrid_Ensemble/
│   ├── notebook.ipynb          # Stacking · Voting · SHAP · LIME
│   └── results/README.md
│
├── 06_RUL_Prediction/
│   ├── notebook.ipynb          # Weibull · LSTM/GRU Regression · Early Warning
│   └── results/README.md
│
└── README.md
```

### Pipeline Flow

```
Raw SCADA Data
      │
      ▼
┌─────────────────────┐
│  01 · EDA &         │  Rolling features (24h/48h/168h window)
│  Feature Engineering│  Lag features · FFT · Mutual Information
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐    ┌──────────────────────────┐
│  02 · Classical ML  │    │  03 · Unsupervised        │
│  Baselines          │    │  Anomaly Detection        │
│  RF · XGB · LGBM   │    │  IF · OC-SVM · LOF · AE  │
└────────┬────────────┘    └────────────┬─────────────┘
         │                              │
         └──────────────┬───────────────┘
                        ▼
         ┌──────────────────────────┐
         │  04 · Time-Series DL     │
         │  LSTM · TCN · Transformer│
         └──────────────┬───────────┘
                        │
                        ▼
         ┌──────────────────────────┐
         │  05 · Hybrid Ensemble    │
         │  Stacking · Voting       │
         │  SHAP · LIME (XAI)       │
         └──────────────┬───────────┘
                        │
                        ▼
         ┌──────────────────────────┐
         │  06 · RUL Prediction     │
         │  Weibull · LSTM/GRU      │
         │  Early Warning System    │
         └──────────────────────────┘
```

---

## Notebook Descriptions

### 01 — EDA & Feature Engineering

**Goal:** Deep understanding of the sensor data and construction of an enriched feature set.

| Technique | Description |
|-----------|-------------|
| Time-series visualization | Per-sensor signal plots with anomaly timeline overlay |
| Correlation matrix | Inter-sensor relationship analysis |
| Rolling statistics | Mean / Std over 24h, 48h, 168h windows |
| Lag features | Delayed values at 1h, 6h, 12h, 24h offsets |
| FFT | Periodic component decomposition |
| Mutual Information | Preliminary feature importance ranking |
| Class imbalance analysis | Anomaly rate distribution and class ratio assessment |

---

### 02 — Classical ML Baselines

**Goal:** Establish strong benchmarks using traditional supervised learning methods.

| Technique | Configuration |
|-----------|---------------|
| Train/test split | Temporal (chronological, no shuffle) |
| Class balancing | SMOTE oversampling + `class_weight='balanced'` |
| Random Forest | `n_estimators=100`, balanced class weights |
| XGBoost | `n_estimators=200`, `scale_pos_weight` tuned |
| LightGBM | `n_estimators=200`, balanced class weights |
| Logistic Regression | StandardScaler, `class_weight='balanced'` |
| Threshold optimization | F1-maximizing threshold search on validation set |
| Feature importance | Top-20 features per model |

---

### 03 — Unsupervised Anomaly Detection

**Goal:** Label-free anomaly detection to evaluate raw signal separability.

| Method | Description |
|--------|-------------|
| Isolation Forest | Contamination tuning via validation-set anomaly rate |
| One-Class SVM | RBF kernel, trained on normal-only data |
| Local Outlier Factor | k=20 neighbors, local density estimation |
| Autoencoder (Keras) | MSE reconstruction error as anomaly score; threshold at 95th percentile |

---

### 04 — Time-Series Deep Learning

**Goal:** Capture temporal dependencies and sequential fault patterns.

| Technique | Configuration |
|-----------|---------------|
| Sliding window | window_size=48, stride=1 |
| LSTM | 2-layer, dropout=0.3, class-weighted loss |
| TCN | Dilated causal convolutions, 4 residual blocks (dilation: 1, 2, 4, 8) |
| Transformer Encoder | Multi-head self-attention + positional encoding |
| Early stopping | patience=10, monitor=`val_loss` |
| LR scheduling | `ReduceLROnPlateau(factor=0.5, patience=5)` |

---

### 05 — Hybrid Ensemble & Explainability

**Goal:** Maximize predictive performance and explain model decisions.

| Technique | Description |
|-----------|-------------|
| Stacking | OOF predictions as meta-features; Logistic Regression meta-learner |
| Soft voting | Uniform and AUC-weighted probability averaging |
| Unsupervised + Supervised hybrid | IF/AE anomaly scores combined with ML classifier outputs |
| SHAP | TreeExplainer, summary plots, temporal feature importance |
| LIME | Local instance-level explanations for individual predictions |

---

### 06 — RUL Prediction

**Goal:** Answer *"When should maintenance be scheduled?"* with a concrete time horizon.

| Technique | Description |
|-----------|-------------|
| RUL label construction | Countdown from each timestamp to next anomaly event (max\_rul=168h) |
| Degradation curve analysis | Sensor drift patterns in the pre-anomaly window |
| Weibull distribution | `scipy.stats.weibull_min`; MTTF estimation |
| LSTM/GRU regression | Sliding window input, Huber loss |
| Early warning system | Alarm accuracy at 24h / 48h / 72h before anomaly |
| Maintenance timeline | Color-coded risk zones (safe / caution / critical) |

---

## Methods & Techniques

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Chronological train/test split** | Prevents temporal data leakage; reflects real deployment conditions |
| **Multi-sensor fusion** | Gearbox faults manifest across multiple sensor channels simultaneously |
| **Continuous anomaly scoring** | Richer signal than binary labels for ensemble calibration |
| **Huber loss for RUL** | Robust to outlier RUL values without ignoring them entirely |
| **SMOTE + class_weight dual strategy** | Handles severe class imbalance (~2–5% anomaly rate) at both data and loss levels |
| **SHAP + LIME** | Complementary global and local explanations for interpretable maintenance decisions |

---

## Results

> Results will be updated after full notebook execution. Metrics reported on the held-out chronological test set.

| Method | Category | F1 | ROC-AUC | PR-AUC |
|--------|----------|----|---------|--------|
| Logistic Regression | Classical ML | TBD | TBD | TBD |
| Random Forest | Classical ML | TBD | TBD | TBD |
| XGBoost | Classical ML | TBD | TBD | TBD |
| LightGBM | Classical ML | TBD | TBD | TBD |
| Isolation Forest | Unsupervised | — | TBD | TBD |
| One-Class SVM | Unsupervised | — | TBD | TBD |
| LOF | Unsupervised | — | TBD | TBD |
| Autoencoder | Unsupervised | — | TBD | TBD |
| LSTM | Deep Learning | TBD | TBD | TBD |
| TCN | Deep Learning | TBD | TBD | TBD |
| Transformer Encoder | Deep Learning | TBD | TBD | TBD |
| Stacking Ensemble | Ensemble | TBD | TBD | TBD |
| Weighted Voting | Ensemble | TBD | TBD | TBD |

**RUL Prediction (regression)**

| Model | MAE (hours) | RMSE (hours) | Early Warning Acc. (72h) |
|-------|-------------|--------------|--------------------------|
| Weibull baseline | TBD | TBD | TBD |
| LSTM regression | TBD | TBD | TBD |
| GRU regression | TBD | TBD | TBD |

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/emirsecer1/turbine-gearbox-predictive-maintenance.git
cd turbine-gearbox-predictive-maintenance
```

### 2. Install dependencies

```bash
pip install pandas numpy scipy matplotlib seaborn scikit-learn \
            xgboost lightgbm imbalanced-learn tensorflow \
            shap lime kaggle joblib
```

### 3. Download the dataset

```bash
kaggle datasets download -d aiwithcagri/wind-turbine-gearbox-anomaly-detection-5year-scada
unzip wind-turbine-gearbox-anomaly-detection-5year-scada.zip -d data/
```

### 4. Run notebooks in order

```
01_EDA_Feature_Engineering/notebook.ipynb
02_Classical_ML_Baselines/notebook.ipynb
03_Anomaly_Detection_Unsupervised/notebook.ipynb
04_TimeSeries_DeepLearning/notebook.ipynb
05_Hybrid_Ensemble/notebook.ipynb
06_RUL_Prediction/notebook.ipynb
```

> **Kaggle users:** All notebooks are configured to run directly in the Kaggle notebook environment. Dataset paths resolve automatically to `/kaggle/input/wind-turbine-gearbox-anomaly-detection-5year-scada/`.

---

## Dependencies

```python
# Core data processing
pandas >= 1.5.0
numpy >= 1.23.0
scipy >= 1.9.0

# Visualization
matplotlib >= 3.6.0
seaborn >= 0.12.0

# Machine learning
scikit-learn >= 1.1.0
xgboost >= 1.7.0
lightgbm >= 3.3.0
imbalanced-learn >= 0.10.0

# Deep learning
tensorflow >= 2.10.0

# Explainability
shap >= 0.41.0
lime >= 0.2.0.1

# Utilities
kaggle >= 1.5.0
joblib >= 1.2.0
```

---

## Citation

If you use this work in your research, please cite:

```bibtex
@misc{secer2025turbine,
  author       = {Secer, Emir},
  title        = {Wind Turbine Gearbox Predictive Maintenance: Anomaly Detection and RUL Prediction via SCADA Time-Series Data},
  year         = {2025},
  institution  = {Fırat University, Department of Mechatronics Engineering},
  howpublished = {\url{https://github.com/emirsecer1/turbine-gearbox-predictive-maintenance}},
  note         = {Undergraduate Thesis Project}
}
```

---

## License

This project is released under the [MIT License](LICENSE).

---

<div align="center">

*Developed at Fırat University, Department of Mechatronics Engineering*  
*Contributions, issues, and pull requests are welcome.*

</div>
