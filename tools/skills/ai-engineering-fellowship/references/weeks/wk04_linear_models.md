# Week 4: Statistical ML: Linear Models (Churn & CLV)

---
relevancy_tier: CALIBRATED_REFERENCE
mentor_score: 88/100
fellowship_rating: 8.5/10
classroom_id: 864517298853
quiz_id: 864506361006
local_path: F:\FuseAIF2026\M1\WK4
github_repo: https://github.com/AaradhyaDT/fuseAiF_wk4_linear_models
---

## 1. Overview & Problem Formulation
- **Scenario**: Data Scientist at a Telecom Company predicting churn and Customer Lifetime Value (CLV).
- **Dataset**: Telco Customer Churn (Kaggle), 7,043 rows, 21 features (~26.5% positive churn rate).
- **Core Models**: Logistic Regression (L1/L2), Ridge Classifier, SGDClassifier, Ridge Regression for CLV.
- **Validation**: Stratified 5-fold cross-validation, ROC-AUC $0.841 \pm 0.005$.

---

## 2. SOTA Industry Best Practices & Production Standards
- **Cost-Utility Threshold Tuning**: The default 0.5 decision threshold minimizes overall error rate, which severely under-penalizes False Negatives in churn retention. The decision threshold was empirically tuned to **0.385**, optimizing high-risk capture for a targeted top-200 customer budget segment.
- **Zero-Leakage In-Fold Preprocessing**: Numeric imputation and standard scaling are fitted exclusively within each cross-validation fold using `sklearn.pipeline.Pipeline`.
- **Target Leakage Detection**: Explicitly tested and removed columns such as `TotalCharges` when predicting customer tenure, since total charges is a direct algebraic product of monthly charges and tenure.

---

## 3. Mentor Evaluation & Quality Rating
- **Assignment Grade**: **88 / 100** (W4: Linear Model Assignment).
- **Quiz Score**: **23 / 25** (Linear Model Quiz Assignment).
- **Fellowship Rating**: **8.5 / 10**.
- **Mentor Calibration Note**: Excellent problem formulation and threshold tuning; minor suggestions on documenting the regularization penalty path (Lasso L1 shrinkage coefficient profiles).

---

## 4. Local-First & GitHub Fallback Resolution (`INV-RESOLVE-FUSE`)
- **Local Directory**: [`F:\FuseAIF2026\M1\WK4`](file:///F:/FuseAIF2026/M1/WK4)
  - `misc/outputs/` — Exported HTML reports, learning curves, and ROC plots.
  - `.agents/rules/` — Agent execution constraints.
- **GitHub Remote Fallback**:
  - `https://github.com/AaradhyaDT/fuseAiF_wk4_linear_models`
  - Workspace: `https://github.com/AaradhyaDT/FUSE_AIF_2026_M1` (under `WK4/`)
  - Clone: `gh repo clone AaradhyaDT/fuseAiF_wk4_linear_models`

---

## 5. Key Implementation Snippets

### Threshold Tuning for Customer Churn
```python
import numpy as np
from sklearn.metrics import precision_recall_curve

def find_optimal_churn_threshold(y_true, y_prob, cost_fn: float = 5.0, cost_fp: float = 1.0) -> float:
    """Find decision threshold minimizing business loss."""
    precisions, recalls, thresholds = precision_recall_curve(y_true, y_prob)
    # Total cost = cost_fn * (1 - recall) * P + cost_fp * (1 - precision) * P_pred
    total_costs = []
    for th in thresholds:
        preds = (y_prob >= th).astype(int)
        fn = np.sum((y_true == 1) & (preds == 0))
        fp = np.sum((y_true == 0) & (preds == 1))
        total_costs.append(cost_fn * fn + cost_fp * fp)
    
    best_idx = np.argmin(total_costs)
    return float(thresholds[best_idx])
```

---

## 6. Classroom Quiz Analysis & Conceptual Traps
- **Quiz ID**: `864506361006` (23/25).
- **L1 vs L2 Sparsity**: L1 regularization (Lasso) drives non-informative feature coefficients strictly to zero due to the sharp diamond geometry of the $L_1$ ball intersecting the loss contours on the coordinate axes. L2 regularization (Ridge) shrinks coefficients smoothly toward zero but never forces exact zeros.
