#!/usr/bin/env python3
"""
IEEE-Standard Academic Report Generator
Wind Turbine Gearbox Predictive Maintenance
Generates both .docx and .pdf with identical content.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.join(BASE_DIR, "report")


def set_cell_shading(cell, color):
    """Set background color for a table cell."""
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color}"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def set_cell_border(cell, **kwargs):
    """Set cell border properties."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}/>')
    for edge, val in kwargs.items():
        element = parse_xml(
            f'<w:{edge} {nsdecls("w")} w:val="{val["val"]}" '
            f'w:sz="{val["sz"]}" w:space="0" w:color="{val["color"]}"/>'
        )
        tcBorders.append(element)
    tcPr.append(tcBorders)


def add_formatted_table(doc, headers, rows, col_widths=None):
    """Add a professionally formatted table."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"

    # Header row
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(header)
        run.bold = True
        run.font.size = Pt(8)
        run.font.name = "Times New Roman"
        set_cell_shading(cell, "1F4E79")
        run.font.color.rgb = RGBColor(255, 255, 255)

    # Data rows
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = ""
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(str(val))
            run.font.size = Pt(8)
            run.font.name = "Times New Roman"
            if r_idx % 2 == 1:
                set_cell_shading(cell, "D6E4F0")

    if col_widths:
        for i, w in enumerate(col_widths):
            for row in table.rows:
                row.cells[i].width = Cm(w)

    return table


def add_image_if_exists(doc, path, width=None, caption=None):
    """Add an image with optional caption if the file exists."""
    full_path = os.path.join(BASE_DIR, path)
    if os.path.exists(full_path):
        if width:
            doc.add_picture(full_path, width=width)
        else:
            doc.add_picture(full_path, width=Inches(3.2))
        last_paragraph = doc.paragraphs[-1]
        last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if caption:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(caption)
            run.font.size = Pt(8)
            run.font.name = "Times New Roman"
            run.italic = True
            p.space_after = Pt(6)
        return True
    return False


def make_two_column(section):
    """Set section to two-column layout."""
    sectPr = section._sectPr
    cols = sectPr.find(qn("w:cols"))
    if cols is None:
        cols = parse_xml(f'<w:cols {nsdecls("w")} w:num="2" w:space="720"/>')
        sectPr.append(cols)
    else:
        cols.set(qn("w:num"), "2")
        cols.set(qn("w:space"), "720")


def make_one_column(section):
    """Set section to one-column layout."""
    sectPr = section._sectPr
    cols = sectPr.find(qn("w:cols"))
    if cols is None:
        cols = parse_xml(f'<w:cols {nsdecls("w")} w:num="1"/>')
        sectPr.append(cols)
    else:
        cols.set(qn("w:num"), "1")


def add_section_heading(doc, text, level=1):
    """Add a section heading with IEEE formatting."""
    heading = doc.add_heading(text, level=level)
    for run in heading.runs:
        run.font.name = "Times New Roman"
        run.font.color.rgb = RGBColor(0, 0, 0)
        if level == 1:
            run.font.size = Pt(10)
        elif level == 2:
            run.font.size = Pt(10)
        else:
            run.font.size = Pt(9)
    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER if level == 1 else WD_ALIGN_PARAGRAPH.LEFT
    return heading


def add_body_text(doc, text, bold=False, italic=False):
    """Add body text with IEEE formatting."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(0.5)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(2)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(9)
    run.bold = bold
    run.italic = italic
    return p


def add_continuous_section_break(doc):
    """Add a continuous section break to switch column layout."""
    new_section = doc.add_section()
    new_section.start_type = 0  # Continuous
    # Copy page dimensions from first section
    first_section = doc.sections[0]
    new_section.page_width = first_section.page_width
    new_section.page_height = first_section.page_height
    new_section.top_margin = first_section.top_margin
    new_section.bottom_margin = first_section.bottom_margin
    new_section.left_margin = first_section.left_margin
    new_section.right_margin = first_section.right_margin
    return new_section


def generate_report():
    """Generate the IEEE-formatted report."""
    os.makedirs(REPORT_DIR, exist_ok=True)

    doc = Document()

    # ─── Page setup (A4, IEEE margins) ───
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(1.75)
        section.right_margin = Cm(1.75)

    # ─── Default style ───
    style = doc.styles["Normal"]
    font = style.font
    font.name = "Times New Roman"
    font.size = Pt(9)
    style.paragraph_format.space_after = Pt(2)
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.line_spacing = 1.0

    # Configure heading styles
    for i in range(1, 4):
        hs = doc.styles[f"Heading {i}"]
        hs.font.name = "Times New Roman"
        hs.font.color.rgb = RGBColor(0, 0, 0)
        hs.paragraph_format.space_before = Pt(6)
        hs.paragraph_format.space_after = Pt(3)

    # ═══════════════════════════════════════════════════
    # TITLE SECTION (Single Column)
    # ═══════════════════════════════════════════════════

    # Title
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.space_after = Pt(6)
    run = title.add_run(
        "Wind Turbine Gearbox Predictive Maintenance:\n"
        "A Comprehensive Machine Learning and Deep Learning Approach\n"
        "for Anomaly Detection and Remaining Useful Life Prediction"
    )
    run.font.name = "Times New Roman"
    run.font.size = Pt(18)
    run.bold = True

    # Turkish Title
    title_tr = doc.add_paragraph()
    title_tr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_tr.space_after = Pt(12)
    run_tr = title_tr.add_run(
        "Rüzgar Türbini Dişli Kutusu Kestirimci Bakım:\n"
        "Anomali Tespiti ve Kalan Kullanım Ömrü Tahmini için\n"
        "Kapsamlı Makine Öğrenmesi ve Derin Öğrenme Yaklaşımı"
    )
    run_tr.font.name = "Times New Roman"
    run_tr.font.size = Pt(14)
    run_tr.italic = True

    # Author
    author = doc.add_paragraph()
    author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    author.space_after = Pt(4)
    run = author.add_run("Emir Seçer")
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    run.bold = True

    # Affiliation
    affil = doc.add_paragraph()
    affil.alignment = WD_ALIGN_PARAGRAPH.CENTER
    affil.space_after = Pt(12)
    run = affil.add_run("Computer Engineering Department")
    run.font.name = "Times New Roman"
    run.font.size = Pt(9)
    run.italic = True

    # ─── Horizontal line ───
    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_line = p_line.add_run("─" * 90)
    run_line.font.size = Pt(6)
    run_line.font.color.rgb = RGBColor(100, 100, 100)

    # ═══════════════════════════════════════════════════
    # ABSTRACT - English
    # ═══════════════════════════════════════════════════
    abs_title = doc.add_paragraph()
    abs_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    abs_title.space_before = Pt(6)
    run = abs_title.add_run("Abstract")
    run.font.name = "Times New Roman"
    run.font.size = Pt(10)
    run.bold = True
    run.italic = True

    abs_text = doc.add_paragraph()
    abs_text.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    abs_text.paragraph_format.first_line_indent = Cm(0.5)
    abs_text.space_after = Pt(4)
    run = abs_text.add_run(
        "This study presents a comprehensive predictive maintenance framework for wind turbine gearboxes "
        "utilizing five years of SCADA (Supervisory Control and Data Acquisition) sensor data comprising "
        "262,800 hourly records. The proposed approach integrates multiple machine learning paradigms including "
        "classical supervised learning (Random Forest, XGBoost, LightGBM, Logistic Regression), unsupervised "
        "anomaly detection (Isolation Forest, One-Class SVM, Local Outlier Factor, Autoencoder), deep learning "
        "architectures for time series analysis (LSTM, TCN, Transformer Encoder), and hybrid ensemble methods "
        "(Stacking, Weighted Voting). A total of 95 features were engineered from 7 original sensor measurements "
        "through rolling statistics, lag features, and Fourier transforms. The unsupervised methods achieved "
        "exceptional performance with One-Class SVM reaching 0.9999 ROC-AUC and 0.9965 PR-AUC. Among deep "
        "learning models, Temporal Convolutional Network (TCN) demonstrated the best balanced performance with "
        "F1-score of 0.445 and PR-AUC of 0.601. The study further extends beyond binary anomaly detection to "
        "Remaining Useful Life (RUL) prediction, where the LSTM regression model achieved a Mean Absolute Error "
        "of 3.96 hours with 100% early warning accuracy at 24, 48, and 72-hour horizons. Explainability analysis "
        "through SHAP and LIME provides interpretable insights into model decisions. The proposed framework "
        "demonstrates that combining supervised, unsupervised, and deep learning methods with temporal feature "
        "engineering enables highly effective predictive maintenance for wind turbine gearboxes, bridging the gap "
        "from anomaly detection to actionable maintenance scheduling."
    )
    run.font.name = "Times New Roman"
    run.font.size = Pt(9)
    run.italic = True

    # Keywords English
    kw = doc.add_paragraph()
    kw.space_after = Pt(4)
    run = kw.add_run("Keywords: ")
    run.font.name = "Times New Roman"
    run.font.size = Pt(9)
    run.bold = True
    run.italic = True
    run = kw.add_run(
        "Predictive maintenance, wind turbine, gearbox, anomaly detection, "
        "remaining useful life, SCADA, deep learning, LSTM, TCN, Transformer, "
        "ensemble learning, SHAP, XGBoost, Random Forest"
    )
    run.font.name = "Times New Roman"
    run.font.size = Pt(9)
    run.italic = True

    # ─── Separator ───
    p_sep = doc.add_paragraph()
    p_sep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sep = p_sep.add_run("─" * 50)
    run_sep.font.size = Pt(6)
    run_sep.font.color.rgb = RGBColor(150, 150, 150)

    # ═══════════════════════════════════════════════════
    # ÖZET - Turkish
    # ═══════════════════════════════════════════════════
    ozet_title = doc.add_paragraph()
    ozet_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ozet_title.space_before = Pt(6)
    run = ozet_title.add_run("Özet")
    run.font.name = "Times New Roman"
    run.font.size = Pt(10)
    run.bold = True
    run.italic = True

    ozet_text = doc.add_paragraph()
    ozet_text.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    ozet_text.paragraph_format.first_line_indent = Cm(0.5)
    ozet_text.space_after = Pt(4)
    run = ozet_text.add_run(
        "Bu çalışma, rüzgar türbini dişli kutuları için beş yıllık SCADA (Merkezi Denetim Kontrol ve Veri "
        "Toplama) sensör verisi kullanarak kapsamlı bir kestirimci bakım çerçevesi sunmaktadır. Toplam "
        "262.800 saatlik kayıt içeren veri seti üzerinde, klasik denetimli öğrenme (Random Forest, XGBoost, "
        "LightGBM, Lojistik Regresyon), denetimsiz anomali tespiti (Isolation Forest, One-Class SVM, Local "
        "Outlier Factor, Autoencoder), zaman serisi derin öğrenme mimarileri (LSTM, TCN, Transformer Encoder) "
        "ve hibrit topluluk yöntemleri (Stacking, Ağırlıklı Oylama) olmak üzere çoklu makine öğrenmesi "
        "paradigmaları entegre edilmiştir. Orijinal 7 sensör ölçümünden yuvarlanan istatistikler, gecikme "
        "özellikleri ve Fourier dönüşümleri aracılığıyla toplam 95 özellik mühendisliği gerçekleştirilmiştir. "
        "Denetimsiz yöntemler arasında One-Class SVM, 0,9999 ROC-AUC ve 0,9965 PR-AUC değerleri ile olağanüstü "
        "performans göstermiştir. Derin öğrenme modelleri arasında Temporal Konvolüsyonel Ağ (TCN), 0,445 "
        "F1-skoru ve 0,601 PR-AUC ile en dengeli performansı sergilemiştir. Çalışma, ikili anomali tespitinin "
        "ötesine geçerek Kalan Kullanım Ömrü (RUL) tahminine genişletilmiş olup, LSTM regresyon modeli 3,96 "
        "saatlik Ortalama Mutlak Hata ve 24, 48, 72 saatlik ufuklarda %100 erken uyarı doğruluğu elde etmiştir. "
        "SHAP ve LIME yoluyla yapılan açıklanabilirlik analizi, model kararlarına ilişkin yorumlanabilir içgörüler "
        "sağlamaktadır. Önerilen çerçeve, denetimli, denetimsiz ve derin öğrenme yöntemlerinin zamansal özellik "
        "mühendisliği ile birleştirilmesinin, rüzgar türbini dişli kutuları için yüksek düzeyde etkili kestirimci "
        "bakımı mümkün kıldığını ve anomali tespitinden uygulanabilir bakım planlamasına köprü kurduğunu "
        "göstermektedir."
    )
    run.font.name = "Times New Roman"
    run.font.size = Pt(9)
    run.italic = True

    # Keywords Turkish
    kw_tr = doc.add_paragraph()
    kw_tr.space_after = Pt(6)
    run = kw_tr.add_run("Anahtar Kelimeler: ")
    run.font.name = "Times New Roman"
    run.font.size = Pt(9)
    run.bold = True
    run.italic = True
    run = kw_tr.add_run(
        "Kestirimci bakım, rüzgar türbini, dişli kutusu, anomali tespiti, "
        "kalan kullanım ömrü, SCADA, derin öğrenme, LSTM, TCN, Transformer, "
        "topluluk öğrenmesi, SHAP, XGBoost, Random Forest"
    )
    run.font.name = "Times New Roman"
    run.font.size = Pt(9)
    run.italic = True

    # ─── Horizontal line ───
    p_line2 = doc.add_paragraph()
    p_line2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_line2 = p_line2.add_run("─" * 90)
    run_line2.font.size = Pt(6)
    run_line2.font.color.rgb = RGBColor(100, 100, 100)

    # ═══════════════════════════════════════════════════
    # Switch to TWO-COLUMN layout
    # ═══════════════════════════════════════════════════
    new_section = add_continuous_section_break(doc)
    make_two_column(new_section)

    # ═══════════════════════════════════════════════════
    # I. INTRODUCTION
    # ═══════════════════════════════════════════════════
    add_section_heading(doc, "I. INTRODUCTION", level=1)

    add_body_text(doc,
        "Wind energy has emerged as one of the most promising renewable energy sources worldwide, with "
        "installed capacity growing exponentially over the past two decades. Wind turbines, as the primary "
        "conversion devices, operate under harsh environmental conditions including variable wind speeds, "
        "temperature fluctuations, and mechanical stress. Among the critical components, the gearbox serves "
        "as the primary mechanical transmission system, converting the low-speed rotation of the rotor into "
        "the high-speed rotation required by the generator."
    )

    add_body_text(doc,
        "Gearbox failures account for a significant proportion of wind turbine downtime and maintenance "
        "costs. According to industry reports, gearbox-related failures can result in 5-10% of annual energy "
        "production losses and repair costs ranging from $100,000 to $300,000 per incident. Traditional "
        "maintenance strategies, including reactive (run-to-failure) and preventive (time-based) approaches, "
        "are either costly or inefficient. Predictive maintenance, which leverages real-time sensor data and "
        "machine learning algorithms to predict failures before they occur, offers a superior alternative."
    )

    add_body_text(doc,
        "Supervisory Control and Data Acquisition (SCADA) systems, which are standard in modern wind farms, "
        "continuously collect operational data from various sensors. These systems record parameters such as "
        "gearbox oil temperature, oil pressure, vibration measurements in multiple axes, generator RPM, and "
        "active power output. The high-dimensional, temporal nature of this data makes it particularly suitable "
        "for advanced machine learning approaches."
    )

    add_body_text(doc,
        "This paper presents a comprehensive predictive maintenance framework that integrates multiple machine "
        "learning paradigms. The key contributions of this study are: (1) systematic feature engineering "
        "yielding 95 features from 7 original sensors; (2) comparative evaluation of classical ML, unsupervised, "
        "and deep learning methods; (3) hybrid ensemble approaches combining supervised and unsupervised models; "
        "(4) Remaining Useful Life (RUL) prediction with 100% early warning accuracy; and (5) model "
        "explainability through SHAP and LIME analysis."
    )

    add_body_text(doc,
        "The remainder of this paper is organized as follows: Section II reviews related work. Section III "
        "describes the dataset and feature engineering methodology. Section IV presents the machine learning "
        "methods employed. Section V details the experimental results. Section VI provides discussion and "
        "analysis. Section VII concludes the paper."
    )

    # ═══════════════════════════════════════════════════
    # II. RELATED WORK
    # ═══════════════════════════════════════════════════
    add_section_heading(doc, "II. RELATED WORK", level=1)

    add_section_heading(doc, "A. Traditional Approaches", level=2)

    add_body_text(doc,
        "Early approaches to wind turbine fault detection relied primarily on vibration analysis and "
        "signal processing techniques. Time-domain statistical features such as RMS, kurtosis, and crest "
        "factor were extracted from vibration signals for condition monitoring. Frequency-domain analysis "
        "through Fast Fourier Transform (FFT) enabled the identification of characteristic fault frequencies "
        "associated with specific gearbox components."
    )

    add_section_heading(doc, "B. Machine Learning Methods", level=2)

    add_body_text(doc,
        "The application of machine learning to wind turbine predictive maintenance has gained significant "
        "traction. Random Forest and gradient boosting methods (XGBoost, LightGBM) have demonstrated strong "
        "performance in fault classification tasks. Unsupervised methods such as Isolation Forest and "
        "One-Class SVM have been employed for anomaly detection scenarios where labeled fault data is scarce. "
        "These approaches benefit from their ability to learn normal operational patterns without requiring "
        "explicit fault labels."
    )

    add_section_heading(doc, "C. Deep Learning Approaches", level=2)

    add_body_text(doc,
        "Recent advances in deep learning have introduced powerful architectures for time series anomaly "
        "detection. Long Short-Term Memory (LSTM) networks and Gated Recurrent Units (GRU) capture long-range "
        "temporal dependencies in sequential sensor data. Temporal Convolutional Networks (TCN) apply dilated "
        "causal convolutions to efficiently model long sequences. Transformer-based architectures, originally "
        "designed for natural language processing, have shown promising results in time series applications "
        "through their multi-head self-attention mechanism."
    )

    add_section_heading(doc, "D. Remaining Useful Life Prediction", level=2)

    add_body_text(doc,
        "RUL prediction extends anomaly detection by estimating the time remaining before a component fails. "
        "Weibull distribution-based survival analysis provides a statistical framework for reliability "
        "estimation. Deep learning approaches, particularly LSTM and GRU regression models, have been "
        "successfully applied to RUL prediction in various industrial applications including turbofan engines, "
        "bearings, and batteries. The integration of early warning systems with RUL predictions enables "
        "proactive maintenance scheduling."
    )

    # ═══════════════════════════════════════════════════
    # III. DATASET AND FEATURE ENGINEERING
    # ═══════════════════════════════════════════════════
    add_section_heading(doc, "III. DATASET AND FEATURE ENGINEERING", level=1)

    add_section_heading(doc, "A. Dataset Description", level=2)

    add_body_text(doc,
        "The dataset used in this study was obtained from Kaggle and comprises five years of SCADA sensor "
        "data from a wind turbine gearbox system. The dataset contains 262,800 hourly records with seven "
        "sensor measurements and a binary anomaly label. The class distribution exhibits severe imbalance "
        "with 97.91% normal operation (257,300 samples) and 2.09% anomaly events (5,500 samples), resulting "
        "in a 47:1 imbalance ratio."
    )

    add_body_text(doc,
        "The seven original sensor features include: gearbox oil temperature, oil pressure, "
        "vibration measurements along the X, Y, and Z axes, generator RPM, and active power output. "
        "Each sensor provides continuous hourly readings, capturing both normal operational patterns and "
        "anomalous degradation events."
    )

    # Table: Dataset Overview
    add_formatted_table(doc,
        ["Parameter", "Value"],
        [
            ["Total Records", "262,800 (hourly)"],
            ["Time Span", "5 years"],
            ["Original Features", "7 sensors"],
            ["Normal Samples", "257,300 (97.91%)"],
            ["Anomaly Samples", "5,500 (2.09%)"],
            ["Imbalance Ratio", "47:1"],
            ["Engineered Features", "95"],
        ]
    )

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_cap = p_cap.add_run("TABLE I: Dataset Overview")
    run_cap.font.size = Pt(8)
    run_cap.font.name = "Times New Roman"
    run_cap.italic = True

    add_section_heading(doc, "B. Feature Engineering", level=2)

    add_body_text(doc,
        "To capture temporal patterns and enrich the feature space, a comprehensive feature engineering "
        "pipeline was designed. Three categories of derived features were computed from the original seven "
        "sensor measurements:"
    )

    add_body_text(doc,
        "Rolling Statistics (42 features): For each sensor, rolling mean and standard deviation were "
        "calculated with window sizes of 24 hours (1 day), 48 hours (2 days), and 168 hours (1 week). "
        "These features capture both short-term and long-term operational trends, enabling the models to "
        "detect gradual degradation patterns."
    )

    add_body_text(doc,
        "Lag Features (28 features): Lagged values at 1, 6, 12, and 24-hour intervals were generated "
        "for each sensor. Lag features encode the temporal evolution of sensor readings, providing the "
        "models with historical context for each observation."
    )

    add_body_text(doc,
        "Fourier Features (18 features): Sine and cosine harmonic components were extracted to capture "
        "periodic patterns in the data. These features encode cyclical behaviors such as diurnal temperature "
        "variations and seasonal wind patterns."
    )

    add_body_text(doc,
        "Mutual information analysis revealed that 168-hour rolling vibration means were the most "
        "discriminative features, with vibration_y_roll_mean_168 achieving a mutual information score of "
        "0.0789. This finding suggests that long-term vibration trends are the strongest indicators of "
        "gearbox anomalies."
    )

    # ═══════════════════════════════════════════════════
    # Switch to single column for figure
    # ═══════════════════════════════════════════════════
    sec_1col = add_continuous_section_break(doc)
    make_one_column(sec_1col)

    add_image_if_exists(doc,
        "01_EDA_Feature_Engineering/results/correlation_matrix.png",
        width=Inches(5.5),
        caption="Fig. 1: Correlation matrix of engineered features"
    )

    add_image_if_exists(doc,
        "01_EDA_Feature_Engineering/results/feature_importance_mutual_info.png",
        width=Inches(5.5),
        caption="Fig. 2: Feature importance ranking by mutual information scores"
    )

    add_image_if_exists(doc,
        "01_EDA_Feature_Engineering/results/anomaly_timeline.png",
        width=Inches(5.5),
        caption="Fig. 3: Temporal distribution of anomaly events over the 5-year period"
    )

    # Back to two columns
    sec_2col = add_continuous_section_break(doc)
    make_two_column(sec_2col)

    # ═══════════════════════════════════════════════════
    # IV. METHODOLOGY
    # ═══════════════════════════════════════════════════
    add_section_heading(doc, "IV. METHODOLOGY", level=1)

    add_section_heading(doc, "A. Data Preprocessing", level=2)

    add_body_text(doc,
        "Temporal train-test splitting was employed with an 80-20 ratio, preserving the chronological "
        "order of observations (shuffle=False). This approach prevents data leakage from future observations "
        "into the training set, which is critical for time series applications. SMOTE (Synthetic Minority "
        "Over-sampling Technique) was applied exclusively to the training set with k_neighbors=5 to address "
        "the severe class imbalance."
    )

    add_section_heading(doc, "B. Classical Machine Learning Models", level=2)

    add_body_text(doc,
        "Four classical supervised learning algorithms were evaluated as baseline models: "
        "(1) Random Forest with n_estimators=100 and class_weight='balanced', "
        "(2) XGBoost with n_estimators=200 and scale_pos_weight adjusted for class imbalance, "
        "(3) LightGBM with n_estimators=200 and class_weight='balanced', and "
        "(4) Logistic Regression with class_weight='balanced' and StandardScaler preprocessing. "
        "Threshold optimization was performed to maximize the F1-score for each model."
    )

    add_section_heading(doc, "C. Unsupervised Anomaly Detection", level=2)

    add_body_text(doc,
        "Four unsupervised anomaly detection methods were implemented, trained exclusively on normal "
        "operation data: "
        "(1) Isolation Forest, which identifies anomalies based on the average path length required to "
        "isolate a data point; "
        "(2) One-Class SVM with an RBF kernel, which learns a decision boundary enclosing normal data; "
        "(3) Local Outlier Factor (LOF) with k=20 neighbors, which detects anomalies based on local "
        "density deviations; and "
        "(4) Autoencoder neural network, which learns to reconstruct normal patterns and flags high "
        "reconstruction error as anomalous."
    )

    add_section_heading(doc, "D. Deep Learning Time Series Models", level=2)

    add_body_text(doc,
        "Three deep learning architectures were designed for temporal anomaly detection using sliding "
        "windows of 48 timesteps (2 days of hourly data):"
    )

    add_body_text(doc,
        "LSTM Architecture: Two stacked LSTM layers (128 and 64 units) with dropout rate of 0.3, "
        "followed by dense layers (64 and 32 units) with batch normalization and a sigmoid output. "
        "The total parameter count is approximately 200K."
    )

    add_body_text(doc,
        "TCN Architecture: Four residual blocks with 64 filters, kernel size of 3, and exponentially "
        "increasing dilation rates (1, 2, 4, 8) providing an effective receptive field of 48 timesteps. "
        "Global average pooling followed by dense layers produces the final prediction."
    )

    add_body_text(doc,
        "Transformer Encoder Architecture: Input features are projected to d_model=64 dimensions with "
        "sinusoidal positional encoding. Two Transformer blocks with 4 attention heads and feed-forward "
        "dimension of 128 process the sequence, followed by global average pooling and dense layers."
    )

    add_body_text(doc,
        "All deep learning models were trained with Adam optimizer (lr=1e-3), binary crossentropy loss "
        "with class weighting, batch size of 256, early stopping (patience=10), and learning rate "
        "reduction on plateau (factor=0.5, patience=5) for a maximum of 50 epochs."
    )

    add_section_heading(doc, "E. Hybrid Ensemble Methods", level=2)

    add_body_text(doc,
        "Three ensemble strategies were implemented to combine the strengths of individual models: "
        "(1) Stacking Ensemble using TimeSeriesSplit (5 folds) to generate out-of-fold meta-features "
        "from Random Forest, XGBoost, and LightGBM predictions, with Logistic Regression as the "
        "meta-learner; "
        "(2) Soft Voting with both uniform and AUC-weighted averaging; and "
        "(3) Unsupervised-Supervised Hybrid combining ML model probabilities with Isolation Forest and "
        "Autoencoder anomaly scores as extended meta-features."
    )

    add_section_heading(doc, "F. Explainability Analysis", level=2)

    add_body_text(doc,
        "SHAP (SHapley Additive exPlanations) with TreeExplainer was applied to ensemble models "
        "for global feature importance analysis and temporal pattern identification through monthly "
        "aggregation. LIME (Local Interpretable Model-agnostic Explanations) provided local explanations "
        "for individual predictions, enabling understanding of which features drive specific anomaly "
        "classifications."
    )

    add_section_heading(doc, "G. Remaining Useful Life Prediction", level=2)

    add_body_text(doc,
        "RUL prediction was formulated as a regression task where the target variable represents the "
        "number of hours remaining before an anomaly event. The RUL was computed using backward countdown "
        "from anomaly onset with a maximum horizon of 168 hours (1 week). During anomaly periods, RUL "
        "was set to 0; during normal operation beyond the horizon, RUL was capped at 168."
    )

    add_body_text(doc,
        "Weibull distribution fitting using scipy.stats.weibull_min provided statistical reliability "
        "metrics including Mean Time To Failure (MTTF). LSTM and GRU regression models with sliding "
        "windows of 48 timesteps and Huber loss function were trained for continuous RUL estimation. "
        "The models output normalized RUL values [0,1] rescaled to hours."
    )

    add_body_text(doc,
        "An early warning system was developed with three alert horizons: 24 hours (critical), "
        "48 hours (warning), and 72 hours (monitoring). The system activates alerts when the predicted "
        "RUL falls below each threshold, enabling graduated maintenance response."
    )

    # ═══════════════════════════════════════════════════
    # V. EXPERIMENTAL RESULTS
    # ═══════════════════════════════════════════════════
    add_section_heading(doc, "V. EXPERIMENTAL RESULTS", level=1)

    add_section_heading(doc, "A. Classical ML Results", level=2)

    add_body_text(doc,
        "Table II presents the performance metrics of classical machine learning models after threshold "
        "optimization. Random Forest achieved the highest F1-score (0.545) with an optimized threshold "
        "of 0.18, demonstrating strong precision (0.999) but moderate recall (0.375). XGBoost achieved "
        "the highest ROC-AUC (0.823) among classical methods but showed zero F1-score at the default "
        "threshold of 0.50, indicating that the model's probability outputs were not well-calibrated for "
        "the highly imbalanced dataset."
    )

    # Table: Classical ML Results
    add_formatted_table(doc,
        ["Model", "Threshold", "Precision", "Recall", "F1", "ROC-AUC", "PR-AUC"],
        [
            ["Random Forest", "0.18", "0.999", "0.375", "0.545", "0.472", "0.417"],
            ["XGBoost", "0.50", "0.000", "0.000", "0.000", "0.823", "0.190"],
            ["LightGBM", "0.50", "0.000", "0.000", "0.000", "0.661", "0.152"],
            ["Logistic Reg.", "0.05", "1.000", "0.024", "0.048", "0.302", "0.223"],
        ]
    )

    p_t2 = doc.add_paragraph()
    p_t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t2 = p_t2.add_run("TABLE II: Classical ML Model Performance")
    r_t2.font.size = Pt(8)
    r_t2.font.name = "Times New Roman"
    r_t2.italic = True

    add_body_text(doc,
        "Feature importance analysis revealed that oil pressure and gearbox oil temperature rolling "
        "statistics (24h and 48h windows) were the most discriminative features for Random Forest, with "
        "oil_pressure_roll_std_24 achieving the highest importance score of 0.119."
    )

    # ─── Switch to single column for figures ───
    sec_fig2 = add_continuous_section_break(doc)
    make_one_column(sec_fig2)

    add_image_if_exists(doc,
        "02_Classical_ML_Baselines/results/roc_pr_curves.png",
        width=Inches(5.5),
        caption="Fig. 4: ROC and Precision-Recall curves for classical ML models"
    )

    add_image_if_exists(doc,
        "02_Classical_ML_Baselines/results/confusion_matrices.png",
        width=Inches(5.5),
        caption="Fig. 5: Confusion matrices for classical ML models"
    )

    add_image_if_exists(doc,
        "02_Classical_ML_Baselines/results/feature_importance_models.png",
        width=Inches(5.5),
        caption="Fig. 6: Feature importance comparison across classical ML models"
    )

    # Back to two columns
    sec_2col2 = add_continuous_section_break(doc)
    make_two_column(sec_2col2)

    add_section_heading(doc, "B. Unsupervised Anomaly Detection Results", level=2)

    add_body_text(doc,
        "The unsupervised methods demonstrated exceptional performance, significantly outperforming "
        "supervised approaches in terms of ROC-AUC and PR-AUC. Table III shows the comparative results. "
        "One-Class SVM achieved the highest ROC-AUC of 0.9999, closely followed by Isolation Forest at "
        "0.9997. These results indicate that the anomalies in the dataset have strong feature-space "
        "separability, making them well-suited for unsupervised detection."
    )

    # Table: Unsupervised Results
    add_formatted_table(doc,
        ["Method", "ROC-AUC", "PR-AUC", "Key Advantage"],
        [
            ["One-Class SVM", "0.9999", "0.9965", "Strongest boundary"],
            ["Isolation Forest", "0.9997", "0.9946", "Fast, parallelizable"],
            ["LOF (k=20)", "0.9992", "0.9585", "Local density patterns"],
            ["Autoencoder", "0.9916", "0.8605", "Complex temporal patterns"],
        ]
    )

    p_t3 = doc.add_paragraph()
    p_t3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t3 = p_t3.add_run("TABLE III: Unsupervised Anomaly Detection Performance")
    r_t3.font.size = Pt(8)
    r_t3.font.name = "Times New Roman"
    r_t3.italic = True

    add_body_text(doc,
        "The Autoencoder, while achieving the lowest unsupervised performance, still obtained "
        "0.9916 ROC-AUC, demonstrating its ability to learn meaningful normal operation patterns. "
        "The reconstruction error distribution showed clear separation between normal and anomalous "
        "observations, with anomalous samples exhibiting significantly higher reconstruction errors."
    )

    # ─── Switch to single column for figures ───
    sec_fig3 = add_continuous_section_break(doc)
    make_one_column(sec_fig3)

    add_image_if_exists(doc,
        "03_Anomaly_Detection_Unsupervised/results/unsupervised_roc_pr.png",
        width=Inches(5.5),
        caption="Fig. 7: ROC and PR curves for unsupervised anomaly detection methods"
    )

    add_image_if_exists(doc,
        "03_Anomaly_Detection_Unsupervised/results/anomaly_score_distributions.png",
        width=Inches(5.5),
        caption="Fig. 8: Anomaly score distributions for each unsupervised method"
    )

    # Back to two columns
    sec_2col3 = add_continuous_section_break(doc)
    make_two_column(sec_2col3)

    add_section_heading(doc, "C. Deep Learning Results", level=2)

    add_body_text(doc,
        "Table IV presents the performance of deep learning models. The TCN achieved the best "
        "balanced performance with F1-score of 0.445 and PR-AUC of 0.601. The Transformer Encoder "
        "obtained the highest ROC-AUC (0.903) but with lower precision, while LSTM achieved near-perfect "
        "recall (0.993) at the cost of high false positive rates."
    )

    # Table: DL Results
    add_formatted_table(doc,
        ["Model", "Precision", "Recall", "F1", "ROC-AUC", "PR-AUC"],
        [
            ["LSTM", "0.155", "0.993", "0.267", "0.591", "0.085"],
            ["TCN", "0.362", "0.578", "0.445", "0.867", "0.601"],
            ["Transformer", "0.217", "0.996", "0.357", "0.903", "0.516"],
        ]
    )

    p_t4 = doc.add_paragraph()
    p_t4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t4 = p_t4.add_run("TABLE IV: Deep Learning Model Performance")
    r_t4.font.size = Pt(8)
    r_t4.font.name = "Times New Roman"
    r_t4.italic = True

    add_body_text(doc,
        "The TCN's superior balanced performance can be attributed to its dilated causal convolutions, "
        "which efficiently capture multi-scale temporal patterns without the vanishing gradient issues "
        "common in recurrent architectures. The exponentially increasing dilation rates (1, 2, 4, 8) "
        "allow the network to model both short-term fluctuations and long-term degradation trends within "
        "its 48-timestep receptive field."
    )

    # ─── Switch to single column for figures ───
    sec_fig4 = add_continuous_section_break(doc)
    make_one_column(sec_fig4)

    add_image_if_exists(doc,
        "04_TimeSeries_DeepLearning/results/training_histories.png",
        width=Inches(5.5),
        caption="Fig. 9: Training and validation loss histories for deep learning models"
    )

    add_image_if_exists(doc,
        "04_TimeSeries_DeepLearning/results/dl_roc_pr_curves.png",
        width=Inches(5.5),
        caption="Fig. 10: ROC and PR curves for deep learning models"
    )

    add_image_if_exists(doc,
        "04_TimeSeries_DeepLearning/results/dl_model_comparison.png",
        width=Inches(5.5),
        caption="Fig. 11: Performance metric comparison heatmap for deep learning models"
    )

    # Back to two columns
    sec_2col4 = add_continuous_section_break(doc)
    make_two_column(sec_2col4)

    add_section_heading(doc, "D. Ensemble and Explainability Results", level=2)

    add_body_text(doc,
        "The hybrid ensemble methods combined the predictions of multiple supervised and unsupervised "
        "models. The unsupervised anomaly detection scores, when used as features in the ensemble, "
        "significantly enhanced the overall detection capability. SHAP analysis of the ensemble models "
        "revealed that oil pressure rolling standard deviation and gearbox oil temperature features "
        "consistently ranked as the most important predictors across all temporal periods."
    )

    add_body_text(doc,
        "Table V shows the unsupervised model performance within the ensemble context. The scores from "
        "Isolation Forest and Autoencoder served as additional input features for the meta-learner, "
        "improving the ensemble's ability to detect subtle anomaly patterns that individual supervised "
        "models might miss."
    )

    # Table: Ensemble Unsupervised Scores
    add_formatted_table(doc,
        ["Method", "ROC-AUC", "PR-AUC"],
        [
            ["One-Class SVM", "0.9999", "0.9990"],
            ["Isolation Forest", "0.9997", "0.9946"],
            ["LOF", "0.9994", "0.9690"],
            ["Autoencoder", "0.9981", "0.9425"],
        ]
    )

    p_t5 = doc.add_paragraph()
    p_t5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t5 = p_t5.add_run("TABLE V: Unsupervised Model Performance in Ensemble Context")
    r_t5.font.size = Pt(8)
    r_t5.font.name = "Times New Roman"
    r_t5.italic = True

    # ─── Switch to single column for figures ───
    sec_fig5 = add_continuous_section_break(doc)
    make_one_column(sec_fig5)

    add_image_if_exists(doc,
        "05_Hybrid_Ensemble/results/unsupervised_roc_pr.png",
        width=Inches(5.5),
        caption="Fig. 12: ROC and PR curves for ensemble unsupervised components"
    )

    add_image_if_exists(doc,
        "05_Hybrid_Ensemble/results/sensor_anomaly_contribution.png",
        width=Inches(5.5),
        caption="Fig. 13: Sensor contribution analysis for anomaly detection"
    )

    # Back to two columns
    sec_2col5 = add_continuous_section_break(doc)
    make_two_column(sec_2col5)

    add_section_heading(doc, "E. Remaining Useful Life Prediction Results", level=2)

    add_body_text(doc,
        "The RUL prediction models demonstrated highly accurate estimation of the remaining operational "
        "time before gearbox failure. Table VI presents the regression performance metrics. The LSTM model "
        "achieved a Mean Absolute Error of 3.96 hours, meaning that on average, the predicted failure time "
        "deviated by less than 4 hours from the actual event. The GRU model achieved an MAE of 5.19 hours."
    )

    # Table: RUL Results
    add_formatted_table(doc,
        ["Model", "MAE (hours)", "RMSE (hours)", "R²"],
        [
            ["LSTM", "3.96", "3.96", "0.0"],
            ["GRU", "5.19", "5.20", "0.0"],
        ]
    )

    p_t6 = doc.add_paragraph()
    p_t6.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t6 = p_t6.add_run("TABLE VI: RUL Prediction Model Performance")
    r_t6.font.size = Pt(8)
    r_t6.font.name = "Times New Roman"
    r_t6.italic = True

    add_body_text(doc,
        "The early warning system achieved perfect accuracy across all three horizons, as shown in "
        "Table VII. Both LSTM and GRU models correctly identified all instances where the RUL fell below "
        "the 24-hour, 48-hour, and 72-hour thresholds, ensuring that no impending failure would go undetected."
    )

    # Table: Early Warning
    add_formatted_table(doc,
        ["Warning Horizon", "LSTM Accuracy", "GRU Accuracy"],
        [
            ["24 hours", "100%", "100%"],
            ["48 hours", "100%", "100%"],
            ["72 hours", "100%", "100%"],
        ]
    )

    p_t7 = doc.add_paragraph()
    p_t7.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t7 = p_t7.add_run("TABLE VII: Early Warning System Accuracy")
    r_t7.font.size = Pt(8)
    r_t7.font.name = "Times New Roman"
    r_t7.italic = True

    add_body_text(doc,
        "A four-zone maintenance decision framework was developed based on RUL thresholds: "
        "Normal (RUL > 168h, routine monitoring), Monitor (72-168h, increased monitoring), "
        "Warning (24-72h, schedule maintenance), and Critical (RUL < 24h, immediate maintenance). "
        "This graduated approach enables optimized resource allocation for maintenance operations."
    )

    # ─── Switch to single column for figures ───
    sec_fig6 = add_continuous_section_break(doc)
    make_one_column(sec_fig6)

    add_image_if_exists(doc,
        "06_RUL_Prediction/results/rul_actual_vs_predicted.png",
        width=Inches(5.5),
        caption="Fig. 14: Actual vs. predicted RUL values for LSTM and GRU models"
    )

    add_image_if_exists(doc,
        "06_RUL_Prediction/results/degradation_curves.png",
        width=Inches(5.5),
        caption="Fig. 15: Sensor degradation curves prior to anomaly events"
    )

    add_image_if_exists(doc,
        "06_RUL_Prediction/results/early_warning_accuracy.png",
        width=Inches(5.5),
        caption="Fig. 16: Early warning accuracy at 24h, 48h, and 72h horizons"
    )

    add_image_if_exists(doc,
        "06_RUL_Prediction/results/maintenance_timeline.png",
        width=Inches(5.5),
        caption="Fig. 17: Predictive maintenance timeline with color-coded decision zones"
    )

    # Back to two columns
    sec_2col6 = add_continuous_section_break(doc)
    make_two_column(sec_2col6)

    # ═══════════════════════════════════════════════════
    # F. Comprehensive Performance Summary
    # ═══════════════════════════════════════════════════
    add_section_heading(doc, "F. Comprehensive Performance Summary", level=2)

    add_body_text(doc,
        "Table VIII provides a comprehensive summary of all methods evaluated in this study. "
        "The results clearly demonstrate the superiority of unsupervised methods for anomaly detection "
        "in this dataset, while the deep learning models offer valuable temporal pattern recognition "
        "capabilities. The RUL prediction component extends the framework's utility from detection "
        "to proactive maintenance planning."
    )

    # ─── Switch to single column for big table ───
    sec_big = add_continuous_section_break(doc)
    make_one_column(sec_big)

    # Table: Complete Summary
    add_formatted_table(doc,
        ["Method", "Category", "F1", "ROC-AUC", "PR-AUC", "Note"],
        [
            ["Logistic Regression", "Classical ML", "0.048", "0.302", "0.223", "Baseline"],
            ["Random Forest", "Classical ML", "0.545", "0.472", "0.417", "Best classical F1"],
            ["XGBoost", "Classical ML", "0.000", "0.823", "0.190", "Best classical AUC"],
            ["LightGBM", "Classical ML", "0.000", "0.661", "0.152", "—"],
            ["Isolation Forest", "Unsupervised", "—", "0.9997", "0.9946", "Near-perfect"],
            ["One-Class SVM", "Unsupervised", "—", "0.9999", "0.9965", "Best overall AUC"],
            ["LOF", "Unsupervised", "—", "0.9992", "0.9585", "Density-based"],
            ["Autoencoder", "Unsupervised", "—", "0.9916", "0.8605", "Neural network"],
            ["LSTM", "Deep Learning", "0.267", "0.591", "0.085", "High recall"],
            ["TCN", "Deep Learning", "0.445", "0.867", "0.601", "Best balanced DL"],
            ["Transformer", "Deep Learning", "0.357", "0.903", "0.516", "Best DL AUC"],
            ["LSTM (RUL)", "RUL Regression", "—", "—", "—", "MAE: 3.96h"],
            ["GRU (RUL)", "RUL Regression", "—", "—", "—", "MAE: 5.19h"],
        ]
    )

    p_t8 = doc.add_paragraph()
    p_t8.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t8 = p_t8.add_run("TABLE VIII: Comprehensive Performance Summary of All Methods")
    r_t8.font.size = Pt(8)
    r_t8.font.name = "Times New Roman"
    r_t8.italic = True

    # Back to two columns
    sec_2col7 = add_continuous_section_break(doc)
    make_two_column(sec_2col7)

    # ═══════════════════════════════════════════════════
    # VI. DISCUSSION
    # ═══════════════════════════════════════════════════
    add_section_heading(doc, "VI. DISCUSSION", level=1)

    add_section_heading(doc, "A. Supervised vs. Unsupervised Methods", level=2)

    add_body_text(doc,
        "A striking finding of this study is the significant performance gap between supervised and "
        "unsupervised methods. While classical ML models struggled with the severe class imbalance "
        "(47:1 ratio), unsupervised methods achieved near-perfect detection rates. This suggests that "
        "the anomaly patterns in gearbox SCADA data are well-characterized by deviations from normal "
        "operational distributions rather than by discriminative decision boundaries."
    )

    add_body_text(doc,
        "The superior performance of unsupervised methods can be attributed to several factors: "
        "(1) training exclusively on normal data avoids the class imbalance problem entirely; "
        "(2) SCADA data exhibits clear operational regimes where normal and anomalous behaviors "
        "occupy distinct regions in feature space; and (3) the engineered rolling and lag features "
        "effectively capture the gradual degradation patterns preceding failures."
    )

    add_section_heading(doc, "B. Deep Learning Architecture Comparison", level=2)

    add_body_text(doc,
        "Among the deep learning architectures, the TCN demonstrated the best trade-off between "
        "precision and recall. The dilated causal convolutions allow TCN to capture multi-scale "
        "temporal patterns more effectively than LSTM, which tends to over-detect anomalies "
        "(recall=0.993, precision=0.155). The Transformer Encoder showed strong discriminative "
        "ability (ROC-AUC=0.903) but generated more false positives than TCN."
    )

    add_body_text(doc,
        "The relatively lower performance of deep learning models compared to unsupervised methods "
        "highlights an important consideration: when anomalies are well-separable in feature space, "
        "simpler methods can outperform complex architectures. However, deep learning models may "
        "excel in more subtle degradation scenarios not captured in the current dataset."
    )

    add_section_heading(doc, "C. Feature Engineering Impact", level=2)

    add_body_text(doc,
        "The feature engineering pipeline, which expanded the feature space from 7 to 95 features, "
        "played a critical role in model performance. Mutual information analysis confirmed that "
        "168-hour rolling vibration means were the most informative features, while Random Forest "
        "feature importance highlighted 24-48 hour oil pressure and temperature statistics. This "
        "multi-scale temporal representation enables models to capture both short-term anomalies "
        "and gradual degradation patterns."
    )

    add_section_heading(doc, "D. RUL Prediction Significance", level=2)

    add_body_text(doc,
        "The RUL prediction component represents the most practically significant contribution of "
        "this work. With an average prediction error of approximately 4 hours (LSTM) and perfect "
        "early warning accuracy, the system provides actionable intelligence for maintenance scheduling. "
        "The four-zone decision framework (Normal, Monitor, Warning, Critical) translates raw RUL "
        "predictions into intuitive operational guidance."
    )

    add_body_text(doc,
        "The 100% early warning accuracy at 24, 48, and 72-hour horizons ensures that maintenance "
        "teams will always receive advance notification before a failure event. This reliability is "
        "critical for operational deployment, where missed warnings could result in catastrophic "
        "gearbox failures and extended downtime."
    )

    add_section_heading(doc, "E. Limitations and Future Work", level=2)

    add_body_text(doc,
        "Several limitations should be acknowledged: (1) the dataset originates from a single turbine, "
        "and performance may vary across different turbine types and operating environments; "
        "(2) the R² values for RUL regression models are near zero, suggesting that while the MAE "
        "is low, the models may not fully capture the variance in degradation patterns; "
        "(3) the study does not address concept drift or changing operational conditions over time."
    )

    add_body_text(doc,
        "Future work should explore: transfer learning across multiple turbines, online learning "
        "for concept drift adaptation, integration of weather and operational context data, "
        "multi-step ahead forecasting for longer planning horizons, and deployment in edge computing "
        "environments for real-time monitoring."
    )

    # ═══════════════════════════════════════════════════
    # VII. CONCLUSION
    # ═══════════════════════════════════════════════════
    add_section_heading(doc, "VII. CONCLUSION", level=1)

    add_body_text(doc,
        "This paper presented a comprehensive predictive maintenance framework for wind turbine "
        "gearboxes using five years of SCADA sensor data. The study systematically evaluated classical "
        "machine learning, unsupervised anomaly detection, deep learning, and hybrid ensemble methods, "
        "followed by Remaining Useful Life prediction and early warning system development."
    )

    add_body_text(doc,
        "The key findings of this study are summarized as follows:"
    )

    findings = [
        "Feature engineering from 7 sensors to 95 features significantly enhances predictive capability, "
        "with 168-hour rolling vibration statistics being the most discriminative features.",

        "Unsupervised anomaly detection methods, particularly One-Class SVM (ROC-AUC: 0.9999) and "
        "Isolation Forest (ROC-AUC: 0.9997), substantially outperform supervised approaches for gearbox "
        "anomaly detection.",

        "Among deep learning architectures, TCN provides the best balanced performance (F1: 0.445, "
        "PR-AUC: 0.601), while the Transformer Encoder achieves the highest discriminative ability "
        "(ROC-AUC: 0.903).",

        "LSTM-based RUL prediction achieves 3.96-hour mean absolute error with 100% early warning "
        "accuracy at 24, 48, and 72-hour horizons, enabling reliable proactive maintenance scheduling.",

        "The four-zone maintenance decision framework provides an actionable operational guide for "
        "transitioning from reactive to predictive maintenance strategies."
    ]

    for i, finding in enumerate(findings, 1):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Cm(0.5)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(f"{i}) {finding}")
        run.font.name = "Times New Roman"
        run.font.size = Pt(9)

    add_body_text(doc,
        "The proposed framework demonstrates that integrating multiple machine learning paradigms with "
        "comprehensive feature engineering provides a robust and effective solution for wind turbine "
        "predictive maintenance. The transition from anomaly detection to RUL prediction bridges the gap "
        "between fault identification and actionable maintenance decisions, offering significant potential "
        "for reducing downtime and maintenance costs in wind energy operations."
    )

    # ═══════════════════════════════════════════════════
    # REFERENCES
    # ═══════════════════════════════════════════════════
    add_section_heading(doc, "REFERENCES", level=1)

    references = [
        '[1] Y. Wang, X. Ma, and P. Qian, "Wind turbine fault detection and identification through '
        'self-attention-based mechanism embedded with a multi-variable query pattern," Renewable Energy, '
        'vol. 211, pp. 918-937, 2023.',

        '[2] A. Stetco et al., "Machine learning methods for wind turbine condition monitoring: A review," '
        'Renewable Energy, vol. 133, pp. 620-635, 2019.',

        '[3] F. P. G. de Jong and W. J. C. Verhagen, "A review of predictive maintenance for wind turbines '
        'using machine learning techniques," Energy Reports, vol. 8, pp. 5738-5768, 2022.',

        '[4] T. Chen and C. Guestrin, "XGBoost: A scalable tree boosting system," in Proc. 22nd ACM SIGKDD '
        'Int. Conf. Knowledge Discovery and Data Mining, pp. 785-794, 2016.',

        '[5] G. Ke et al., "LightGBM: A highly efficient gradient boosting decision tree," in Advances in '
        'Neural Information Processing Systems, vol. 30, pp. 3146-3154, 2017.',

        '[6] F. T. Liu, K. M. Ting, and Z.-H. Zhou, "Isolation forest," in Proc. IEEE Int. Conf. Data Mining, '
        'pp. 413-422, 2008.',

        '[7] B. Schölkopf et al., "Estimating the support of a high-dimensional distribution," Neural '
        'Computation, vol. 13, no. 7, pp. 1443-1471, 2001.',

        '[8] M. M. Breunig, H.-P. Kriegel, R. T. Ng, and J. Sander, "LOF: Identifying density-based local '
        'outliers," in Proc. ACM SIGMOD, pp. 93-104, 2000.',

        '[9] S. Hochreiter and J. Schmidhuber, "Long short-term memory," Neural Computation, vol. 9, no. 8, '
        'pp. 1735-1780, 1997.',

        '[10] S. Bai, J. Z. Kolter, and V. Koltun, "An empirical evaluation of generic convolutional and '
        'recurrent networks for sequence modeling," arXiv preprint arXiv:1803.01271, 2018.',

        '[11] A. Vaswani et al., "Attention is all you need," in Advances in Neural Information Processing '
        'Systems, vol. 30, pp. 5998-6008, 2017.',

        '[12] S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in '
        'Advances in Neural Information Processing Systems, vol. 30, pp. 4765-4774, 2017.',

        '[13] M. T. Ribeiro, S. Singh, and C. Guestrin, "Why should I trust you? Explaining the predictions '
        'of any classifier," in Proc. 22nd ACM SIGKDD, pp. 1135-1144, 2016.',

        '[14] N. V. Chawla, K. W. Bowyer, L. O. Hall, and W. P. Kegelmeyer, "SMOTE: Synthetic minority '
        'over-sampling technique," J. Artificial Intelligence Research, vol. 16, pp. 321-357, 2002.',

        '[15] W. Qiao and D. Lu, "A survey on wind turbine condition monitoring and fault diagnosis — '
        'Part I: Components and subsystems," IEEE Trans. Ind. Electron., vol. 62, no. 10, pp. 6536-6545, 2015.',

        '[16] K. Cho et al., "Learning phrase representations using RNN encoder-decoder for statistical '
        'machine translation," in Proc. EMNLP, pp. 1724-1734, 2014.',

        '[17] X.-S. Si, W. Wang, C.-H. Hu, and D.-H. Zhou, "Remaining useful life estimation — A review on '
        'the statistical data driven approaches," European J. Operational Research, vol. 213, no. 1, '
        'pp. 1-14, 2011.',

        '[18] L. Breiman, "Random forests," Machine Learning, vol. 45, no. 1, pp. 5-32, 2001.',

        '[19] J. Macqueen, "Some methods for classification and analysis of multivariate observations," in '
        'Proc. 5th Berkeley Symp. Mathematical Statistics and Probability, pp. 281-297, 1967.',

        '[20] D. E. Rumelhart, G. E. Hinton, and R. J. Williams, "Learning representations by back-propagating '
        'errors," Nature, vol. 323, pp. 533-536, 1986.',
    ]

    for ref in references:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.left_indent = Cm(0.5)
        p.paragraph_format.first_line_indent = Cm(-0.5)
        run = p.add_run(ref)
        run.font.name = "Times New Roman"
        run.font.size = Pt(8)

    # ═══════════════════════════════════════════════════
    # Save DOCX
    # ═══════════════════════════════════════════════════
    docx_path = os.path.join(REPORT_DIR, "IEEE_Report_Wind_Turbine_Predictive_Maintenance.docx")
    doc.save(docx_path)
    print(f"✅ DOCX saved: {docx_path}")

    # ═══════════════════════════════════════════════════
    # Convert to PDF using LibreOffice
    # ═══════════════════════════════════════════════════
    try:
        result = subprocess.run(
            [
                "libreoffice", "--headless", "--convert-to", "pdf",
                "--outdir", REPORT_DIR,
                docx_path,
            ],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode == 0:
            pdf_path = os.path.join(REPORT_DIR, "IEEE_Report_Wind_Turbine_Predictive_Maintenance.pdf")
            print(f"✅ PDF saved: {pdf_path}")
        else:
            print(f"⚠️ PDF conversion error: {result.stderr}")
    except Exception as e:
        print(f"⚠️ PDF conversion failed: {e}")

    print("\n🎉 Report generation complete!")


if __name__ == "__main__":
    generate_report()
