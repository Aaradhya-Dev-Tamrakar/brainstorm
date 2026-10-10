# Calm Authority Academic Writing Guide

This reference adapts the **Anthropic Calm Authority Standard** (`writing-like-claude`) specifically for academic engineering thesis reports, fellowship capstones, and formal technical monographs.

---

## 1. Core Philosophy: The Whiteboard Test & Empirical Proof

In high-stakes academic and regulatory engineering, credibility is never asserted; it is mathematically and empirically demonstrated:

$$\text{Trust} = \text{Precision} + \text{Scope Boundaries} + \text{Empirical Proof}$$

> **The Whiteboard Test**: Write as if you are explaining the mechanics of your system to a senior engineering faculty member or an external regulatory auditor at a whiteboard. You are not marketing a product; you are communicating an engineered reality.

---

## 2. The 10 Invariants of Academic Calm Authority

### 1. Factual Declarative Section Openings
Begin sections and chapters with a factual declarative statement of what exists, what was measured, or what was established.
- *Avoid*: "In recent years, artificial intelligence has witnessed explosive growth and revolutionized facial analysis."
- *Prefer*: "Automated facial analysis systems are now embedded across commercial and public-sector classification tasks, with empirical audits documenting statistically significant error disparities across demographic cohorts."

### 2. The 1-Sentence Empirical Thesis
Every major chapter, section, and abstract must contain a single declarative thesis sentence summarizing the factual finding or architectural mechanism.

### 3. Strict Hype Blacklist & Active Verb Replacement
Marketing superlatives and empty intensifiers are strictly prohibited:

| Prohibited Term | Calm Authority Replacement |
| :--- | :--- |
| *Revolutionary / Game-changing* | *Demonstrated, empirically verified, foundational* |
| *Groundbreaking* | *Methodological, foundational, rigorous* |
| *Supercharge / Unleash* | *Accelerate, scale, optimize, compute* |
| *Seamless / Seamlessly* | *Directly integrated, unified, continuous* |
| *Cutting-edge / Next-gen* | *Current state-of-the-art, contemporary* |
| *Magic / Effortlessly* | *Deterministically, automatically, via [algorithm]* |
| *Phenomenal / Miracle* | *Statistically significant, $p < 0.01$* |
| *Incomparable / Flawless* | *Within standard deviation $\sigma = 0.02$* |

### 4. Explicit Scope Boundaries & Descoping Cut-Lists
True academic rigor is demonstrated by declaring what the system **cannot** do. Stating non-goals, failure modes, and out-of-scope boundaries builds epistemic trust:
- Dedicate an explicit `\subsection{Scope}` and `\subsection{Limitations}` in Chapter 1.
- Document an explicit **Cut-List** in Chapter 4 defining exactly which secondary features were descoped when engineering trade-offs arose (e.g., *"UTKFace was profiled during exploratory analysis and cut due to DEX age estimation noise; FairFace was retained as the sole audited benchmark"*).

### 5. Statistical Rigor & The $n \ge 30$ Guardrail
Never report bare point estimates for demographic cohorts or benchmark evaluations:
- **Sample Size Guard**: Any cohort with $n < 30$ observations must be suppressed or flagged as statistically insufficient (`insufficient_sample = True`), never scored.
- **Uncertainty Quantification**: Pair all point estimates with 95% bootstrap confidence intervals (e.g., $B \ge 1{,}000$ Bias-Corrected and Accelerated [BCa] resamples).
- **Hypothesis Testing**: Accompany disparity claims with exact $p$-values from Pearson's $\chi^2$ test of independence or Fisher's exact test for sparse tables.

### 6. Functional Precision in Architecture & SOLID Principles
Avoid reciting textbook definitions of Object-Oriented principles. Map every principle directly to an engineered module:
- *Single Responsibility*: Five distinct pipeline modules where no module accesses another's internal memory state.
- *Open-Closed / Strategy*: Interchangeable computation strategies (`FairnessBackend` $\to$ `AIF360Backend` / `FairlearnBackend`) so adding a new metric requires zero modification to core engine loops.
- *Liskov Substitution*: Narrow interfaces (`ModelInterface`) ensuring in-process inference and batch predictions file ingestion are interchangeable drop-in implementations.

### 7. Sentence & Paragraph Geometry
- **Paragraphs**: 1 idea per paragraph, 2 to 5 sentences maximum.
- **Sentences**: 1 action or relationship per sentence.
- Prefer active voice with concrete subjects (*"The metrics engine computes demographic parity"* rather than *"Demographic parity is computed by the engine"*).

### 8. Pinned Benchmark Tables & Pareto Transparency
When comparing models, algorithms, or pipelines:
- Use standardized LaTeX `booktabs` tables with explicit row and column headers.
- Document compute environments (CPU vs. GPU, memory ceilings, execution latency).
- Report multi-objective trade-offs (e.g. accuracy vs. disparate impact ratio).

### 9. Regulatory & Standards Alignment
Trace engineered features to external institutional benchmarks:
- EU AI Act (Regulation 2024/1689), specifically Article 10 (Data Governance) and Annex IV (Technical Documentation).
- NIST AI Risk Management Framework (AI RMF 1.0) core functions: Govern, Map, Measure, Manage.
- IEEE 830 Software Requirements Specifications standard for Functional Requirements.

### 10. Actionable Conclusion Over Redundant Recapitulation
The concluding chapter must not merely repeat the introduction. Instead:
- Summarize concrete verified empirical findings.
- Re-examine initial limitations with engineering honesty.
- Define actionable future research directions and open scientific questions.
