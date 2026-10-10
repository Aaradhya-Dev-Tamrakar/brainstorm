# Workstation Installed Applications & Operational Tooling Catalog

This catalog documents the workstation runtime environment, software tools, and domain utilities available on Aaradhya's workstation, mapping them to `/adaptive-workflow` tiers, domain archetypes, and execution boundaries.

---

## 1. Workstation Host Runtime & Baseline Environment

- **Host Architecture**: Intel Core Ultra 7 155H (16 physical cores, 22 logical threads), 16 GB physical RAM.
- **Steady State Headroom**: 11.0–12.0 GB free RAM under NovaOptimizer (`Run-Optimization.bat`).
- **Core Interpreters**:
  - Python `3.12.10` & `3.14.7` (managed via `uv`).
  - Node.js & Deno (MCP servers, web sidecars, and tooling).
  - PowerShell 7 (`pwsh`) & native Win32 `ctypes`.
- **Navigation & Environment**:
  - `zoxide`: Sub-millisecond directory jumping across ecosystem modules.
  - NVM for Windows: Node version management without global path pollution.

---

## 2. Adaptive Workflow Ecosystem Integration (Tiers 0 – 1E)

| Tier / Subsystem | Software Tool | Canonical Version / Role | Execution Mechanism | Primary Responsibility in Ecosystem |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 0** | **Python & `uv`** | `3.12.10` / `3.14.7` | Native process (<20 ms) | Solves mathematical CPM DAGs (`adaptive_orchestrator.py`), reconciles registries (`reconciliation_engine.py`), executes `pytest`. |
| **Tier 0** | **Git & GitHub CLI** | `git` / `gh` | Native CLI | Manages ephemeral worktrees (`.worktrees/<task_id>`), repo multi-sync (`sync.bat`), and institutional PRs (`gh pr create`). |
| **Tier 0** | **Fast Directory Navigation** | `zoxide` | Shell hook | High-speed directory switching across 28 modules and satellite workspaces. |
| **Tier 1A / 1B** | **LM Studio** | `v0.4.21+2` | Port 1234 REST/SSE | Hosts local GGUF models (`qwen-router`, `fleet-master-3b`, `fleet-master-7b`) for <50 ms intent triage and Agent-Reflex self-healing. |
| **Tier 1A / 1B** | **Ollama** | `v0.33.1` | Headless CLI / Daemon | Standalone fallback runtime for quantized small language model execution. |
| **Tier 1C** | **Copilot CLI** | `copilot.exe` (GitHub) | Headless Subprocess | Drives 27 pooled worker accounts (`worker_1`..`worker_27`) under `~/.copilot-workers/` inside isolated git worktrees. |
| **Tier 1C** | **Docker Desktop & WSL** | Windows Subsystem for Linux | Containerized runtime | Sandboxed service isolation, Unix CLI environments, and container tests. |
| **Tier 1C** | **Eclipse Mosquitto** | MQTT Broker | Micro-broker daemon | Lightweight telemetry distribution, inter-process signaling, and fleet message passing. |
| **Tier 1E** | **Google Chrome & Brave** | Chromium / CDP | Headless CDP / Browser | Google Colab GPU/TPU execution (`colab-cloud-accelerator`), Google Drive sync, and CDP problem/solution harvesting. |
| **Tier 1E** | **LocalSend** | `v1.18.2` | P2P Wi-Fi transfer | Zero-cloud LAN distribution of model weights, datasets, and generated artifacts to mobile/tablet devices. |
| **Documentation** | **TeXstudio & Pandoc** | `Pandoc 3.11` / LaTeX | Local CLI / GUI | Multi-pass compilation of formal research dossiers (`report/main.pdf`), engineering reports, and Beamer defense decks. |
| **Documentation** | **`wkhtmltox`** | Blink rendering engine | CLI converter | Dual-format HTML-to-PDF rendering for fairness audits and compliance reports (`compliance-report-harmonizer`). |
| **Documentation** | **Typora & Obsidian** | Desktop Knowledge Base | Native Markdown / Obsidian | Offline Markdown knowledge graph navigation with `[[wikilinks]]` and epistemic provenance tracking. |

---

## 3. Professional Domain Applications & Capabilities

These installed professional tools operate alongside the agent mesh and provide specialized capabilities for hardware engineering, mathematical modeling, and production tasks:

### 1. Electronics, RF & Mechanical Hardware Design (`DOMAIN_HARDWARE` / `DOMAIN_AEC_CAD`)
- **Keysight Advanced Design System (ADS 2022) & EEsof**: High-frequency RF, microwave planar EM simulation, and MMIC circuit design (`rf-link-budget-calc`).
- **SimNEC 5.1**: Antenna radiation pattern modeling, transmission line matching, and RF Smith chart impedance calculations.
- **Autodesk Fusion**: Conversational 3D CAD/CAM parametric design (`fusion360-mcp`), mechanical enclosure fit checks, and 3D print slicing.
- **xTool Creative Space (`v2.7.22`)**: Laser cutting/engraving vector toolpaths for physical acrylic and wood enclosure fabrication.
- **MATLAB R2018b**: High-level matrix computation, control system loop modeling (`control-systems-sim`), and DSP filter simulation.

### 2. Software Development, Logic & Automation (`ENGINEERING_DEV` / `SYSADMIN_SECURITY`)
- **Android Studio**: Android mobile development, Kotlin Compose, and embedded hardware HAL integration (`Alpha-SuperApp`).
- **Microsoft Visual Studio Code**: Polyglot editor for manual inspection, ad-hoc edits, and extension debugging.
- **SWI-Prolog**: Declarative knowledge-base querying, formal first-order logic reasoning, and constraint logic programming.
- **AutoHotkey**: Desktop keyboard shortcuts, macro automation, and Windows input automation.

### 3. Enterprise Office, Scheduling & Documents (`RESEARCH_ACADEMIC` / `SWARM_ORCHESTRATION`)
- **Microsoft Office Professional Plus 2019** (Word, Excel, PowerPoint): Formal business reporting, financial models, and presentation slide decks.
- **Microsoft Project Professional 2019**: Traditional Waterfall Gantt scheduling, critical path tracking, and enterprise resource leveling (`pm-workflow-orchestrator`).
- **Microsoft Visio Professional 2019**: Formal systems architecture schematics, network topology diagrams, and process flowcharts.
- **PDFgear & PDF Architect 10 (with OCR Module)**: High-precision PDF manipulation, page assembly, and document text OCR extraction.

### 4. Media & Creative Production
- **Blender 5.2**: 3D spatial modeling, technical animation, photorealistic product rendering, and visual assets.
- **Audacity 3.7.8**: Multi-track audio editing, waveform filtering, and vocal noise suppression for podcast/video assets.
- **HandBrake 1.11.2**: Hardware-accelerated batch video transcoding and compression for demonstration walkthroughs.
- **FFmpeg (Essentials Build)**: CLI-driven media conversion, audio extraction, video slicing, and stream manipulation.
- **Canva**: Visual graphics design, poster layout, and fast presentation styling.

### 5. High-Throughput Transfer, Networking & Remote Access
- **JDownloader 2, XDM, & qBittorrent**: Multi-threaded download acceleration and distributed dataset pulling.
- **KDE Connect**: Local network cross-device sync (shared clipboard, notification forwarding, phone-laptop file transfers).
- **Chrome Remote Desktop & Host**: Encrypted remote access to workstation from external mobile devices.

### 6. System Utility & Machine Maintenance (`SYSADMIN_SECURITY`)
- **PowerToys**: FancyZones window tiling, system color picker, image resizer, and Markdown preview handlers.
- **Revo Uninstaller Pro 5.5.2**: Deep registry and residual file uninstaller for maintaining a pristine workstation state.
- **Winaero Tweaker**: OS telemetry tuning, context menu customization, and performance tweaks.
- **WinRAR (`v7.23`)**: Multi-format archive extraction and compression (`.rar`, `.7z`, `.tar.gz`, `.zip`).
