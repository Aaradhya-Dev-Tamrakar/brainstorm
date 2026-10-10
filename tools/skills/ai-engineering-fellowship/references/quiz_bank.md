# Google Classroom Master Quiz Bank & Conceptual Traps

Consolidated question bank, trick concepts, mathematical equations, and verified answers extracted from Aaradhya's 17 weekly Google Classroom quizzes in the Fusemachines AI Fellowship 2026 (`849624491859`).

---

## Week 1: Data Wrangling & SQL Fundamentals
- **Core Focus**: Data cleansing, anomaly detection, SQL joins and aggregations.
- **Conceptual Trap**: Treating `NULL` as equivalent to `0` or empty string in SQL queries. In SQL, `NULL = NULL` evaluates to `UNKNOWN`, not `TRUE`. Any arithmetic with `NULL` produces `NULL`.
- **Key Formula**: Standardized Z-Score:
  $$Z = \frac{x - \mu}{\sigma}, \quad \text{IQR Outlier Bound: } [Q_1 - 1.5 \cdot \text{IQR}, \; Q_3 + 1.5 \cdot \text{IQR}]$$
- **High-Yield Question**: When joining large transaction tables with customer profiles, why use `LEFT JOIN` over `INNER JOIN`?
  - *Answer*: `INNER JOIN` silently drops customers who have zero transactions, leading to selection bias when analyzing churn or customer inactivity.

---

## Week 2: Software Development Concepts & FastAPI
- **Core Focus**: Concurrency, containerization, async I/O, REST conventions.
- **Conceptual Trap**: Running CPU-bound blocking code inside an `async def` FastAPI route. This blocks the main asyncio event loop thread and serializes all concurrent incoming requests.
- **High-Yield Question**: What is the difference between Docker Compose `ports` vs `expose`?
  - *Answer*: `ports` binds container ports to the host machine's physical network interface. `expose` makes ports accessible *only* to other containers linked on the same internal Docker bridge network without exposing them to the external host.

---

## Week 3: GenAI, Text-to-SQL & Agentic Query Execution (Score: 31/34)
- **Core Focus**: Prompt chaining, SQL injection prevention, AST validation, structured JSON outputs.
- **Conceptual Trap**: Relying only on regex string matching to block SQL injection. Attackers bypass regex using whitespace obfuscation, multi-line comments (`/* ... */`), or hex encodings.
- **SOTA Defense**: Parse the candidate query with an SQL Abstract Syntax Tree (AST) engine (`sqlglot`). Assert that the AST root is strictly a `Select` node and contains zero DDL/DML statements.

---

## Week 4: Statistical ML: Linear Models (Score: 23/25)
- **Core Focus**: Logistic regression, regularization (L1/L2), threshold optimization, ROC-AUC.
- **Conceptual Trap**: Misinterpreting Logistic Regression coefficients when features are not standardized. A larger coefficient on an unscaled feature does not imply greater feature importance.
- **Key Formula**: Log-Odds (Logit):
  $$\ln\left(\frac{p}{1 - p}\right) = \beta_0 + \sum_{i=1}^n \beta_i x_i \implies p = \frac{1}{1 + e^{-(\beta_0 + \mathbf{\beta}^T \mathbf{x})}}$$
- **High-Yield Question**: In severe class imbalance (e.g. 5% churn), why is Accuracy a dangerous metric?
  - *Answer*: The "Accuracy Trap" — a naïve model predicting constant negative achieves 95% accuracy while identifying zero actual churning customers. Evaluate using ROC-AUC, PR-AUC, and F1-score instead.

---

## Week 5: Tree-Based Ensembles & SHAP (Score: 19/20)
- **Core Focus**: Random Forest, XGBoost, Gini impurity, SMOTE in-fold pipeline, TreeSHAP.
- **Conceptual Trap**: Fitting SMOTE before cross-validation. This synthesizes minority points across the entire dataset, leaking test distributions into the training partition and yielding unrealistically optimistic scores.
- **Key Formula**: Tree-based Gini Impurity:
  $$I_G(t) = 1 - \sum_{i=1}^C p_i^2$$
- **High-Yield Question**: How does Random Forest achieve lower variance than a single decision tree?
  - *Answer*: Random Forest trains $B$ decorrelated trees using bootstrap aggregation (bagging) and random feature subspace sampling ($m = \sqrt{p}$). The variance of the average of $B$ independent trees decreases as $\frac{1}{B} \sigma^2 + \frac{B-1}{B} \rho \sigma^2$.

---

## Week 6: Probabilistic Models & Bayesian Inference (Score: 20/20)
- **Core Focus**: Bayes' theorem, conjugate priors (Beta-Binomial, Dirichlet-Multinomial), MAP vs MLE, MCMC convergence.
- **Conceptual Trap**: Using point estimates (MAP) and assuming it represents full Bayesian inference. MAP ignores the volume and spread of posterior parameter uncertainty.
- **Key Formula**: Bayes' Theorem:
  $$P(\theta \mid D) = \frac{P(D \mid \theta) P(\theta)}{P(D)} = \frac{P(D \mid \theta) P(\theta)}{\int P(D \mid \theta') P(\theta') d\theta'}$$
- **High-Yield Question**: What does a Gelman-Rubin $\hat{R} > 1.05$ indicate in PyMC?
  - *Answer*: Chains have not mixed or converged to the same stationary target distribution; sampling must be run longer or parameterized differently.

---

## Week 7: Customer Segmentation & Unsupervised Clustering
- **Core Focus**: K-Means, Hierarchical Clustering, DBSCAN, Silhouette Analysis.
- **Conceptual Trap**: Choosing $k$ in K-Means using only the Elbow heuristic on Inertia. Inertia decreases monotonically as $k$ increases; verify optimal $k$ using Silhouette Scores ($\ge 0.5$) and Davies-Bouldin Index.
- **High-Yield Question**: Why does DBSCAN outperform K-Means on retail transaction datasets?
  - *Answer*: DBSCAN does not assume spherical clusters or equal cluster sizes, and natively identifies arbitrary density shapes while isolating transaction noise/outliers into a distinct $-1$ label.

---

## Week 8: Time Series Analysis & Forecasting (Score: 15/15)
- **Core Focus**: Stationarity, ARIMA/SARIMAX orders, ACF/PACF, Ljung-Box test, Diebold-Mariano test.
- **Conceptual Trap**: Applying standard K-Fold shuffle cross-validation to time series data. This leaks future temporal dependencies into past training instances.
- **Key Formula**: SARIMA Model Specification:
  $$\Phi_P(B^s) \phi_p(B) (1 - B)^d (1 - B^s)^D X_t = \Theta_Q(B^s) \theta_q(B) \epsilon_t$$
- **High-Yield Question**: How do you confirm whether an ARIMA model's residuals represent pure white noise?
  - *Answer*: Perform the **Ljung-Box Q-test** at multiple lags (including seasonal lags 12, 24). If $p > 0.05$, reject autocorrelation; the residuals are uncorrelated white noise.

---

## Week 9: Neural Network Foundations & Defect CNNs
- **Core Focus**: Activation functions, backpropagation, CNN layers, BatchNorm, Dropout, Optuna.
- **Conceptual Trap**: Placing `BatchNorm2d` after the non-linear activation (ReLU) or forgetting to call `model.eval()` before test inference. In `model.train()`, BatchNorm updates running mean/variance; in `model.eval()`, it freezes them.
- **Key Formula**: Convolution Output Spatial Dimension:
  $$W_{\text{out}} = \left\lfloor \frac{W_{\text{in}} - K + 2P}{S} \right\rfloor + 1$$

---

## Week 10: Classical Image Processing (OpenCV)
- **Core Focus**: Color spaces (HSV), morphology, Canny edge detection, Hough Circle transform.
- **Conceptual Trap**: Segmenting objects by color in BGR/RGB space. RGB channels are highly coupled with illumination intensity. In HSV, chromatic information is isolated in Hue ($H$), making it invariant to shadows.
- **High-Yield Question**: What are the 5 sequential stages of the Canny edge detector?
  - *Answer*: (1) Gaussian smoothing, (2) Sobel gradient magnitude & direction, (3) Non-Maximum Suppression (NMS), (4) Double thresholding (high & low thresholds), (5) Edge tracking by hysteresis.

---

## Week 11: Computer Vision & Vision Transformers (Score: 20/20)
- **Core Focus**: ResNet transfer learning, GradCAM, IoU, Faster R-CNN, Vision Transformers (ViT), CLIP zero-shot.
- **Conceptual Trap**: Fine-tuning an entire Vision Transformer on a small dataset without warm-up. ViTs lack the translation equivariance and locality inductive biases of CNNs, causing severe overfitting if trained from scratch without large data.
- **Key Formula**: Intersection over Union (IoU):
  $$\text{IoU} = \frac{\text{Area}(B_{\text{pred}} \cap B_{\text{true}})}{\text{Area}(B_{\text{pred}} \cup B_{\text{true}})}$$

---

## Week 12: NLP & Sequence Labeling / NER (Score: 20/20)
- **Core Focus**: Named Entity Recognition, CoNLL-2003, WNUT-17, Conditional Random Fields (CRF), BIO tagging.
- **Conceptual Trap**: Evaluating sequence labeling models using token-level accuracy. Since most tokens are `O` (Outside), token accuracy will be >95% even if the model identifies zero entities. Use span-level micro/macro F1 score via `seqeval`.
- **High-Yield Question**: Why does a Linear-Chain CRF outperform independent Softmax classification for NER?
  - *Answer*: CRF models the transition probability between adjacent entity tags (e.g. learning that `I-PER` can never follow `O` directly without a preceding `B-PER`), enforcing global label consistency.

---

## Week 13: Sequence Learning & LSTMs (Score: 19/20)
- **Core Focus**: Recurrent Neural Networks (RNNs), LSTM cell architecture, gating mechanisms.
- **Key Formula**: LSTM Cell Gates:
  $$f_t = \sigma(W_f x_t + U_f h_{t-1} + b_f) \quad \text{(Forget Gate)}$$
  $$i_t = \sigma(W_i x_t + U_i h_{t-1} + b_i) \quad \text{(Input Gate)}$$
  $$C_t = f_t \odot C_{t-1} + i_t \odot \tanh(W_c x_t + U_c h_{t-1} + b_c) \quad \text{(Cell State)}$$
  $$o_t = \sigma(W_o x_t + U_o h_{t-1} + b_o), \quad h_t = o_t \odot \tanh(C_t) \quad \text{(Hidden State)}$$

---

## Week 14: Transformers & Foundational Models (Score: 20/20)
- **Core Focus**: Scaled Dot-Product Attention, Multi-Head Attention, BERT vs Decoder-Only, LoRA fine-tuning.
- **Key Formula**: Scaled Dot-Product Attention:
  $$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$
- **High-Yield Question**: Why is the dot product scaled by $\frac{1}{\sqrt{d_k}}$?
  - *Answer*: For large $d_k$, the dot product grows large in magnitude, pushing the softmax function into regions with extremely small gradients (vanishing gradient problem). The $\frac{1}{\sqrt{d_k}}$ scaling preserves unit variance.

---

## Week 15: Engineering AI Systems & Production RAG
- **Core Focus**: Vector embeddings, semantic chunking, vLLM local serving, Docker containerization.
- **Conceptual Trap**: Chunking strictly by character count without overlap or boundary awareness. Splitting sentences across chunks destroys semantic retrieval context. Use recursive character chunking with 15–20% token overlap.

---

## Week 16: Agentic AI Systems & Evaluation Harness
- **Core Focus**: ReAct decision loops, tool invocation, context memory budgeting, LLM-as-a-judge.
- **Conceptual Trap**: Unbounded agentic retry loops. Without a deterministic circuit breaker or step count threshold, an agent can get stuck in an infinite tool-calling loop, burning API quotas.

---

## Week 17: Production MLOps (Dual Track)
- **Core Focus**: MLflow experiment & trace tracking, Evidently AI data drift, Apache Airflow DAGs.
- **High-Yield Question**: How does Evidently AI detect numerical feature drift?
  - *Answer*: Uses the two-sample **Kolmogorov-Smirnov (K-S) test** (for continuous variables) or **Wasserstein Distance** comparing the reference baseline distribution against current production batches. If $p < 0.05$, a drift alert is emitted.
