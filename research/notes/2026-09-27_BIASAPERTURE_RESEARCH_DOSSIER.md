# Research Note: BiasAperture (Diagnostic Fairness & Bias Audit Platform)

- **Date & Time**: 2026-09-27 (Updated 2026-10-01)
- **Target Repository**: [[BiasAperture]] (`F:\Aaradhya-Dev-Tamrakar\BiasAperture` / https://github.com/fuseai-fellowship/BiasAperture-A-Diagnostic-Framework-for-Demographic-Bias-Auditing-in-Facial-Analysis-Models)
- **NotebookLM Grounding IDs**:
  - Strategy & Foundations: `99bee3c6-07ed-4ff0-8ac8-0027b18ad06a`
  - References & Literature: `bbac9235-404b-4c39-a2a4-1f30069af30b`
  - Source & Technical Specs: `928b5ed7-1353-4cb3-a1ce-b215e80b7db4`
  - Repo State & Synthesis: `6e9505f0-2d5c-4655-8bc7-9f97cf9620b9`
- **Orchestration**: Multi-profile fleet delegation: User 2 (`dev83` - Lead Orchestrator) -> User 3 (`xavier` - Scout) -> User 4 (`adtbei79001` - Reviewer)
- **Epistemic Classification**: `EMPIRICALLY_VERIFIED`
- **Related Documents**: `[[2026-10-01_GEMINI_NOTEBOOKLM_WORKSPACE_REGISTRY]]`, `[[AARADHYA_MASTER_v165]]`

---

## 1. Executive Summary & Authorship
**BiasAperture** is an offline, diagnostic and evaluative software framework for auditing demographic bias in facial analysis computer vision models.
- **Authors**: Aaradhya Dev Tamrakar, Tisha Manandhar
- **Supervisor**: Shreejan Kisee, Teaching Assistant, Fusemachines AI Fellowship Program, Kathmandu, Nepal.
- **Status**: Milestones M1–M4 Completed (100%), M5 System Orchestration & Case Studies Active, Proposal Defense Completed, 85/85 Tests Passing, Clean Ruff Linting.
- **Recent Milestone**: 12-Item Modularity & SRP Architecture Refactor Completed (Issue #32, PR #33).

---

## 2. Milestone Architecture & GitHub Project Anchoring (2026-10-01)

| Milestone | Title | Scope & Status |
|:---|:---|:---|
| **M1** | **`M1: Schema Lock & Literature Matrix`** | Locked demographic taxonomy (7 race $\times$ 9 age $\times$ 2 gender), $n \ge 30$ CLT sample guard, canonical `SubjectRecord` & `MetricResult` schemas, 20-paper literature review matrix. *(Closed / Verified)* |
| **M2** | **`M2: Dual Data & Reporting Foundations`** | Data Ingestion pipeline (`data_ingestion.py`, strict/permissive validation modes, cohort profiling) and Jinja2 offline HTML compliance report generator (`report/generator.py`). *(Closed / Verified)* |
| **M3** | **`M3: Core Fairness & Statistical Rigor Engines`** | Pure-math metrics (`metrics.py`), dual-backend (`FairlearnBackend` + `AIF360Backend`), hypothesis testing ($\chi^2$, Fisher exact), Holm-Bonferroni FWER correction, and Stratified BCa Bootstrap CI ($B \ge 1,000$). *(Closed / Verified)* |
| **M4** | **`M4: End-to-End Orchestration & Surrogate Explainability`** | `CrossValidationOrchestrator` (backend consensus & divergence alerts), `ShapExplainerEngine` (surrogate proxy attribution on flagged disparities), and unified CLI (`bias-aperture audit`). *(Closed / Verified)* |
| **M5** | **`M5: Benchmark Validation, Final Thesis & Capstone Defense`** | Empirical validation on full FairFace dataset (97,698 released benchmark images), 50-page formal LaTeX thesis (`report/main.pdf`), 18-slide Beamer defense presentation deck, and final Viva defense. *(Active / In Progress ~95%)* |
| **Phase 2** | **`Phase 2: Post-Capstone Product Upgrade Sprint`** | Research & product upgrades: Spatial SHAP pixel attribution, multi-dataset ingestion, PDF export, and EU AI Act timeline alignment. *(Open / Backlog)* |

---

## 3. Modularity & Single Responsibility Architecture Refactor (Issue #32, PR #33)

Following technical advisor feedback on debuggability and code modularity, 12 systemic refactorings were executed and verified against all 85 pytest suites:

1. **God-Function Decompositions**:
   - `_build_core_metric_results` (452 lines in `fairness/backends.py`) decomposed into 5 single-responsibility helpers:
     - `_make_insufficient_result`: Unified factory for NFR-003 sample-suppressed rows.
     - `_make_*_fn`: Closure factories for metric evaluation during bootstrap sampling.
     - `_build_summary_row`: Global cross-group summary metric row builder.
     - `_build_subgroup_rows`: Per-demographic-group disparity row builder.
     - `_detect_divergences`: Extracted divergence detection from `CrossValidationOrchestrator.run()`.
   - `DataIngestionPipeline.ingest_records` (258 lines in `data_ingestion.py`) decomposed into distinct processing stages: `_validate_columns()`, `_validate_and_convert_row()`, and `_check_duplicate()`.
   - `HTMLReportGenerator._prepare_template_context` (121 lines in `report/generator.py`) analytical logic decoupled into `_build_subgroup_matrix()` and `_build_executive_summary()`.
   - `cli.py:main()` orchestration logic extracted into a reusable `AuditPipeline` application service runner class, allowing programmatic invocation without CLI argv.

2. **Structured Logging & Error Observability**:
   - Replaced raw console `print()` and `sys.stderr` in `cli.py` with standard library `logging.getLogger` and a configured `StreamHandler`.
   - Added structured module-level loggers to `data_ingestion.py` and `fairness/statistics.py`.
   - Replaced silent `except Exception: continue` and silent fallbacks in `fairness/statistics.py` with `logger.warning` / `logger.debug` diagnostic messages.

3. **Single-Source-of-Truth Constants**:
   - Replaced hardcoded `0.05` in `report/generator.py` with `schema.ALPHA`.
   - Replaced hardcoded `30` in `fairness/statistics.py` with `schema.MIN_SUBGROUP_SAMPLE_SIZE`.
   - Centralized `MIN_POSITIVE_SUPPORT = 5` in `schema.py` and wired into `base.py` and `data_ingestion.py`.
   - Created canonical `format_intersectional_key()` in `schema.py` ensuring consistent key ordering across modules.

4. **Duplicate I/O Deprecation**:
   - Marked `PredictionsFileInterface` in `model_interface.py` as deprecated, establishing `DataIngestionPipeline.ingest_file()` as the canonical ingestion path.

---

## 4. Collaborative Peer Review & Git Governance Protocol

Codified in `AGENTS.md` and global workflow skills:
- **Explicit Handles Invariant**: Never use ambiguous `@me` in multi-developer repositories to prevent identity collisions across team members or agent runs.
- **Reciprocal Peer Review**:
  - When Aaradhya opens a PR: assign `AaradhyaDT` and request review from `tiixsha` (`gh pr create --assignee AaradhyaDT --reviewer tiixsha`).
  - When Tisha opens a PR: assign `tiixsha` and request review from `AaradhyaDT` (`gh pr create --assignee tiixsha --reviewer AaradhyaDT`).
- **No Organization Review Handles**: Strictly use personal handles (`AaradhyaDT`, `tiixsha`) for reviews and assignments.
- **Issue-PR Linking**: All PRs must embed resolution keywords (`Closes #<ID>`) and post immediate cross-referencing comments on issue threads.

---

## 5. Core Architectural & Methodological Pillars

### I. The Core Four Disparity Metrics
1. **Demographic Parity Difference (DPD)**: $P(\hat{Y}=1 | A=A_{priv}) - P(\hat{Y}=1 | A=A_{unpriv})$
2. **Disparate Impact Ratio (DIR)**: $\frac{P(\hat{Y}=1 | A=A_{unpriv})}{P(\hat{Y}=1 | A=A_{priv})}$
3. **Equal Opportunity Difference (EOP)**: $P(\hat{Y}=1 | A=A_{priv}, Y=1) - P(\hat{Y}=1 | A=A_{unpriv}, Y=1)$ (True Positive Rate parity)
4. **Equalized Odds Difference (EOD)**: $\max(|FPR_{priv} - FPR_{unpriv}|, |TPR_{priv} - TPR_{unpriv}|)$

### II. Dual Harmonization Engine (Fairlearn + AIF360)
To eliminate single-library mathematical bias, BiasAperture runs **Fairlearn** and **AIF360** in parallel with mathematical harmonization (reconciling sign conventions, zero-denominator contracts, and max-of-gaps formulations).

### III. Statistical Rigour & Guardrails
- **BCa Bootstrap Confidence Intervals**: 95% confidence intervals with $B \ge 1,000$ resamples.
- **Hypothesis Testing**: Pearson's $\chi^2$ independence test with Fisher's exact test fallback for sparse $2\times2$ tables (any expected cell count $< 5$).
- **$n < 30$ Sample Size Guard**: Demographic subgroups with fewer than 30 samples are strictly suppressed from metric calculation (`insufficient_sample=True`, `metric_value=None`).

### IV. Non-Negotiable Diagnostic Scope Invariants
- **Diagnostic-Only**: BiasAperture measures and reports disparities; it **never** performs model retraining, in-processing weight alterations, or synthetic image generation.
- **Zero-Network Air-Gapped**: Runs entirely offline with zero external CDN dependencies, embedding Jinja2 standalone templates and base64 visuals.

### V. Regulatory Compliance Mapping
Mapped to **Article 10 & 13 of the EU AI Act** (High-Risk AI Data Governance & Transparency) and **NIST AI RMF 1.0 (Measure 2.11)**.
