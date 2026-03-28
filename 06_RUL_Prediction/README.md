# ⏱️ 06 — Remaining Useful Life (RUL) Prediction

![Step](https://img.shields.io/badge/Pipeline_Step-06-blue)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Category](https://img.shields.io/badge/Category-Predictive_Maintenance-purple)
![Weibull](https://img.shields.io/badge/Weibull-Reliability-red)
![LSTM](https://img.shields.io/badge/LSTM-Regression-orange)
![GRU](https://img.shields.io/badge/GRU-Regression-yellow)
![Report Section](https://img.shields.io/badge/Report_Section-Chapter_8:_RUL_Prediction-orange)

---

## 🇹🇷 Türkçe Özet

Bu klasör, projenin en özgün katkısını içerir: "Ne zaman bozulacak?" sorusunu cevaplayan Kalan Kullanım Ömrü (RUL) tahmini. Anomali başlangıcından geriye doğru 168 saatlik (1 hafta) geri sayım ile RUL hesaplanır. Weibull dağılımı ile güvenilirlik analizi yapılır. LSTM ve GRU regresyon modelleri ile RUL tahmini gerçekleştirilir. En iyi model LSTM'dir (MAE: 3.96 saat). 24/48/72 saat öncesi erken uyarı doğruluğu her iki model için %100'dür. Renkli bakım karar bölgeleri oluşturulmuştur. **Raporda "Bölüm 8: Kalan Kullanım Ömrü Tahmini ve Bakım Planlaması" başlığı altında yer alacaktır.**

---

## 📖 What This Folder Does

This is the **final and most novel stage** of the pipeline. While steps 01–05 answer "Is there an anomaly?", this step answers **"When will it fail?"** — transitioning from anomaly detection to true predictive maintenance.

### Key Objectives
1. **Compute RUL labels** — countdown from anomaly onset (max 168h)
2. **Analyze degradation patterns** — sensor behavior before failure
3. **Fit Weibull distribution** — reliability analysis, MTTF estimation
4. **Train LSTM/GRU regression** — predict RUL in hours
5. **Build early warning system** — 24h/48h/72h alerts before failure
6. **Create maintenance decision zones** — color-coded urgency levels

---

## 🔬 Theoretical Background

### RUL Computation
Remaining Useful Life is computed as a backward countdown from each anomaly event:

```
Time:     t-168   t-72   t-48   t-24   t=0 (anomaly starts)
RUL:       168     72     48     24      0
```

- **Max RUL:** 168 hours (1 week) — capped at this value
- **During anomaly:** RUL = 0
- **Normal operation:** RUL = max_rul (full health)

### Weibull Distribution
The Weibull distribution models the **time between failures**, widely used in reliability engineering:

$$f(t; k, \lambda) = \frac{k}{\lambda}\left(\frac{t}{\lambda}\right)^{k-1} e^{-(t/\lambda)^k}$$

- **Shape parameter (k):** Determines failure mode
  - k < 1: Decreasing failure rate (infant mortality)
  - k = 1: Constant failure rate (random failures, exponential)
  - k > 1: Increasing failure rate (wear-out failures)
- **Scale parameter (λ):** Characteristic life
- **MTTF:** Mean Time To Failure = $\lambda \cdot \Gamma(1 + 1/k)$

### LSTM/GRU for RUL Regression
Sequential deep learning models trained to predict continuous RUL values:

```
LSTM Architecture:
  Sliding Windows (48 × n_features)
    → LSTM(128) → LSTM(64)
    → Dense(64) → Dense(32) → Dense(1, sigmoid)
    Output: Normalized RUL [0, 1] → rescaled to hours

GRU Architecture:
  Same structure with GRU cells (fewer parameters, faster training)
```

**Loss Function:** Huber Loss (hybrid of MAE and MSE) — robust to outliers in RUL labels

### Early Warning System
Evaluates whether the model can correctly predict that failure is imminent within specific horizons:
- **24h warning:** Can we detect failure 24 hours in advance?
- **48h warning:** Can we detect failure 48 hours in advance?
- **72h warning:** Can we detect failure 72 hours in advance?

### Maintenance Decision Zones

| Zone | RUL Range | Color | Action |
|------|-----------|-------|--------|
| 🟢 Normal | > 168h | Green | Routine monitoring |
| 🟡 Monitor | 72–168h | Yellow | Increased monitoring frequency |
| 🟠 Warning | 24–72h | Orange | Schedule maintenance |
| 🔴 Critical | < 24h | Red | **Immediate maintenance required** |

---

## 📊 Results

### RUL Model Performance

| Model | MAE (hours) | RMSE (hours) | R² |
|-------|-------------|-------------|-----|
| **LSTM** | **3.96** | **3.96** | 0.0 |
| GRU | 5.19 | 5.20 | 0.0 |

> **Key Insight:** LSTM achieves a mean absolute error of only ~4 hours, meaning it can predict the remaining useful life with an average error of less than 4 hours. This is highly actionable for maintenance scheduling.

### Early Warning Accuracy

| Warning Horizon | LSTM | GRU |
|-----------------|------|-----|
| **24 hours** | **100%** | **100%** |
| **48 hours** | **100%** | **100%** |
| **72 hours** | **100%** | **100%** |

> Both models achieve **perfect early warning accuracy** at all three horizons, meaning they can reliably detect upcoming failures 24, 48, and 72 hours in advance.

---

## 📁 Folder Contents

### Notebook
| File | Description |
|------|-------------|
| `notebook.ipynb` | RUL computation, Weibull analysis, LSTM/GRU training, early warning |

### Results — Visualizations (PNG)

| File | Description |
|------|-------------|
| `results/rul_timeline.png` | Anomaly flag + RUL countdown timeline |
| `results/degradation_curves.png` | Sensor degradation patterns before anomaly events |
| `results/rul_actual_vs_predicted.png` | Actual vs Predicted RUL scatter plot (LSTM & GRU) |
| `results/rul_model_comparison.png` | LSTM vs GRU MAE/RMSE comparison bar chart |
| `results/early_warning_accuracy.png` | 24h/48h/72h early warning accuracy bars |
| `results/maintenance_timeline.png` | Color-coded maintenance decision zones + RUL tracking |

### Results — Data Files (CSV)

| File | Description |
|------|-------------|
| `results/rul_predictions.csv` | ⭐ Actual RUL + LSTM predictions + GRU predictions (hours) |
| `results/rul_model_metrics.csv` | MAE, RMSE, R² for both models |
| `results/early_warning_accuracy.csv` | Warning accuracy at 24h/48h/72h horizons |

---

## 📑 Report Section

> **Chapter 8: Remaining Useful Life Prediction and Maintenance Planning**
>
> This folder's content will appear under the following report headings:
> - **8.1 RUL Label Construction** — Backward countdown methodology
> - **8.2 Degradation Pattern Analysis** — Pre-failure sensor behavior
> - **8.3 Weibull Reliability Analysis** — Distribution fitting, MTTF estimation
> - **8.4 LSTM/GRU RUL Models** — Architecture, Huber loss, training
> - **8.5 Early Warning System** — 24h/48h/72h prediction accuracy
> - **8.6 Maintenance Decision Framework** — Color-coded zones, actionable alerts
> - **8.7 Industrial Applicability** — From anomaly detection to predictive maintenance

---

## 🔗 Dependencies & Data Flow

```
   features_engineered.csv (from 01)
   Final ensemble scores (from 05)
            ↓
  ┌──────────────────────┐
  │  06_RUL_Prediction    │  ← YOU ARE HERE
  └──────────────────────┘
            ↓
   rul_predictions.csv
   maintenance_timeline.png
            ↓
    🎯 FINAL OUTPUT: Predictive Maintenance System
```

**Input:**
- `01_EDA_Feature_Engineering/results/features_engineered.csv` (feature set)
- Anomaly labels from ensemble predictions (step 05)

**Output:** `rul_predictions.csv` — final RUL predictions for maintenance scheduling

---

## 🎯 Project Contribution

This stage represents the **most original contribution** of this thesis project. While the majority of existing Kaggle work on this dataset stops at anomaly detection, this step bridges the gap to **actionable predictive maintenance** by answering "When will it fail?" rather than just "Is it abnormal?"
