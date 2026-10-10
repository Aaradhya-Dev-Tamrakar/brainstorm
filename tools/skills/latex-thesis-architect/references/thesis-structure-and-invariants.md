# Thesis Structure & Invariants Reference Specification

This specification codifies the formal structural blueprint and architectural invariants for academic engineering thesis reports, fellowship capstone monographs, and project proposals built with `latex-thesis-architect`.

---

## 1. Directory Anatomy

```
report/
├── at_fuse_aif.cls          # Master LaTeX class (12pt scrreprt, IEEE/IOE compliant)
├── main.tex                 # Master document orchestrator
├── vars.tex                 # Centralized project metadata variables
├── references.bib           # Verified BibTeX citations
├── .latexmkrc               # Multi-pass build runner configuration
└── src/
    ├── frontmatter/
    │   ├── _coverBase.tex   # Standardized cover / title page
    │   ├── abstract.tex     # Abstract & keywords
    │   ├── acknow.tex       # Formal acknowledgments
    │   ├── abbreviations.tex# Glossaries acronym definitions
    │   ├── symbols.tex      # Glossaries mathematical symbol entries
    │   └── toc.tex          # TOC, LOF, LOT, and glossary printers
    ├── chapters/
    │   ├── intro.tex        # Chapter 1: Introduction & Scope
    │   ├── literatureReview.tex # Chapter 2: Literature & Theoretical Basis
    │   ├── requirements.tex # Chapter 3: IEEE 830 FRs & NFRs
    │   ├── systemArchitectureAndMethodology.tex # Chapter 4: Architecture & SOLID
    │   └── conclusion.tex   # Chapter 5/6: Conclusions & Open Directions
    ├── backmatter/
    │   └── back.tex         # Appendices, schemas, and extended tables
    └── images/              # High-resolution diagrams, flowcharts, plots
```

---

## 2. Invariants by Chapter

### Chapter 1: Introduction (`intro.tex`)
Must be labeled `\label{chap:intro}` and contain:
1. **Background**: Contextualize the problem within contemporary engineering realities, citing foundational studies (e.g. Buolamwini & Gebru, NIST evaluations).
2. **Problem Statement**: Explicitly formulate the technical or empirical gap between theory and available software/systems.
3. **Objectives**:
   - `\subsection{General Objective}`: Exactly one overarching sentence defining what the platform or research achieves.
   - `\subsection{Specific Objectives}`: 4 to 6 numbered, verifiable engineering goals (e.g. architecture design, toolkit integration, reporting, validation, regulatory mapping).
4. **Scope and Limitations**:
   - `\subsection{Scope}`: Explicit enumeration of included capabilities, supported formats, and target benchmarks.
   - `\subsection{Limitations}`: Explicit declaration of what is excluded, failure modes, data assumptions, and the project cut-list.

### Chapter 2: Literature Review (`literatureReview.tex`)
Must be labeled `\label{chap:litreview}` and contain:
1. **Taxonomy & Theoretical Foundations**: Mathematical derivation of core metrics, loss functions, or algorithms.
2. **Comparative Literature Matrix**: A structured `table` comparing 4 to 8 prior works across feature dimensions, benchmarks, and limitations.
3. **Regulatory & Standards Context**: Discussion of binding frameworks (EU AI Act, ISO/IEC standards, NIST AI RMF).
4. **Identified Engineering Gaps**: Explicit summary of why prior work fails to solve the operational problem.

### Chapter 3: Requirement Analysis (`requirements.tex`)
Must be labeled `\label{chap:requirements}` and contain:
1. **Functional Requirements (FR)**:
   - Formulated with IEEE 830 `shall` statements: `FR-001 (Data Ingestion): The system shall load, validate, and standardise...`
   - Numbered monotonically (`FR-001` through `FR-011`).
2. **Non-Functional Requirements (NFR)**:
   - Must contain quantifiable numeric thresholds (e.g. `n >= 30` sample size guard, $B \ge 1{,}000$ bootstrap iterations, runtime under 4 hours on NVIDIA T4, $\alpha = 0.05$ significance).
3. **System Requirements**:
   - Hardware: Minimum (CPU dev workstation) vs. Recommended (GPU benchmark environment).
   - Software: Operating systems, runtime, core libraries, and framework dependencies.

### Chapter 4: System Architecture and Methodology (`systemArchitectureAndMethodology.tex`)
Must be labeled `\label{chap:methodology}` and contain:
1. **Design Principles**: Concrete implementation of SOLID principles mapped directly to code modules.
2. **Architectural Modules Table**: Listing each module, primary responsibility, functional requirements satisfied, and dependent libraries.
3. **High-Level Workflow Diagram**: Visual dataflow flowchart referencing `\label{fig:workflow}`.
4. **Design Patterns Table**: Mapping patterns (Adapter, Strategy, Builder, Factory, Facade) to modules and descoping cut-lists.
5. **Regulatory Traceability Matrix**: Mapping computed metrics/features to specific clauses of the EU AI Act (Article 10, Annex IV) and NIST AI RMF functions.
6. **Mathematical Formalisms**: Complete LaTeX equations for all computed metrics, loss terms, and confidence intervals.
7. **Schedule & Critical Path (CPM)**: Work breakdown structure (WBS), milestones, and CPM dependency DAG.
8. **Verification & Statistical Strategy**: Grounded validation protocol ensuring findings are statistically defensible.

### Chapter 5/6: Conclusion & Future Work (`conclusion.tex`)
Must be labeled `\label{chap:conclusion}` and contain:
1. **Summary of Contributions**: Factual recapitulation of what was built and empirically verified.
2. **Empirical Highlights**: Quantitative metrics achieved on standard benchmarks.
3. **Limitations Revisited**: Epistemic honesty regarding remaining constraints and assumptions.
4. **Future Research Directions**: Concrete, actionable research milestones.

---

## 3. Typographic & LaTeX Standards

1. **Cross-Referencing**:
   - Always use `\cref{fig:name}` ("Fig. 1") or `\Cref{chap:intro}` ("Chapter 1") from the `cleveref` package. Never write raw "Figure \ref{...}".
2. **Tables**:
   - Strictly use `booktabs`: `\toprule`, `\midrule`, `\bottomrule`.
   - Never use vertical grid lines (`|`).
   - Use `tabularx` or `p{width}` for multi-line text wrapping.
3. **Math & Units**:
   - Wrap mathematical variables in `$x$`.
   - Use `\siunitx` for physical units (e.g. `\SI{5}{\giga\byte}`).
   - Declare math operators using `\DeclareMathOperator`.
4. **Acronyms & Glossary**:
   - Register acronyms in `src/frontmatter/abbreviations.tex` via `\newacronym{key}{Short}{Long}`.
   - Reference via `\gls{key}` (singular) or `\glspl{key}` (plural).
   - Register math symbols in `src/frontmatter/symbols.tex` via `\newglossaryentry{symb:key}{...}`.
