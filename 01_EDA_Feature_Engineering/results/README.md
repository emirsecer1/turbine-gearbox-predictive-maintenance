# 01 — EDA & Feature Engineering: Results

Bu klasör, `01_EDA_Feature_Engineering/notebook.ipynb` çalıştırıldıktan sonra oluşturulan görsel ve çıktıları içerir.

## Beklenen Çıktılar

### Görseller (PNG)

| Dosya | Açıklama |
|-------|----------|
| `missing_values.png` | Her feature için eksik değer yüzdesi |
| `sensor_time_series.png` | Tüm sensörlerin zaman serisi (anomali dönemleri kırmızı ile işaretli) |
| `correlation_matrix.png` | Feature korelasyon ısı haritası |
| `anomaly_timeline.png` | 5 yıllık anomali zaman çizelgesi + aylık anomali yoğunluğu |
| `rolling_features.png` | Rolling mean / rolling std karşılaştırması (24h, 48h, 168h) |
| `lag_autocorrelation.png` | Ototokorelasyon fonksiyonu (ACF) grafiği |
| `fft_analysis.png` | Zaman ve frekans domain analizi (FFT) |
| `feature_importance_mutual_info.png` | Mutual information bazlı top-20 feature önemi |
| `class_imbalance.png` | Sınıf dağılımı (pasta + bar grafik) |

### Veri Dosyaları

| Dosya | Açıklama |
|-------|----------|
| `../data/processed/features_engineered.csv` | Mühendislik uygulanmış tam feature seti |

## Oluşturulan Feature Grupları

### Rolling Features (window = 24, 48, 168)
- `{sensor}_roll_mean_24` — 24 saatlik hareketli ortalama
- `{sensor}_roll_mean_48` — 48 saatlik hareketli ortalama
- `{sensor}_roll_mean_168` — 168 saatlik (haftalık) hareketli ortalama
- `{sensor}_roll_std_24/48/168` — Hareketli standart sapma

### Lag Features (lag = 1, 6, 12, 24)
- `{sensor}_lag_1` — 1 adım (saat) önceki değer
- `{sensor}_lag_6` — 6 saat önceki değer
- `{sensor}_lag_12` — 12 saat önceki değer
- `{sensor}_lag_24` — 24 saat önceki değer

### Fourier Features
- `{sensor}_sin_k / {sensor}_cos_k` — k. harmonik (k=1,2,3) için sinüs/kosinüs bileşenleri

## Temel Bulgular

> Notebook çalıştırıldıktan sonra bu bölüm gerçek değerler ile güncellenmelidir.

- **Dataset boyutu:** ~ TBD satır × TBD sütun
- **Anomali oranı:** ~ TBD%
- **Sınıf dengesizliği oranı:** ~ TBD:1 (normal:anomali)
- **En güçlü feature (MI):** TBD
- **Yüksek korelasyonlu çiftler:** TBD

## Sonraki Adım

Bu notebook'un çıktısı olan `features_engineered.csv`, `02_Classical_ML_Baselines` notebook'una girdi olarak kullanılmaktadır.
