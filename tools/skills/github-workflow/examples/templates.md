# Issue & Pull Request Markdown Templates

Standardized templates for structuring GitHub issues, milestone releases, and pull requests to maintain high-agency team clarity.

---

## 1. Feature / Refactor Issue Template

```markdown
## Overview
[Concise summary of the architectural motivation, user need, or advisor feedback driving this work.]

## Scope & Non-Goals
- **In Scope**: [What is being addressed]
- **Out of Scope**: [Explicit boundaries or cut-list items]

## Tasks
- [ ] [Subtask 1: Initial setup / data model / interface]
- [ ] [Subtask 2: Core implementation]
- [ ] [Subtask 3: Edge case handling & error guards]
- [ ] [Subtask 4: Documentation / docstrings update]
- [ ] [Subtask 5: Verification (test suite + linting)]
```

---

## 2. Bug Fix Issue Template

```markdown
## Problem Description
[Describe the bug, unexpected behavior, or discrepancy encountered.]

## Reproduction Steps
1. Run `[command]`
2. Observe error `[error output or stack trace]`

## Root Cause Analysis
[Backtracked explanation of why the failure occurred.]

## Proposed Fix & Acceptance Checklist
- [ ] [Identify root file and line]
- [ ] [Apply diff-precise correction]
- [ ] [Add regression test covering the edge case]
- [ ] [Verify full test suite and lint passes]
```

---

## 3. Pull Request Template

```markdown
## Summary
- [Bullet 1 summarizing key addition or refactor]
- [Bullet 2 detailing architectural decisions or design patterns applied]
- [Bullet 3 highlighting synchronization or configuration updates]

Closes #[ISSUE_NUMBER]

## Verification
| Verification Gate | Command Executed | Outcome | Status |
| :--- | :--- | :--- | :--- |
| **Unit / Invariant Tests** | `uv run --extra dev pytest` | 116 / 116 passed | `PASS` |
| **Lint & Formatting** | `uv run --extra dev ruff check src/` | 0 errors | `PASS` |
| **Self-Healing Audit** | `python scripts/ci_self_healing.py` | 0 violations, 0 secret hits | `PASS` |

## Notes for Reviewer
[Optional notes pointing the reviewer to specific files, diffs, or design choices.]
```

---

## 4. Milestone Release & SHA Integrity Template

> [!IMPORTANT]
> Never use placeholder or synthetic strings (e.g. `rel50`, `upg47`). All commit references must link to authentic 7–40 hex Git commit SHAs resolving directly on GitHub.

```markdown
## Release Summary: [Milestone Name / Version Tag]

- **Target Repository**: `[Owner/Repo]`
- **Head Commit SHA**: [`[7-char-sha]`](https://github.com/[Owner]/[Repo]/commit/[full-sha])
- **Verified Invariants**: [e.g. 100% test pass, SMT Z3 verified, zero secret leaks]

### Shipped Highlights
- [Feature 1 with issue anchor #12]
- [Bug fix 2 with issue anchor #15]
```

---

## 5. Issue Progress Audit Comment Template

```markdown
### 🧪 Verification & Completion Summary
- **Implementation**: [Brief summary of code additions/refactors]
- **Verification Gates**:
  - `pytest`: 100% pass (X tests passing)
  - `ruff`: Clean pass (0 errors)
  - `sync.bat -WhatIf`: Verified dry-run status and CI bypass
- **Tracking Anchor**: Completed subtasks [1-5] via `gh-task`. Ready for PR dispatch.
```
