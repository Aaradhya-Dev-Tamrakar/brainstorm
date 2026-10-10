# Standardized Cross-Tool Ecosystem Pipelines

This document specifies the eight canonical cross-repository execution pipelines connecting computational engines, presentation hubs, and utility tools across Aaradhya's ecosystem.

---

## Pipeline 1: Fleet Batch Swarm to Google Drive & NotebookLM

Connects high-throughput autonomous batch generation to living Google Drive manifests and NotebookLM knowledge bases.

```mermaid
flowchart LR
    Task["Lead Agent / Commander\nDecomposes SKU Batch"] --> Queue["Fleet-Orchestrator\n(orchestrator-state/tasks/)"]
    Queue --> Pool["27x Copilot Workers\n(.worktrees/<task_id>)"]
    Pool --> Checkpoints["orchestrator-state/checkpoints/"]
    Checkpoints --> DriveSync["scripts/sync_drive.py --push"]
    DriveSync --> Drive["Google Drive Workspace"]
    Drive --> NLM["super-nlm\n(NotebookLM Ingestion)"]
```

### Protocol:
1. Commander constructs declarative task JSON matching `claude_copilot_hybrid_cycle.json` or `iv_ii_course_study_pack.json`.
2. Headless workers claim atomic leases, execute inside ephemeral `.worktrees/<task_id>`, and commit changes to task branches.
3. Upon checkpoint completion, execute `python scripts/sync_drive.py --push` to update cloud drive files while preserving Google Drive `fileId` references.
4. Call `super-nlm.sync_notebooks` to trigger NotebookLM source indexing.

---

## Pipeline 2: Academic & Coursework Knowledge Pipeline

Bridges university curriculum management, assignment tracking, and multimedia study downloads.

```mermaid
flowchart LR
    Classroom["google-classroom-mcp\n(Fetch assignments & notes)"] --> Architect["academic-notebook-architect\n(Scaffold IOE curriculum)"]
    Architect --> NLM["super-nlm\n(Generate mind maps & audio)"]
    NLM --> Downloader["super-nlm-downloads\n(Download Studio artifacts)"]
    Downloader --> LocalSend["localsend-mcp\n(P2P transfer to mobile/tablet)"]
```

### Protocol:
1. Query active assignments via `classroom.list_coursework`.
2. Scaffold semester directory using `academic-notebook-architect` (e.g. `academics/semester-7/`).
3. Sync notes to subject notebook via `super-nlm.query_notebook` or Drive sync.
4. Download generated audio overviews and mind maps using `super-nlm-downloads`.
5. Dispatch files to mobile devices over local Wi-Fi using `localsend-mcp`.

---

## Pipeline 3: Edge AI, Demographics & Calm Publishing

Bridges edge sensor models, demographic bias auditing, publication-grade PDF compilation, and portfolio onboarding.

```mermaid
flowchart LR
    EdgeModel["SPARK\n(Edge sensor kinematics)"] --> BiasAudit["BiasAperture\n(Demographic parity audit)"]
    BiasAudit --> PDF["md2pdf-desktop\n(FastMCP / LaTeX render)"]
    PDF --> Writing["writing-like-claude\n(Tier L4 report / L1 blurb)"]
    Writing --> Portfolio["portfolio-project-manager\n(AaradhyaDT.github.io)"]
```

### Protocol:
1. Generate classification logs or predictions in `SPARK` (`F:\Aaradhya-Dev-Tamrakar\SPARK`).
2. Audit statistical parity and disparate impact in `BiasAperture` (`pytest src/tests/`).
3. Compile technical audit dossier to PDF using `md2pdf-desktop` (`python test_md2pdf.py`).
4. Audit prose against calm authority standards using `audit_calm_writing.py --tier L4`.
5. Onboard project to `F:\AaradhyaDT\AaradhyaDT.github.io` with token-zero link encryption using `portfolio-project-manager`.

---

## Pipeline 4: Windows Host Security & Optimization

Coordinates digital forensics artifact hunting, kernel-level NTFS privacy locks, and OS tuning.

```mermaid
flowchart LR
    DFIR["Cyber-Forensics\n(Stealth evasion hunt)"] --> Vault["Win-Vault\n(Kernel NTFS ACL lock)"]
    Vault --> Optimizer["system-optimizer\n(NovaOptimizer RAM purge)"]
```

### Protocol:
1. Scan suspect folders for Alternate Data Streams (ADS) and CLSID masquerades:
   `pwsh F:\Aaradhya-Dev-Tamrakar\Cyber-Forensics\tests\test_evasion_hunter.ps1`.
2. Secure sensitive research data or credentials via kernel-level NTFS access denial:
   `.\Vault.bat` in `Win-Vault`.
3. Purge standby memory caches (`EmptyWorkingSet`) and boost foreground thread priorities:
   `.\Run.bat` in `system-optimizer`.

---

## Pipeline 5: Conversational CAD & Physical Fabrication

Bridges physical maker staging, conversational 3D CAD modeling, and parametric slicing.

```mermaid
flowchart LR
    Makerspace["makerspace\n(Hardware specs & 3D assets)"] --> FusionBridge["fusion360-mcp\n(Conversational CAD API)"]
    FusionBridge --> Viewport["Autodesk Fusion 360\n(Native Add-In viewport)"]
    Viewport --> Slicer["3D Print Slicing Staging"]
```

### Protocol:
1. Read hardware mechanical envelope from `F:\Aaradhya-Dev-Tamrakar\makerspace`.
2. Execute conversational CAD primitives via `fusion360-mcp` (e.g. `create_box`, `create_cylinder`, `extrude_sketch`).
3. Verify viewport rendering and export STL/STEP to fabrication staging.

---

## Pipeline 6: Ecosystem Cross-Sync & Invariant Reconciliation

Executes automated synchronization, inventory accounting, and regression verification across all repositories.

```mermaid
flowchart LR
    Root["brainstorm\n(Central Mesh Root)"] --> CrossSync[".\\sync.bat -CrossSync\n(Audit tool git health)"]
    CrossSync --> CrossPull[".\\sync.bat -CrossPull\n(Rebase clean tool repos)"]
    CrossPull --> Reconcile[".\\sync.bat -Reconcile\n(Synchronize registry counts)"]
    Reconcile --> AuditGate[".\\audit.bat\n(Certify 0 invariant errors)"]
```

### Protocol:
1. From `F:\Aaradhya-Dev-Tamrakar\brainstorm`, execute `.\sync.bat -CrossSync` to audit branch statuses across discovered repositories.
2. Execute `.\sync.bat -CrossPull` to safely rebase clean sibling repositories.
3. Run `.\sync.bat -Reconcile` to auto-synchronize counts across `ecosystem.registry.json` and documentation.
4. Execute `.\audit.bat` to certify 0 invariant errors across all 27 tool modules.

---

## Pipeline 7: Cloud GPU Acceleration, SLM Fine-Tuning & Edge Intent Routing

Connects transcript dataset harvesting, remote GPU fine-tuning in Google Colab, quantized INT4 GGUF cloud streaming, and local sub-50ms intent and time allocation routing.

```mermaid
flowchart LR
    Datasets["Task Datasets &\nSession Transcripts"] --> ColabGPU["colab-cloud-accelerator\n(Colab Pro L4 / Unsloth LoRA)"]
    ColabGPU --> GGUF["Quantized INT4 GGUF\n(qwen_intent_router_q4_k_m)"]
    GGUF --> Drive["Google Drive Sync\n(scripts/sync_drive.py --push)"]
    Drive --> LMStudio["LM Studio Port 1234\n(<50ms Socket Ping)"]
    LMStudio --> Adaptive["adaptive-workflow\n(Fast Intent Triage & Time Allocation)"]
```

### Protocol:
1. Harvest task datasets using `Fleet-Orchestrator/tests/test_harvest_task_time_dataset.py`.
2. Offload LoRA fine-tuning to Colab L4 GPU via `colab run` or `ColabCloudAdapter` using `notebooks/slm_time_router_forge.ipynb` (synced at `colab_train_intent_router`, Drive ID `1xlweNlXJ4maBCfUJVkReZLHMTWwKsYGh`).
3. Export quantized INT4 GGUF model and push to Google Drive via `scripts/upload_large_model_to_drive.py`.
4. Mount locally into LM Studio on port 1234 (`models/qwen_intent_router_q4_k_m.gguf`).
5. Route incoming tasks with sub-50ms latency and dynamic task time allocation.

---

## Pipeline 8: AI Fellowship Curriculum & Golden Reference Architecture Pipeline

Bridges incoming AI/ML engineering requirements with instructor-grade golden blueprints, local repository code (`F:\FuseAIF2026`), Google Colab GPU accelerators, and fairness compliance audits.

```mermaid
flowchart LR
    Task["AI/ML Engineering Task"] --> AIE["ai-engineering-fellowship\n(INV-RESOLVE-FUSE Protocol)"]
    AIE --> Codebase{"Local-First Probe\nF:\\FuseAIF2026\\M*\\WK*?"}
    Codebase -- "Present" --> LocalCode["Inspect & Reuse Local Code\n(0 latency, offline)"]
    Codebase -- "Unmounted" --> GHCode["GitHub Fallback Clone\n(AaradhyaDT/fuseAiF_wk*)"]
    LocalCode --> ColabRun["colab-cloud-accelerator\n(Train on L4/A100 VM)"]
    GHCode --> ColabRun
    ColabRun --> Compliance["BiasAperture / compliance-report-harmonizer\n(Fairness & Disparate Impact Audit)"]
    Compliance --> Delivery["Production Delivery & sync.bat"]
```

### Protocol:
1. When `/adaptive-workflow` triages an `AI_ENGINEERING_ML` task, invoke `ai-engineering-fellowship` to look up relevant week dossiers (`references/weeks/wk*.md`) and SOTA best practices.
2. Resolve code via `INV-RESOLVE-FUSE`: check local path `F:\FuseAIF2026\M{X}\WK{Y}` first; fall back to GitHub remote (`AaradhyaDT/fuseAiF_wk*`) if unmounted.
3. If heavy GPU training is required, offload execution to `colab-cloud-accelerator` (A100/L4 GPU) with automated `runtime.unassign()` teardown.
4. If auditing model fairness or demographic bias, route metrics through `BiasAperture` and format with `compliance-report-harmonizer`.
5. Stage and deliver verified changes via `.\sync.bat`.


