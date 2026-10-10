# Regulatory and Standards Traceability Matrix

This reference provides canonical LaTeX table templates and alignment mappings for grounding AI systems, fairness audits, and software engineering capstones in international regulatory and technical standards.

---

## 1. EU AI Act & NIST AI RMF Alignment Table

Incorporate this table into Chapter 4 (`systemArchitectureAndMethodology.tex`) to establish direct regulatory audit compliance:

```latex
\begin{table}[htbp]
    \centering
    \renewcommand{\arraystretch}{1.3}
    \caption{Mapping of system features to international regulatory and governance frameworks.}
    \label{tab:regmapping}
    \begin{tabular}{p{3.2cm}p{3.8cm}p{3.8cm}p{3.2cm}}
        \toprule
        \textbf{System Feature} & \textbf{EU AI Act (2024/1689)} & \textbf{NIST AI RMF 1.0} & \textbf{IEEE Standard} \\
        \midrule
        Data Ingestion \& Validation & Article~10(2)(b): Data provenance and validation & MAP 1.1: Context and data risks mapped & IEEE 830-1998 (FR-001) \\
        Core Disparity Metrics & Article~10(2)(f): Examination of possible biases & MEASURE 2.5: Demographic disparities evaluated & IEEE 7000-2021 \\
        Bootstrap Uncertainty ($95\%$ BCa) & Article~10(3): Statistical representativeness & MEASURE 2.11: Uncertainty quantification & IEEE 1012-2016 \\
        Sparse Cohort Suppression ($n < 30$) & Article~10(4): Statistical robustness & MEASURE 2.6: Sample size limitations guarded & IEEE 7003-2021 \\
        Explainability \& Attribution & Article~13(1): Interpretability of high-risk AI & MAP 2.3: Proxy variable entanglement identified & IEEE 7001-2021 \\
        Exportable Compliance Dossier & Annex~IV(2)(e): Technical documentation & GOVERN 1.2: Institutional audit logging & IEEE 829-2008 \\
        \bottomrule
    \end{tabular}
\end{table}
```

---

## 2. IEEE 830 Functional & Non-Functional Formalism

In Chapter 3 (`requirements.tex`), requirements must be structured with explicit traceability:

```latex
\section{Functional Requirements}
\begin{enumerate}
    \item \textbf{FR-001 (Data Ingestion):} The system shall load, validate, and standardise benchmark datasets, validating image integrity and aligning demographic labels into the locked internal schema.
    \item \textbf{FR-002 (Inference Adapter):} The system shall obtain model predictions via either in-process execution or precomputed predictions file ingestion.
    \item \textbf{FR-003 (Metric Computation):} The system shall compute canonical disparity metrics cross-validated between independent backends.
    \item \textbf{FR-004 (Statistical Significance):} The system shall compute Pearson's $\chi^2$ test of independence and 95\% bootstrap confidence intervals for each reported disparity.
\end{enumerate}

\section{Non-Functional Requirements}
\begin{enumerate}
    \item \textbf{NFR-001 (Statistical Rigour):} All significance testing shall enforce a significance threshold of $\alpha = 0.05$ with exact $p$-values reported.
    \item \textbf{NFR-002 (Uncertainty Quantification):} Every reported metric shall include 95\% confidence intervals computed from a minimum of 1{,}000 bootstrap resamples.
    \item \textbf{NFR-003 (Sparse Sample Guardrail):} Demographic cohorts with fewer than thirty observations ($n < 30$) shall be automatically suppressed from disparity computation.
    \item \textbf{NFR-004 (Execution Latency):} A full benchmark evaluation over 10{,}000 images shall complete within 30 minutes on standard compute hardware.
\end{enumerate}
```
