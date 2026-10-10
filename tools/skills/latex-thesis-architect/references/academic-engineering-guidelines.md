# Academic Engineering Report & Presentation Guidelines

This reference documents the modular academic reporting standards and defense presentation protocols for undergraduate engineering capstones, project proposals, progress evaluations, and thesis reports.

Canonical Repositories:
- **Report Template**: [`https://github.com/Aaradhya-Dev-Tamrakar/latex-engineering-report-template`](https://github.com/Aaradhya-Dev-Tamrakar/latex-engineering-report-template) (`engineering-report.cls`)
- **Beamer Template**: [`https://github.com/Aaradhya-Dev-Tamrakar/latex-beamer-presentation-template`](https://github.com/Aaradhya-Dev-Tamrakar/latex-beamer-presentation-template) (`beamer-presentation.cls`)

---

## 1. Project Lifecycle & Report Deliverables

Academic engineering curricula typically enforce a three-stage progression:

### Phase 1: Project Proposal Report
- **Goal**: Establish technical feasibility, problem significance, formal objectives, methodology, and schedule.
- **Frontmatter**:
  1. Base Cover Page (`src/frontmatter/_coverBase.tex`) without supervisor signature lines.
  2. Acknowledgements (`src/frontmatter/acknow.tex`).
  3. Abstract (`src/frontmatter/abstract.tex`).
  4. Table of Contents (TOC), List of Figures (LOF), List of Tables (LOT).
  5. List of Abbreviations & List of Symbols (`src/frontmatter/toc.tex`).
- **Main Matter**:
  - Chapter 1: Introduction (Background, Problem Statement, Objectives, Scope & Limitations).
  - Chapter 2: Literature Review (Prior art, comparative analysis, theoretical foundation).
  - Chapter 3: Requirement Analysis (IEEE 830 FRs & NFRs, System Hardware/Software specs).
  - Chapter 4: System Architecture and Methodology (Block diagrams, workflow, mathematical formulation).
  - Chapter 5/6: Expected Results / Preliminary Work.
- **Mandatory Appendices**:
  - `Appendix A`: Cost Estimate / Bill of Materials (BOM) Budget.
  - `Appendix B`: Project Timeline / Gantt Chart.

---

### Phase 2: Mid-Term Progress Report
- **Goal**: Demonstrate functional prototypes, preliminary benchmark results, hardware/software integration, and schedule compliance.
- **Frontmatter**: Standard frontmatter matching Proposal.
- **Main Matter Updates**:
  - Chapter 5: **Implementation Details** (Hardware schematics, software modules, algorithm implementation, interface wiring).
  - Chapter 6: **Result and Analysis** (Preliminary benchmark data, initial accuracy/loss curves, latency benchmarks).
  - Chapter 7: **Remaining Tasks** (Specific deliverables remaining before final submission, adjusted Gantt chart).
- **Appendices**: Updated budget expenditures and updated Gantt chart.

---

### Phase 3: Final Defense Report & Thesis
- **Goal**: Full peer-review grade engineering monograph documenting all verified capabilities.
- **Mandatory Institutional Frontmatter**:
  1. **Base Cover Page** (`_coverBase.tex`).
  2. **Supervisor Cover Page** (`_coverWithSupervisors.tex`).
  3. **Certificate of Approval** (`certificate.tex`): 2x2 signature grid for:
     - Project Supervisor
     - External Examiner
     - Project Coordinator
     - Head of Department
  4. **Student Declaration** (`declar.tex`): Signed originality statement.
  5. **Copyright Notice** (`copyright.tex`): Institutional copyright assignment.
  6. Acknowledgements, Abstract, TOC, LOF, LOT, Abbreviations, Symbols.
- **Main Matter**:
  - Full Chapters 1 through 7 (Intro, LitReview, Requirements, Architecture/Methodology, Implementation Details, Results & Discussion, Conclusion).
- **Mandatory Appendices**:
  - `Appendix A`: Technical Data Sheets / Pinouts / Schematics.
  - `Appendix B`: Final Cost Breakdown & Procurement Audit.
  - `Appendix C`: Completed Project Timeline.
  - `Appendix D`: Plagiarism Report certification under institutional ceiling.
  - References: IEEE style (`\bibliographystyle{IEEEtran}`).

---

## 2. Minimalist Beamer Presentation Protocol (`beamer-presentation.cls`)

The Beamer class enforces **16:9 widescreen, distraction-free typography** designed for high-contrast auditorium projection:

- **Typography**: Helvetica sans-serif (`helvet`) with large bold titles.
- **Color Scheme**: High-contrast black on white (no gradients or heavy banners).
- **Footline**: Subtle date on bottom-left, clean slide number on bottom-right.
- **Navigation**: Distracting floating navigation symbols are disabled.

### Defense Deck Blueprints

| Defense Stage | Target Duration | Recommended Slides | Key Slide Sequence |
| :--- | :--- | :--- | :--- |
| **Proposal Defense** | 10–12 minutes | 12–15 slides | `01-title` $\to$ `02-motivation` $\to$ `03-background` $\to$ `04-problem` $\to$ `05-objectives` $\to$ `06-scope` $\to$ `09-literature` $\to$ `10-methodology` $\to$ `11-expected-outcome` $\to$ `15-timeline` $\to$ `16-references` $\to$ `18-qna` |
| **Mid-Term Defense** | 10–15 minutes | 14–18 slides | Above slides + Prototype architecture, live hardware photos / UI captures, preliminary loss/accuracy curves, and remaining sprint tasks |
| **Final Thesis Defense** | 15–20 minutes | 18–25 slides | Full presentation including: Problem $\to$ Literature Gap $\to$ Mathematical Model $\to$ Architecture $\to$ Empirical Results $\to$ Error/Ablation Analysis $\to$ Verification Proof $\to$ Conclusion $\to$ Demo/Q&A |

---

## 3. Fast Scaffolding with `latex-thesis-architect`

```powershell
python scripts/scaffold_thesis.py \
  "path/to/project" \
  --template full-pack \
  --title "Distributed Autonomous Swarm Framework" \
  --author1 "Author 1" --roll1 "ROLL-001" \
  --author2 "Author 2" --roll2 "ROLL-002" \
  --supervisor "Supervisor Name" \
  --coordinator "Project Coordinator" \
  --hod "Head of Department"
```

Resulting directory tree:
```
project/
├── report/           # Full academic engineering report (engineering-report.cls)
└── presentation/     # 16:9 widescreen Beamer deck (beamer-presentation.cls)
```
