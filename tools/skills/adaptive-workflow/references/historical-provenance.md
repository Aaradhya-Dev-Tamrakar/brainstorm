# Baseline Lock & Historical Provenance

This document records the architectural baseline lock, historical provenance, and governance invariants for the Adaptive Workflow meta-orchestrator (`adaptive-workflow`).

---

## 1. Provenance & Version Lifecycle

- **Origin Baseline**: `v3.5.0-adaptive-workflow` (Initial meta-orchestrator specification).
- **Current Calibration**: `v3.7.0-calibrated` (Zero-AI deterministic engine, Anthropic Calm Authority, bounded mathematical scheduling).
- **Date of Inception**: 2026-10-09 (Official Day of Creation of the Adaptive Workflow meta-orchestrator).
- **Architectural Scope**: Central meta-orchestration root for Aaradhya's personal ecosystem across **28 tool modules** (24 computational engines and 4 presentation hubs) across **32 Git tracking branches**.
- **Execution Fleet**: $W = 27$ pooled GitHub Copilot worker accounts managed via `Fleet-Orchestrator`.

---

## 2. Invariant Registry

The adaptive workflow engine guarantees deterministic execution through seven non-negotiable architectural invariants:

1. **`INV-FAST-PATH`**:
   Routine development mechanics (`audit.bat`, `sync.bat`, formatters, linters, unittests, simulation runs, git status) execute natively via pure Python and shell commands in <20 ms with 0 AI tokens and <10 MB RAM.

2. **`INV-CTX-FIREBREAK`**:
   Primary session context remains pristine (<5k tokens). High-volume batch workloads delegate to an ephemeral child subagent (`Role: 'Fleet Commander'`, `TypeName: 'self'`) that returns strictly a <300 word executive manifest.

3. **`INV-FLEET-FIRST`**:
   All non-trivial implementation tasks default to the 27 pooled Copilot workers in `Fleet-Orchestrator`, maximizing utilization of the 5,400 monthly credits ($0 out-of-pocket).

4. **`INV-CPM-SOLVER`**:
   Topological DAG dependencies, early/late times ($ES, EF, LS, LF$), and total/free slacks ($TS, FS$) are calculated via exact topological sorting in pure Python with zero prompt arithmetic.

5. **`INV-FENCE-TOKEN`**:
   Monotonic integer fencing tokens are maintained per task and verified during branch integration to prevent split-brain writes from evicted or stale workers.

6. **`INV-PRE-EXIST-GUARD`**:
   Worktree projections resolve the canonical Git common directory and back up any pre-existing files before projection, ensuring clean restoration upon teardown.

7. **`INV-AUDIT-ORDER`**:
   Deterministic verification sequence enforced before every commit:
   1. Unittest discovery (`python -m unittest discover -s sim -p "test_*.py"`)
   2. Graph update (`graphify update .`)
   3. Document reconciliation (`python sim/reconciliation_engine.py --fix`)
   4. Staged zero-leak checks (`git grep --untracked "file:///" tools/skills/adaptive-workflow/`)
   5. SKILL.md budget check ($\le 8,192\text{ bytes}$)
   6. Full structural & behavioral audit (`.\audit.bat`, target: 0 errors)

---

## 3. Style & Tone Standards

In accordance with the Anthropic Calm Authority engineering voice:
- All speculative rhetoric, fantasy metaphors, and role-playing terms are strictly deprecated and eliminated.
- All diagrams and documentation use plain-text structural labels with zero emojis or decorative unicode glyphs.
- Hyperlinks use clean relative repository paths.
