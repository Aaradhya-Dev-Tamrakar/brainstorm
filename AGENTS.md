# Agent Rules & Workflow Guidelines — GitHub Pilot

Welcome, Agent. This repository (`F:\Aaradhya-Dev-Tamrakar\github-pilot`) houses **GitHub Pilot**, the macro-plane profile orchestrator, fleet health auditor, and ecosystem navigator for Aaradhya's multi-account GitHub presence (`Aaradhya-Dev-Tamrakar` and `AaradhyaDT`).

---

## 1. Core Mission & The "Token-Zero" Philosophy

While tools like GitHub Copilot operate **micro-plane** (inside individual files and repositories), GitHub Pilot operates **macro-plane** (across accounts, repositories, profiles, and public developer signals).

### Strict Token-Zero Directive
- **Never burn LLM context on mechanical operations**: Parsing paginated GitHub APIs, diffing git commits, scraping DOM nodes, and rendering SVG radars must be executed by **deterministic local Python scripts**, NOT by conversational LLM round-trips.
- **Agent Handoff**: When agents invoke `github-pilot`, scripts emit dense, pre-digested summaries (`< 1 KB`), not raw megabyte API payloads.
- **Cache-First**: All network requests to GitHub APIs or scraping targets must leverage `.cache/pilot/` with TTLs to prevent rate-limit exhaustion and unnecessary latency.

---

## 2. Git Workflow & Automation (CRITICAL — STRICT ENFORCEMENT)

To avoid breaking remote tracking, leaking secrets, or desynchronizing repository state:
**NEVER run raw `git add`, `git commit`, `git push`, or `git pull` directly.**

**ALWAYS execute `.\sync.ps1` for repository synchronization and version control.**

### Core Sync Commands
- **Routine Sync (Auto Conventional Commit & Push)**:
  ```powershell
  .\sync.ps1
  ```
- **Custom Scoped Commit**:
  ```powershell
  .\sync.ps1 -m "feat(audit): add branch protection rule verification"
  ```
- **Run Pre-Commit Tests**:
  ```powershell
  .\sync.ps1 -Test
  ```
- **Dry-Run Mode (Preview changes & secret scan)**:
  ```powershell
  .\sync.ps1 -WhatIf
  ```
- **Repository Telemetry**:
  ```powershell
  .\sync.ps1 -Status
  ```

---

## 3. CLI & Execution Commands

GitHub Pilot is driven by the Typer CLI (`pilot/cli.py`):

```powershell
# Check configuration, rate limits, and multi-account health
python -m pilot.cli status

# Deterministic fleet audit across all ecosystem repos
python -m pilot.cli audit

# Regenerate dynamic profile README and SVG stats
python -m pilot.cli profile

# Generate cross-repository conventional commit changelog
python -m pilot.cli digest --days 7

# Scrape trending topics without burning API tokens
python -m pilot.cli scrape trending --topic ai
```

---

## 4. Multi-Account & Security Governance

- **Zero-Secret Leakage**: Personal Access Tokens (PATs) and credentials reside exclusively in `.env` (or OS environment variables) and are loaded through `pilot/config.py`.
- **Pre-Commit Guard**: `sync.ps1` scans for GitHub tokens (`ghp_`, `github_pat_`), private keys, and authorization headers before staging.
- **Account Separation**: Telemetry explicitly distinguishes between primary personal namespace (`Aaradhya-Dev-Tamrakar`) and mirror/experiment namespace (`AaradhyaDT`).

---

## 5. Testing & Verification Gates

Before finalizing changes:
1. Run unit test suite:
   ```powershell
   pytest tests/
   ```
2. Verify CLI entrypoint:
   ```powershell
   python -m pilot.cli status
   ```
3. Run safe git dry-run:
   ```powershell
   .\sync.ps1 -WhatIf
   ```
