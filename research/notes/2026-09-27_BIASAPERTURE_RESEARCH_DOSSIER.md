# Research Note: BiasAperture (Diagnostic Fairness & Bias Audit Platform)

- **Date & Time**: 2026-09-27 (Updated 2026-10-01)
- **Target Repository**: [[BiasAperture]] (`F:\Aaradhya-Dev-Tamrakar\BiasAperture` / https://github.com/AaradhyaDT/BiasAperture)
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
- **Status**: Milestones M1–M4 Completed (100%), M5 System Orchestration & Case Studies Active, Proposal Defense Completed, 85/85 Tests Passing.

---

## 2. Core Architectural & Methodological Pillars

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
