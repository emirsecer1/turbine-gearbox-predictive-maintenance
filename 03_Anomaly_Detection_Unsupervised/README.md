# 🔍 03 — Unsupervised Anomaly Detection

![Step](https://img.shields.io/badge/Pipeline_Step-03-blue)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Category](https://img.shields.io/badge/Category-Unsupervised_Learning-purple)
![Isolation Forest](https://img.shields.io/badge/Isolation_Forest-Anomaly-red)
![Autoencoder](https://img.shields.io/badge/Autoencoder-Neural_Net-yellow)
![Report Section](https://img.shields.io/badge/Report_Section-Chapter_5:_Unsupervised_Anomaly-orange)

---

## 🇹🇷 Türkçe Özet

Bu klasör, etiket kullanmadan (unsupervised) anomali tespiti gerçekleştirir. Dört farklı yöntem uygulanır: Isolation Forest, One-Class SVM, Local Outlier Factor (LOF) ve Autoencoder. Tüm yöntemlerin anomali skorları [0,1] aralığına normalize edilerek karşılaştırılır. En iyi sonuçlar One-Class SVM (ROC-AUC: 0.9999) ve Isolation Forest (ROC-AUC: 0.9997) ile elde edilmiştir. Isolation Forest ve Autoencoder skorları, 05_Hybrid_Ensemble aşamasına girdi olarak aktarılır. **Raporda "Bölüm 5: Etiketsiz Anomali Tespiti Yöntemleri" başlığı altında yer alacaktır.**

---

## 📖 What This Folder Does

This stage applies **label-free anomaly detection** methods to identify gearbox anomalies without relying on supervised labels. Four fundamentally different algorithms are compared, each with a unique approach to defining "normality."

### Key Objectives
1. **Detect anomalies without labels** — unsupervised paradigm
2. **Compare 4 distinct methods** — tree-based, kernel-based, density-based, neural
3. **Generate continuous anomaly scores** — normalized to [0,1]
4. **Identify sensor contributions** — which sensors drive anomaly scores
5. **Provide unsupervised signals** for the hybrid ensemble (step 05)

---

## 🔬 Theoretical Background

### Isolation Forest (IF)
Isolates anomalies by randomly partitioning the feature space with decision trees. Anomalies require **fewer splits** to be isolated, resulting in shorter average path lengths:

$$s(x, n) = 2^{-\frac{E[h(x)]}{c(n)}}$$

where $h(x)$ is the path length and $c(n)$ is the average path length for a dataset of size $n$.

- **Advantage:** Fast, scalable, parallelizable
- **Best for:** General-purpose anomaly detection on large datasets

### One-Class SVM (OC-SVM)
Maps data to a high-dimensional feature space using a kernel function (RBF) and finds a hyperplane that maximally separates normal data from the origin:

$$\min_{w,\xi,\rho} \frac{1}{2}\|w\|^2 + \frac{1}{\nu n}\sum_i \xi_i - \rho$$

- **Advantage:** Strong boundary definition with kernel trick
- **Best for:** Small-to-medium datasets with clear normal clusters

### Local Outlier Factor (LOF)
Compares the local density of each point to its $k$ nearest neighbors. Points in significantly lower-density regions are flagged as outliers:

$$LOF_k(x) = \frac{\sum_{o \in N_k(x)} \frac{lrd_k(o)}{lrd_k(x)}}{|N_k(x)|}$$

- **Advantage:** Detects local anomalies in clustered data
- **Best for:** Datasets with varying density regions

### Autoencoder (Neural Network)
An encoder-decoder architecture trained on **normal data only**. Anomalies produce high reconstruction error because the network has not learned their patterns:

$$\text{Anomaly Score} = \|x - \hat{x}\|^2 = MSE(x, Decoder(Encoder(x)))$$

- **Advantage:** Learns complex nonlinear patterns from multi-sensor data
- **Best for:** Time series with complex temporal dependencies

---

## 📊 Results

### Method Comparison

| Method | ROC-AUC | PR-AUC |
|--------|---------|--------|
| **One-Class SVM** | **0.9999** | **0.9965** |
| Isolation Forest | 0.9997 | 0.9946 |
| LOF (k=20) | 0.9992 | 0.9585 |
| Autoencoder | 0.9916 | 0.8605 |

> **Key Insight:** All unsupervised methods achieve very high ROC-AUC (>0.99), demonstrating that anomalies in this dataset have strong separability in feature space. One-Class SVM and Isolation Forest lead the ranking.

### Method Trade-offs

| Method | Advantage | Disadvantage | Scalability |
|--------|-----------|-------------|-------------|
| **Isolation Forest** | Fast, parallelizable | Assumes global anomaly structure | ✅ Excellent |
| **One-Class SVM** | Strong boundary, best AUC | Slow on large data, kernel selection | ⚠️ Limited |
| **LOF** | Captures local density patterns | Degrades in high dimensions | ⚠️ Moderate |
| **Autoencoder** | Learns complex temporal patterns | Training time, hyperparameter sensitive | ✅ Good |

---

## 📁 Folder Contents

### Notebook
| File | Description |
|------|-------------|
| `notebook.ipynb` | Unsupervised anomaly detection training and evaluation |

### Results — Visualizations (PNG)

| File | Description |
|------|-------------|
| `results/anomaly_score_distributions.png` | Normal vs anomaly score histograms for each method (4 subplots) |
| `results/unsupervised_roc_pr.png` | ROC and PR curves comparison for all 4 methods |
| `results/autoencoder_training.png` | Autoencoder training/validation loss curve |
| `results/sensor_anomaly_contribution.png` | Sensor-to-anomaly-score correlation (which sensors contribute most) |
| `results/unsupervised_comparison.png` | ROC-AUC and PR-AUC bar chart comparison |

### Results — Data Files (CSV)

| File | Description |
|------|-------------|
| `results/all_anomaly_scores.csv` | ⭐ IF + Autoencoder anomaly scores + true labels (full dataset) |
| `results/unsupervised_comparison.csv` | ROC-AUC and PR-AUC per method |

---

## 📑 Report Section

> **Chapter 5: Unsupervised Anomaly Detection Methods**
>
> This folder's content will appear under the following report headings:
> - **5.1 Motivation for Unsupervised Approaches** — Label scarcity in industrial settings
> - **5.2 Isolation Forest** — Algorithm description, contamination tuning
> - **5.3 One-Class SVM** — Kernel selection, training on normal data
> - **5.4 Local Outlier Factor** — Density-based anomaly detection
> - **5.5 Autoencoder** — Architecture, reconstruction error-based scoring
> - **5.6 Comparison and Analysis** — ROC/PR curves, score distributions
> - **5.7 Sensor Contribution Analysis** — Which sensors drive anomaly detection

---

## 🔗 Dependencies & Data Flow

```
   features_engineered.csv (from 01)
            ↓
  ┌──────────────────────────────────┐
  │  03_Anomaly_Detection_Unsupervised│  ← YOU ARE HERE
  └─────────┬────────────────────────┘
            ↓
   all_anomaly_scores.csv
            ↓
         [05] Hybrid Ensemble (unsupervised signals)
```

**Input:** `01_EDA_Feature_Engineering/results/features_engineered.csv`  
**Output:** `all_anomaly_scores.csv` → used by step 05 (Hybrid Ensemble for IF + AE signals)
