# Machine Learning Pipeline - Phishing URL Detection

This directory contains dataset processing, exploratory analysis, Random Forest model training, evaluation metrics, serialized artifacts, and feature extraction documentation for the **AI Phishing Detection System**.

---

## 📌 Dataset Overview

- **Dataset Source**: [UCI Machine Learning Repository - Phishing Websites (ID: 327)](https://archive.ics.uci.edu/dataset/327/phishing)
- **Dataset Size**: 11,055 total records (8,844 train / 2,211 test)
- **Total Columns**: 31 columns (30 feature variables + 1 target variable `result`)
- **Dataset Citation**: 
  > Mohammad, R. M., Thabtah, F., & McCluskey, L. (2012). *Phishing Websites Dataset*. UCI Machine Learning Repository. https://doi.org/10.24432/C55W4D.

---

## 📊 1. Exploratory Data Analysis (EDA)

Exploratory analysis was conducted strictly on the training set (`ml/data/train.csv`):
- **Target Balance**: 55.70% Legitimate (`1`) vs 44.30% Phishing (`-1`).
- **Key Visualizations Saved**:
  - `ml/outputs/eda/class_distribution.png`: Target class frequency bar chart.
  - `ml/outputs/eda/correlation_heatmap.png`: Full 31x31 Pearson correlation matrix.
  - `ml/outputs/eda/feature_importance_eda.png`: Feature correlation with target variable.
  - `ml/outputs/eda/feature_distributions.png`: Distributions of top correlated features (`sslfinal_state`, `url_of_anchor`, `prefix_suffix`, `web_traffic`).
  - `ml/outputs/eda/target_distribution.png`: Class proportion pie chart.

---

## 🌲 2. Model & Algorithm

- **Model Type**: Random Forest Classifier (`sklearn.ensemble.RandomForestClassifier`)
- **Config**:
  - `n_estimators`: 200
  - `random_state`: 42
  - `n_jobs`: -1
  - `max_depth`: None

---

## 🏋️ 3. Training Process

- Trained exclusively on `ml/data/train.csv` (8,844 samples, 30 features).
- **Data Leakage Prevention**:
  - The 80/20 train/test split was performed before model training.
  - Test set samples were never seen during model fitting.
- **Serialized Artifacts**:
  - `ml/models/phishing_rf_model.pkl`: Serialized Random Forest model artifact.
  - `ml/models/feature_columns.pkl`: Ordered feature column names list.
  - `ml/models/model_metadata.json`: Model metadata & performance metrics.

---

## 📈 4. Measured Evaluation Metrics

Evaluated exclusively on `ml/data/test.csv` (2,211 unseen test samples):

| Metric | Score | Percentage |
|---|---|---|
| **Accuracy** | `0.9742` | **97.42%** |
| **Phishing Precision (-1)** | `0.9782` | **97.82%** |
| **Phishing Recall (-1)** | `0.9633` | **96.33%** |
| **Phishing F1-Score (-1)** | `0.9707` | **97.07%** |
| **Macro F1-Score** | `0.9738` | **97.38%** |

### Confusion Matrix (Test Set: 2,211 Samples)

| Actual \ Predicted | Predicted Phishing (-1) | Predicted Legitimate (1) |
|---|---|---|
| **Actual Phishing (-1)** | **944** (True Phishing) | 36 (False Legitimate) |
| **Actual Legitimate (1)** | 21 (False Phishing) | **1,210** (True Legitimate) |

---

## 🔑 5. Real-Time Feature Extraction (Phase 4)

Real-time feature extraction connects raw URLs to the trained Random Forest model via `backend/app/services/url_feature_extractor.py`:

- **URL-derived Features (12 Features)**: `having_ip_address`, `url_length`, `shortining_service`, `having_at_symbol`, `double_slash_redirecting`, `prefix_suffix`, `having_sub_domain`, `sslfinal_state`, `port`, `https_token`, `abnormal_url`, `redirect`.
- **Webpage & Domain-derived Features (18 Features)**: Documented with safe fallbacks in `backend/app/services/feature_metadata.py` to prevent SSRF vulnerabilities.
- **Column Order Enforcement**: Features are formatted into a DataFrame reordered 100% identically according to `ml/models/feature_columns.pkl`.

---

## ⚠️ 6. Model Limitations

> [!IMPORTANT]
> - **Inference Wording**: Predictions output `"likely_phishing"` or `"likely_legitimate"`. The model does **not** claim a URL is "100% safe".
> - **Static Analysis Scope**: Feature extraction inspects URL structure and metadata. Automated external HTTP crawling is disabled for SSRF safety.

---

## 🔄 7. Reproducibility & Testing Instructions

### Run Automated Unit Tests
```bash
pytest tests/
```

### Run Model Evaluation
```bash
python ml/src/evaluate_model.py
```
