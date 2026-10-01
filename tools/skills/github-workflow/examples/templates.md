# Issue & Pull Request Markdown Templates

Standardized templates for structuring GitHub issues and pull requests to maintain high-agency team clarity.

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
- `[test command, e.g. uv run --extra dev pytest]`: [result, e.g. 85/85 passed]
- `[lint command, e.g. uv run --extra dev ruff check src/]`: [result, e.g. 0 errors]
- `[formatting command, e.g. uv run --extra dev ruff format --check src/]`: [result, e.g. Clean]

## Notes for Reviewer
[Optional notes pointing the reviewer to specific files, diffs, or design choices.]
```
