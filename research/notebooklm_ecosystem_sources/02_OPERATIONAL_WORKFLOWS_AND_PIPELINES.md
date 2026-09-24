# Document 2: Operational Workflows & Autonomous Compound Pipelines

## 1. Overview of Autonomous Compound Pipelines
When individual tools in the 22-module mesh expose standardized MCP interfaces or headless CLI endpoints, complex multi-stage engineering pipelines emerge dynamically. The ecosystem formalizes six primary compound workflows:

---

## 2. The 6 Flagship Compound Pipelines

### Pipeline A: Rapid Learning & Cognitive Absorption
```
Screen Q&A (DOM Extraction)
       │
       ▼
Super-NLM (Multi-Account Cross-Notebook Grounding)
       │
       ▼
md2pdf-desktop (LaTeX Styled Synthesis Compilation)
       │
       ▼
RSVP Reader (Optimal Recognition Point Visual HUD @ 750 WPM)
```
- **Purpose**: Rapidly extracts questions or reference papers from web browsers, queries NotebookLM for cross-source synthesis, formats a high-fidelity PDF, and streams it into the RSVP high-speed reader for rapid ingestion.

### Pipeline B: Heavy Compute & Automated Model Fairness Auditing
```
Claude Worker Fleet (SKU Pipeline Decomposition)
       │
       ▼
NovaOptimizer (Win32 NT RAM Cache Purge & Process Priority Boost)
       │
       ▼
BiasAperture (Demographic Disparity & Fairness Evaluation)
       │
       ▼
Alpha-SuperApp (Mobile Telemetry & Hardware Control Dashboard)
```
- **Purpose**: Decomposes large ML evaluation jobs across the local worker fleet, triggers bare-metal memory purging (`EmptyWorkingSet`) to maximize GPU/CPU headroom, runs statistical disparity metrics, and publishes results to mobile dashboards.

### Pipeline C: Physical Hardware & CAD Prototyping
```
SPARK (Wearable Sensor Kinematics & Fall Detection Telemetry)
       │
       ▼
Fusion 360 MCP Bridge (Conversational 3D Parametric CAD Automation)
       │
       ▼
Makerspace / 3D Printing Staging (Physical Fabrication Enclosure)
       │
       ▼
md2pdf-desktop (Engineering Dossier & Clinical Explainability Report)
```
- **Purpose**: Translates edge sensor dimensions and kinematic load data from ESP32-S3 wearables into native parametric 3D CAD models inside Autodesk Fusion 360, preps 3D print assets, and generates clinical PDF dossiers with SHAP plots.

### Pipeline D: Invariant Discovery & Automated Arbitrage
```
Screen Q&A / Super-NLM (Documentation Ingestion)
       │
       ▼
Nexus (Contextual Formalizer & Spec Extraction)
       │
       ▼
AI Constraint Solver / SMT (Z3 Combinatorial & Symbolic Verification)
       │
       ▼
Executable Sandbox (Anvil / Docker Runtime Verification)
       │
       ▼
md2pdf-desktop (Verification Dossier & Counterexample Proof)
```
- **Purpose**: Automatically parses API specifications, converts natural language constraints into formal logical invariants, runs SMT solver verification, and isolates reproducible counterexamples.

### Pipeline E: Autonomous YouTube Media Ingestion & DSP Processing
```
Media Ingestion (yt-dlp-live / Downloader Scripts Hub)
       │
       ▼
Nightcore DSP Engine (Resampling, Pitch/Speed Scaling)
       │
       ▼
WhisperX ASS Karaoke Engine (Word-Level Subtitle Alignment)
       │
       ▼
Intel Arc QSV Hardware Accelerator (FFmpeg GPU Render)
       │
       ▼
yt-dlp-live Stream Relay Daemon (RTMP Broadcasting)
```
- **Purpose**: Captures audio/video streams, applies real-time DSP audio transforms, generates timed karaoke subtitles, renders video using Intel Arc hardware acceleration, and relays the stream.

### Pipeline F: Zero-Cloud P2P Device Handoff
```
Jarvis / Claude Orchestrator (Report & Asset Generation)
       │
       ▼
md2pdf-desktop (Compiled Academic PDF)
       │
       ▼
LocalSend MCP Server (mTLS Direct Wi-Fi / LAN Push)
       │
       ▼
Mobile / Tablet Device (Zero-Cloud Instant Inspection)
```
- **Purpose**: Enables immediate, private, air-gapped pushing of generated engineering reports and binaries from local desktop workstations to mobile devices without cloud intermediary storage.

---

## 3. Unified Repository Synchronization Engine (`sync.ps1`)

To prevent Git merge collisions across 25 branches and 22 repositories, direct `git add`, `git commit`, or `git push` commands are strictly forbidden. All version control is executed deterministically through `sync.ps1`:

### Core Automation Commands
- `.\sync.ps1`: Routine synchronization. Performs pre-commit secret scanning, checks branch health, detects uncommitted changes, formats branch-scoped conventional commits (e.g. `docs(spark):`, `feat(super-nlm):`), and pushes with `--rebase --autostash`.
- `.\sync.ps1 -m "feat(arch): detailed summary"`: Commits major architectural updates.
- `.\sync.ps1 -b <BranchName>`: Switches and synchronizes a specific tool branch.
- `.\sync.ps1 -AllBranches`: Synchronizes all 25 remote tracking branches in a single automated loop.
- `.\sync.ps1 -CrossSync`: Audits cross-repo synchronization across all discovered tools on disk.
- `.\sync.ps1 -CrossPull`: Safely rebases and pulls updates across clean tool repositories.
- `.\sync.ps1 -Reconcile`: Dynamically reconciles documentation counts across registry, ontology, audit, and README.
- `.\sync.ps1 -WhatIf`: Previews changes without touching Git state.

---

## 4. Zero-Token Deterministic Verification Batch Gates

Verification does not waste LLM tokens. Fast, deterministic local batch scripts ensure continuous repository validity:

| Shortcut Batch | Underlying Engine | Runtime & Target |
| :--- | :--- | :--- |
| **`.\audit.bat`** | `sim/reconciliation_engine.py` | ~50 ms (Target: 0 errors). Validates schemas, links, module counts, and contracts. |
| **`.\sim.bat`** | `sim/warehouse_mem_sim.py` | ~20 ms. Executes discrete-event queue simulation for memory subsystems. |
| **`.\archive.bat`** | `sim/transcript_archiver.py` | ~100 ms. Exports verbatim AI transcripts with ISO timestamps into `research/transcripts/`. |
| **`.\build_report.bat`** | `pdflatex / bibtex` | ~3 s. Compiles full formal research paper into `report/main.pdf`. |

---

## 5. Autonomous Multi-Agent Teamwork Orchestration (`/teamwork-preview`)

When executing complex swarm engineering tasks, the ecosystem applies the `agent-teams-orchestration` pattern:
1. **Role Division**: Scout (codebase explorer), Reviewer (adversarial auditor), Writer (implementer), Lead (synthesizer).
2. **Concurrency Isolation**: Agents work on isolated files or separate Git worktree branches (`Workspace: 'branch'`) to prevent race conditions.
3. **Bounded Stopping Criteria**: Hard budgets on iterations, time, and token thresholds prevent runaway execution loops.
4. **Epistemic Provenance**: All vetted outputs are compiled into the local Obsidian knowledge graph (`[[wikilinks]]`).
