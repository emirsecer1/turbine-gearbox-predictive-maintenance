# 🌬️ Turbine Gearbox Predictive Maintenance

>  Wind Turbine Gearbox Anomaly Detection & Remaining Useful Life Prediction

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)](https://tensorflow.org/)
[![Kaggle](https://img.shields.io/badge/Dataset-Kaggle-20BEFF.svg)](https://www.kaggle.com/datasets/aiwithcagri/wind-turbine-gearbox-anomaly-detection-5year-scada/data)

## 📋 Proje Özeti

Bu proje, rüzgar türbini vites kutusunun 5 yıllık SCADA verileri üzerinde anomali tespiti ve kalan kullanım ömrü (RUL) tahmini gerçekleştirmek amacıyla oluşturulmuştur. Klasik makine öğrenmesinden derin öğrenme mimarilerine ve açıklanabilir yapay zekaya kadar geniş bir yelpazede teknik uygulamalar içermektedir.

---

## 📊 Dataset

| Özellik | Değer |
|---------|-------|
| **Kaynak** | [Kaggle — Wind Turbine Gearbox Anomaly Detection 5-Year SCADA](https://www.kaggle.com/datasets/aiwithcagri/wind-turbine-gearbox-anomaly-detection-5year-scada/data) |
| **Format** | SCADA, zaman serisi, CSV |
| **Süre** | 5 yıl |
| **Etiket** | Anomali etiketli (binary) |
| **Özellikler** | Gearbox sıcaklık sensörleri, güç, rüzgar hızı, devir sayısı vb. |

### Dataset İndirme (Kaggle API)
```bash
pip install kaggle
mkdir -p ~/.kaggle && cp kaggle.json ~/.kaggle/ && chmod 600 ~/.kaggle/kaggle.json
kaggle datasets download -d aiwithcagri/wind-turbine-gearbox-anomaly-detection-5year-scada
unzip wind-turbine-gearbox-anomaly-detection-5year-scada.zip -d data/
```

---

## 📁 Proje Yapısı

```
turbine-gearbox-predictive-maintenance/
│
├── 📁 01_EDA_Feature_Engineering/
│   ├── notebook.ipynb              ← Keşifsel analiz & özellik mühendisliği
│   └── results/README.md           ← Beklenen çıktılar açıklaması
│
├── 📁 02_Classical_ML_Baselines/
│   ├── notebook.ipynb              ← RF, XGBoost, LightGBM, Logistic Regression
│   └── results/README.md
│
├── 📁 03_Anomaly_Detection_Unsupervised/
│   ├── notebook.ipynb              ← Isolation Forest, OC-SVM, LOF, Autoencoder
│   └── results/README.md
│
├── 📁 04_TimeSeries_DeepLearning/
│   ├── notebook.ipynb              ← LSTM, TCN, Transformer Encoder
│   └── results/README.md
│
├── 📁 05_Hybrid_Ensemble/
│   ├── notebook.ipynb              ← Stacking, Voting, SHAP, LIME
│   └── results/README.md
│
├── 📁 06_RUL_Prediction/
│   ├── notebook.ipynb              ← Weibull, LSTM/GRU regression, Early Warning
│   └── results/README.md
│
└── README.md
```

---

## 📓 Notebook Açıklamaları

### 01 — EDA & Feature Engineering
**Amaç:** Verinin derinlemesine anlaşılması ve gelişmiş özellik seti oluşturulması.

| Teknik | Açıklama |
|--------|----------|
| Zaman serisi görselleştirme | Her sensör + anomali timeline |
| Korelasyon matrisi | Sensörler arası ilişki analizi |
| Rolling features | Mean/Std (window: 24h, 48h, 168h) |
| Lag features | Gecikmeli değerler (1, 6, 12, 24h) |
| Fourier Transform (FFT) | Periyodik bileşen analizi |
| Mutual Information | Özellik önemi ön değerlendirmesi |
| Class imbalance analizi | Anomali oranı ve dağılımı |

---

### 02 — Classical ML Baselines
**Amaç:** Geleneksel yöntemlerle güçlü bir benchmark oluşturmak.

| Teknik | Açıklama |
|--------|----------|
| Temporal split | Shuffle=False, kronolojik train/test |
| SMOTE | Azınlık sınıfı oversampling |
| Random Forest | n_estimators=100, class_weight=balanced |
| XGBoost | n_estimators=200, scale_pos_weight |
| LightGBM | n_estimators=200, class_weight=balanced |
| Logistic Regression | class_weight=balanced, StandardScaler |
| Threshold optimization | F1 maximize eden threshold bulma |
| Feature importance | Top-20 özellik önemi grafikleri |

---

### 03 — Anomaly Detection (Unsupervised)
**Amaç:** Etiket kullanmadan anomali tespiti.

| Teknik | Açıklama |
|--------|----------|
| Isolation Forest | Contamination tuning, ağaç bazlı izolasyon |
| One-Class SVM | RBF kernel, normal veri üzerinde eğitim |
| LOF | k=20 komşu, yerel yoğunluk |
| Autoencoder (Keras) | MSE reconstruction error tabanlı anomali skoru |

---

### 04 — Time Series Deep Learning
**Amaç:** Zaman bağımlılığını modelleyen derin öğrenme mimarileri.

| Teknik | Açıklama |
|--------|----------|
| Sliding window | window_size=48, stride=1 |
| LSTM | 2 katman, dropout=0.3, class weighting |
| TCN | Dilated causal conv., 4 residual blok (dilation: 1,2,4,8) |
| Transformer Encoder | Multi-head attention + positional encoding |
| Early stopping | patience=10, val_loss monitored |
| LR scheduler | ReduceLROnPlateau(factor=0.5) |

---

### 05 — Hybrid Ensemble
**Amaç:** En iyi sonucu elde etmek ve kararları açıklamak.

| Teknik | Açıklama |
|--------|----------|
| Stacking | OOF predictions + Logistic Regression meta-learner |
| Soft Voting | Uniform ve AUC-weighted olasılık ortalaması |
| Unsupervised+Supervised hibrit | IF/AE skorları + ML model tahminleri |
| SHAP | TreeExplainer, summary plot, temporal analysis |
| LIME | Bireysel tahmin yerel açıklaması |

---

### 06 — RUL Prediction
**Amaç:** "Ne zaman bakım yapılmalı?" sorusunu cevaplamak.

| Teknik | Açıklama |
|--------|----------|
| RUL hesaplama | Anomali öncesi geri sayım (max_rul=168h) |
| Degradation curve | Anomali öncesi sensör örüntü analizi |
| Weibull distribution | scipy.stats.weibull_min, MTTF hesaplama |
| LSTM/GRU regression | Sliding window + Huber loss |
| Early warning | 24h/48h/72h öncesi alarm doğruluğu |
| Maintenance timeline | Renk kodlu karar bölgeleri |

---

## 📦 Kullanılan Kütüphaneler

```python
# Temel veri işleme
pandas>=1.5.0
numpy>=1.23.0
scipy>=1.9.0

# Görselleştirme
matplotlib>=3.6.0
seaborn>=0.12.0

# Makine öğrenmesi
scikit-learn>=1.1.0
xgboost>=1.7.0
lightgbm>=3.3.0
imbalanced-learn>=0.10.0

# Derin öğrenme
tensorflow>=2.10.0  # veya keras standalone

# Açıklanabilirlik
shap>=0.41.0
lime>=0.2.0.1

# Veri edinimi
kaggle>=1.5.0
joblib>=1.2.0
```

---

## 📈 Sonuçların Özet Tablosu

> Notebook'lar çalıştırıldıktan sonra bu tablo gerçek değerlerle güncellenmelidir.

| Yöntem | Kategori | F1 | ROC-AUC | PR-AUC |
|--------|----------|-----|---------|--------|
| Logistic Regression | Classical ML | TBD | TBD | TBD |
| Random Forest | Classical ML | TBD | TBD | TBD |
| XGBoost | Classical ML | TBD | TBD | TBD |
| LightGBM | Classical ML | TBD | TBD | TBD |
| Isolation Forest | Unsupervised | — | TBD | TBD |
| Autoencoder | Unsupervised | — | TBD | TBD |
| LSTM | Deep Learning | TBD | TBD | TBD |
| TCN | Deep Learning | TBD | TBD | TBD |
| Transformer | Deep Learning | TBD | TBD | TBD |
| Stacking Ensemble | Ensemble | TBD | TBD | TBD |
| Weighted Voting | Ensemble | TBD | TBD | TBD |

---

## 🚀 Getting Started

### 1. Repo'yu klonla
```bash
git clone https://github.com/emirsecer1/turbine-gearbox-predictive-maintenance.git
cd turbine-gearbox-predictive-maintenance
```

### 2. Bağımlılıkları yükle
```bash
pip install pandas numpy scipy matplotlib seaborn scikit-learn \
            xgboost lightgbm imbalanced-learn tensorflow \
            shap lime kaggle joblib
```

### 3. Dataset'i indir
```bash
kaggle datasets download -d aiwithcagri/wind-turbine-gearbox-anomaly-detection-5year-scada
unzip wind-turbine-gearbox-anomaly-detection-5year-scada.zip -d data/
```

### 4. Notebook'ları çalıştır (sırayla)
```
01_EDA_Feature_Engineering/notebook.ipynb
02_Classical_ML_Baselines/notebook.ipynb
03_Anomaly_Detection_Unsupervised/notebook.ipynb
04_TimeSeries_DeepLearning/notebook.ipynb
05_Hybrid_Ensemble/notebook.ipynb
06_RUL_Prediction/notebook.ipynb
```

### Kaggle Ortamında
Bu notebook'lar Kaggle notebook ortamında doğrudan çalışacak şekilde tasarlanmıştır. Dataset path'i otomatik olarak `/kaggle/input/wind-turbine-gearbox-anomaly-detection-5year-scada/` olarak ayarlanır.

---

## 🏆 Mevcut Sonuçları Geçmek İçin Stratejiler

| Strateji | Açıklama |
|----------|----------|
| **Temporal leakage önleme** | Random shuffle yerine kronolojik split |
| **Multi-sensor fusion** | Tek sensör değil, sensör kombinasyonları |
| **Anomaly scoring** | Binary label yerine sürekli anomali skoru |
| **PatchTST / Transformer** | SOTA time series mimarileri |
| **Threshold optimization** | F1-maximize eden özel threshold |
| **SMOTE + class_weight** | İkili strateji ile imbalance yönetimi |

---

## 📄 Lisans

MIT License — Bu proje açık kaynak olarak paylaşılmıştır.

---

*Bu proje, rüzgar enerjisi sistemlerinin güvenilirlik analizine katkıda bulunmak amacıyla geliştirilmiştir.*
