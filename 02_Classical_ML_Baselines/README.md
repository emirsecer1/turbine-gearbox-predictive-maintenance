# 🤖 02 — Classical Machine Learning Baselines

![Step](https://img.shields.io/badge/Pipeline_Step-02-blue)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Category](https://img.shields.io/badge/Category-Supervised_ML-purple)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-red)
![XGBoost](https://img.shields.io/badge/XGBoost-Boosting-green)
![LightGBM](https://img.shields.io/badge/LightGBM-Boosting-yellowgreen)
![Report Section](https://img.shields.io/badge/Report_Section-Chapter_4:_Classical_ML-orange)

---

## 🇹🇷 Türkçe Özet

Bu klasör, mühendislenmiş özellik seti üzerinde dört klasik makine öğrenmesi modeli (Random Forest, XGBoost, LightGBM, Logistic Regression) ile anomali sınıflandırması yapar. Zaman serisi verilerinde veri sızıntısını önlemek için kronolojik (temporal) bölme kullanılır. SMOTE ile sınıf dengesizliği giderilir (yalnızca eğitim setinde). F1 skorunu maksimize eden threshold optimizasyonu yapılır. En iyi model XGBoost (ROC-AUC: 0.823), optimize threshold ile en iyi F1 Random Forest'tır (F1: 0.545). **Raporda "Bölüm 4: Klasik Makine Öğrenmesi ile Anomali Tespiti" başlığı altında yer alacaktır.**

---

## 📖 What This Folder Does

This is the **supervised learning baseline** stage. It trains four classical machine learning models for binary anomaly classification, establishes benchmark performance metrics, and identifies the most important features using model-native importance measures.

### Key Objectives
1. **Temporal train/test split** — prevent data leakage in time series
2. **Handle class imbalance** — SMOTE oversampling on training set only
3. **Train 4 classifiers** — RF, XGBoost, LightGBM, Logistic Regression
4. **Optimize decision thresholds** — maximize F1 score per model
5. **Extract feature importance** — identify top predictive features

---

## 🔬 Theoretical Background

### Temporal Split (vs Random Split)
In time series data, random shuffling causes **data leakage** — future observations leak into training. The temporal split preserves chronological order:
- **Train:** First 80% of data (chronologically)
- **Test:** Last 20% (future data)

### SMOTE (Synthetic Minority Over-sampling Technique)
Addresses class imbalance (97.9% normal vs 2.1% anomaly) by generating synthetic minority class samples via k-nearest-neighbor interpolation:

$$x_{new} = x_i + \lambda \cdot (x_{nn} - x_i), \quad \lambda \sim U(0,1)$$

> ⚠️ **SMOTE is applied ONLY to the training set** to prevent optimistic bias on the test set.

### Random Forest
An ensemble of decision trees trained on bootstrap samples with random feature subsets. Reduces variance through bagging while maintaining low bias.

### XGBoost / LightGBM
Gradient boosting frameworks that sequentially add weak learners to minimize a differentiable loss function. XGBoost uses level-wise growth; LightGBM uses leaf-wise growth for faster training.

### Threshold Optimization
Default threshold (0.5) is suboptimal for imbalanced datasets. The optimal threshold maximizes the F1 score:

$$\text{threshold}^* = \arg\max_{\tau} F_1(\tau)$$

---

## 📊 Results

### Model Performance (Default Threshold = 0.5)

| Model | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|-------|-----------|--------|----|---------|--------|
| Random Forest | 0.000 | 0.000 | 0.000 | 0.472 | 0.417 |
| **XGBoost** | 0.000 | 0.000 | 0.000 | **0.823** | 0.190 |
| LightGBM | 0.000 | 0.000 | 0.000 | 0.661 | 0.152 |
| Logistic Regression | 1.000 | 0.012 | 0.023 | 0.302 | 0.223 |

### Model Performance (Optimized Threshold)

| Model | Threshold | Precision | Recall | F1 (opt) | ROC-AUC |
|-------|-----------|-----------|--------|----------|---------|
| **Random Forest** | **0.18** | **0.999** | **0.375** | **0.545** | 0.472 |
| XGBoost | 0.50 | 0.000 | 0.000 | 0.000 | 0.823 |
| LightGBM | 0.50 | 0.000 | 0.000 | 0.000 | 0.661 |
| Logistic Regression | 0.05 | 1.000 | 0.024 | 0.048 | 0.302 |

### Top-5 Feature Importance

**Random Forest:**
| Feature | Importance |
|---------|-----------|
| `oil_pressure_roll_std_24` | 0.119 |
| `oil_pressure_roll_std_48` | 0.118 |
| `gearbox_oil_temp_roll_std_48` | 0.107 |
| `gearbox_oil_temp_roll_mean_24` | 0.099 |
| `gearbox_oil_temp_roll_std_24` | 0.074 |

**XGBoost:**
| Feature | Importance |
|---------|-----------|
| `oil_pressure_roll_std_24` | 0.991 |
| `particle_count` | 0.002 |
| `oil_pressure_lag_1` | 0.002 |
| `oil_pressure` | 0.001 |
| `particle_count_lag_1` | 0.001 |

> **Key Insight:** Oil pressure rolling standard deviation (24h window) is overwhelmingly the most important feature across all tree-based models. Temperature rolling statistics follow closely.

---

## 📁 Folder Contents

### Notebook
| File | Description |
|------|-------------|
| `notebook.ipynb` | Classical ML training, evaluation, and comparison notebook |

### Results — Visualizations (PNG)

| File | Description |
|------|-------------|
| `results/smote_balancing.png` | Class distribution before and after SMOTE |
| `results/confusion_matrices.png` | 2×2 confusion matrices for all 4 models |
| `results/roc_pr_curves.png` | ROC and Precision-Recall curves for all models |
| `results/threshold_optimization.png` | Threshold vs F1 score curve per model |
| `results/feature_importance_models.png` | Top-20 feature importance for RF, XGBoost, LightGBM |
| `results/model_comparison.png` | Metric comparison heatmap across all models |

### Results — Data Files (CSV)

| File | Description |
|------|-------------|
| `results/model_metrics.csv` | Precision/Recall/F1/ROC-AUC/PR-AUC (threshold=0.5) |
| `results/model_metrics_optimized_threshold.csv` | Metrics with F1-maximizing threshold |
| `results/feature_importance_random_forest.csv` | RF feature importances (all features, sorted) |
| `results/feature_importance_xgboost.csv` | XGBoost feature importances |
| `results/feature_importance_lightgbm.csv` | LightGBM feature importances |
| `results/test_predictions.csv` | ⭐ Test set predictions — all model probabilities + true labels |

---

## 📑 Report Section

> **Chapter 4: Anomaly Detection with Classical Machine Learning**
>
> This folder's content will appear under the following report headings:
> - **4.1 Experimental Setup** — Temporal split, SMOTE, class weighting
> - **4.2 Model Descriptions** — RF, XGBoost, LightGBM, Logistic Regression
> - **4.3 Evaluation Metrics** — Precision, Recall, F1, ROC-AUC, PR-AUC
> - **4.4 Threshold Optimization** — F1-maximizing threshold analysis
> - **4.5 Feature Importance Analysis** — Top features per model
> - **4.6 Baseline Results Discussion** — Performance comparison, limitations

---

## 🔗 Dependencies & Data Flow

```
   features_engineered.csv (from 01)
            ↓
  ┌──────────────────────────┐
  │  02_Classical_ML_Baselines│  ← YOU ARE HERE
  └─────────┬────────────────┘
            ↓
   test_predictions.csv
            ↓
         [05] Hybrid Ensemble (stacking base model)
```

**Input:** `01_EDA_Feature_Engineering/results/features_engineered.csv`  
**Output:** `test_predictions.csv` → used by step 05 (Hybrid Ensemble)
