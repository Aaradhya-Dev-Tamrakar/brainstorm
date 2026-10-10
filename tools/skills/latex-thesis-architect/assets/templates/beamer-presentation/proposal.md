# Proposal Defense Guide

**File:** `main_proposal_presentation.tex` -> `main_proposal_presentation.pdf`

## Slide Order

| # | Slide | File | What to Include |
|---|-------|------|-----------------|
| 1 | Title + Outline | `01-title.tex` | Project title, team members with roll numbers, supervisor name, department, date |
| 2 | Motivation | `02-motivation.tex` | Why this project matters, the gap or problem you identified |
| 3 | Introduction | `03-background.tex` | Brief background of the domain, key concepts, proposed system overview |
| 4 | Objectives | `05-objectives.tex` | Exact objectives as submitted in your proposal report |
| 5 | Literature Review | `09-literature-review.tex` | Table of 3-5 related papers with their objective, methodology, findings, limitations |
| 6 | Scope Of Project | `06-scope.tex` | What the project covers and what it does not |
| 7 | Project Applications | `08-applications.tex` | Real-world use cases and target users |
| 8 | Methodology | `10-methodology.tex` | System block diagram, working principle, workflow, flowchart, hardware/software requirements, algorithm/ML architecture, dataset preparation |
| 9 | Expected Outcome | `11-expected-outcome.tex` | What you expect the system to achieve once built |
| 10 | Future Enhancements | `13-future-enhancements.tex` | Planned improvements beyond the current scope |
| 11 | Conclusion | `14-conclusion.tex` | Summary of the proposed system, feasibility, expected outcomes, significance |
| 12 | References | `16-references.tex` | Cited papers and resources |

## Checklist Before Presenting

- [ ] Replace all placeholder text with your actual content
- [ ] Update project title and subtitle in `main_proposal_presentation.tex`
- [ ] Fill in student names and roll numbers (e.g. ROLL-001)
- [ ] Add supervisor name and title
- [ ] Objectives match exactly what you submitted in the report
- [ ] Literature review table has real papers (minimum 3)
- [ ] System block diagram and flowchart figures are inserted
- [ ] Hardware and software requirements are specific to your project
- [ ] Expected outcomes are realistic and measurable
- [ ] References are complete and properly cited
- [ ] Remove the italic guide note from the Objectives slide
- [ ] Replace all `[Figure Placeholder]` boxes with actual images
- [ ] Compile and review the PDF end-to-end
- [ ] Practice the presentation (aim for 10-15 minutes)

## How to Compile

```bash
latexmk -pdf main_proposal_presentation.tex
latexmk -c  # clean auxiliary files, keeps PDF
```
