# Multi-Remote Synchronization & Ecosystem Automation

This document outlines version control synchronization rules, parameter flags, and automated workflows when operating in repositories that utilize `Makefile`, `make.bat`, and `sync.bat` / `sync.ps1` / `sync.sh`.

---

## 1. Architectural Role & Invariants

Repositories in the ecosystem (`brainstorm`, `Claude-Desktop`, `BiasAperture`, `AaradhyaDT.github.io`, `system-optimizer`, etc.) use unified multi-remote synchronization wrappers as their central orchestration engine.

### Invariant Rule
When `sync.ps1`, `sync.bat`, `sync.sh`, `scripts/sync.ps1`, `scripts/sync.bat`, `scripts/sync.sh`, or a `Makefile` with a `sync` target is present in the repository:
- Direct `git commit`, `git push`, or `git add` commands are **strictly forbidden**.
- All changes must be processed through the sync wrapper (`make sync`, `.\sync.bat`, `.\scripts\sync.bat`, `./scripts/sync.sh`) to ensure multi-remote consistency, secret scanning, and atomic tracking.

### Decluttered Directory Topology
To meet high-standard academic and open-source evaluation criteria (TAs, external reviewers) without cluttering the project root:
```
repo/
├── Makefile             # Canonical POSIX interface across Linux, macOS, and CI
├── make.bat             # Zero-dependency Windows dispatcher (native CMD/PowerShell)
├── sync.bat             # (Optional) Root backward-compatibility forwarder shim
├── scripts/
│   ├── sync.ps1         # Full PowerShell synchronization engine
│   ├── sync.bat         # Windows execution wrapper
│   ├── sync.sh          # POSIX shell execution wrapper
│   └── verify.py        # Deterministic verification engine
```

### Multi-Remote Mirroring Topology
Certain projects synchronize across multiple remotes:
- **`origin`**: Canonical repository (compulsory upstream, e.g. organization or primary project repo).
- **`duo`**: Primary collaborator or developer personal fork (compulsory).
- **`org`**: Organizational mirror or secondary backup (optional / best-effort).

---

## 2. Command Reference

### Universal Makefile Interface (Cross-Platform)
Standard entrypoint across POSIX platforms (Linux, macOS, containers):
```bash
# 1. Routine Sync (auto-generates conventional commit message with churn stats)
make sync

# 2. Track A: Semantic commit linked to tracked issue
make sync ARGS="-m 'feat(scope): descriptive message (#26)'"

# 3. Track B: Automated BRL Pull Request Workflow
make sync ARGS="-PR -m 'feat(p2p): campus swarm marketplace' -Issue 26 -Reviewer tiixsha"

# 4. Skip CI Runner Execution (explicit bypass)
make sync ARGS="-SkipCI -m 'docs(notes): update research matrix (#26)'"

# 5. Dry-Run Preview Mode
make sync ARGS="-WhatIf"

# 6. Safe Pull Only
make sync ARGS="-PullOnly"
```

### Windows Environment (make.bat & sync.bat)
Windows developers can invoke `make` directly via the zero-dependency `make.bat` wrapper, or use `.\sync.bat`:
```cmd
:: Via make.bat dispatcher:
make sync
make sync -m "feat(scope): descriptive message (#26)"
make sync -PR -m "feat(p2p): campus swarm marketplace" -Issue 26 -Reviewer tiixsha
make sync -SkipCI -m "docs(notes): update research matrix (#26)"
make sync -WhatIf
make sync -PullOnly

:: Via direct sync.bat wrapper (root or scripts/):
.\sync.bat -m "feat(scope): descriptive message (#26)"
.\scripts\sync.bat -m "feat(scope): descriptive message (#26)"
```

### POSIX Shell Wrapper (sync.sh)
For Linux/macOS environments where PowerShell is not installed:
```bash
./scripts/sync.sh -m "feat(scope): descriptive message (#26)"
./scripts/sync.sh -PullOnly
```

### Parameter Reference & Aliases

| Parameter | Aliases | Description |
| :--- | :--- | :--- |
| `-Message` | `-m` | Custom conventional commit message. If omitted, generates an intelligent conventional commit with churn stats. |
| `-PullRequest` | `-PR`, `-pr` | Automates feature branch isolation, verification gates, remote push, and PR creation via GitHub CLI. |
| `-Issue` | | Anchors the commit and Pull Request to a tracked GitHub issue number. |
| `-Reviewer` | | Assigns peer reviewer handle(s) to the generated Pull Request. |
| `-SkipCI` | `-NoCI`, `-SkipActions` | Appends `[skip ci]` to bypass GitHub Actions runner matrices. Automatically auto-detected on operational/doc changes. |
| `-WhatIf` | `-DryRun` | Previews changes, secret scan hits, and commit messages without altering local Git index or remote branches. |
| `-PullOnly` | | Safely pulls remote updates (`--rebase --autostash`) and exits immediately. |

---

## 3. Selective CI Runner Bypass & Staged Auto-Detection

Modern `sync.ps1` scripts implement an intelligent staged file inspection engine (`Test-ShouldSkipCI`):

### How Auto-Detection Works
1. Staged changes are captured via `git diff --cached --name-only`.
2. Paths are normalized and evaluated against the operational / documentation whitelist:
   - Markdown documents: `*.md`
   - Orchestrator state and runtime entities: `orchestrator-state/**`
   - Development and diagnostic logs: `dev-logs/**`, `*.log`
   - Knowledge graph artifacts: `graphify-out/**`
   - Generated outputs and benchmark results: `outputs/**`, `benchmarks/**`
   - Worker prompts and memory trackers: `worker-prompts/**`, `*.memory-appended`
   - License and ignore files: `LICENSE`, `.gitignore`
3. If **100%** of staged files match the operational/doc criteria, `sync.ps1` automatically appends `[skip ci]` to the commit message:
   ```
   [09:42:40] CI Runner Bypass: auto-detected operational/doc-only changes. Appended [skip ci] to commit message.
   ```
4. If **any** source code, test spec, configuration, or critical script is staged (e.g. in `server/`, `client/`, `tests/`, `scripts/`), auto-detection yields to full CI execution.

---

## 4. Conflict Prevention & Hygiene Built-Ins

1. **Pre-Commit Secret Scanning Guard**:
   Scans staged diffs for AWS keys (`AKIA`), OpenAI keys (`sk-`), Anthropic keys (`sk-ant-`), GitHub PATs (`ghp_`, `github_pat_`), Google API keys (`AIza`), Slack tokens, and private key headers. Aborts and unstages if detected.
2. **Auto-Rebase Drift Guard**:
   Pulls with `git pull --rebase --autostash origin <branch>` before staging to resolve remote drift smoothly.
3. **Main-Only File Guards**:
   Files like `docs/CHANGELOG.md` or compiled report PDFs are conflict-prone across concurrent feature branches. The sync utility automatically un-stages them on feature branches to keep timestamps main-only.
4. **Forced Refspec for Mirroring**:
   Mirror synchronization uses `+refs/remotes/$originRemote/$branchName:refs/heads/$branchName` to ensure secondary remotes (`duo`, `org`) reflect exact upstream state even after rebases.

---

## 5. Root Decluttering & Evaluator Best Practices

1. **Why Evaluators Flag Root `.ps1` Scripts**:
   In collaborative, academic, and open-source project reviews (e.g. TA evaluations, capstone defenses, open-source maintainers), repositories that place platform-specific scripts (`sync.ps1`, `build.bat`) directly in the root directory appear cluttered and Windows-centric. Reviewers look for standard UNIX build conventions: a clean root containing `Makefile`, `README.md`, `LICENSE`, and standard configuration files.
2. **The Reorganized Standard**:
   - Keep the canonical POSIX `Makefile` at the repository root.
   - For Windows users without native `make`, provide `make.bat` in the root to dispatch targets (`make test`, `make lint`, `make sync`) without requiring external tool installations.
   - Relocate orchestration scripts (`sync.ps1`, `sync.bat`, `sync.sh`) into `scripts/`.
   - Maintain a lightweight root `sync.bat` shim if existing automation or developer muscle-memory expects `.\sync.bat` at root.
3. **Cross-Platform CI & Container Integration**:
   CI pipelines, containerized environments, and Linux/macOS developers can execute `make sync` or `./scripts/sync.sh` natively without needing PowerShell (`pwsh`) installed.

