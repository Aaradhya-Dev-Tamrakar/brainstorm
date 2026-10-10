# LaTeX Beamer Presentation Template (Campus / Institution)

A minimalist, high-contrast 16:9 widescreen LaTeX Beamer template designed for engineering project defenses and technical presentations at Campus / Institution, Faculty of Engineering (Engineering Faculty), University Name.

---

## 1. Overview

The presentation class (`beamer-presentation.cls`) enforces clean typography and eliminates visual clutter:
- **Aspect Ratio**: 16:9 widescreen (`aspectratio=169`).
- **Typography**: Helvetica sans-serif (`helvet`) with large centered bold frame titles.
- **Color Scheme**: High-contrast black on white (no colored gradients or distracting banner headers).
- **Footline**: Subtle date on bottom-left, clean slide number on bottom-right.
- **Navigation Chrome**: Floating navigation symbols and section balls are disabled.

---

## 2. Defense Entry Points

The repository provides three dedicated entry points matching the institutional engineering lifecycle:

| Stage | Master Document | Recommended Slides | Description |
| :--- | :--- | :--- | :--- |
| **Proposal Defense** | [`main_proposal_presentation.tex`](main_proposal_presentation.tex) | 12–15 slides | Problem significance, motivation, objectives, scope, literature review, methodology, expected outcome, timeline. |
| **Mid-Term Progress** | [`main_mid_presentation.tex`](main_mid_presentation.tex) | 14–18 slides | Prototype demo, preliminary benchmark results, progress check vs. Gantt, remaining sprint tasks. |
| **Final Thesis Defense** | [`main_final_presentation.tex`](main_final_presentation.tex) | 18–25 slides | Complete evaluation metrics, error/ablation analysis, mathematical model, discussion, conclusion, Q&A. |

---

## 3. Directory Structure

```
.
├── beamer-presentation.cls                     # 16:9 widescreen Beamer class
├── main_proposal_presentation.tex     # Proposal defense master
├── main_mid_presentation.tex          # Mid-term progress master
├── main_final_presentation.tex        # Final thesis defense master
├── proposal.md                        # Proposal preparation checklist
├── mid-defense.md                     # Mid-term defense checklist
├── final-defense.md                   # Final defense checklist
└── src/
    ├── images/                        # Figures, schematics, and university logo
    └── slides/                        # Modular slide components
        ├── 01-title.tex               # Title frame
        ├── 02-motivation.tex          # Project motivation
        ├── 03-background.tex          # Background context
        ├── 04-problem-statement.tex   # Formal problem statement
        ├── 05-objectives.tex          # General & specific objectives
        ├── 06-scope.tex               # In-scope & limitations
        ├── 07-originality.tex         # Novelty and contributions
        ├── 08-applications.tex        # Practical use cases
        ├── 09-literature-review.tex   # Comparative literature matrix
        ├── 10-methodology.tex         # System architecture & workflow
        ├── 11-expected-outcome.tex    # Target metrics
        ├── 11-results.tex             # Empirical plots and tables
        ├── 12-discussion.tex          # Discussion & trade-offs
        ├── 13-future-enhancements.tex # Open research directions
        ├── 14-conclusion.tex          # Final conclusions
        ├── 15-timeline.tex            # Gantt chart & milestones
        ├── 16-references.tex          # IEEE citations
        └── 18-qna.tex                 # Questions & answers frame
```

---

## 4. Configuration Guide

Edit metadata variables at the top of the relevant `main_*.tex` file:

```latex
\projecttitle{PROJECT TITLE IN FULL UPPERCASE}
\projectsubtitle{Project Proposal / Progress / Final Defense Presentation}

\newcommand{\studentone}{Student Name 1}
\newcommand{\rollone}{ROLL-001}
\newcommand{\studenttwo}{Student Name 2}
\newcommand{\rolltwo}{ROLL-002}
\newcommand{\studentthree}{Student Name 3}
\newcommand{\rollthree}{ROLL-003}
\newcommand{\studentfour}{Student Name 4}
\newcommand{\rollfour}{ROLL-004}

\presentername{\studentone}
\studentroll{\rollone}
\supervisorname{Supervisor Name}
\supervisortitle{Supervisor Title}
\departmentname{Department of Engineering}
\institutionname{Faculty of Engineering, Campus / Institution}
\presentationdate{\today}
\academicyear{Academic Year: 2026/2027}
```

---

## 5. Compilation

### Using `latexmk` (Recommended)
```powershell
# Proposal presentation
latexmk -pdf main_proposal_presentation.tex

# Mid-term presentation
latexmk -pdf main_mid_presentation.tex

# Final presentation
latexmk -pdf main_final_presentation.tex

# Clean build artifacts
latexmk -C
```

### Using `pdflatex` Directly
```powershell
pdflatex main_proposal_presentation.tex
pdflatex main_proposal_presentation.tex
```

---

## 6. Stage Checklists

Consult the accompanying Markdown guidelines before each defense:
- [`proposal.md`](proposal.md): Content flow and checklist for proposal defense.
- [`mid-defense.md`](mid-defense.md): Milestones and slide balance for mid-term defense.
- [`final-defense.md`](final-defense.md): Complete verification requirements for final defense.
