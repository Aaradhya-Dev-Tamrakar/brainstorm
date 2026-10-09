# Adaptive Workflow Routing Scenarios & Operational Walkthroughs

This document contains end-to-end walkthroughs demonstrating how `adaptive-workflow` routes, plans, verifies, and synchronizes tasks across diverse operational domains.

---

## Scenario 1: Non-Trivial Engineering Feature (Track B PR Workflow)

**User Objective**: Implement dynamic task queue with exponential backoff retries in `src/queue/engine.py`.

1. **Stage 1 (Scope)**: Classified as `ENGINEERING_DEV`, Tier 2 (Multi-Step).
2. **Stage 2 (Route)**: Routed to `github-workflow`, `feature-dev`, `systems-concurrency-harness`.
3. **Stage 3 (Plan)**:
   - Created tracked GitHub issue: `gh issue create --title "[Feature] Dynamic Task Queue" --assignee "AaradhyaDT" --label "enhancement,WP3"`.
   - Isolated branch: `feat/dynamic-queue-#42`.
4. **Stage 4 (Verify)**: Run unit tests and lint:
   ```powershell
   uv run --extra dev ruff check src/
   uv run --extra dev pytest tests/test_queue.py
   ```
5. **Stage 5 (Sync)**: Automated PR dispatch via `sync.bat`:
   ```powershell
   .\sync.bat -PR -m "feat(queue): implement dynamic queue with backoff" -Issue 42 -Reviewer tiixsha
   ```

---

## Scenario 2: Domain Hardware & Embedded Signal Pipeline

**User Objective**: Synthesize a 50Hz notch filter in Python and scaffold a non-blocking ISR circular buffer in C.

1. **Stage 1 (Scope)**: Classified as `DOMAIN_HARDWARE`, Tier 2.
2. **Stage 2 (Route)**: Routed to `dsp-signal-engine`, `embedded-firmware-scaffold`, `systems-concurrency-harness`.
3. **Stage 3 (Plan)**: WBS decomposed into filter pole-zero placement, Q15 fixed-point coefficient quantization, and atomic ISR ring buffer.
4. **Stage 4 (Verify)**: Frequency attenuation confirmed $> 40\text{ dB}$ at 50Hz. Tagged `EMPIRICALLY_VERIFIED`.
5. **Stage 5 (Sync)**: Synchronized via maintainer bridge:
   ```powershell
   .\sync.bat -m "feat(firmware): add Q15 50Hz notch filter and ISR ring buffer"
   ```

---

## Scenario 3: Academic Curriculum Scaffolding & Super-NLM Ingestion

**User Objective**: Scaffold Semester 7 Project Management course notes and sync to personal NotebookLM notebook.

1. **Stage 1 (Scope)**: Classified as `RESEARCH_ACADEMIC`, Tier 2.
2. **Stage 2 (Route)**: Routed to `academic-notebook-architect`, `super-nlm`, `google-classroom-mcp`.
3. **Stage 3 (Plan)**: Target directory `academics/semester-7/CT658/`. Target notebook: Personal Notebook (`95a79d26-2f87-42cd-8cb9-8361a1e56059`).
4. **Stage 4 (Verify)**: Syllabus coverage verified (100% units present).
5. **Stage 5 (Sync)**: Push changes with CI runner suppression:
   ```powershell
   .\sync.bat -SkipCI -m "docs(academics): scaffold semester 7 project management notes"
   ```

---

## Scenario 4: Portfolio Project Onboarding (`AaradhyaDT.github.io`)

**User Objective**: Register a new autonomous robotics research project with AES-256 encrypted access link.

1. **Stage 1 (Scope)**: Classified as `FRONTEND_PRODUCT`, Tier 2. Authoritative target: `F:\AaradhyaDT\AaradhyaDT.github.io`.
2. **Stage 2 (Route)**: Routed to `portfolio-project-manager`, `modern-web-guidance`, `design-taste-frontend`.
3. **Stage 3 (Plan)**: Allocate next sequential project ID, encrypt GitHub repository URL into `access.js`, insert card markup.
4. **Stage 4 (Verify)**: Execute portfolio verification gate:
   ```powershell
   python scripts/verify.py
   ```
   Confirmed all 26 categories pass, including Category 26 (authentic commit SHAs) and Category 22 (filter pills).
5. **Stage 5 (Sync)**: Push to canonical repository:
   ```powershell
   .\sync.bat -m "feat(portfolio): onboard autonomous robotics research build"
   ```

---

## Scenario 5: Micro Bugfix / Tier 1 Direct Execution

**User Objective**: Update regex in `scripts/parse_logs.py` to match negative numbers.

1. **Stage 1 (Scope)**: Classified as `ENGINEERING_DEV`, Tier 1 (Routine / Micro $\le 2$ files).
2. **Stage 2 (Route)**: Direct execution; no preliminary plan pause.
3. **Stage 3 (Plan)**: Formulate minimal in-place diff.
4. **Stage 4 (Verify)**: Run `pytest tests/test_parse_logs.py`. Passed 100%.
5. **Stage 5 (Sync)**: Push via maintainer bridge:
   ```powershell
   .\sync.bat -m "fix(parser): support negative numbers in log regex"
   ```

---

## Scenario 6: High-Volume Batch Task Delegated to Fleet-Orchestrator

**User Objective**: Generate 50 standardized hardware sensor test fixtures across `SPARK`.

1. **Stage 1 (Scope)**: Classified as `SWARM_ORCHESTRATION` / `BATCH_COMPUTE`. Backend selected: `FLEET_SWARM`.
2. **Stage 2 (Route)**: Routed to `fleet-orchestrator`, `references/fleet-command-architecture.md`.
3. **Stage 3 (Plan)**: Commander generates 50 task JSONs targeting `SPARK` with SKU `claude_copilot_hybrid_cycle`. Writes payloads to `F:\Aaradhya-Dev-Tamrakar\Fleet-Orchestrator\orchestrator-state\tasks/`.
4. **Stage 4 (Verify)**: Headless workers execute in isolated `.worktrees/`. 15-minute lease eviction active. Commander monitors checkpoints until all 50 report `"done"`.
5. **Stage 5 (Sync)**: Push deliverables to Google Drive:
   ```powershell
   python F:\Aaradhya-Dev-Tamrakar\Fleet-Orchestrator\scripts\sync_drive.py --push
   ```

---

## Scenario 7: Drafting an Engineering Release Dossier (`writing-like-claude`)

**User Objective**: Draft a formal model launch report with Pareto frontiers and benchmark grids.

1. **Stage 1 (Scope)**: Classified as `RESEARCH_ACADEMIC`, Tier L4 (Model Launch Dossier, 2,000–5,000 words).
2. **Stage 2 (Route)**: Routed to `writing-like-claude`, `references/calm-authority-writing.md`.
3. **Stage 3 (Plan)**: Structured with factual-state title, 1-sentence thesis, pinned benchmark comparison table, and explicit non-goals.
4. **Stage 4 (Verify)**: Audit against calm authority invariants:
   ```powershell
   python "F:\Aaradhya-Dev-Tamrakar\brainstorm\.agents\skills\writing-like-claude\scripts\audit_calm_writing.py" --tier L4 dossier.md
   ```
   Certified 0 banned marketing hype words, valid benchmark grid, and non-goals presence.
5. **Stage 5 (Sync)**: Synchronize report into repository with `-SkipCI`.

---

## Scenario 8: Autonomous Multi-Agent Swarm Orchestration

**User Objective**: Full multi-front ecosystem audit and documentation synchronization.

1. **Stage 1 (Scope)**: Macro-endeavor spanning research, code, and standards.
2. **Stage 2 (Route)**: Lead Agent computes Macro-CPM graph, identifying 3 parallel slack branches ($TS > 0$).
3. **Stage 3 (Plan)**:
   - Lead Agent dispatches 3 concurrent Domain Commanders in a single `invoke_subagent` call:
     - Commander 1 (Core Repos) $\to$ `scout_core.md`.
     - Commander 2 (Aux & AEC) $\to$ `scout_aux.md`.
     - Commander 3 (Calm Writing) $\to$ `scout_calm.md`.
   - Each Commander strictly respects the $\le 1,200$-word budget.
   - Lead Agent tracks conversation IDs in the Active Commander Ledger.
4. **Stage 4 (Verify)**:
   - Lead Agent unlocks Milestone Convergence Gate upon 3/3 completions.
   - Dispatches Adversarial Reviewer on Critical Path (`Model: "pro"`).
   - Reviewer audits physical paths, checks schema consistency, verifies epistemic badges, and runs `audit_calm_writing.py`.
5. **Stage 5 (Sync)**: Lead Agent writes final verified documents symmetrically across global and workspace repositories, certifying clean status via `.\audit.bat --fix`.

---

## Scenario 9: Cloud GPU Model Fine-Tuning & Remote Notebook Execution

**User Objective**: Fine-tune the Qwen intent router LoRA on a cloud GPU and inspect training metrics in Google Colab.

1. **Stage 1 (Scope)**: Classified as `SWARM_ORCHESTRATION` / `CLOUD_ACCELERATOR`, Tier 1C. Local headless `.ipynb` execution strictly forbidden.
2. **Stage 2 (Route)**: Routed to `colab-cloud-accelerator`, `ColabCloudAdapter`, `slm-router-forge`.
3. **Stage 3 (Plan)**:
   - Identify tracked Colab notebook: `colab_train_intent_router` (ID `1xlweNlXJ4maBCfUJVkReZLHMTWwKsYGh`), mirrored at `notebooks/slm_time_router_forge.ipynb`.
   - Ephemeral batch route: Allocate Colab VM with NVIDIA L4 GPU via `colab new -s router-forge --gpu L4`.
   - Interactive route: Use `colab-mcp` (`open_colab_browser_connection`) to inspect live training loss in the browser.
4. **Stage 4 (Verify)**:
   - Execute fine-tuning: `colab exec -s router-forge -f train_router.py`.
   - Export quantized `q4_k_m` GGUF (~397 MB) to cloud storage.
   - Enforce teardown: `colab stop -s router-forge` (`INV-COLAB-LIFECYCLE`), releasing compute units.
   - Verify health: `colab sessions` confirms 0 remaining active VMs.
5. **Stage 5 (Sync)**:
   - Push updated model metadata to `drive-manifest.json`.
   - Mount local GGUF in LM Studio on port 1234, verifying sub-50ms intent and task time allocation.
