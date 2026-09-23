# 🏛️ DECISION RECORD: DEC-002 (Personal R&D ⇄ Duo-Capstone Boundary & Audit Evidence Discipline)

```text
Decision ID:          DEC-002
Title:                Boundary Between the Personal Tool Ecosystem and the Duo Capstone, Backend Authority, and the Evidence-Calibrated Auditing Research Wedge
Status:               PROPOSED (Awaiting Architect Ratification)
Decision Date:        2026-09-21
Principal Architect:  Aaradhya Dev Tamrakar (ADT)
Governing RFC:        research/architectures/ARCH-RFC-003-CAPSTONE-DEFENSE-STANDARD.md, research/architectures/ARCH-RFC-006-INFORMATION-BOUNDARY.md
Evidence Tier:        E1 — DESIGN SPECIFICATION
Epistemic Class:      HEURISTIC_HYPOTHESIS (research novelty), EMPIRICALLY_VERIFIED (ecosystem inventory anchors only)
Source Transcripts:   research/transcripts/2026-09-21_EVALUATE-FOUR-PROJECTS_CONVERSATION.md
```

---

## 1. Context & Problem

The 2026-09-21 evaluation transcript ([`2026-09-21_EVALUATE-FOUR-PROJECTS_CONVERSATION.md`](../transcripts/2026-09-21_EVALUATE-FOUR-PROJECTS_CONVERSATION.md)) evaluated `brainstorm`, `super-nlm`, `Claude-Desktop` and `AaradhyaDT.github.io` as **one system rather than four repositories**, and then extended the evaluation into the BiasAperture capstone (a two-person academic project: ADT + Tisha Manandhar).

Two governance questions were left open by that dialogue and must be fixed before they generate drift:

1. **Ownership/dependency ambiguity:** nothing currently states whether the four personal repositories are _inputs_ to the capstone or _runtime dependencies_ of it. Silent absorption of the capstone into personal R&D would compromise academic ownership and the defensibility trail required by [`ARCH-RFC-003`](../architectures/ARCH-RFC-003-CAPSTONE-DEFENSE-STANDARD.md).
2. **Evidentiary status of the audit stack:** the transcript records that BiasAperture runs **FairFace** as its empirical dataset, **Fairlearn** as its primary backend, and retains an **implemented** AIF360 adapter. Presenting both backends as co-equal empirical evidence is an epistemic inflation of the kind prohibited by [`POL-001`](../../schemas/evidence-policy.md).

Additionally, the transcript proposed a research extension (audit self-calibration) that had no falsifiable card in this repository, leaving the Three-Output Rule of [`AGENTS.md`](../../AGENTS.md) unmet for that session.

---

## 2. Decisions

**D1 — Capstone boundary (non-dependency).**
`BiasAperture` remains a duo-owned academic artifact. The personal ecosystem performs _support_ roles only and MUST NOT appear in the capstone's core dependency graph:

- `super-nlm` → research memory / literature oracle (knowledge retrieval, not numerical evidence).
- `Claude-Desktop` → private experiment fleet for running and QA-ing audit sweeps.
- `brainstorm` → methodology and evidence-governance framework (evidence tiers, evidence chains).
- `AaradhyaDT.github.io` → public demonstration surface.

**D2 — Backend authority & metric harmonization.**
Fairlearn is the **authoritative runtime backend** for the FairFace empirical path. AIF360 is retained as an **implemented secondary adapter** for framework validation on structured/synthetic inputs and for interoperability — not as co-equal empirical evidence. Both remain behind the common fairness abstraction.
- **Metric Formulation Divergence:** As verified on 2026-09-23, Fairlearn defines Equalized Odds Difference as the Chebyshev bound $\max(|\Delta\text{TPR}|, |\Delta\text{FPR}|)$, whereas AIF360 computes the mean gap $\frac{1}{2}(|\Delta\text{TPR}| + |\Delta\text{FPR}|)$. Direct quantitative comparison between backends emits a `DivergenceAlert` with `difference=NaN` rather than a misleading numerical delta; silent fallback is strictly forbidden.
- **Statistical Rigor Foundation:** Invariant statistical safeguards established on 2026-09-23 mandate metric-specific hypothesis testing ($\chi^2$ selection rate for DPD/DIR, conditional TPR for EOP, joint odds test for EOD), stratified subgroup bootstrap percentile CIs ($B \ge 1,000$), delete-$d$ block jackknife variance estimation ($n > 300, d = \max(1, n // 100)$), and Holm-Bonferroni FWER step-down correction.

**D3 — Dataset provenance correction.**
UTKFace is **not** part of the empirical evaluation (labels are embedded in filenames and estimated by DEX then human-checked). FairFace is the evaluation dataset, and its annotation provenance must be described precisely: crowd-sourced human annotation with a subsequent model-assisted disagreement re-verification stage — not merely "manually labelled".

**D4 — Research wedge (adopted for evaluation, not yet implemented).**
"Evidence-Calibrated Fairness Auditing": Stage A = audit calibration via controlled prediction-layer bias injection; Stage B (stretch) = evidence-adaptive sampling to reach a target precision with fewer evaluations. Roadmap extension above a frozen core: `M5 Integration & Case Studies` → `M6 Audit Calibration` → `M7 Evidence Sufficiency` → `M8 Adaptive Audit [stretch]` → `M9 Final Evaluation` → `M10 Final Demonstrator`. **M1–M5 are unchanged.** The falsifiable form of Stage A is recorded as [`HYP-005`](../hypotheses/HYP-005-EVIDENCE-CALIBRATED-FAIRNESS-AUDIT.yaml).

**D5 — Claim language and evidence discipline.**
Every fairness claim carries an evidence chain (injection configuration, seed, sample size, predictions artifact, audit command, reported metric, confidence interval, p-value, trial count). Findings report an **evidence profile** (observed disparity, CI, p, support, backend agreement, calibration sensitivity, reproducibility) — never a single composite "fairness score" — and are worded as conditional: _"statistically supported disparity under this audit specification."_ Calibration results may never be reported as "the model is biased".

---

## 3. Consequences & Downstream Actions (Status as of 2026-09-23)

- **Completed (BiasAperture repo):** 10-finding statistical integrity remediation merged (commit `cc152da`, 85/85 tests passing). Implemented metric-specific $\chi^2$ tests, stratified subgroup bootstrap percentile CIs, delete-$d$ block jackknife, Holm-Bonferroni FWER correction, AIF360 backend fault isolation, intersectional compound axis (`race_gender`), and surrogate tree explainability scoping (spatial SHAP deferred).
- **Pending (BiasAperture repo, research wedge M6+):** a `calibration/` module (prediction-layer bias injectors, calibration runner, operating-characteristic reporting), a `calibrate` CLI surface, audit-run artifact capture, and an evidence-profile section in the audit report.
- **Pending (this repository):** a second falsifiable card for Stage B (adaptive/stratified sampling reaching a target confidence-interval width with fewer evaluations than uniform sampling).
- **Pending (novelty due diligence):** the transcript itself warns that query-efficient active fairness auditing predates this work (Yan & Zhang, 2022) and that 2026 black-box auditing work overlaps the idea. The novelty claim is therefore recorded as a **strong candidate, not established**; a systematic literature pass is required before any novelty assertion enters the capstone report or a publication draft.
- **Explicitly rejected by the transcript (recorded to prevent re-proposal):** a new composite "fairness score", spatial SHAP as the novelty claim, "more fairness metrics" as novelty, and "we added AI/LLM to fairness auditing" framing.

---

## 4. Verification Anchors

- Ecosystem inventory anchors used above resolve against [`schemas/ecosystem.registry.json`](../../schemas/ecosystem.registry.json): 21 tool modules; 17 computational engines; 4 presentation hubs; 6 compound workflows; 27 research artifacts.
- Transcript fidelity is guaranteed by [`INV-EPI-001`](../invariants/INV-EPI-001.md): the source dialogue is preserved verbatim in `research/transcripts/`.
- This record is a design-tier artifact (E1). It becomes E2+ only when the calibration module executes and is audited.
