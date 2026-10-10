# SOTA Industry Best Practices & Production Standards Matrix

Curated production standards, design patterns, and anti-patterns across the 5 core AI/ML engineering domains taught in the Fusemachines AI Fellowship 2026.

---

## 1. Data Engineering, SQL & Backend APIs (Weeks 1–3)

### Relational SQL & Preprocessing (Week 1)
- **Window Functions Over Nested Subqueries**: Prefer `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC)` for event-recency deduplication over costly correlated subqueries.
- **Explicit NULL Semantics**: In numerical aggregations, use `COALESCE(val, 0)` and guard division via `NULLIF(denominator, 0)` to prevent runtime divide-by-zero crashes.
- **Contract & Schema Validation**: Use **Pandera** or **Pydantic** to assert strict data types, non-nullability, and value bounds on incoming CSVs before data reaches pipeline logic.
- **Vectorized Operations**: Reject Python `for` loops or `.apply()` on DataFrames; enforce native vectorized NumPy/Pandas operations or DuckDB for analytical queries.

### Production FastAPI Architecture (Week 2 — The Mentor Invariant)
- **The APIRouter Mandate (`INV-FUSE-ROUTER`)**: Never write monolithic single-file APIs (the exact anti-pattern penalized in Week 2, 75/100).
- **Standard Layout**:
  ```
  app/
  ├── core/            # Config, security, database session factory
  ├── db/              # Base model, migrations (Alembic)
  ├── models/          # SQLAlchemy ORM entity tables
  ├── schemas/         # Pydantic v2 request & response schemas
  ├── routers/         # Domain endpoints (routers/customers.py, routers/health.py)
  └── services/        # Business logic & repository queries
  ```
- **Async DB Sessions**: Use `AsyncSession` with SQLAlchemy 2.0 and `asyncpg` for non-blocking I/O.
- **Connection Health**: Enforce connection pool recycling (`pool_recycle=1800`, `pool_pre_ping=True`) to handle dropped PostgreSQL TCP sockets.

### Agentic Text-to-SQL (Week 3)
- **Zero Raw DDL/DML**: Enforce AST-level SQL validation (using `sqlglot` or `sqlparse`) ensuring the query AST only contains `Select` statements. Block `DROP`, `DELETE`, `UPDATE`, `ALTER`, `INSERT`.
- **Context-Window Schema Pruning**: Do not inject entire multi-table schemas into the LLM prompt. First run table retrieval/pruning to only include columns relevant to the user query.
- **Self-Correction & Reflection Loop**: Structure the agentic loop as `Planner -> Generator -> AST Validator -> Dry-Run Executor -> Explainer`. If the database engine returns a syntax/column error, feed the error back into the generator with a max retry limit of 3.

---

## 2. Statistical Machine Learning & Ensembles (Weeks 4–7)

### Leakage-Free Preprocessing (Week 4)
- **Fit on Train Only**: Any scaling (`StandardScaler`, `RobustScaler`), imputation, or target encoding must be fitted strictly on training folds inside a `Pipeline`.
- **Multicollinearity Checks**: Compute Variance Inflation Factors (VIF > 5 indicates severe collinearity) before interpreting linear regression coefficients.
- **Cost-Utility Threshold Tuning**: The default 0.5 decision threshold is almost always wrong for imbalanced data. Compute ROC curves and Precision-Recall curves to tune the threshold specifically to business cost:
  $$\text{Expected Cost} = C_{\text{FP}} \cdot P(\text{FP}) + C_{\text{FN}} \cdot P(\text{FN})$$

### Tree Ensembles & Imbalanced Classes (Week 5 — Fellowship 9.0 Benchmark)
- **The ImbPipeline Rule**: When applying SMOTE or ADASYN, you **MUST** use `imblearn.pipeline.Pipeline`, not standard scikit-learn pipeline, to ensure synthetic oversampling is restricted strictly to training folds and never leaks into test folds.
- **SHAP Explainability**: Use `shap.TreeExplainer` for exact, polynomial-time feature attribution. Export both Global Summary plots (feature importance) and Local Waterfall plots (individual prediction audit).
- **Production Serialization**: Serialize full preprocessor + estimator pipelines with `joblib.dump(..., compress=3)` along with a machine-readable JSON Model Card containing train date, commit SHA, and metric thresholds.

### Probabilistic Inference & Bayesian Modeling (Week 6)
- **MCMC Diagnostics**: Always verify Markov Chain Monte Carlo convergence using Gelman-Rubin statistic $\hat{R} < 1.01$ and Effective Sample Size (ESS > 400 per chain).
- **Predictive Checks**: Perform Prior Predictive Checks to verify prior distributions are weakly informative, and Posterior Predictive Checks (PPC) to ensure observed data falls within the 94% highest density interval (HDI).

### Customer Segmentation & Unsupervised Clustering (Week 7)
- **Robust Feature Engineering**: For skewed retail transaction data, compute RFM (Recency, Frequency, Monetary) metrics and apply `RobustScaler` (median & IQR) rather than `StandardScaler` to prevent outliers from distorting cluster centroids.
- **Tendency Before Clustering**: Compute the **Hopkins Statistic** ($H > 0.75$) to statistically prove data contains clusters before running K-Means.
- **Multi-Metric Validation**: Validate cluster count $k$ across Silhouette Score ($\ge 0.50$), Davies-Bouldin Index (lower is better), and Calinski-Harabasz Index.

---

## 3. Time Series Forecasting (Week 8)

### Time Series Invariants
- **Temporal Split Only**: Never use standard shuffle cross-validation on time series. Always use expanding-window `TimeSeriesSplit` to prevent future data leakage.
- **Stationarity Verification**: Run both **Augmented Dickey-Fuller (ADF)** (tests unit root) and **KPSS** (tests trend stationarity) before fitting ARIMA models.
- **Residual Autocorrelation**: Ensure model residuals pass the **Ljung-Box test** ($p > 0.05$) across seasonal lags (lags 12, 24).
- **Ensemble Dominance**: Combine diverse model families (e.g., Holt-Winters for seasonality + SARIMA for linear autocorrelation + LSTM/XGBoost for non-linear residuals). Verify statistical superiority using the **Diebold-Mariano test** ($p < 0.05$).

---

## 4. Deep Learning & Computer Vision (Weeks 9–11)

### PyTorch Architecture & Hardening (Week 9)
- **Explicit `nn.Module`**: Subclass `torch.nn.Module` and define `__init__` and `forward` explicitly; avoid unstructured sequential hacks for branching models.
- **Batch Normalization & Dropout Pairing**: Place `BatchNorm2d` immediately after `Conv2d` (and before ReLU), and place `Dropout(p)` before the final classification `Linear` layer.
- **Mixed Precision (`torch.amp`)**: Use `torch.autocast('cuda')` and `GradScaler` for 2–3x faster training and 50% VRAM reduction on modern GPUs.
- **Automated Hyperparameter Optimization**: Use **Optuna** with `MedianPruner` or `Hyperband` to terminate underperforming learning rates and batch sizes early.

### Classical Image Processing (Week 10)
- **Color-Space Robustness**: Use HSV or LAB color spaces for segmentation rather than RGB. RGB channels are heavily entangled with illumination/shadows, whereas HSV separates chromaticity (Hue) from lighting (Value).
- **Morphological Pipelines**: Clean color masks with morphological Opening (erosion then dilation to remove salt noise) followed by Closing (dilation then erosion to close interior holes).

### Vision Transformers & Zero-Shot Deployment (Week 11)
- **Zero-Shot CLIP as Strong Baseline**: In domains with limited annotated samples, evaluate zero-shot OpenAI CLIP (`openai/clip-vit-base-patch32`) before fine-tuning a heavy CNN. (Week 11 benchmark: CLIP achieved 92.0% zero-shot accuracy vs 74.1% for fine-tuned ResNet-50).
- **ONNX Export & Runtime Quantization**: Export trained PyTorch vision models to ONNX (`torch.onnx.export`) with dynamic batch axes, then apply INT8 quantization via `onnxruntime` for low-latency CPU/edge deployment.

---

## 5. Applied NLP, Agentic AI & Production MLOps (Weeks 12–17)

### Sequence Labeling & NER (Week 12)
- **BIOES Tagging**: Prefer BIOES (Begin, Inside, Outside, End, Single) over standard BIO. Explicitly marking single-token entities and segment boundaries improves CRF transition matrix resolution.
- **Out-of-Vocabulary (OOV) Stress Testing**: Always test NER models against emerging datasets like WNUT-17 to expose generalization drop on unseen entity surfaces.

### Agentic Routing & Small Language Models (Week 14)
- **Encoder Transformers vs. SLMs**:
  - For pure intent classification (<20 classes): Fine-tuned ModernBERT / DeBERTa-v3 delivers <10ms inference at >95% accuracy.
  - For open-ended routing with tool arguments: Quantized Small Language Models (Qwen 2.5 0.5B / SmolLM 1.7B) via LoRA deliver rich structured argument outputs under 50ms.

### Production RAG & AI Assistants (Week 15)
- **Hybrid Retrieval**: Combine dense semantic embeddings (`text-embedding-3-small` or BGE) with sparse BM25 keyword matching via Reciprocal Rank Fusion (RRF).
- **Re-ranking**: Pass top-25 hybrid results through a Cross-Encoder reranker (`bge-reranker-large`) to select top-5 high-precision context chunks.
- **Local Serving**: Serve open-weights LLMs (Llama 3, Mistral) via **vLLM** for continuous batching and PagedAttention speedups.

### Agentic Loop Governance & Eval Harness (Week 16)
- **Context Budgeting**: Enforce strict token firebreaks. Truncate historical scratchpad turns after execution checkpoints.
- **Deterministic Eval Harness**: Test agentic systems against a golden set of 50+ deterministic cases. Verify tool choice accuracy, parameter extraction, and step count efficiency before deploying.

### Production MLOps (Week 17)
- **Virtual Environment Determinism**: Use `uv` with pinned `pyproject.toml` and lockfiles for instantaneous, deterministic environments.
- **Dual Experiment & Trace Tracking**: Use MLflow for traditional metric logging (loss, accuracy, ROC) and MLflow Tracing / OpenTelemetry for agentic LLM call graphs and token costs.
- **Data & Model Drift Monitoring**: Deploy **Evidently AI** to compute Wasserstein distance / Kolmogorov-Smirnov tests on feature distributions between reference and production inferences.
- **Orchestration**: Schedule periodic batch retraining or drift evaluation pipelines using Apache Airflow DAGs with Docker operators.
