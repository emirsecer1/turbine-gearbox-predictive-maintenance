# 02 — Classical ML Baselines: Results

Bu klasör, `02_Classical_ML_Baselines/notebook.ipynb` çalıştırıldıktan sonra oluşturulan görsel ve çıktıları içerir.

## Beklenen Çıktılar

### Görseller (PNG)

| Dosya | Açıklama |
|-------|----------|
| `smote_balancing.png` | SMOTE öncesi ve sonrası sınıf dağılımı |
| `confusion_matrices.png` | Dört model için 2×2 confusion matrix |
| `roc_pr_curves.png` | Dört model için ROC ve PR eğrileri |
| `threshold_optimization.png` | Threshold vs F1 score eğrisi (model başına) |
| `feature_importance_models.png` | RF, XGBoost, LightGBM için top-20 feature önem grafikleri |
| `model_comparison.png` | Tüm modellerin metrik karşılaştırma ısı haritası |

### Model Dosyaları

| Dosya | Açıklama |
|-------|----------|
| `../models/best_classical_model.pkl` | F1 skoruna göre en iyi model (joblib formatı) |

## Beklenen Metrik Tablosu

Aşağıdaki tablo, notebook çalıştırıldıktan sonra güncellenecektir:

| Model | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|-------|-----------|--------|-----|---------|--------|
| Random Forest | TBD | TBD | TBD | TBD | TBD |
| XGBoost | TBD | TBD | TBD | TBD | TBD |
| LightGBM | TBD | TBD | TBD | TBD | TBD |
| Logistic Regression | TBD | TBD | TBD | TBD | TBD |

## Metodoloji Notları

### Temporal Split
- **Önemli:** Zaman serisi verilerinde klasik random split kullanılmaz. Bu, gelecek verinin geçmişi "görmesi" anlamına gelir (data leakage).
- **Çözüm:** Kronolojik sıraya göre split — ilk %80 train, son %20 test.

### SMOTE Uygulaması
- SMOTE **yalnızca training setine** uygulanır.
- Test seti ham (orijinal dağılım ile) bırakılır — gerçek dünya performansını yansıtır.
- k_neighbors=5 ile komşuluk bazlı sentez.

### Threshold Optimizasyonu
- Varsayılan threshold=0.5 değil, F1'i maksimize eden threshold seçilir.
- Özellikle dengesiz veri setlerinde önemli fark yaratır.

## Sonraki Adım

Bu notebook'un çıktıları şu amaçlarla kullanılır:
- `05_Hybrid_Ensemble` — stacking ensemble için temel model
- `06_RUL_Prediction` — degradation pattern için referans
