# Tier L1 Worked Examples: Portfolio Manifest & Pull Request

This file contains two reference implementations of **Tier L1 (Micro — 100–300 words)** demonstrating zero-fluff, active-verb technical precision.

---

## Example 1: Portfolio Project Manifest (`portfolio-project-manager`)

This manifest is formatted for ingestion by `scripts/add_project.py` on `AaradhyaDT.github.io`:

```json
{
  "title": "Windows Pilot — Semantic UIA & MCP Desktop Automation Engine",
  "repo_url": "https://github.com/AaradhyaDT/windows-pilot",
  "category": ["apps", "hardware"],
  "status": "Sep 2026",
  "bullets": [
    "Controls native Windows 11 desktop applications via Microsoft UI Automation COM interfaces.",
    "Exposes headless screen perception and silent window capture through a native MCP server.",
    "Executes UI test scripts with resolution-independent element bounding boxes in under 200ms."
  ],
  "tags": ["Python 3.10+", "Win32 API", "MCP Server", "Windows 11"],
  "section": "personal",
  "tier": "vip"
}
```

---

## Example 2: GitHub Pull Request Description (`github-workflow`)

```markdown
## Summary
Enforces sample suppression for demographic cohorts where $n < 30$ in the fairness compliance pipeline to prevent false disparity signals.

## Changes
- Add sample size validation check in `fairness_audit.py`.
- Suppress point estimates for cohorts below 30 samples and assign `.badge-guard` CSS classes.
- Move insufficient sample groups into collapsible `<details>` blocks in exported HTML reports.

## Test Proof
All 26 behavioral tests and 12 SMT invariants passed cleanly:
```bash
pytest tests/test_sample_suppression.py -v
# 26 passed in 1.42s
```

## Non-Goals
This change does not generate synthetic data or impute missing demographic features.
```
