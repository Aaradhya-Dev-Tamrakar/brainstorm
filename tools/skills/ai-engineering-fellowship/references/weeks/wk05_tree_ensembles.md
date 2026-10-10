# Week 5: Tree-Based Ensembles, SMOTE & SHAP Explainability

---
relevancy_tier: GOLDEN_REFERENCE
mentor_score: 100/100
fellowship_rating: 9.0/10
classroom_id: 854602584131
quiz_id: 854598412704
local_path: F:\FuseAIF2026\M2\WK5
github_repo: https://github.com/AaradhyaDT/fuseAiF_wk5_telco_churn_ensembles
---

## 1. Overview & Golden Benchmark
- **Fellowship Rating**: **9.0 / 10** — *Highest individual assignment score achieved in the fellowship.*
- **Objective**: Develop a production-serialized customer churn prediction and tenure regression system with tree ensembles, leakage-free resampling, and local/global explainability.
- **Models**: Random Forest vs. XGBoost Classifier, DecisionTree vs XGBoost Regressor for tenure.
- **Explainability**: SHAP global feature impact and local waterfall decomposition.

---

## 2. SOTA Industry Best Practices & Production Standards
- **Zero-Leakage Resampling (`INV-SMOTE-GUARD`)**: Never apply SMOTE or random undersampling on the raw dataset. Always use `imblearn.pipeline.Pipeline`, which restricts synthetic oversampling strictly to training folds and leaves validation/test folds untouched.
- **TreeSHAP Exact Feature Attribution**: Compute exact Shapley values in polynomial time ($O(TLD^2)$) using `shap.TreeExplainer`.
- **Model Card Formalization**: Provide complete operational metadata (target distribution, fairness evaluations, out-of-distribution limitations, and inference latency).
- **Production Serialization**: Serialize the end-to-end pipeline (ColumnTransformer preprocessor + calibrated estimator) via `joblib.dump(pipeline, "telco_churn_pipeline_v1.joblib")`.

---

## 3. Mentor Evaluation & Quality Rating
- **Assignment Grade**: **100 / 100** ("Trees and Ensembles Assignment").
- **Quiz Score**: **19 / 20** ("Trees and Ensembles Quiz").
- **Evaluation Commentary**: Flawless leakage isolation; excellent model card; clear distinction between global feature importance and directional local waterfall forces.

---

## 4. Local-First & GitHub Fallback Resolution (`INV-RESOLVE-FUSE`)
- **Local Directory**: [`F:\FuseAIF2026\M2\WK5`](file:///F:/FuseAIF2026/M2/WK5)
  - `telco_churn_pipeline_v1.joblib` — Serialized production model artifact.
  - `misc/` — SHAP force plots, learning curves, and model card markdown.
- **GitHub Remote Fallback**:
  - `https://github.com/AaradhyaDT/fuseAiF_wk5_telco_churn_ensembles`
  - Clone: `gh repo clone AaradhyaDT/fuseAiF_wk5_telco_churn_ensembles`

---

## 5. Golden Implementation Snippets

### Zero-Leakage ImbPipeline with XGBoost
```python
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBClassifier

def build_leakage_free_churn_pipeline(num_cols, cat_cols):
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_cols),
            ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), cat_cols),
        ]
    )
    # SMOTE is executed strictly inside cv train folds during fit()
    return ImbPipeline([
        ("preprocessor", preprocessor),
        ("smote", SMOTE(random_state=42)),
        ("classifier", XGBClassifier(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=4,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            eval_metric="auc"
        ))
    ])
```

---

## 6. Classroom Quiz Analysis & Conceptual Traps
- **Quiz ID**: `854598412704` (19/20).
- **Bagging vs Boosting Gradient**: Bagging (Random Forest) trains independent trees on bootstrap samples to reduce variance. Boosting (XGBoost) fits trees sequentially on the negative gradients (pseudo-residuals) of the loss function, primarily reducing bias.
