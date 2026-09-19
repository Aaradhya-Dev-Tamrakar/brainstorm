# 🧠 Personal Tool Ecosystem & Jarvis R&D Laboratory

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Status: Evidence-Driven R&D](https://img.shields.io/badge/Status-Evidence--Driven%20R%26D-brightgreen)
![Ontology: 21 Modules | 17 Computational](https://img.shields.io/badge/Ontology-21%20Modules%20%7C%2017%20Computational-indigo)
![Evidence: Calibrated E0-E5](https://img.shields.io/badge/Evidence-Calibrated%20E0--E5-orange)
![Engine: sync.ps1](https://img.shields.io/badge/Engine-sync.ps1%20v2.0-cyan)

> An evidence-driven personal systems-R&D control repository and dynamic capability mesh interconnecting tools, hardware, and AI engines across `F:\AaradhyaDT`, `F:\Aaradhya-Dev-Tamrakar`, and `F:\FuseAIF2026`.

---

## 📌 Authoritative Governance & Evidence Standards

To eliminate ambiguity between what is **implemented**, what is **experimentally demonstrated**, and what is **proposed research**, this repository adheres to formal governance standards:

* 📖 **[Canonical Capability & Ecosystem Ontology](schemas/capability-ontology.md):** Formal definitions of Repository $\to$ Project $\to$ Capability $\to$ Interface $\to$ Workflow.  
  *Canonical Inventory:* **21 Tool Modules** | **17 Computational Engines** | **4 Presentation Hubs** | **6 Compound Workflows** | **19 Research Specs & Experiments**.
* 📜 **[Calibrated Evidence Policy (E0–E5)](schemas/evidence-policy.md):** Enforces evidence tiers and distinguishes formalization correctness, solver correctness, and empirical runtime correctness.
* 🗂️ **[Machine-Readable Capability Registry (YAML)](schemas/capability-registry.yaml):** Single source of truth recording inputs, outputs, interfaces, benchmarks, maintenance overhead, and evidence tiers for every ecosystem capability.
* 📋 **[Repository Epistemic Audit](report/repository-audit.md):** Granular audit classifying all major repository claims against traceable artifacts.
* 🔬 **[Quantitative Claims & Methodology Audit](report/quantitative-claims-audit.md):** Detailed register of every benchmark, sample size, hardware spec, and variance figure.
* 💰 **[Defensible Economic Model & Capital Accounting](report/economic-model.md):** Tracks direct cash expenditure, compute cost, human effort, replacement cost, and integration overhead separately; no market-value claim is made without external evidence.
* ⚙️ **Low-Cost Cognitive-Worker Baseline:** Minimizes fixed subscription commitments and measures actual marginal API/compute cost per verified task.
* ⚠️ **[Known Limitations & Failure Modes](report/limitations.md):** Transparent disclosure of technical risks, formalization gaps, benchmark dependencies, and maintenance debt.

### Required `main` branch checks

The following repository-owned checks are the merge gates for the Evidence-Backed
Ecosystem. Configure them as required status checks in GitHub branch protection or
repository rulesets after the workflows are present on the default branch:

| Repository | Required check |
|---|---|
| `super-nlm` | `pytest` |
| `Claude-Desktop` | `Python tests` |
| `Claude-Desktop` | `Lease security (adversarial)` |
| `Claude-Desktop` | `PowerShell tests` |
| `brainstorm` | `verify` |
| `AaradhyaDT.github.io` | `verify` |

Recommended policy: require pull requests, required checks to be up to date before
merge, one approving review, and no force pushes to `main`. Branch protection is a
GitHub-admin operation; the repository workflows intentionally provide the stable
check names but do not attempt to manage account-level rulesets.

---

## 🧭 Core Architecture: Capability Mesh & Decoupled Cognition

Rather than building an isolated chatbot, this repository models tools as **autonomous, headless-callable capability modules** governed by deterministic contracts:

```
┌────────────────────────────────────────────────────────────────────────────────┐
│ 1. JARVIS COGNITIVE INTERFACE                                                  │
│    Vendor-Agnostic Interface │ Orchestration Root │ Verification Supervisor    │
│    (LLM is a replaceable commodity worker, NOT the system identity)            │
└───────────────────────────────────────┬────────────────────────────────────────┘
                                        │ High-Level Intent
┌───────────────────────────────────────▼────────────────────────────────────────┐
│ 2. ORCHESTRATION & STATE LAYER                                                 │
│    Task Decomposition │ Worker Session Runtime (WSR) │ SQLite WAL Checkpointing │
│    • Invariant: "The task belongs to the orchestrator, not the worker"         │
└───────────────────────────────────────┬────────────────────────────────────────┘
                                        │ Typed Capability Contracts
┌───────────────────────────────────────▼────────────────────────────────────────┐
│ 3. CAPABILITY MESH (17 Computational Engines across 21 Modules)               │
│    • Ingestion : Screen Q&A (DOM), Super-NLM (Notebooks), Google Classroom MCP │
│    • Compute   : Fusion 360 MCP (CAD), BiasAperture (Fairness), SPARK (Edge AI)│
│    • Solvers   : AI Constraint Solver (Cryptarithmetic & CSP)                  │
│    • Actuation : NovaOptimizer (Win32 NT Tuning), LocalSend MCP (mTLS P2P LAN) │
│    • Publishing: md2pdf (LaTeX PDF), RSVP Reader (HUD), Nepali OCR AI          │
└───────────────────────────────────────┬────────────────────────────────────────┘
                                        │ Deterministic Verification & Reality
┌───────────────────────────────────────▼────────────────────────────────────────┐
│ 4. DETERMINISTIC VERIFICATION LAYER (The Ground Truth)                         │
│    SMT / Z3 Solvers │ Executable Sandboxes │ Win32 NT APIs │ Automated Lints   │
└────────────────────────────────────────────────────────────────────────────────┘
```

### ⚡ Emergent Compound Workflows
When autonomous modules are chained via MCP and Semantic Contracts, new workflows emerge dynamically:
- **Pipeline A (Rapid Learning):** `Screen Q&A` $\to$ `Super-NLM` $\to$ `md2pdf-desktop` $\to$ `RSVP Reader` (750 WPM synthesis).
- **Pipeline B (Heavy Compute/Audit):** `Claude Fleet` $\to$ `NovaOptimizer` (RAM purge/priority) $\to$ `BiasAperture` $\to$ `Alpha-SuperApp`.
- **Pipeline C (Physical Hardware Prototyping):** `SPARK` $\to$ `Fusion 360 MCP` (parametric CAD) $\to$ `md2pdf-desktop` (engineering dossier).
- **Pipeline D (Invariant & Arbitrage Discovery):** `Screen Q&A / Super-NLM` $\to$ `Nexus` (formalizer) $\to$ `AI Solver / SMT` $\to$ `Z3 Sandbox` $\to$ `md2pdf-desktop`.
- **Pipeline E (Autonomous YouTube Media Cluster):** `Media Ingestion` $\to$ `Nightcore DSP Engine` $\to$ `WhisperX ASS Karaoke` $\to$ `Intel Arc QSV Render` $\to$ `yt-dlp-live Relay`.
- **Pipeline F (Zero-Cloud Device Handoff):** `Jarvis / Claude` $\to$ `md2pdf-desktop` (compiled report) $\to$ `localsend-mcp` (mTLS Wi-Fi push to phone/tablet).

---

## 🎯 Flagship Research Wedge: Headless Invariant Assurance Engine

To avoid the "grand unified platform" trap, the ecosystem anchors its near-term research around a single high-leverage wedge: **Software, API & Protocol Invariant Assurance**.

```text
Natural-Language Specification / API Documentation
                    ↓
Formalization into Typed Capability Contract (E1)
                    ↓
Candidate Invariant Formulation
                    ↓
SMT Symbolic Verification (Z3 Solver)
                    ↓
Executable Sandbox Verification (Docker / Anvil)
                    ↓
Reproducible Counterexample or Evidence Dossier (E4/E5)
```

* **Target Domain:** Software state machines, REST/FastAPI endpoints, and deterministic protocol rules.
* **Core Metric:** **Discovery Cost Efficiency** ($(\text{financial} + \text{compute cost}) / \text{verified discoveries}$) with **100% recall enforced on planted synthetic violations**.

---

## 🗓️ Near-Term R&D Roadmap

Rather than expanding the ecosystem by inventing new projects, the immediate engineering sequence focuses on **evidence, reliability, and integration**:

1. **Canonical Registry & Ontological Hardening:** Maintain single source of truth across all tools (`schemas/capability-registry.yaml`). *(Completed)*
2. **Comprehensive Epistemic Audit:** Audit all numbers, evidence tiers, and citations (`report/`). *(Completed)*
3. **Economic Model Correction:** Decouple living expenses from productive CAPEX/OPEX and vectorize resource tracking. *(Completed)*
4. **Invariant Assurance Engine MVP:** Build synthetic state machine invariant generator and Z3 verification loop. *(Months 0–3)*
5. **Reproducibility Benchmark Suite:** Containerize simulation models (`sim/`) with deterministic seeds and test assertions. *(Months 1–3)*
6. **2-Capability Composition Test:** Formally measure synergy between `Super-NLM` and `md2pdf-desktop`. *(Months 2–4)*
7. **3-Capability Composition Test:** Chain `Screen Q&A` $\to$ `Super-NLM` $\to$ `RSVP Reader` with end-to-end telemetry. *(Months 4–6)*
8. **Worker Session Runtime (WSR) Abstraction:** Standardize the task checkpointing harness for zero-loss profile migration. *(Months 6–9)*
9. **Jarvis Executive Interface:** Assemble the vendor-agnostic high-level interface over the verified capability mesh. *(Months 9–12)*

---

## 🗂️ Authoritative Ecosystem Catalog

The ecosystem encompasses **21 tool modules** cataloged in `schemas/ecosystem.registry.json` and synchronized via tracking branches in `brainstorm` (17 active computational engines + 4 presentation/educational hubs + 1 orchestration root):

> 📖 **Machine-Readable Registry:** [`schemas/capability-registry.yaml`](schemas/capability-registry.yaml) | [`schemas/ecosystem.registry.json`](schemas/ecosystem.registry.json)  
> 📜 **Ontology Standard:** [`schemas/capability-ontology.md`](schemas/capability-ontology.md)

| # | Dedicated Branch | Tool / Module | Category | Execution Context | Evidence Tier | Core Superpower |
|---|---|---|---|---|:---:|---|
| 1 | `super-nlm` | **Super-NLM Hub** | Orchestration | Cloud / Hybrid | **E3** | Multi-account Google NotebookLM aggregator, cross-notebook synthesis, token ring agent rotation |
| 2 | `Autodesk-Fusion-360-MCP-Server` | **Fusion 360 MCP Bridge** | Actuation | Local Desktop | **E3** | Conversational 3D CAD, zero-dependency parametric modeling automation via native Python Add-In |
| 3 | `system-optimizer` | **NovaOptimizer** | Computation | Local (Bare Metal) | **E4** | Micro-footprint Windows OS tuning, deep RAM purge (`EmptyWorkingSet`), thread priority boosting |
| 4 | `SPARK` | **SPARK Wearable Gateway** | Computation | Edge Hardware | **E4** | Two-layer edge fall detection, sensor kinematics, SHAP clinical explainability, automated PDF reporting |
| 5 | `Nexus` | **Nexus** | Orchestration | Local / Hybrid | **E3** | Project-centric AI workspace, prompt multiplexing across parallel LLMs, contextual note memory |
| 6 | `Claude-Desktop` | **Claude Worker Fleet (v2)** | Orchestration | Local / Distributed| **E3** | Multi-profile session persistence, distributed DAG task worker fleet, SKU pipeline decomposition |
| 7 | `BiasAperture` | **BiasAperture** | Computation | Local / Compute | **E4** | Demographic bias auditing framework for vision models, disparity metrics, automated LaTeX/PDF generation |
| 8 | `Alpha-SuperApp` | **Alpha-SuperApp** | Computation | Mobile Device | **E2** | Mobile super-app: Computer Vision, BLE hardware control, Personal Finance, AI assistants |
| 9 | `screen-qa-extension` | **Screen Q&A** | Ingestion | Ambient Browser | **E3** | Ambient browser intelligence, instant question extraction and zero-click overlay response |
| 10 | `md2pdf-desktop` | **md2pdf-desktop & MCP** | Publishing | Local Desktop / Fleet MCP | **E3** | Publication-quality Markdown-to-PDF rendering pipeline with LaTeX math, callouts, and FastMCP server |
| 11 | `yt-dlp-live` | **yt-dlp-live** | Ingestion | Local Daemon | **E3** | Resilient live stream capture daemon, auto-cut, and lossless remuxing/relaying |
| 12 | `AI` | **AI Constraint Solver** | Computation | Local Microservice | **E3** | Cryptarithmetic and combinatorial constraint satisfaction solver with JSON metrics reporting |
| 13 | `rsvp-reading` | **RSVP Reader** | Presentation | Local Web | **E3** | High-speed RSVP reader with Optimal Recognition Point (ORP) highlighting for EPUB/PDF |
| 14 | `Aaradhya-Dev-Tamrakar.github.io` | **Portfolio Website** | Presentation | Web Hub | **E4** | Central portfolio, interactive radar, and project presentation engine |
| 15 | `AaradhyaDT.github.io` | **Portfolio Mirror** | Presentation | Mirror Web | **E4** | Secondary public mirror and documentation host |
| 16 | `makerspace` | **Makerspace** | Presentation | Hardware Hub | **E2** | Physical maker laboratory, fabrication assets, and 3D printing staging |
| 17 | `react-workshop-ieeekecktm` | **React Workshop** | Presentation | Educational | **E3** | Hands-on curriculum and modern frontend architecture reference |
| 18 | `github-pilot` | **GitHub Pilot** | Computation | Local / Fleet CLI | **E3** | Autonomous macro-plane GitHub profile, fleet health auditor, and ecosystem navigator |
| 19 | `nepali-ocr-ai` | **Nepali OCR AI** | Computation | Local / Microservice | **E3** | Nepali vision OCR, Varnavinyas grammar engine, Preeti-Unicode transcoder, and Word docx repair |
| 20 | `google-classroom-mcp` | **Google Classroom MCP** | Ingestion / Actuation | Local Desktop / Fleet MCP | **E3** | Direct Google Classroom integration for courses, coursework, assignments, announcements, and submissions |
| 21 | `localsend-mcp` | **LocalSend MCP Server** | Ingestion / Actuation | Local Desktop / Fleet MCP | **E3** | Zero-cloud local P2P file, text, and clipboard transfer across LAN/Wi-Fi devices with mutual TLS |

---

## ⚡ Unified Synchronization Engine (`sync.ps1`)

The repository includes a PowerShell automation engine designed specifically for multi-branch ecosystem operations:

```powershell
# 1. Routine sync on active branch (pulls, stages, verifies secrets, auto-commits & pushes)
.\sync.ps1

# 2. Switch and sync a specific tool branch
.\sync.ps1 -b SPARK
.\sync.ps1 -Branch super-nlm -m "docs(super-nlm): document multi-account session rotation"

# 3. Synchronize all repository branches with GitHub origin in a single command
.\sync.ps1 -AllBranches

# 4. Audit brainstorm branch status across all local tool repositories on disk
.\sync.ps1 -SyncToolRepos

# 5. Provision a new tool branch in brainstorm and configure its local repo
.\sync.ps1 -NewTool "NovaVision"

# 6. Dry run preview (verifies secret scanner & inspects commit message without changes)
.\sync.ps1 -WhatIf

# 7. View full ecosystem telemetry dashboard
.\sync.ps1 -Status
```

### 🛠️ Zero-Token Architectural & Audit Shortcuts (`.bat`)

| Batch Shortcut | Underlying Engine | Purpose | Execution Cost |
| :--- | :--- | :--- | :--- |
| **`.\audit.bat`** | `sim/reconciliation_engine.py` | Lints entire repo for broken links, missing metadata, and taxonomy drift | **0 Tokens** (~50 ms) |
| **`.\archive.bat`** | `sim/transcript_archiver.py` | Detects significant architectural sessions and exports verbatim logs | **0 Tokens** (~100 ms) |
| **`.\sim.bat`** | `sim/warehouse_mem_sim.py` | Runs GPU-DRAM warehouse discrete event channel simulator | **0 Tokens** (~20 ms) |
| **`.\build_report.bat`** | `pdflatex / bibtex` | Compiles print-ready LaTeX research technical report (`report/main.pdf`) | **0 Tokens** (~3 sec) |

---

## 📄 License

This repository is licensed under the [MIT License](LICENSE).  
Copyright © 2026 Aaradhya Dev Tamrakar. All rights reserved.