# 05 — Hybrid Ensemble: Results

Bu klasör, `05_Hybrid_Ensemble/notebook.ipynb` çalıştırıldıktan sonra oluşturulan görsel ve çıktıları içerir.

## Beklenen Çıktılar

### Görseller (PNG)

| Dosya | Açıklama |
|-------|----------|
| `shap_summary.png` | SHAP dot plot — her özelliğin anomali tahminlerine katkısı |
| `shap_bar.png` | SHAP bar plot — ortalama mutlak SHAP değerleri (feature importance) |
| `shap_temporal.png` | Aylık SHAP değerleri — hangi sensör, hangi zaman diliminde tetikliyor |
| `lime_example.png` | LIME açıklaması — tek bir anomali örneğinin yerel yorumu |
| `final_comparison.png` | Tüm modeller için metrik ısı haritası + F1 bar chart |

## Ensemble Stratejisi

### 1. Stacking Ensemble
**Base modeller:** RF + XGBoost + LightGBM  
**Meta-learner:** Logistic Regression  
**Eğitim:** Out-of-fold (OOF) predictions (TimeSeriesSplit, 5 fold)

```
[RF proba] ─┐
[XGB proba]─┤→ [Meta-feature matrix] → [Logistic Regression] → Final prediction
[LGB proba]─┘
```

**Avantajı:** Her modelin güçlü yönlerini öğrenir, zayıf yönlerini dengeler.

### 2. Soft Voting Ensemble
**Uniform:** Tüm modellere eşit ağırlık  
**AUC-weighted:** Daha yüksek ROC-AUC'a sahip modellere daha fazla ağırlık

```
Final_proba = Σ(weight_i × model_i_proba) / Σ(weight_i)
```

### 3. Unsupervised + Supervised Hibrit
Isolation Forest ve Autoencoder anomali skorları, meta-feature matrisine ek girdi olarak eklenir:

```
[RF proba]  ─┐
[XGB proba] ─┤
[LGB proba] ─┤→ [Extended meta-features] → [Meta-learner] → Final
[IF score]  ─┤
[AE score]  ─┘
```

## Beklenen Kazanım

| Strateji | Beklenen Kazanım vs Best Single Model |
|----------|---------------------------------------|
| Stacking | +1–3% F1 |
| Soft Voting | +0.5–2% F1 |
| Unsupervised Hybrid | +1–4% F1 (özellikle Recall artışı) |

## Açıklanabilirlik Özeti

### SHAP Analizi
- **En önemli özellikler:** Sıcaklık sensörleri (bearing temp, oil temp) genellikle en yüksek SHAP değerlerine sahip olur
- **Zaman bazlı:** Yaz aylarında sıcaklık sensörleri daha baskın, kış aylarında titreşim sensörleri öne çıkabilir
- **Rolling features:** 24h ve 48h rolling std genellikle yüksek öneme sahip (trend değişimini yakalar)

### LIME Analizi
LIME, bireysel tahminler için yerel linear approximation kullanır:
- Anomali tahminini en çok artıran faktörler
- Anomali tahminini en çok azaltan faktörler

## Sonraki Adım

Bu notebook, projenin nihai sonuç tablosunu içerir. Elde edilen en iyi model `06_RUL_Prediction` için de kullanılabilir.
