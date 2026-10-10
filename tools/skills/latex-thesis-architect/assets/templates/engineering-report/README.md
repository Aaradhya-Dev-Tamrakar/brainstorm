# LaTeX Report Template (Campus / Institution)

An IEEE-compliant LaTeX report template designed for major project, minor project, and capstone thesis reports at Campus / Institution, Faculty of Engineering (Engineering Faculty), University Name.

---

## 1. Overview

The document class (`engineering-report.cls`) is based on `scrreprt` (KOMA-Script) and configured to meet institutional Engineering Faculty submission guidelines:
- **Paper Size & Margins**: A4 paper, `left=1.5in`, `right=1.0in`, `top=1.0in`, `bottom=1.0in` (with `0.5in` footskip for centered page numbers).
- **Typography**: Times font (`times` and `newtxmath`) at 12pt with `microtype` enabled.
- **Line Spacing**: 1.5 line spacing (`\onehalfspacing`) throughout main text.
- **Tables & Figures**: Formal `booktabs` styling (no vertical grid lines), captions matching IEEE standards.
- **Cross-Referencing**: Automatic uppercase cross-referencing via `cleveref` (`\cref{...}` and `\Cref{...}`).
- **Glossaries**: Automatic multi-pass processing for acronyms (`\gls{...}`) and mathematical symbols.

---

## 2. Directory Structure

```
.
├── engineering-report.cls        # IEEE-compliant 12pt scrreprt document class
├── main.tex                 # Master document orchestrator
├── vars.tex                 # Centralized project metadata configuration
├── references.bib           # BibTeX bibliography database
├── 0_draft.md               # Draft writing guidelines
├── 1_proposal.md            # Proposal report checklist & outline
├── 2_progress.md            # Mid-term progress report checklist & outline
├── 3_final.md               # Final thesis report checklist & outline
└── src/
    ├── frontmatter/         # Institutional prelim pages
    │   ├── _coverBase.tex   # Base cover page (Proposal / Progress)
    │   ├── _coverWithSupervisors.tex # Official cover page with supervisor titles
    │   ├── certificate.tex  # Certificate of Approval (4 signature grid)
    │   ├── declar.tex       # Student Declaration of Originality
    │   ├── copyright.tex    # Departmental copyright statement
    │   ├── acknow.tex       # Acknowledgments
    │   ├── abstract.tex     # Abstract & keywords
    │   ├── abbreviations.tex# Glossary acronym definitions (\newacronym)
    │   ├── symbols.tex      # Glossary symbol definitions (\newglossaryentry)
    │   └── toc.tex          # TOC, LOF, LOT, and glossary inclusion
    ├── chapters/            # Report body chapters
    │   ├── intro.tex        # Chapter 1: Introduction, Problem, Objectives, Scope
    │   ├── literatureReview.tex # Chapter 2: Literature Review & Taxonomy
    │   ├── requirements.tex # Chapter 3: IEEE 830 Functional & Non-Functional Reqs
    │   ├── systemArchitectureAndMethodology.tex # Chapter 4: Architecture, Modules, Workflow
    │   ├── implementation.tex # Chapter 5: Hardware/Software Implementation Details
    │   ├── resultAndAnalysis.tex # Chapter 6: Empirical Results & Evaluation
    │   └── conclusion.tex   # Chapter 7: Conclusions & Future Work
    └── backmatter/          # Appendices and supplementary documentation
        ├── studentGuide.tex # Reference guide for LaTeX formatting
        ├── budget.tex       # Appendix A: Cost estimate / BOM budget
        └── timeline.tex     # Appendix B: Gantt chart & project timeline
```

---

## 3. Configuration Guide

Project metadata is centralized in [`vars.tex`](vars.tex). Edit this single file to update titles, authors, and faculty committee details across all frontmatter pages:

```latex
% University & Institutional Details
\newcommand\cUniversity{University Name}
\newcommand\cDepartment{Faculty of Engineering}
\newcommand\cCampus{Campus / Institution}
\newcommand\cDocumentType{A MAJOR PROJECT REPORT}  % Options: MAJOR/MINOR PROJECT PROGRESS/PROPOSAL REPORT
\newcommand\cTitle{PROJECT TITLE IN FULL UPPERCASE}
\newcommand\cTitleShort{Short Title for Header}

% Author Details (1 to 4 authors supported)
\renewcommand\cSubmittedI{Author 1}
\renewcommand\cSubmittedII{Author 2}
\renewcommand\cSubmittedIII{Author 3}
\renewcommand\cSubmittedIV{}  % Leave empty if 3 authors

\renewcommand\cSubmittedIRoll{(ROLL-001)}
\renewcommand\cSubmittedIIRoll{(ROLL-002)}
\renewcommand\cSubmittedIIIRoll{(ROLL-003)}
\renewcommand\cSubmittedIVRoll{}

% Faculty & Committee
\newcommand\cSupervisor{Supervisor Name}
\newcommand\cSupervisorTitle{Project Supervisor}
\newcommand\cSupervisorDept{Department of Engineering}
\newcommand\cSupervisorAddress{Campus / Institution}

\newcommand\cProjectCoordinator{Project Coordinator}
\newcommand\cProjectCoordinatorTitle{Project Coordinator}
\newcommand\cProjectCoordinatorDept{Department of Engineering}
\newcommand\cProjectCoordinatorAddress{Campus / Institution}

\newcommand\cHOD{Head of Department}
\newcommand\cHODTitle{Head of Department}
\newcommand\cHODDept{Department of Engineering}
\newcommand\cHODAddress{Campus / Institution}

\newcommand\cExternalExaminer{External Examiner}
\newcommand\cExternalExaminerTitle{External Examiner}
\newcommand\cExternalExaminerDept{External Institution}
\newcommand\cExternalExaminerAddress{City, Country}

% Date
\newcommand\cDate{Month Year}
\newcommand\cDateFull{Month DD, YYYY}
```

---

## 4. Compilation

### Using `latexmk` (Recommended)
```powershell
# Build complete PDF with automatic BibTeX and glossaries passes
latexmk -pdf main.tex

# Clean auxiliary build artifacts
latexmk -C
```

### Manual Multi-Pass Compilation
```powershell
pdflatex main.tex
bibtex main
makeglossaries main
pdflatex main.tex
pdflatex main.tex
```

---

## 5. Lifecycle Guidelines & Checklists

- [`1_proposal.md`](1_proposal.md): Required sections and appendices for Project Proposal.
- [`2_progress.md`](2_progress.md): Deliverables and prototype checkpoints for Mid-Term Progress.
- [`3_final.md`](3_final.md): Mandatory formal pages (Certificate of Approval, Declaration, Copyright) and Plagiarism Report for Final Defense.
