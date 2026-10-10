# Baseline Lock & Historical Provenance

This document records the architectural baseline lock, historical provenance, and governance invariants for the Adaptive Workflow meta-orchestrator (`adaptive-workflow`).

---

## 1. Provenance & Version Lifecycle

- **Origin Baseline**: `v3.5.0-adaptive-workflow` (Initial meta-orchestrator specification).
- **Prior Calibration**: `v3.9.0-calibrated` (Fleet Master Brain 3B/7B Dual-Model Hierarchy, Antigravity 504-Conversation Trajectory Harvester, Agent-Reflex Autonomous Self-Healing, and Tool-Speculator Prefetching).
- **Current Calibration**: `v3.10.0-calibrated` (AI Engineering Fellowship SOTA Reference Integration, 8-Archetype Matrix, and `INV-RESOLVE-FUSE` Local-First / GitHub Fallback Gateway).
- **Date of Inception**: 2026-10-09 (Official Day of Creation of the Adaptive Workflow meta-orchestrator).
- **Architectural Scope**: Central meta-orchestration root for Aaradhya's personal ecosystem across **28 tool modules** (24 computational engines and 4 presentation hubs) across **32 Git tracking branches**.
- **Execution Fleet**: $W = 27$ pooled GitHub Copilot worker accounts, Copilot Headless REST, Claude CDP, Colab Cloud GPU/TPU Accelerator (A100/L4), Fleet Master Brain (3B & 7B GGUF), and AI Engineering Fellowship reference cluster managed via `Fleet-Orchestrator`.

---

## 2. Invariant Registry

The adaptive workflow engine guarantees deterministic execution through fifteen non-negotiable architectural invariants:

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

7. **`INV-COLAB-LIFECYCLE`**:
   All Colab cloud execution tasks must execute non-interactively without TTY prompts, tear down rented VMs upon completion (`colab stop` in finally handler or `runtime.unassign()`), and uphold the Jupyter Notebook Invariant (zero local headless `.ipynb` execution).

8. **`INV-AUDIT-ORDER`**:
   Deterministic verification sequence enforced before every commit:
   1. Unittest discovery (`python -m unittest discover -s sim -p "test_*.py"`)
   2. Knowledge graph update (`graphify update .`)
   3. Document reconciliation (`python sim/reconciliation_engine.py --fix`)
   4. Staged zero-leak checks (`git grep --untracked "file:///" tools/skills/adaptive-workflow/`)
   5. SKILL.md budget check ($\le 8,192\text{ bytes}$)
   6. Full structural & behavioral audit (`.\audit.bat`, target: 0 errors)

9. **`INV-AGENT-REFLEX`**:
   Autonomous error recovery loop. Non-zero tool exit codes and tracebacks are intercepted by Agent-Reflex (Fleet Master Brain 3B/7B on port 1234) to synthesize corrective tool actions without consuming primary context.

10. **`INV-SPECULATIVE-PREFETCH`**:
    Incoming development requests predict upcoming action DAG sequences via Tool-Speculator, prefetching target files and warming execution runtimes in parallel.

11. **`INV-DUAL-BRAIN`**:
    Local SLM execution separates tasks between the 3B Daily Driver (1.8 GB for routing, reflex, speculation, and duration budgeting) and 7B Powerhouse (4.36 GB for deep refactoring, test repair, and invariant audits).

12. **`INV-RESUMABLE-RETRIEVAL`**:
    All cloud model pulls from Google Drive use `python -m gdown --continue` to automatically bypass large-file virus-scan redirects and resume interrupted chunks safely.

13. **`INV-COLAB-TEARDOWN`**:
    Autonomous cloud training notebooks conclude with `from google.colab import runtime; runtime.unassign()` to release expensive GPU/TPU VMs immediately upon artifact persistence.

14. **`INV-FIFO-ENQUEUE`**:
    Appending or modifying notebook cells during active cloud training is safe due to Jupyter's FIFO execution queue, preserving in-flight CUDA states.

15. **`INV-RESOLVE-FUSE`**:
    Local-First with GitHub Remote Fallback. All AI/ML engineering code lookups inspect local repository paths (`F:\FuseAIF2026\M{X}\WK{Y}`) first for 0ms latency offline execution; if unmounted (cloud VMs, Colab), resolve to the authenticated GitHub repository link (`https://github.com/AaradhyaDT/fuseAiF_*`).

---

## 3. Style & Tone Standards

In accordance with the Anthropic Calm Authority engineering voice:
- All speculative rhetoric, fantasy metaphors, and role-playing terms are strictly deprecated and eliminated.
- All diagrams and documentation use plain-text structural labels with zero emojis or decorative unicode glyphs.
- Hyperlinks use clean relative repository paths.
