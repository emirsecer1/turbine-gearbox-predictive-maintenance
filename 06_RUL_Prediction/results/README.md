# 06 — RUL Prediction: Results

Bu klasör, `06_RUL_Prediction/notebook.ipynb` çalıştırıldıktan sonra oluşturulan görsel ve çıktıları içerir.

## Beklenen Çıktılar

### Görseller (PNG)

| Dosya | Açıklama |
|-------|----------|
| `rul_timeline.png` | Anomali bayrağı + RUL geri sayım timeline |
| `degradation_curves.png` | Anomali olaylarından önceki sensör degradasyon eğrileri |
| `weibull_fit.png` | Arızalar arası süre histogramı + Weibull fit + Reliability function |
| `rul_actual_vs_predicted.png` | LSTM ve GRU için Actual vs Predicted RUL scatter plot |
| `early_warning_accuracy.png` | 24h/48h/72h erken uyarı doğruluk bar grafikleri |
| `maintenance_timeline.png` | Renklendirilmiş bakım karar bölgeleri + RUL takip grafiği |
| `rul_model_comparison.png` | LSTM vs GRU MAE/RMSE karşılaştırması |

## RUL Tahmin Metodolojisi

### Adım 1: RUL Hesaplama
Her anomali olayından önce geriye doğru geri sayım yapılır:

```
Zaman:  t-168  t-72  t-48  t-24  t-0(anomali başlar)
RUL:     168    72    48    24      0
```

- **Maksimum RUL:** 168 saat (1 hafta) — bunun ötesinde max_rul ile sınırlandırılır
- **Anomali döneminde:** RUL = 0
- **Normal dönemde:** RUL = max_rul (tam sağlık)

### Adım 2: Degradation Curve
Anomali öncesindeki sensör örüntüsü incelenerek degradasyon karakteri analiz edilir.

### Adım 3: Weibull Analysis
Arızalar arası sürelerin (inter-failure times) Weibull dağılımına uyumu test edilir:
- **Shape k:** Arıza modunu belirler
- **Scale λ:** Karakteristik ömür
- **MTTF:** Ortalama arıza süresi = `λ × Γ(1 + 1/k)`

### Adım 4: Deep Learning RUL Model

```
Sliding Windows (48 timestep × n_features)
  ↓
LSTM(128) → LSTM(64) → Dense(64) → Dense(32) → Dense(1, sigmoid)
  ↓                                             ↓
GRU(128)  → GRU(64)  → Dense(64) → Dense(32) → Dense(1, sigmoid)
```

**Loss:** Huber loss (MAE ile MSE'nin hibrit versiyonu — outlier'a dayanıklı)

## Beklenen Performans

| Model | MAE (saat) | RMSE (saat) | R² |
|-------|-----------|------------|-----|
| LSTM | TBD | TBD | TBD |
| GRU | TBD | TBD | TBD |

## Erken Uyarı Kriterleri

| Bölge | RUL Aralığı | Renk | Aksiyon |
|-------|------------|------|---------|
| Normal | > 168h | Yeşil | Rutin izleme |
| Monitor | 72–168h | Sarı | Artan sıklıkta izleme |
| Warning | 24–72h | Turuncu | Bakım planla |
| Critical | < 24h | Kırmızı | Acil bakım |

## Proje Bağlamı

RUL tahmini, anomali tespitinden bir adım öteye geçer:
- **Anomali tespiti:** "Şu an anormal mi?"
- **RUL tahmini:** "Ne zaman bozulacak?"

Bu ayrım, gereksiz bakımları önleyerek **predictive maintenance** (kestirimci bakım) sağlar.

## Tez Katkısı

Bu notebook, projenin en özgün katkısını içermektedir. Mevcut Kaggle çalışmalarının büyük çoğunluğu anomali tespitinde durur; RUL tahminine geçiş gerçek endüstriyel değer yaratır.
