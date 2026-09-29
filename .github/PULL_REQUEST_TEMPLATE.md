## 🎯 Quest & Contributor Information

- **Contributor:** @[github_username]
- **Fellow Profile:** `research/fellows/[github_username].md`
- **Quest ID:** `QUEST-C0-[XX]` (e.g., `QUEST-C0-00`, `QUEST-C0-01`)
- **Target Subsystem / Track:** [e.g., Memory Simulator / NISR Source Census / Devanagari Transcoding]
- **Branch:** `c0/[github_username]/[quest-id]`

---

## 📦 Deliverable Summary

Brief, technical summary of artifacts introduced or modified in this PR:
- [ ] Added / updated artifact 1: `path/to/artifact`
- [ ] Added / updated artifact 2: `path/to/artifact`

---

## 🔍 Verification & Audit Gate Checklist

Before requesting review, you **must** execute `.\audit.bat` locally and ensure all checks pass:

- [ ] **Dual-Layer Audit Passed:** Executed `.\audit.bat` (or `python sim/reconciliation_engine.py --audit-only`) with **0 discrepancies**.
- [ ] **Deterministic Reproducibility:** Verified that simulation scripts, tests, or benchmarks run without manual patching.
- [ ] **Epistemic Calibration:** Findings categorized under calibrated evidence tiers (`FORMALLY_PROVEN`, `EMPIRICALLY_VERIFIED`, `STATISTICALLY_OBSERVED`, `HEURISTIC_HYPOTHESIS`).
- [ ] **Link Integrity:** All relative markdown links and file references resolve to existing paths.
- [ ] **Git Discipline:** Clean commit messages following conventional commit formatting (`feat:`, `docs:`, `test:`).
- [ ] **Agreement Compliance:** Affirmed adherence to the [BRL Contributor Agreement](research/plans/BRL_CONTRIBUTOR_AGREEMENT.md).

---

## 📊 Verification Log Output (Snippet)

```text
Paste the terminal output of your .\audit.bat run here (showing "0 discrepancies"):

```
