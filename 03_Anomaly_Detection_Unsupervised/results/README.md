# 03 — Anomaly Detection (Unsupervised): Results

Bu klasör, `03_Anomaly_Detection_Unsupervised/notebook.ipynb` çalıştırıldıktan sonra oluşturulan görsel ve çıktıları içerir.

## Beklenen Çıktılar

### Görseller (PNG)

| Dosya | Açıklama |
|-------|----------|
| `anomaly_score_distributions.png` | Her yöntem için normal/anomali anomali skoru histogramı (4 subplot) |
| `unsupervised_roc_pr.png` | Dört yöntem için ROC ve PR eğrileri karşılaştırması |
| `autoencoder_training.png` | Autoencoder eğitim/validasyon loss grafiği |
| `sensor_anomaly_contribution.png` | Sensör → anomali skoru korelasyonu (hangi sensör en çok katkı sağlıyor?) |
| `unsupervised_comparison.png` | Yöntemler arası ROC-AUC ve PR-AUC bar karşılaştırması |

### Veri Dosyaları (CSV / JSON)

| Dosya | Açıklama |
|-------|----------|
| `unsupervised_comparison.csv` | IF / OC-SVM / LOF / Autoencoder: ROC-AUC ve PR-AUC tablosu |
| `all_anomaly_scores.csv` | IF ve Autoencoder anomali skorları + gerçek etiket (tüm dataset) |
| `unsupervised_scores.csv` | IF ve AE skorları (05_Hybrid_Ensemble'a girdi) |

## Beklenen Karşılaştırma Tablosu

| Yöntem | ROC-AUC | PR-AUC | Açıklama |
|--------|---------|--------|----------|
| Isolation Forest | TBD | TBD | Ağaç bazlı izolasyon, contamination tuning ile |
| One-Class SVM | TBD | TBD | RBF kernel, nu=contamination_rate |
| LOF | TBD | TBD | k=20 komşu, novelty=True |
| Autoencoder | TBD | TBD | MSE reconstruction error bazlı skor |

## Yöntem Karşılaştırması

| Yöntem | Avantaj | Dezavantaj | En İyi Kullanım |
|--------|---------|------------|-----------------|
| **Isolation Forest** | Hızlı, ölçeklenebilir, paralel | Küresel anomali varsayımı | Genel amaçlı, büyük veri |
| **One-Class SVM** | Güçlü sınır tanımı | Büyük veride yavaş, kernel seçimi zor | Küçük-orta veri |
| **LOF** | Yerel yoğunluk tabanlı | Yüksek boyutta performans düşer | Kümelenmiş anomaliler |
| **Autoencoder** | Kompleks zaman pattern'ları öğrenir | Eğitim süresi, hyperparameter hassasiyeti | Zaman serisi, çok sensörlü veri |

## Teknik Notlar

- **Contamination Tuning:** Gerçek anomali oranı (01_EDA'dan elde edilen) contamination parametresi olarak kullanılır.
- **One-Class SVM:** Büyük veri setlerinde hesaplama maliyeti nedeniyle örneklem (10,000 kayıt) üzerinde eğitilir.
- **Autoencoder:** Yalnızca normal veriler üzerinde eğitilir — böylece anomalileri yüksek reconstruction error ile tanımlar.
- **Anomali Skorları:** Tüm yöntemler [0, 1] aralığına normalize edilir.

## Sonraki Adım

Bu notebook'un unsupervised anomali skorları (`unsupervised_scores.csv`) şu amaçlarla kullanılır:
- `05_Hybrid_Ensemble` — supervised + unsupervised sinyal birleştirme
