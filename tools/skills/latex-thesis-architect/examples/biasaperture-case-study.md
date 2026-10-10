# Case Study Walkthrough: The BiasAperture Capstone Report

This case study breaks down how the **BiasAperture** Fellowship Capstone Report (`report/`) was structured, authored, and audited using the principles now codified in `latex-thesis-architect`.

---

## 1. Project Profile

- **Title**: *BiasAperture: A Diagnostic and Evaluative Framework for Auditing Demographic Bias in Facial Analysis Systems*
- **Program**: Fusemachines AI Fellowship Capstone Program / IOE Pulchowk & Thapathali Campus
- **Class File**: `at_fuse_aif.cls` (12pt, IEEE/IOE compliant `scrreprt`)
- **Key Modules**: Ingestion $\to$ Model Interface $\to$ Fairness Engine $\to$ Surrogate Explainability $\to$ Compliance Reporting

---

## 2. Calm-Authority Implementation in the Report

### Abstract & 1-Sentence Thesis
The abstract opens with an empirical statement and clearly states the thesis:
> *"Automated facial analysis systems are widely deployed despite well-documented accuracy disparities across demographic cohorts, yet independent and reproducible auditing remains rare in practice. This report introduces BiasAperture, a diagnostic software framework that audits third-party facial analysis models for subgroup and intersectional disparities and compiles them into regulator-ready compliance dossiers."*

### Explicit Scope Boundaries & Cut-List
Rather than claiming to solve all aspects of AI bias, the report explicitly scopes its boundaries in Chapter 1 and Chapter 4:
1. **Diagnostic Only**: *"BiasAperture is scoped strictly as diagnostic: it identifies and statistically characterises disparities without altering model weights, applying in-processing mitigations, or synthesizing demographic images."*
2. **Dataset Descoping**: *"UTKFace was profiled during exploratory analysis and cut due to DEX model-estimated age noise and collapsed racial categories; FairFace was retained as the sole audited benchmark."*
3. **Attribution Descoping**: *"Spatial pixel-level SHAP was deferred to future work due to superpixel segmentation instability; demographic-dummy surrogate attribution was implemented instead."*

### Statistical Rigor ($n \ge 30$)
The report enforces empirical honesty:
- Subgroups with $n < 30$ samples are suppressed from scoring and flagged as `insufficient_sample = True`.
- Point estimates are backed by Pearson's $\chi^2$ significance tests and 95% BCa bootstrap confidence intervals with $B \ge 1{,}000$ iterations.

---

## 3. SOLID Principles in Practice

In Chapter 4, SOLID principles are mapped directly to engineering reality:

| Principle | Architectural Mechanism in BiasAperture |
| :--- | :--- |
| **Single Responsibility** | 5 distinct pipeline modules (Ingestion, Interface, Engine, Explainability, Reporting). No module accesses another's memory state. |
| **Open-Closed** | `FairnessBackend` strategy interface: adding a new disparity metric or fairness toolkit requires zero modification to core engine loops. |
| **Liskov Substitution** | `ModelInterface` allows transparent substitution between `InProcessInterface` (live PyTorch/TF inference) and `PredictionsFileInterface` (batch CSV/JSON). |
| **Interface Segregation** | Decoupled minimal contracts between reporting and metrics computation engines. |
| **Dependency Inversion** | Orchestration layer depends on abstract interfaces, never concrete toolkit backends. |

---

## 4. Scaffolding this Pattern with the Skill

To scaffold a report mirroring the BiasAperture architecture:

```powershell
python scripts/scaffold_thesis.py \
  "path/to/project" \
  --title "BiasAperture: A Diagnostic Framework for Demographic Bias Auditing" \
  --university "Fusemachines Inc." \
  --dept "AI Fellowship Program" \
  --author1 "Author 1" \
  --author2 "Author 2" \
  --doc-type "A CAPSTONE THESIS AND FAIRNESS AUDIT REPORT"
```
