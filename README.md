# 🧠 Personal Tool Ecosystem & Jarvis Brainstorm

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Status: Living Architecture](https://img.shields.io/badge/Status-Living%20Architecture-brightgreen)
![Modules: 18 Branches](https://img.shields.io/badge/Modules-18%20Branches-indigo)
![Engine: sync.ps1](https://img.shields.io/badge/Engine-sync.ps1%20v2.0-cyan)

> A unified architectural blueprint and dynamic capability mesh interconnecting tools, hardware, and AI engines across `F:\AaradhyaDT`, `F:\Aaradhya-Dev-Tamrakar`, and `F:\FuseAIF2026`.

---

## 📌 Primary Architectural Blueprint

The complete architectural log, module specifications, and compound workflow designs are documented in:

👉 **[ECOSYSTEM_ARCHITECTURAL_BRAINSTORM.md](ECOSYSTEM_ARCHITECTURAL_BRAINSTORM.md)**

---

## 🧭 Core Concept: The Composable Capability Mesh

Rather than treating projects as isolated applications, this brainstorm models every tool as an **autonomous capability module** spanning **Local**, **Cloud**, and **Hybrid** execution environments.

Connected through standardized protocols (**Model Context Protocol / MCP**, local HTTP endpoints, or CLI manifests), these independent modules combine into a **Personal Jarvis** that moves beyond chat to sensory perception and physical/OS actuation.

```
                             ┌────────────────────────┐
                             │     JARVIS CORTEX      │
                             │   (Nexus / Agent Core) │
                             └───────────┬────────────┘
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 ▼                                               ▼
     ┌────────────────────────┐                     ┌────────────────────────┐
     │   SENSORY ORGANS       │                     │    EXECUTIVE ACTUATORS │
     │   (How Jarvis Sees)    │                     │    (Jarvis's Hands)    │
     ├────────────────────────┤                     ├────────────────────────┤
     │ • Screen Q&A (Browser) │                     │ • NovaOptimizer (OS)   │
     │ • SPARK (Hardware/BLE) │                     │ • Fusion 360 (3D CAD)  │
     │ • yt-dlp-live (Media)  │                     │ • md2pdf (Publishing)  │
     │ • Alpha-SuperApp (Cam) │                     │ • Claude Fleet (Agents)│
     └────────────────────────┘                     └────────────────────────┘
                 │                                               │
                 └───────────────────────┬───────────────────────┘
                                         ▼
                             ┌────────────────────────┐
                             │     DEEP MEMORY        │
                             │  (What Jarvis Remembers│
                             ├────────────────────────┤
                             │ • Super-NLM (Notebooks)│
                             │ • Nexus (Projects/FTS5)│
                             │ • RSVP Reader (Buffer) │
                             └────────────────────────┘
```

### ⚡ Emergent Compound Workflows
When autonomous modules are chained via MCP and Semantic Contracts, new workflows emerge dynamically:
- **Pipeline A (Rapid Learning):** `Screen Q&A` $\rightarrow$ `Super-NLM` $\rightarrow$ `md2pdf` $\rightarrow$ `RSVP Reader` (750 WPM synthesis).
- **Pipeline B (Heavy Compute/Audit):** `Claude Fleet` $\rightarrow$ `NovaOptimizer` (RAM purge/priority) $\rightarrow$ `BiasAperture` $\rightarrow$ `Alpha-SuperApp`.
- **Pipeline C (Physical Hardware Prototyping):** `SPARK` $\rightarrow$ `Fusion 360 MCP` (parametric CAD) $\rightarrow$ `md2pdf` (engineering dossier).
- **Pipeline D (Invariant & Arbitrage Discovery):** `Screen Q&A / Super-NLM` $\rightarrow$ `Nexus` (formalizer) $\rightarrow$ `Claude Fleet / AI Solver` $\rightarrow$ `Z3 SMT Sandbox` $\rightarrow$ `md2pdf`.

---

## 🗂️ Ecosystem Branches & Module Catalog

Every tool in the ecosystem has a corresponding tracking branch in this repository for module-specific brainstorm logs, manifests, and interface prototypes:

| # | Dedicated Branch | Tool / Module | Tech Stack | Execution Context | Core Superpower |
|---|---|---|---|---|---|
| 1 | `super-nlm` | **Super-NLM Hub** | Python (FastAPI), React, MCP | Cloud / Hybrid | Multi-account Google NotebookLM aggregator, cross-notebook synthesis, MCP round-robin agent rotation |
| 2 | `Autodesk-Fusion-360-MCP-Server` | **Autodesk Fusion 360 MCP** | Python, Fusion 360 API, MCP | Local Desktop | Conversational 3D CAD, parametric modeling automation via AI / MCP |
| 3 | `system-optimizer` | **NovaOptimizer** | C# .NET 10, WPF, Win32/NT APIs | Local (Bare Metal) | Micro-footprint Windows OS tuning, deep RAM cache purge (`EmptyWorkingSet`), process priority boosting |
| 4 | `SPARK` | **SPARK Wearable Gateway** | C/C++ (ESP32-S3), Python, SHAP, BLE | Edge Hardware / Local | Two-layer edge fall detection, sensor kinematics, SHAP clinical explainability, automated PDF reporting |
| 5 | `Nexus` | **Nexus** | FastAPI, React (Vite), SQLite FTS5 | Local / Hybrid | Project-centric AI workspace, prompt multiplexing across parallel LLMs, contextual note memory |
| 6 | `Claude-Desktop` | **Claude Worker Fleet (v2)** | FastAPI coordinator, SQLite WAL, PowerShell | Local / Distributed | Multi-profile session persistence, distributed DAG task worker fleet, SKU pipeline decomposition |
| 7 | `BiasAperture` | **BiasAperture** | PyTorch, Python CLI, LaTeX | Local / Compute | Demographic bias auditing framework for vision models, disparity metrics, automated LaTeX/PDF generation |
| 8 | `Alpha-SuperApp` | **Alpha-SuperApp** | Kotlin 2.2, Jetpack Compose, Android 16 | Mobile Device | Mobile super-app: Computer Vision, BLE hardware control, Personal Finance, AI assistants |
| 9 | `screen-qa-extension` | **Screen Q&A** | Chrome MV3 (JS), Gemini Flash | Ambient Browser | Ambient browser intelligence, instant question extraction and zero-click overlay response |
| 10 | `md2pdf-desktop` | **md2pdf-desktop** | Python, Tkinter, Pandoc, wkhtmltopdf | Local Desktop | Publication-quality Markdown-to-PDF rendering pipeline |
| 11 | `yt-dlp-live` | **yt-dlp-live** | PowerShell, yt-dlp, FFmpeg | Local Daemon | Resilient live stream capture daemon, auto-cut, and lossless remuxing/relaying |
| 12 | `AI` | **AI Constraint Solver** | Python, FastAPI, CLI | Local Microservice | Cryptarithmetic and combinatorial constraint satisfaction solver with JSON metrics reporting |
| 13 | `rsvp-reading` | **RSVP Reader** | Svelte, Vite | Local Web | High-speed RSVP reader with Optimal Recognition Point (ORP) highlighting for EPUB/PDF |
| 14 | `Aaradhya-Dev-Tamrakar.github.io` | **Portfolio Website** | Static Web, Vanilla JS, CSS | Web Hub | Central portfolio, interactive radar, and project presentation engine |
| 15 | `AaradhyaDT.github.io` | **Portfolio Mirror** | Static Web | Mirror Web | Secondary public mirror and documentation host |
| 16 | `makerspace` | **Makerspace** | CAD / Hardware Assets | Hardware Hub | Physical maker laboratory, fabrication assets, and 3D printing staging |
| 17 | `react-workshop-ieeekecktm` | **React Workshop** | React, TypeScript, Vite | Educational | Hands-on curriculum and modern frontend architecture reference |

---

## ⚡ Unified Synchronization Engine (`sync.ps1`)

The repository includes a PowerShell automation engine designed specifically for multi-branch ecosystem operations:

```powershell
# 1. Routine sync on active branch (pulls, stages, verifies secrets, auto-commits & pushes)
.\sync.ps1

# 2. Switch and sync a specific tool branch
.\sync.ps1 -b SPARK
.\sync.ps1 -Branch super-nlm -m "docs(super-nlm): document multi-account session rotation"

# 3. Synchronize all 18 tool branches with GitHub origin in a single command
.\sync.ps1 -AllBranches

# 4. Audit brainstorm branch status across all 17 local repositories on disk
.\sync.ps1 -SyncToolRepos

# 5. Provision a new tool branch in brainstorm and configure its local repo
.\sync.ps1 -NewTool "NovaVision"

# 6. Dry run preview (verifies secret scanner & inspects commit message without changes)
.\sync.ps1 -WhatIf

# 7. View full ecosystem telemetry dashboard
.\sync.ps1 -Status
```

### Safety Features
- **Staged Secret Scanner Guard**: Scans diffs for accidentally staged API keys (OpenAI, Anthropic, Google/Gemini, GitHub, AWS, Slack, private keys) and halts execution before any commit is made.
- **Dynamic Branch-Aware Commits**: Generates scoped conventional commits automatically (e.g. `docs(spark): ...`, `feat(super-nlm): ...`, `docs(ecosystem): ...`).
- **Autostash Rebase Recovery**: Pulls using `--rebase --autostash` and retries pushes automatically if remote history has diverged.

---

## 📄 License

This repository is licensed under the [MIT License](LICENSE).  
Copyright © 2026 Aaradhya Dev Tamrakar. All rights reserved.