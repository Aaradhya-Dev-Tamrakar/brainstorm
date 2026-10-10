# Final Defense Guide

**File:** `main_final_presentation.tex` -> `main_final_presentation.pdf`

## Slide Order

| # | Slide | File | What to Include |
|---|-------|------|-----------------|
| 1 | Title + Outline | `01-title.tex` | Project title, team members with roll numbers, supervisor name, department, date |
| 2 | Motivation | `02-motivation.tex` | Why this project matters |
| 3 | Introduction | `03-background.tex` | Domain background, key concepts, final system overview |
| 4 | Objectives | `05-objectives.tex` | Same objectives from your report |
| 5 | Literature Review | `09-literature-review.tex` | Complete table of related papers referenced throughout the project |
| 6 | Scope Of Project | `06-scope.tex` | Final scope of the completed project |
| 7 | Project Applications | `08-applications.tex` | Real-world use cases and demonstrated applications |
| 8 | Methodology | `10-methodology.tex` | Complete implementation: final architecture, all diagrams, trained models, dataset details |
| 9 | Results | `11-results.tex` | Full results: precision-recall curves, ROC curves, confusion matrix, screenshots, prototype photos |
| 10 | Analysis | `12-discussion.tex` | Thorough analysis of results, comparison with objectives, strengths and weaknesses |
| 11 | Future Enhancements | `13-future-enhancements.tex` | Potential improvements beyond current work |
| 12 | Conclusion | `14-conclusion.tex` | Summary of the developed system, contributions, results achieved, significance |
| 13 | References | `16-references.tex` | All cited papers and resources |

## Checklist Before Presenting

- [ ] All placeholder text replaced with final content
- [ ] Project title and subtitle updated in `main_final_presentation.tex`
- [ ] Student names, roll numbers, and supervisor filled in
- [ ] Methodology slides show the **completed** system with real diagrams
- [ ] All figure placeholders replaced with actual images/screenshots
- [ ] Results include quantitative metrics (accuracy, precision, recall, F1, etc.)
- [ ] Confusion matrix, ROC curve, precision-recall curve are from actual experiments
- [ ] Prototype/dashboard screenshots are from the working system
- [ ] Analysis thoroughly discusses results and compares against objectives
- [ ] Each objective from slide 4 is addressed in the results/conclusion
- [ ] Conclusion summarizes all key contributions clearly
- [ ] References are complete (all cited works included)
- [ ] Remove the italic guide note from the Objectives slide
- [ ] Compile and review the PDF end-to-end
- [ ] Practice the presentation (aim for 15-20 minutes)

## Key Differences from Mid-Defense

- Results must be **complete and final** (not preliminary)
- Analysis should be comprehensive with proper metric comparisons
- Conclusion should tie back to every original objective
- All figures must be from the finished, working system

## How to Compile

```bash
latexmk -pdf main_final_presentation.tex
latexmk -c  # clean auxiliary files, keeps PDF
```
