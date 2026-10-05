# 📋 BRL Engineering Handoff: Automated PR Workflow & Ecosystem Sync (`sync.ps1`)

```text
Document ID:          NOTE-2026-10-05-PR-AUTOMATION-HANDOFF
Date & Timestamp:     2026-10-05T08:10:00+05:45
Author:               Aaradhya Dev Tamrakar (Principal Architect)
Context:              Central Orchestration Root (F:\Aaradhya-Dev-Tamrakar\brainstorm)
Governing Decisions:  DEC-003, DEC-003-A (Main Branch Enforcement Alignment), github-workflow skill
Target Deliverables:  sync.ps1 automated -PR workflow, BRL cohort governance scaffolding, branch lifecycle management
```

---

## 1. Context & Architectural Rationale

### The Problem
During recent ecosystem commits (`2ddac71`), the Git push to `origin/main` emitted:
```text
remote: Bypassed rule violations for refs/heads/main:
remote: - Required status check "verify" is expected.
```
While this bypass is technically authorized under **`DEC-003-A`** for the solo maintainer (because local `audit.bat` verifies 100% of invariants before pushing), Aaradhya established a foundational governance principle for **BRL (Brainstorm Research Lab)**:

> **"Auto-merge is also a bypass when I am working alone. For now all my personal workflows that are anti-BRL will be personal bypasses, till I fix my cohort members and train them to use these. Slow but sure beats fast bugs."**

### Strategic Objectives for the Next Session
1. **Scaffold the BRL Automated PR Workflow** into `sync.ps1` and `sync.bat` via a `-PR` / `-PullRequest` flag.
2. **Automate Branch Derivation**: Eliminate the friction of manually inventing and cleaning up branch names.
3. **Bridge Phase 1 and Phase 2 Governance**:
   - **Phase 1 (Founder Velocity — Now)**: Routine direct push via `sync.bat` remains functional for quick maintenance.
   - **Phase 2 (BRL Team Standard — Implemented)**: `sync.bat -PR` enforces branch isolation, local verification, remote branch push, and structured PR dispatch via GitHub CLI (`gh pr create`).

---

## 2. Technical State of the Repository

- **Active Branch**: `main` (clean working tree, fully synced with `origin/main` at commit `2ddac71`).
- **Verified Checks**: `scripts/verify.py` and `audit.bat` pass with **0 discrepancies across 303 documentation and schema files**, 26/26 unit tests pass, and 12/12 Z3 SMT invariant benchmarks hold.
- **GitHub CLI (`gh`)**: Installed and authenticated as `AaradhyaDT` with full `repo` and `workflow` scopes.
- **GitHub Ruleset**: `Evidence-Backed-Ecosystem-main` (ruleset id `23533023`) enforces:
  - `deletion` (blocks branch deletion)
  - `non_fast_forward` (blocks force pushes)
  - `required_status_checks: verify` (runs `.github/workflows/verification.yml`)
  - `bypass_actors`: RepositoryRole (`actor_id: 5`, bypass_mode: `always`).

---

## 3. Detailed Specifications for `sync.ps1` Updates

The next session must implement the following capabilities in `sync.ps1` and `sync.bat`:

### A. New Parameters in `sync.ps1`
```powershell
[Alias("pr")]
[switch]$PullRequest,

[string]$Issue,              # Optional: Links to a tracked GitHub issue number (e.g. -Issue 42)
[string]$Reviewer,           # Optional: Assigns peer reviewer handle for BRL team workflow
```

### B. Automated Branch Slug Derivation (`Get-FeatureBranchSlug`)
A helper function that converts the conventional commit message into a standardized branch name:
- Input: `feat(p2p): campus swarm marketplace` $\rightarrow$ Output: `feat/p2p-campus-swarm-marketplace`
- Input: `fix(aria2): resolve local path detection` $\rightarrow$ Output: `fix/aria2-resolve-local-path-detection`
- Input: With `-Issue 42`: $\rightarrow$ `feat/p2p-campus-swarm-marketplace-#42`

### C. The `-PR` Execution Flow
When `-PR` (or `-PullRequest`) is passed:
1. **Branch Checkout**:
   - If on `main`: checks out the derived branch (`git checkout -b $featureBranch`).
   - If already on a feature branch: proceeds on that branch.
2. **Deterministic Pre-Commit Gate**:
   - Executes `Find-StagedSecrets` (secret scanner).
   - Executes dynamic reconciliation (`sim/reconciliation_engine.py --fix`).
   - Runs `audit.bat` (structural + behavioral test suites).
   - Updates Graphify knowledge graph (`graphify update .`).
3. **Commit**:
   - `git commit -m "$Message"`
4. **Push Feature Branch**:
   - `git push -u origin $featureBranch`
5. **Pull Request Dispatch via `gh` CLI**:
   - Checks if a PR already exists for `$featureBranch`.
   - If not, runs:
     ```powershell
     gh pr create --base main --head $featureBranch --title "$Message" --body "$prBody"
     ```
   - If `-Reviewer <handle>` is provided, sets `--reviewer $Reviewer`.
   - If `-Issue <ID>` is provided, appends `Closes #<ID>` to the PR body.
6. **Post-Dispatch Hygiene**:
   - Prints the PR URL and review status.
   - Provides option to switch back to `main` (`git checkout main`).

---

## 4. Key Files to Modify in the Next Session

1. **`sync.ps1`**: Add `-PR`, `-Issue`, `-Reviewer` parameters, slug derivation, and `gh pr create` orchestration.
2. **`sync.bat`**: Ensure `-PR` and associated arguments pass through to PowerShell.
3. **`scripts/README.md`**: Document the `-PR` workflow under the script catalog.
4. **`AGENTS.md`**: Update Section 1 & 6 to document the dual-track execution model (Maintainer Local Gate vs. BRL Cohort `-PR` Workflow).

---

## 5. Ready-to-Paste Prompt for the Next Chat

Copy and paste the exact prompt below into the new session:

```markdown
We are implementing the automated Pull Request workflow (-PR switch) in sync.ps1 and sync.bat for the brainstorm repository, based on the architectural handoff document:
`research/notes/2026-10-05_BRL_AUTOMATED_PR_WORKFLOW_AND_SYNC_HANDOFF.md`

### Context & Philosophy:
1. Solo-maintainer direct pushes via .\sync.bat with the maintainer bypass are currently active (DEC-003-A), but serve strictly as a founder-velocity bridge.
2. We are now building the institutional governance for BRL (Brainstorm Research Lab) so that incoming cohort members follow a strict, automated GitHub Flow (Branch -> Local Verification Gate -> Remote Push -> PR -> Remote Clean-Room CI -> Peer Review -> Merge).
3. Do not use fake auto-merges: PRs must be created cleanly via `gh pr create`, linked to issues when provided, and left ready for peer review.

### Tasks to Execute:
1. Update `sync.ps1` to support `-PR` (alias `-pr`), `-Issue <id>`, and `-Reviewer <handle>`.
2. Add automated branch slug derivation from conventional commit messages (`feat/...`, `fix/...`, `docs/...`).
3. Implement the branch creation, push, and `gh pr create` flow with full metadata.
4. Ensure `sync.bat` transparently forwards the `-PR` flag.
5. Update `scripts/README.md` and `AGENTS.md` to document the BRL automated PR workflow.
6. Run `scripts/verify.py` and `audit.bat` to certify zero discrepancies.

Please review `research/notes/2026-10-05_BRL_AUTOMATED_PR_WORKFLOW_AND_SYNC_HANDOFF.md` and proceed with implementation.
```
