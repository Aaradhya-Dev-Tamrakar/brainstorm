# Mid-Defense Guide

**File:** `main_mid_presentation.tex` -> `main_mid_presentation.pdf`

## Slide Order

| # | Slide | File | What to Include |
|---|-------|------|-----------------|
| 1 | Title + Outline | `01-title.tex` | Project title, team members with roll numbers, supervisor name, department, date |
| 2 | Motivation | `02-motivation.tex` | Why this project matters (can refine from proposal) |
| 3 | Introduction | `03-background.tex` | Domain background, key concepts, system overview |
| 4 | Objectives | `05-objectives.tex` | Same objectives from your report (unchanged from proposal) |
| 5 | Literature Review | `09-literature-review.tex` | Updated table of related papers (may add new ones found during implementation) |
| 6 | Scope Of Project | `06-scope.tex` | Refined scope based on actual progress |
| 7 | Project Applications | `08-applications.tex` | Real-world use cases |
| 8 | Methodology | `10-methodology.tex` | Updated with actual implementation details -- real diagrams, actual hardware/software used, trained model details |
| 9 | Results | `11-results.tex` | Preliminary results: initial accuracy, early prototypes, partial outputs |
| 10 | Analysis | `12-discussion.tex` | Discuss what the results mean so far, compare with expectations |
| 11 | Future Enhancements | `13-future-enhancements.tex` | What remains to be done, improvements planned for final phase |
| 12 | Conclusion | `14-conclusion.tex` | Progress summary, what was achieved, what is pending |
| 13 | References | `16-references.tex` | All cited papers and resources |

## Checklist Before Presenting

- [ ] All placeholder text replaced with actual content
- [ ] Project title and subtitle updated in `main_mid_presentation.tex`
- [ ] Student names, roll numbers, and supervisor filled in
- [ ] Methodology slides updated with real implementation (not just plans)
- [ ] System block diagram replaced with actual architecture diagram
- [ ] Flowchart reflects the implemented system flow
- [ ] Hardware/software lists match what you actually used
- [ ] At least partial results shown (even if incomplete)
- [ ] Analysis discusses current progress honestly
- [ ] Future enhancements reflect remaining work for final phase
- [ ] All `[Figure Placeholder]` boxes replaced with real screenshots/figures
- [ ] References updated with any new papers cited
- [ ] Compile and review the PDF end-to-end
- [ ] Practice the presentation (aim for 12-15 minutes)

## Key Differences from Proposal

- Methodology should show **actual implementation**, not just plans
- Include **preliminary results** (even partial or incomplete)
- Analysis should compare progress against original objectives
- Future enhancements focus on **remaining work**, not distant ideas

## How to Compile

```bash
latexmk -pdf main_mid_presentation.tex
latexmk -c  # clean auxiliary files, keeps PDF
```
