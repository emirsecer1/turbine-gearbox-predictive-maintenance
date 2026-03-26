# 04 — Time Series Deep Learning: Results

Bu klasör, `04_TimeSeries_DeepLearning/notebook.ipynb` çalıştırıldıktan sonra oluşturulan görsel ve çıktıları içerir.

## Beklenen Çıktılar

### Görseller (PNG)

| Dosya | Açıklama |
|-------|----------|
| `training_histories.png` | LSTM, TCN, Transformer için eğitim/validasyon loss grafikleri |
| `dl_roc_pr_curves.png` | Derin öğrenme modellerinin ROC ve PR eğrileri |
| `dl_model_comparison.png` | Metrik karşılaştırma ısı haritası |

### Model Dosyaları

| Dosya | Açıklama |
|-------|----------|
| `lstm_best.h5` | En iyi LSTM model ağırlıkları |
| `tcn_best.h5` | En iyi TCN model ağırlıkları |
| `transformer_best.h5` | En iyi Transformer model ağırlıkları |

## Model Mimarileri

### LSTM (Long Short-Term Memory)
```
Input (48, n_features)
  → LSTM(128, return_sequences=True, dropout=0.3)
  → LSTM(64, return_sequences=False, dropout=0.3)
  → Dense(64, relu) + BatchNorm + Dropout(0.3)
  → Dense(32, relu)
  → Dense(1, sigmoid)
```
**Parametre sayısı:** ~200K (n_features'a bağlı)

### TCN (Temporal Convolutional Network)
```
Input (48, n_features)
  → 4× ResidualBlock(filters=64, kernel=3, dilation=2^i, SpatialDropout=0.2)
  → GlobalAveragePooling1D
  → Dense(64, relu) + Dropout(0.3)
  → Dense(1, sigmoid)
```
**Dilations:** 1, 2, 4, 8 → Effective receptive field = 48 timesteps

### Transformer Encoder
```
Input (48, n_features)
  → Dense(d_model=64)  [Feature projection]
  → + PositionalEncoding
  → 2× TransformerBlock(heads=4, ff_dim=128, dropout=0.1)
     (MultiHeadAttention → Add+Norm → FFN → Add+Norm)
  → GlobalAveragePooling1D
  → Dense(64, relu) + Dropout
  → Dense(1, sigmoid)
```

## Eğitim Konfigürasyonu

| Parametre | Değer |
|-----------|-------|
| Window size | 48 (saatlik veri için 2 gün) |
| Stride | 1 |
| Batch size | 256 |
| Optimizer | Adam (lr=1e-3) |
| Loss | Binary Crossentropy |
| Class weighting | pos_weight = n_normal / n_anomaly |
| Early stopping | patience=10, val_loss monitored |
| LR scheduler | ReduceLROnPlateau(factor=0.5, patience=5) |
| Max epochs | 50 |

## Beklenen Performans

| Model | F1 | ROC-AUC | PR-AUC | Eğitim Süresi |
|-------|-----|---------|--------|---------------|
| LSTM | TBD | TBD | TBD | ~GPU: 10-20 dk |
| TCN | TBD | TBD | TBD | ~GPU: 5-10 dk |
| Transformer | TBD | TBD | TBD | ~GPU: 8-15 dk |

## Sonraki Adım

Bu notebook'un en iyi modeli (`04_best_model`) şu amaçlarla kullanılır:
- `05_Hybrid_Ensemble` — stacking ensemble için temel model
