# Agent Rules & Workflow Guidelines — Brainstorm & Ecosystem Orchestration

Welcome, Agent. This repository (`F:\Aaradhya-Dev-Tamrakar\brainstorm`) serves as the **central architectural brain, R&D incubator, and capability mesh root** for Aaradhya's personal tool ecosystem across 23 tool modules (19 computational engines, 4 presentation hubs) and 26 Git tracking branches.

To preserve repository integrity, avoid merge collisions, eliminate hallucinated claims, and maintain zero-drift deterministic verification, you **MUST** strictly adhere to the following operating principles.

---

## 1. Git Workflow & Ecosystem Automation (CRITICAL — STRICT ENFORCEMENT)

To avoid breaking multi-branch tracking and prevent wasteful multi-step Git commands, **NEVER run individual `git add`, `git commit`, `git push`, or `git pull` commands directly.**

**ALWAYS execute `.\sync.ps1` for repository synchronization and version control.**

### Core Commands

- **Routine / Active Branch Sync**:
  ```powershell
  .\sync.ps1
  ```
  _Automatically runs pre-commit secret scans, checks branch health, detects uncommitted changes, formats branch-scoped conventional commits (e.g., `docs(spark):`, `feat(super-nlm):`), and pushes with `--rebase --autostash` safety._

- **Major Features / Architectural Changes**:
  ```powershell
  .\sync.ps1 -m "feat(arch): detailed architectural commit summary"
  ```

- **Switch & Sync Tool Branch**:
  ```powershell
  .\sync.ps1 -b SPARK
  ```

- **Sync All Ecosystem Branches**:
  ```powershell
  .\sync.ps1 -AllBranches
  ```

- **Cross-Repository Tool Health Check**:
  ```powershell
  .\sync.ps1 -SyncToolRepos
  ```

- **Dynamic Ecosystem Cross-Sync (Status & Pull)**:
  ```powershell
  .\sync.ps1 -CrossSync                   # Audit cross-repo synchronization across all discovered tools
  .\sync.ps1 -CrossPull                   # Safely rebase and pull updates across clean tool repos
  ```

- **Dynamic Invariant & Documentation Auto-Reconciliation**:
  ```powershell
  .\sync.ps1 -Reconcile                   # Dynamically reconcile counts across registry, ontology, audit & README
  ```

- **Safe Pull Only**:
  ```powershell
  .\sync.ps1 -PullOnly
  ```

- **Dry-Run Mode (Preview changes without touching Git state)**:
  ```powershell
  .\sync.ps1 -WhatIf
  ```

---

## 2. Knowledge Graph & Codebase Navigation (Graphify)

This repository maintains an active **Graphify Knowledge Graph** under `graphify-out/` representing all 23 interconnected modules, RFCs, capability contracts, simulation engines, and research logs.

- **Map First**: Read `graphify-out/GRAPH_REPORT.md` (and inspect God Nodes / Surprising Connections) **before** deep-diving into raw files.
- **Relationship Queries**: Prefer graph traversal commands over blind file reads or brute-force grep:
  ```powershell
  graphify query "<question>"             # Broad BFS traversal
  graphify query "<question>" --dfs       # Deep causal trace
  graphify path "<ConceptA>" "<ConceptB>" # Shortest dependency path
  graphify explain "<NodeName>"           # Plain-language node context
  ```
- **Graph Updates**: Whenever you modify architectural specifications, RFCs, simulation scripts, or schemas, update the knowledge graph:
  ```powershell
  graphify update .
  ```

---

## 3. Epistemic Governance & Evidence Tiers (ARCH-RFC-001 & ARCH-RFC-002)

To maintain absolute epistemic honesty and prevent speculative AI claims from polluting repository ground truth:

1. **Calibrated Evidence Tiers (`ARCH-RFC-001`)**:
   Every finding, metric, or spec statement must be categorized:
   - `FORMALLY_PROVEN`: Mathematically verified via SMT/Z3 solvers or deductive formal logic.
   - `EMPIRICALLY_VERIFIED`: Confirmed via executed deterministic scripts in `sim/` with reproducible parameters.
   - `STATISTICALLY_OBSERVED`: Supported by experimental benchmark runs with confidence intervals.
   - `HEURISTIC_HYPOTHESIS`: Unverified architectural design, conceptual intuition, or working assumption.

2. **The Multi-Model Cognitive Council (`ARCH-RFC-002`)**:
   Frontier models are commodities with distinct inductive biases. Delegate tasks according to natural comparative advantage:
   - **ChatGPT Think (`o1`/`o3-mini`)**: The Adversarial Skeptic & Reviewer (dismantling unearned claims, literature sanity).
   - **Claude (`Sonnet`/`Opus`)**: The Systems & Code Craftsman (clean architectural layers, idiomatic implementations).
   - **Perplexity (`Sonar`/`Pro`)**: The Empirical Grounder (live arXiv citations, 2025/2026 conference tracking).
   - **Grok (`xAI`)**: The First-Principles Provocateur (contrarian stress-testing, physics boundary checks).
   - **Gemini / Antigravity**: The Synthesizer & Living Repository (large-context orchestration, Git execution, tool coordination).

3. **Verbatim Epistemic History Invariant (`INV-EPI-001`)**:
   Never discard or lossy-compress foundational architectural dialogues, peer reviews, or strategic pivots. Significant conversations must be exported verbatim with ISO timestamps into [`research/transcripts/`](research/transcripts/).

4. **The Three-Output Rule**:
   To avoid recursive planning loops, every brainstorming or engineering session must terminate in at least one of:
   - An Experiment Log (`research/experiments/INV-xxx.md` or `EXP-xxx.md`)
   - An Executable Implementation Artifact (`sim/*.py`, code, or formal schema)
   - A Falsifiable Claim / Hypothesis Card (`research/hypotheses/HYP-xxx.yaml`)

---

## 4. Verification Gates & Reality Layer (Deterministic Ground Truth)

Speculative text is never ground truth; deterministic execution is. Before finalizing changes:

1. **Zero-Discrepancy Audit Gate**:
   ```powershell
   .\audit.bat                             # Verify structural consistency and simulation tests (Target: 0 errors)
   .\audit.bat --fix                       # Automatically reconcile physical research counts across docs
   ```
   _Executes `sim/reconciliation_engine.py`. Verifies schema validity, cross-branch consistency, inventory counts, and contract integrity across all 23 modules. Target: 0 errors._

2. **Simulation Sanity Check**:
   ```powershell
   .\sim.bat
   ```
   _Executes `sim/warehouse_mem_sim.py` (discrete-event queue simulation) to ensure numerical simulations run without regressions._

3. **Technical Report Compilation**:
   ```powershell
   .\build_report.bat
   ```
   _Compiles the formal LaTeX research dossier into `report/main.pdf`._

---

## 5. Operational Rules & Efficiency

- **Zero-Waste Execution**: Be concise, rigorous, and dive straight to work. Avoid conversational filler.
- **The Task Belongs to the Orchestrator, Not the Worker**: As established in the Worker Session Runtime (`FLEET-001`), workers are ephemeral execution agents; task state, memory checkpoints, and invariants remain permanently externalized in the repository.
- **Contract Adherence**: Any new capability module or tool must provide a contract matching [`schemas/capability.contract.v1.json`](schemas/capability.contract.v1.json) and be cataloged in [`schemas/ecosystem.registry.json`](schemas/ecosystem.registry.json).
- **Autonomous Swarms & Teamwork (`/teamwork-preview`)**: Whenever the `/teamwork-preview` slash command, `teamwork_preview` subagent, or any multi-agent swarm is invoked, the agent **MUST automatically activate and apply the `agent-teams-orchestration` skill** (`C:\Users\Aaradhya\.gemini\config\skills\agent-teams-orchestration\SKILL.md`). All teamwork prompt drafting (`prompt_draft.md`) must strictly enforce Scout-Reviewer-Writer-Lead role separation, file/branch concurrency isolation, bounded stopping criteria, and Obsidian knowledge graph compilation.
