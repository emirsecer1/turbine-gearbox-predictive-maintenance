# 🧠 04 — Time Series Deep Learning

![Step](https://img.shields.io/badge/Pipeline_Step-04-blue)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Category](https://img.shields.io/badge/Category-Deep_Learning-purple)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)
![LSTM](https://img.shields.io/badge/LSTM-Recurrent-red)
![TCN](https://img.shields.io/badge/TCN-Convolutional-green)
![Transformer](https://img.shields.io/badge/Transformer-Attention-yellow)
![Report Section](https://img.shields.io/badge/Report_Section-Chapter_6:_Deep_Learning-orange)

---

## 🇹🇷 Türkçe Özet

Bu klasör, zaman serisi bağımlılıklarını modelleyen üç derin öğrenme mimarisi ile anomali tespiti gerçekleştirir: LSTM, TCN (Temporal Convolutional Network) ve Transformer Encoder. 48 saatlik (2 günlük) kayan pencere yaklaşımı kullanılır. En iyi performansı TCN modeli göstermiştir (F1: 0.445, ROC-AUC: 0.867). Eğitilmiş modeller `.h5` formatında kaydedilmiştir. Transformer en yüksek ROC-AUC'a (0.903) sahipken, TCN en dengeli metrikleri sunar. **Raporda "Bölüm 6: Derin Öğrenme ile Zaman Serisi Anomali Tespiti" başlığı altında yer alacaktır.**

---

## 📖 What This Folder Does

This stage leverages **deep learning architectures** specifically designed for sequential/temporal data to capture complex patterns that classical ML models may miss. Three state-of-the-art architectures are trained and compared.

### Key Objectives
1. **Capture temporal dependencies** — use sliding window approach
2. **Train 3 deep architectures** — LSTM, TCN, Transformer
3. **Handle class imbalance** — class-weighted loss function
4. **Save trained models** — `.h5` format for deployment/ensemble use
5. **Compare training dynamics** — learning curves, convergence behavior

---

## 🔬 Theoretical Background

### Sliding Window Approach
Time series data is converted to supervised learning by creating overlapping windows:
- **Window size:** 48 timesteps (2 days of hourly data)
- **Stride:** 1 (maximum overlap for data efficiency)
- **Shape:** `(batch, 48, n_features)` → binary classification output

### LSTM (Long Short-Term Memory)
A recurrent architecture that addresses the vanishing gradient problem using gating mechanisms:

$$f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)$$ *(forget gate)*
$$i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i)$$ *(input gate)*
$$o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o)$$ *(output gate)*

```
Architecture:
  Input (48, n_features)
    → LSTM(128, return_sequences=True, dropout=0.3)
    → LSTM(64, return_sequences=False, dropout=0.3)
    → Dense(64, relu) + BatchNorm + Dropout(0.3)
    → Dense(32, relu)
    → Dense(1, sigmoid)
```

### TCN (Temporal Convolutional Network)
Uses **dilated causal convolutions** with residual connections to achieve a large receptive field without recurrence:

```
Architecture:
  Input (48, n_features)
    → 4× ResidualBlock(filters=64, kernel=3, dilation=2^i)
       [Conv1D → BatchNorm → ReLU → SpatialDropout(0.2)] × 2
       + Residual connection
    → GlobalAveragePooling1D
    → Dense(64, relu) + Dropout(0.3)
    → Dense(1, sigmoid)

  Dilations: 1, 2, 4, 8 → Receptive field = 48 timesteps
```

**Advantage:** Parallelizable (vs. sequential LSTM), captures long-range dependencies.

### Transformer Encoder
Uses **multi-head self-attention** to capture dependencies between any two time steps regardless of distance:

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

```
Architecture:
  Input (48, n_features)
    → Dense(d_model=64) [Feature projection]
    → + PositionalEncoding (sinusoidal)
    → 2× TransformerBlock(heads=4, ff_dim=128, dropout=0.1)
       [MultiHeadAttention → Add+Norm → FFN → Add+Norm]
    → GlobalAveragePooling1D
    → Dense(64, relu) + Dropout
    → Dense(1, sigmoid)
```

### Training Configuration

| Parameter | Value |
|-----------|-------|
| Window size | 48 (2 days) |
| Stride | 1 |
| Batch size | 256 |
| Optimizer | Adam (lr=1e-3) |
| Loss | Binary Crossentropy |
| Class weighting | pos_weight = n_normal / n_anomaly |
| Early stopping | patience=10, monitor val_loss |
| LR scheduler | ReduceLROnPlateau(factor=0.5, patience=5) |
| Max epochs | 50 |

---

## 📊 Results

### Model Performance Comparison

| Model | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|-------|-----------|--------|----|---------|--------|
| LSTM | 0.155 | **0.993** | 0.267 | 0.591 | 0.085 |
| **TCN** | **0.362** | 0.578 | **0.445** | 0.867 | **0.601** |
| Transformer | 0.217 | 0.996 | 0.357 | **0.903** | 0.516 |

> **Key Insights:**
> - **TCN** achieves the best balanced performance (highest F1 and PR-AUC)
> - **Transformer** has the highest ROC-AUC (0.903) but lower precision
> - **LSTM** achieves near-perfect recall (99.3%) but very low precision → high false positive rate
> - TCN's dilated convolutions effectively capture the temporal patterns in this dataset

### Saved Models

| File | Size | Description |
|------|------|-------------|
| `lstm_best.h5` | 2.1 MB | Best LSTM weights (early stopping) |
| `tcn_best.h5` | 1.5 MB | Best TCN weights (early stopping) |
| `transformer_best.h5` | 1.1 MB | Best Transformer weights (early stopping) |

---

## 📁 Folder Contents

### Notebook
| File | Description |
|------|-------------|
| `notebook.ipynb` | Deep learning model training, evaluation, and comparison |

### Results — Visualizations (PNG)

| File | Description |
|------|-------------|
| `results/training_histories.png` | Training/validation loss curves for all 3 models |
| `results/dl_roc_pr_curves.png` | ROC and PR curves for LSTM, TCN, Transformer |
| `results/dl_model_comparison.png` | Metric comparison heatmap |

### Results — Model Files (H5)

| File | Description |
|------|-------------|
| `results/lstm_best.h5` | ⭐ Best LSTM model weights (Keras format) |
| `results/tcn_best.h5` | ⭐ Best TCN model weights (Keras format) |
| `results/transformer_best.h5` | ⭐ Best Transformer model weights (Keras format) |

### Results — Data Files (CSV)

| File | Description |
|------|-------------|
| `results/dl_model_metrics.csv` | Precision/Recall/F1/ROC-AUC/PR-AUC per model |
| `results/dl_test_predictions.csv` | ⭐ Test set predictions — all model probabilities + true labels |
| `results/training_history_lstm.csv` | LSTM epoch-by-epoch training metrics |
| `results/training_history_tcn.csv` | TCN epoch-by-epoch training metrics |
| `results/training_history_transformer.csv` | Transformer epoch-by-epoch training metrics |

---

## 📑 Report Section

> **Chapter 6: Deep Learning-Based Anomaly Detection**
>
> This folder's content will appear under the following report headings:
> - **6.1 Sliding Window Preprocessing** — Window size selection, data preparation
> - **6.2 LSTM Architecture** — Recurrent approach, gating mechanisms
> - **6.3 TCN Architecture** — Dilated causal convolutions, residual blocks
> - **6.4 Transformer Encoder** — Self-attention mechanism, positional encoding
> - **6.5 Training Strategy** — Class weighting, early stopping, learning rate scheduling
> - **6.6 Results and Comparison** — Performance metrics, training curves
> - **6.7 Discussion** — TCN vs LSTM vs Transformer trade-offs

---

## 🔗 Dependencies & Data Flow

```
   features_engineered.csv (from 01)
            ↓
  ┌──────────────────────────────┐
  │  04_TimeSeries_DeepLearning   │  ← YOU ARE HERE
  └─────────┬────────────────────┘
            ↓
   dl_test_predictions.csv + .h5 models
            ↓
         [05] Hybrid Ensemble (deep learning signals)
```

**Input:** `01_EDA_Feature_Engineering/results/features_engineered.csv`  
**Output:** `dl_test_predictions.csv` + saved `.h5` models → used by step 05 (Hybrid Ensemble)
