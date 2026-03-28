# 🏆 05 — Hybrid Ensemble & Explainability

![Step](https://img.shields.io/badge/Pipeline_Step-05-blue)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Category](https://img.shields.io/badge/Category-Ensemble_&_XAI-purple)
![Stacking](https://img.shields.io/badge/Stacking-Meta_Learner-red)
![SHAP](https://img.shields.io/badge/SHAP-Explainability-green)
![LIME](https://img.shields.io/badge/LIME-Local_Explanation-yellowgreen)
![Report Section](https://img.shields.io/badge/Report_Section-Chapter_7:_Ensemble_&_Explainability-orange)

---

## 🇹🇷 Türkçe Özet

Bu klasör, önceki tüm aşamalardaki modelleri birleştirerek en yüksek performansı elde etmeyi ve kararları açıklamayı hedefler. Üç farklı topluluk stratejisi uygulanır: Stacking (meta-öğrenici olarak Logistic Regression), Soft Voting (eşit ve AUC ağırlıklı) ve Unsupervised+Supervised hibrit yaklaşım. SHAP ile küresel özellik katkıları ve LIME ile bireysel tahmin açıklamaları üretilir. Unsupervised yöntemler son derece yüksek performans göstermiştir: IF (ROC-AUC: 0.9997), OC-SVM (ROC-AUC: 0.9999). **Raporda "Bölüm 7: Topluluk Öğrenmesi ve Açıklanabilir Yapay Zeka" başlığı altında yer alacaktır.**

---

## 📖 What This Folder Does

This is the **integration and explainability** stage. It combines predictions from all previous models (classical ML, unsupervised, deep learning) into a single powerful ensemble, and then uses SHAP and LIME to explain what drives the model's decisions.

### Key Objectives
1. **Combine all model predictions** — stacking, voting, hybrid approaches
2. **Maximize overall performance** — leverage strengths of different paradigms
3. **Explain model decisions** — SHAP (global) and LIME (local) explainability
4. **Analyze temporal patterns** — which sensors matter in which seasons
5. **Generate final anomaly scores** — aggregated ensemble predictions

---

## 🔬 Theoretical Background

### Stacking Ensemble
A two-level learning architecture where base model predictions become features for a meta-learner:

```
Level 0 (Base Models):
  [RF proba] ──┐
  [XGB proba] ─┤→ Meta-feature matrix
  [LGB proba] ─┘

Level 1 (Meta-Learner):
  Meta-features → Logistic Regression → Final prediction
```

Training uses **Out-of-Fold (OOF) predictions** with TimeSeriesSplit (5 folds) to prevent data leakage.

### Soft Voting
Combines model probabilities through weighted averaging:

$$P_{ensemble}(x) = \frac{\sum_{i=1}^{M} w_i \cdot P_i(x)}{\sum_{i=1}^{M} w_i}$$

- **Uniform voting:** $w_i = 1$ for all models
- **AUC-weighted voting:** $w_i = \text{ROC-AUC}_i$ (better models get higher weight)

### Unsupervised + Supervised Hybrid
Extends stacking by incorporating unsupervised anomaly scores as additional meta-features:

```
  [RF proba]  ──┐
  [XGB proba] ──┤
  [LGB proba] ──┤→ Extended meta-features → Meta-learner → Final
  [IF score]  ──┤
  [AE score]  ──┘
```

This captures both supervised decision boundaries and unsupervised distributional anomalies.

### SHAP (SHapley Additive exPlanations)
Based on cooperative game theory, SHAP assigns each feature an importance value for each prediction:

$$\phi_i = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!(|N|-|S|-1)!}{|N|!}[f(S \cup \{i\}) - f(S)]$$

- **Global:** Summary plots show overall feature contributions
- **Temporal:** Monthly SHAP values reveal seasonal sensor patterns

### LIME (Local Interpretable Model-agnostic Explanations)
Creates a local linear approximation around individual predictions:

$$\xi(x) = \arg\min_{g \in G} \mathcal{L}(f, g, \pi_x) + \Omega(g)$$

Explains **why** a specific instance was classified as anomaly or normal.

---

## 📊 Results

### Unsupervised Model Performance (in Ensemble Context)

| Method | ROC-AUC | PR-AUC |
|--------|---------|--------|
| **One-Class SVM** | **0.9999** | **0.9990** |
| Isolation Forest | 0.9997 | 0.9946 |
| LOF | 0.9994 | 0.9690 |
| Autoencoder | 0.9981 | 0.9425 |

> **Key Insight:** When re-evaluated in the ensemble context, all unsupervised methods maintain extremely high ROC-AUC (>0.998). The ensemble framework further improves PR-AUC for OC-SVM from 0.9965 to 0.9990.

---

## 📁 Folder Contents

### Notebook
| File | Description |
|------|-------------|
| `notebook.ipynb` | Ensemble construction, SHAP/LIME explainability analysis |

### Results — Visualizations (PNG)

| File | Description |
|------|-------------|
| `results/anomaly_score_distributions.png` | Anomaly score distributions per method in ensemble |
| `results/unsupervised_roc_pr.png` | ROC and PR curves for ensemble models |
| `results/autoencoder_training.png` | Autoencoder training/validation loss in ensemble context |
| `results/sensor_anomaly_contribution.png` | Sensor contribution to final anomaly scores |
| `results/unsupervised_comparison.png` | Performance bar chart comparison |

### Results — Data Files (CSV)

| File | Description |
|------|-------------|
| `results/all_anomaly_scores.csv` | ⭐ Final ensemble anomaly scores (IF + AE + true labels) |
| `results/unsupervised_scores.csv` | IF + AE scores for downstream use |
| `results/unsupervised_comparison.csv` | Performance metrics per unsupervised method |

---

## 📑 Report Section

> **Chapter 7: Ensemble Learning and Explainable AI**
>
> This folder's content will appear under the following report headings:
> - **7.1 Ensemble Strategies** — Stacking, Soft Voting, Hybrid
> - **7.2 Stacking with Meta-Learner** — OOF predictions, LogReg meta-learner
> - **7.3 Voting Methods** — Uniform vs AUC-weighted probability averaging
> - **7.4 Supervised + Unsupervised Hybrid** — IF/AE score integration
> - **7.5 SHAP Analysis** — Global feature importance, temporal patterns
> - **7.6 LIME Analysis** — Local instance-level explanations
> - **7.7 Final Model Comparison** — All models side-by-side, best model selection

---

## 🔗 Dependencies & Data Flow

```
   test_predictions.csv (from 02)
   all_anomaly_scores.csv (from 03)
   dl_test_predictions.csv (from 04)
            ↓
  ┌──────────────────────┐
  │  05_Hybrid_Ensemble   │  ← YOU ARE HERE
  └─────────┬────────────┘
            ↓
   Final ensemble scores
            ↓
         [06] RUL Prediction
```

**Input:**
- `02_Classical_ML_Baselines/results/test_predictions.csv` (supervised probabilities)
- `03_Anomaly_Detection_Unsupervised/results/all_anomaly_scores.csv` (unsupervised scores)
- `04_TimeSeries_DeepLearning/results/dl_test_predictions.csv` (deep learning probabilities)

**Output:** `all_anomaly_scores.csv`, `unsupervised_scores.csv` → used by step 06 (RUL Prediction)
