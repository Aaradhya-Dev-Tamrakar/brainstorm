# Verbatim Dialogue Transcript: BiasAperture Modularity Refactor & Milestone Governance Audit

- **Date & Time**: 2026-10-01T13:45:00+05:45
- **Epistemic Classification**: `EMPIRICALLY_VERIFIED`
- **Target Repositories**:
  - `BiasAperture`: `fuseai-fellowship/BiasAperture-A-Diagnostic-Framework-for-Demographic-Bias-Auditing-in-Facial-Analysis-Models`
  - `brainstorm`: `F:\Aaradhya-Dev-Tamrakar\brainstorm`
- **Related Issue**: [#32](https://github.com/fuseai-fellowship/BiasAperture-A-Diagnostic-Framework-for-Demographic-Bias-Auditing-in-Facial-Analysis-Models/issues/32)
- **Related PR**: [#33](https://github.com/fuseai-fellowship/BiasAperture-A-Diagnostic-Framework-for-Demographic-Bias-Auditing-in-Facial-Analysis-Models/pull/33)
- **Invariant References**: `INV-EPI-001`, `ARCH-RFC-001`

---

## 1. Context & Motivation
Technical Advisor feedback mandated refactoring the BiasAperture codebase for increased modularity, separation of concerns (Single Responsibility Principle), and ease of debugging without altering locked milestone M1 demographic schemas or statistical confidence guarantees.

Concurrently, repository governance was audited to introduce structured GitHub milestones ($M1 \to M5$ plus Phase 2), link all 33 issues and PRs across the project lifecycle, and codify a deterministic reciprocal peer review protocol between team members Aaradhya Dev Tamrakar (`AaradhyaDT`) and Tisha Manandhar (`tiixsha`).

---

## 2. Core Actions & Deliverables

### A. 12-Item Modularity & SRP Refactoring
1. **Decomposed Monoliths**:
   - `_build_core_metric_results` (452 lines) decomposed into:
     - `_make_insufficient_result`
     - `_make_*_fn` bootstrap metric closure factories
     - `_build_summary_row`
     - `_build_subgroup_rows`
     - `_detect_divergences` (extracted from `CrossValidationOrchestrator.run()`)
   - `DataIngestionPipeline.ingest_records` (258 lines) decomposed into `_validate_columns()`, `_validate_and_convert_row()`, and `_check_duplicate()`.
   - `HTMLReportGenerator._prepare_template_context` (121 lines) analytical logic decoupled into `_build_subgroup_matrix()` and `_build_executive_summary()`.
   - `cli.py:main()` logic decoupled into a standalone `AuditPipeline` runner class.

2. **Structured Logging**:
   - Replaced raw `print()` statements in `cli.py` with standard `logging.getLogger` and a configured `StreamHandler`.
   - Added module loggers to `data_ingestion.py` and `fairness/statistics.py`.
   - Replaced silent `except Exception` blocks with logged diagnostic warnings.

3. **Constant Centralization**:
   - Replaced hardcoded `0.05` in `report/generator.py` with `schema.ALPHA`.
   - Replaced hardcoded `30` in `fairness/statistics.py` with `schema.MIN_SUBGROUP_SAMPLE_SIZE`.
   - Centralized `MIN_POSITIVE_SUPPORT = 5` in `schema.py`.
   - Added canonical `format_intersectional_key()` helper function in `schema.py`.

4. **Deprecation**:
   - Marked `PredictionsFileInterface` in `model_interface.py` as deprecated in favor of `DataIngestionPipeline`.

### B. Milestone & Issue-PR Mapping
- **Milestone 1 (`M1: Schema Lock & Literature Matrix`)**: Linked issues #10, #11, #15.
- **Milestone 2 (`M2: Dual Data & Reporting Foundations`)**: Linked issues #5, #6, #16; PRs #1, #2, #4.
- **Milestone 3 (`M3: Core Fairness & Statistical Rigor Engines`)**: Linked issues #7, #8, #14, #23; PR #3.
- **Milestone 4 (`M4: End-to-End Orchestration & Surrogate Explainability`)**: Linked issues #9, #12, #13, #24, #25.
- **Milestone 5 (`M5: Benchmark Validation, Final Thesis & Capstone Defense`)**: Linked issues #22, #26, #28, #30, #32; PRs #27, #29, #31, #33.
- **Milestone 6 (`Phase 2: Post-Capstone Product Upgrade Sprint`)**: Linked issues #17, #18, #19, #20, #21.

### C. Reciprocal Peer Review Invariants
- When Aaradhya opens a PR: assign `AaradhyaDT`, reviewer `tiixsha`.
- When Tisha opens a PR: assign `tiixsha`, reviewer `AaradhyaDT`.
- Strict prohibition of ambiguous `@me` and organization names in review targets.
- Global skills `github-workflow` and `github-issue-pr-workflow` synchronized.

---

## 3. Verification Evidence
- `uv run --extra dev ruff check src/`: 100% clean (0 errors).
- `uv run --extra dev ruff format --check src/`: Cleanly formatted.
- `uv run --extra dev pytest`: 85/85 tests passed in 61.2s.
- Synchronized across all 3 git remotes (`origin`, `duo`, `org`).
