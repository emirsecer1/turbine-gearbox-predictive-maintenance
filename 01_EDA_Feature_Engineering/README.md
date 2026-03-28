# 📊 01 — Exploratory Data Analysis & Feature Engineering

![Step](https://img.shields.io/badge/Pipeline_Step-01-blue)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Category](https://img.shields.io/badge/Category-EDA_&_Feature_Engineering-purple)
![Python](https://img.shields.io/badge/Python-3.10+-yellow)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-lightblue)
![Report Section](https://img.shields.io/badge/Report_Section-Chapter_3:_Data_Analysis-orange)

---

## 🇹🇷 Türkçe Özet

Bu klasör, 5 yıllık rüzgar türbini SCADA verilerinin keşifsel analizini ve özellik mühendisliğini içerir. Ham veri üzerinde eksik veri analizi, zaman serisi görselleştirme, korelasyon analizi, FFT frekans analizi ve mutual information tabanlı özellik önemi hesaplanır. Rolling (hareketli ortalama/standart sapma), lag (gecikmeli) ve Fourier özellikleri oluşturularak 7 orijinal özellikten 95 özellik üretilir. Çıktı olan `features_engineered.csv` tüm sonraki aşamalarda kullanılır. **Raporda "Bölüm 3: Veri Analizi ve Ön İşleme" başlığı altında yer alacaktır.**

---

## 📖 What This Folder Does

This is the **first stage** of the predictive maintenance pipeline. It performs comprehensive exploratory data analysis (EDA) on the 5-year wind turbine gearbox SCADA dataset and engineers advanced features that serve as input for all downstream models.

### Key Objectives
1. **Understand the data** — distribution, missing values, temporal patterns
2. **Visualize sensor behavior** — time series plots, anomaly timelines
3. **Analyze feature relationships** — correlation matrix, mutual information
4. **Engineer advanced features** — rolling statistics, lag features, Fourier components
5. **Quantify class imbalance** — normal vs. anomaly distribution

---

## 🔬 Theoretical Background

### Rolling Statistics
Rolling (moving) window features capture **local trends and volatility** in time series data:
- **Rolling Mean** (`window=24h, 48h, 168h`): Smooths out short-term noise, reveals underlying trends
- **Rolling Std** (`window=24h, 48h, 168h`): Measures local variability — sudden increases often precede anomalies

$$\mu_{roll}(t, w) = \frac{1}{w}\sum_{i=0}^{w-1} x_{t-i}, \quad \sigma_{roll}(t, w) = \sqrt{\frac{1}{w}\sum_{i=0}^{w-1}(x_{t-i} - \mu_{roll})^2}$$

### Lag Features
Lag features introduce **temporal dependencies** by including past values as separate features:
- `lag_1`: 1-hour delay — captures immediate short-term dynamics
- `lag_6, lag_12, lag_24`: Captures shift patterns and daily cycles

### Fourier Transform (FFT)
FFT decomposes time-domain signals into **frequency components**, revealing periodic patterns:
- Identifies dominant frequencies (e.g., daily/weekly cycles)
- Sin/cos harmonics (k=1,2,3) encode cyclical behavior as features

### Mutual Information
A non-parametric measure of dependency between features and the target variable, capturing **both linear and non-linear relationships** — more general than Pearson correlation.

---

## 📊 Results

### Dataset Overview

| Metric | Value |
|--------|-------|
| **Total Samples** | 262,800 (hourly, 5 years) |
| **Original Features** | 7 sensors |
| **Engineered Features** | 95 total |
| **Rolling Features** | 42 |
| **Lag Features** | 28 |
| **Fourier Features** | 18 |

### Class Distribution

| Class | Count | Percentage |
|-------|-------|------------|
| Normal (0) | 257,300 | 97.91% |
| Anomaly (1) | 5,500 | 2.09% |
| **Imbalance Ratio** | **~47:1** | Normal:Anomaly |

### Top-10 Features by Mutual Information

| Rank | Feature | MI Score |
|------|---------|----------|
| 1 | `vibration_y_roll_mean_168` | 0.0789 |
| 2 | `vibration_x_roll_mean_168` | 0.0789 |
| 3 | `vibration_z_roll_mean_168` | 0.0787 |
| 4 | `vibration_y_roll_mean_48` | 0.0764 |
| 5 | `vibration_x_roll_mean_48` | 0.0764 |
| 6 | `vibration_z_roll_mean_48` | 0.0764 |
| 7 | `vibration_y_roll_mean_24` | 0.0748 |
| 8 | `vibration_x_roll_mean_24` | 0.0746 |
| 9 | `vibration_z_roll_mean_24` | 0.0745 |
| 10 | `oil_pressure_roll_mean_168` | 0.0691 |

> **Key Insight:** Vibration rolling means (especially 168h window) are the most informative features, followed by oil pressure. Longer windows capture more discriminative patterns.

---

## 📁 Folder Contents

### Notebook
| File | Description |
|------|-------------|
| `notebook.ipynb` | Main EDA & feature engineering notebook |

### Results — Visualizations (PNG)

| File | Description |
|------|-------------|
| `results/missing_values.png` | Missing value percentage per feature |
| `results/sensor_time_series.png` | All sensor time series with anomaly periods highlighted in red |
| `results/correlation_matrix.png` | Feature correlation heatmap |
| `results/anomaly_timeline.png` | 5-year anomaly timeline + monthly anomaly density |
| `results/rolling_features.png` | Rolling mean/std comparison (24h, 48h, 168h windows) |
| `results/lag_autocorrelation.png` | Autocorrelation function (ACF) plot |
| `results/fft_analysis.png` | Time-domain and frequency-domain (FFT) analysis |
| `results/feature_importance_mutual_info.png` | Top-20 features ranked by mutual information |
| `results/class_imbalance.png` | Class distribution (pie + bar chart) |

### Results — Data Files (CSV)

| File | Description |
|------|-------------|
| `results/features_engineered.csv` | ⭐ Full engineered feature set (262,800 × 97) — **main output** |
| `results/feature_engineering_summary.csv` | Feature counts by type + anomaly ratio |
| `results/mutual_info_scores.csv` | MI scores for all features (sorted descending) |
| `results/class_distribution.csv` | Normal/Anomaly sample counts and percentages |

---

## 📑 Report Section

> **Chapter 3: Data Analysis and Preprocessing**
>
> This folder's content will appear under the following report headings:
> - **3.1 Dataset Description** — Source, size, sensors, time range
> - **3.2 Exploratory Data Analysis** — Missing values, time series, correlations
> - **3.3 Feature Engineering** — Rolling, lag, Fourier feature construction
> - **3.4 Feature Selection** — Mutual information analysis, top features
> - **3.5 Class Imbalance Analysis** — Distribution, implications for modeling

---

## 🔗 Dependencies & Data Flow

```
Raw SCADA Data (Kaggle)
        ↓
  ┌─────────────────────┐
  │  01_EDA_Feature_Eng  │  ← YOU ARE HERE
  └─────────┬───────────┘
            ↓
   features_engineered.csv
            ↓
  ┌─────────┼─────────┐
  ↓         ↓         ↓
 [02]      [03]      [04]
```

**Input:** Raw SCADA CSV from Kaggle  
**Output:** `features_engineered.csv` → used by steps 02, 03, 04, 05, 06
