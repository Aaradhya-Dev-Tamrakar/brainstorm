# Multi-Remote Synchronization & Ecosystem Automation

This document outlines version control synchronization rules when operating in repositories that utilize `sync.bat` / `sync.ps1`.

---

## 1. The Multi-Remote Pattern

Certain projects (e.g. BiasAperture, Portfolio, System Optimizer) synchronize across multiple remotes:
- **`origin`**: Canonical repository (compulsory upstream, e.g. organization / fellowship repo).
- **`duo`**: Primary collaborator or developer personal fork (compulsory).
- **`org`**: Organizational mirror or secondary backup (optional / best-effort).

### Invariant Rule
When `sync.ps1` or `sync.bat` is present in the repository root:
- Direct `git commit`, `git push`, or `git add` are **strictly forbidden**.
- All changes must be processed through the sync wrapper to ensure multi-remote consistency and atomic tracking.

---

## 2. Command Reference

### Windows Environment
Always prefer `.\sync.bat` across Windows environments:
- It automatically resolves `pwsh` (PowerShell 7+) or `powershell` (Windows PowerShell 5.1).
- It passes `-ExecutionPolicy Bypass`, avoiding execution policy errors (`Restricted`/`RemoteSigned`) on fresh clones without system reconfiguration.

```cmd
:: Semantic commit linked to issue #26
.\sync.bat -m "feat(scope): descriptive message (#26)"

:: Explicit branch targeting (or let sync auto-route)
.\sync.bat -m "refactor(docs): update docstrings (#26)" -Branch refactor/standardize-docstrings

:: Safe pull only with autostash
.\sync.bat -PullOnly

:: Mirror all origin branches across secondary remotes
.\sync.bat -MirrorOnly
```

### Non-Windows Environments
```bash
pwsh -File ./sync.ps1 -m "feat(scope): descriptive message (#26)"
```

---

## 3. Conflict Prevention & Hygiene Built-Ins

1. **Auto-Rebase Drift Guard**:
   Before staging, `sync.ps1` checks how many commits the current branch is behind `origin/main` and runs `git rebase refs/remotes/origin/main` to eliminate drift before pushing.
2. **Main-Only File Guards**:
   Files like `docs/CHANGELOG.md`, `README.md`, or binary artifacts like `report/main.pdf` are conflict-prone across concurrent feature branches. The sync utility automatically un-stages `docs/CHANGELOG.md` on feature branches to keep timestamps main-only.
3. **Forced Refspec for Mirroring**:
   Mirror synchronization uses `+refs/remotes/$originRemote/$branchName:refs/heads/$branchName` to ensure secondary remotes (`duo`, `org`) reflect exact upstream state even after rebases.
