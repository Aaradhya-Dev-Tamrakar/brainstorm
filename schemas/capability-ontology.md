# Canonical Capability & Ecosystem Ontology

```text
Artifact ID:          ONT-001-CAPABILITY-ONTOLOGY
Version:              1.0.0
Status:               CANONICAL
Principal Architect:  Aaradhya Dev Tamrakar (ADT)
Evidence Tier:        E1 — DESIGN SPECIFICATION
Reconciliation Ref:   capability-registry.yaml
```

---

## 1. Motivation & Purpose

Prior documentation in this repository conflated physical Git repositories, goal-oriented student/fellowship projects, callable computational engines, static presentation surfaces, and compound multi-tool workflows under ambiguous terms such as "13 foundational modules" or "17 ecosystem tools."

This document establishes the **authoritative taxonomy and ontological hierarchy** for the entire Aaradhya Dev Tamrakar (ADT) engineering ecosystem. All documentation, manifests, registries, and profile files MUST adhere to the definitions and boundaries established here.

---

## 2. The Canonical Hierarchy

```text
Repository (Physical Container)
    ↓
Project (Goal-Directed Engineering Effort)
    ↓
Capability (Composable, Functional Service Unit)
    ↓
Interface (Protocol Boundary & Calling Surface)
    ↓
Workflow (Multi-Capability Execution Pipeline)
```

### 2.1 Repository
* **Definition:** A distinct version-controlled Git repository, submodule, or tracking branch representing a physical unit of code storage, licensing, and CI/CD.
* **Key Invariant:** A repository is **not** automatically a capability. A repository may host zero active computational capabilities (e.g., pure documentation or asset archives like `makerspace`), or it may host multiple distinct capabilities.
* **Example:** `F:\Aaradhya-Dev-Tamrakar\brainstorm` (the central R&D repository).

### 2.2 Project
* **Definition:** A goal-directed technical initiative bounded by an engineering objective, academic milestone, or fellowship deliverable.
* **Key Invariant:** A project may produce one or more capabilities and may span across multiple repositories or physical microcontrollers.
* **Example:** `SPARK` (Smart Protection & Alerting Resilient Kit — Capstone project spanning ESP32-S3 firmware, sensor fusion, clinical explainability, and mobile telemetry).

### 2.3 Capability
* **Definition:** A modular, reusable, testable functional unit that performs a specific computational, analytical, or hardware-interfacing task with defined input/output contracts.
* **Key Invariant:** Must be headless-callable, deterministic or bounded in behavior, and verifiable against an explicit evidence tier ($E0$–$E5$).
* **Categories:**
  1. `COMPUTATIONAL_ENGINE`: Executes algorithmic processing, optimization, compilation, or simulation (e.g., `system-optimizer`, `AI-Constraint-Solver`, `BiasAperture`).
  2. `INGESTION_SENSOR`: Extracts or captures external data streams, sensor feeds, or DOM trees (e.g., `screen-qa-extension`, `yt-dlp-live`, `SPARK Kinematic Sampler`).
  3. `ORCHESTRATION_COGNITION`: Manages state decomposition, multi-model routing, or memory persistence (e.g., `super-nlm`, `Claude-Desktop Worker Fleet`, `Nexus`).
  4. `ACTUATION_HARDWARE`: Directly interacts with physical hardware, OS kernel primitives, or CAD geometry (e.g., `Autodesk-Fusion-360-MCP-Server`, `NovaOptimizer Win32 API`).
  5. `PRESENTATION_HUB`: Surfaces information to humans via interactive UI, web hosting, or academic publishing (e.g., `Aaradhya-Dev-Tamrakar.github.io`, `md2pdf-desktop`).

### 2.4 Interface
* **Definition:** The concrete communication protocol or boundary surface through which a capability is invoked.
* **Key Invariant:** A capability may expose multiple interfaces simultaneously without altering its underlying logic.
* **Canonical Protocols:**
  - `MCP (Model Context Protocol)`: FastMCP JSON-RPC over stdio/SSE for AI agents.
  - `REST / HTTP`: JSON endpoints over FastAPI or local microservices.
  - `CLI / STDIN-STDOUT`: Posix/Windows shell executables with typed arguments and JSON outputs.
  - `IPC / Win32 NT`: Direct Win32 API calls (`EmptyWorkingSet`, thread priority).
  - `BLE / ISR`: Hardware interrupt service routines and Bluetooth Low Energy GATT characteristics.

### 2.5 Workflow
* **Definition:** A compound directed acyclic graph (DAG) or execution loop that chains two or more capabilities across their respective interfaces to achieve a high-order outcome.
* **Key Invariant:** A workflow owns no persistent state of its own; it orchestrates the outputs of predecessor capabilities into the inputs of successor capabilities.
* **Example:** Pipeline A (`screen-qa-extension` $\to$ `super-nlm` $\to$ `md2pdf-desktop` $\to$ `rsvp-reading`) and Pipeline F (`Jarvis/Claude` $\to$ `md2pdf-desktop` $\to$ `localsend-mcp` $\to$ target device).

---

## 3. Authoritative Ecosystem Count Reconciliation

To eliminate counting discrepancies across `README.md`, `PROFILE.md`, and `ECOSYSTEM_ARCHITECTURAL_BRAINSTORM.md`, the following table represents the **single source of truth**:

| Ontological Dimension | Authoritative Count | Description & Scope |
| :--- | :---: | :--- |
| **Cataloged Tool Modules** | **22** | 18 Computational Engines + 4 Presentation & Educational Hubs registered in `schemas/ecosystem.registry.json`. |
| **Physical Git Repositories** | **22** | 1 Orchestration Root (`brainstorm`) + 21 local tool repositories tracked across local storage (`F:\Aaradhya-Dev-Tamrakar` and `F:\AaradhyaDT`). |
| **Git Tracking Branches in `brainstorm`** | **25** | `main` (orchestrator) + 17 branch mirrors synchronized via `sync.ps1`. |
| **Active Engineering Projects** | **18** | Concrete initiatives: SPARK, STRANGLER-IPU, BiasAperture, Super-NLM, NovaOptimizer, Fusion 360 MCP, Nexus, Claude Fleet, Alpha-SuperApp, Screen Q&A, md2pdf, yt-dlp-live, AI CSP Solver, RSVP Reader, GitHub Pilot, Nepali OCR AI, Google Classroom MCP, LocalSend MCP. |
| **Computational Capabilities** | **18** | Independent functional engines exposing programmatic APIs/CLI/MCP interfaces. |
| **Presentation & Educational Hubs** | **4** | Non-computational repositories: Portfolio Main (`Aaradhya-Dev-Tamrakar.github.io`), Portfolio Mirror (`AaradhyaDT.github.io`), KEC Makerspace digital asset hub, and IEEE React Workshop repo. |
| **Compound Workflows (Pipelines)** | **6** | Formal emergent pipelines (Pipelines A, B, C, D, E, and Pipeline F: Zero-Cloud Device Handoff). |
| **Research Experiments, Specs & RFCs** | **27** | Formal architecture specs (`ARCH-SPEC-001` to `006`), RFCs (`ARCH-RFC-001` to `006`), business plans (`ARCH-PLAN-001`), invariants (`INV-EPI-001`, `INV-MEM-001`, `INV-WSR-002`), empirical sweeps & benchmarks (`EXP-001`, `EXP-DRIVE-SYNC-001`, `EXP-FUSION360-MCP-001` (dual-server: Autodesk native + custom bridge), `EXP-CLASSROOM-MCP-001`, `EXP-LOCALSEND-MCP-001`, `FLEET-001`, `FLEET-002`, `GPU_RAM_ARCHITECTURE_SPEC`, `BMK-MEMORY-001`), and composition benchmarks (`COMPOSE-001`, `COMPOSE-002`). |

---

## 4. Verification & Governance Rules

1. **No Phantom Capabilities:** No project may claim capability status unless it implements a runnable interface (`CLI`, `REST`, `MCP`, or `Firmware`) that can be tested deterministically.
2. **Interface Isolation:** Changes to presentation layers must not break underlying computational contracts.
3. **Registry Enforcement:** All capabilities must have a corresponding entry in [`capability-registry.yaml`](capability-registry.yaml).
