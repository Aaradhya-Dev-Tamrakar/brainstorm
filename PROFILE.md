# Engineering Profile & Technical Dossier: Aaradhya Dev Tamrakar (ADT)

```text
Artifact ID:          PROF-001-ENGINEERING-PROFILE
Version:              2.0.0 (Evidence-Grounded Edition)
Status:               CANONICAL
Principal Architect:  Aaradhya Dev Tamrakar (ADT)
Evidence Tier:        E1 — SPECIFICATION
Verification Ref:     schemas/evidence-policy.md, schemas/capability-registry.yaml
```

---

## 1. Engineering Identity

**Aaradhya Dev Tamrakar (ADT)** is an undergraduate systems and embedded engineer focusing on the boundary between **hardware-software co-design, near-memory computer architecture, embedded Edge AI, and deterministic verification**.

Rather than treating software development as rapid application scripting, ADT approaches engineering through an **evidence-driven systems paradigm**: specifying formal interface contracts, tracking hardware-level bottlenecks (memory walls, bus contention, interrupt latencies), and deploying zero-token deterministic verification gates to eliminate abstraction drift.

---

## 2. Current Academic & Professional Snapshot

* **Degree & Affiliation:** Bachelor of Engineering (B.E.) in Electronics, Communication & Information Engineering (ECIE / BEI) at **Kathmandu Engineering College (KEC), Institute of Engineering (IOE), Tribhuvan University**, Nepal.
* **Academic Standing:** Year IV / Part II (8th & Final Semester). Expected Graduation: **January 2027**.
* **Primary Elective Track:** Aeronautical Telecommunications (CNS/ATM, ICAO navigation standards, radar/ATC communications).
* **Competitive Fellowships:**
  - **Fuse AI Fellow (2026):** 14-week competitive fellowship in deep learning, statistical modeling, and agentic workflows (Fusemachines).
  - **NSSR DataCamp Fellow (Cohort 2):** Competitive track in Applied AI, PostgreSQL engineering, and statistical data analysis (Nepalese Society of Student Researchers).
* **Institutional Leadership:**
  - **Vice Chair — IEEE KEC KTM Student Branch (2026 – Present)**
  - **Event Manager — Electronics Project Club (EPC), KEC**
  - **Makerspace Ambassador — KEC Maker's Space**

---

## 3. Demonstrated Engineering Domains vs. Research Exposure

To maintain epistemic honesty, technical proficiencies are categorized by demonstrated evidence level:

### I. Demonstrated Engineering Competence (Evidence Tiers E3 – E4)
* **Embedded Firmware & Microcontroller Inference (C / C++ / ESP-IDF):** Direct register/driver programming on ESP32-S3 and MPU-6050 with microsecond ISR threshold gating; deployment of INT8 quantized models via TensorFlow Lite Micro.
* **Algorithmic Fairness Auditing (Python / PyTorch / Fairlearn / AIF360):** Evaluated demographic disparity metrics (DIR, EOD, EOP) across 126 intersectional bins with chi-squared significance testing and BCa bootstrap confidence intervals.
* **Discrete-Event Systems Simulation (Python / SimPy):** Modeled multi-queue memory contention, Poisson packet bursts, and CXL pooled bus interfaces.
* **Bare-Metal OS & Memory Tuning (C# .NET 10 / Win32 NT APIs):** Direct P/Invoke integration with Windows NT memory management APIs (`EmptyWorkingSet`, thread priority scheduling).
* **Deterministic Repository Verification & Tooling:** Automated multi-category static verification suites enforcing link integrity, JSON schema validation, and cryptographic asset verification.

### II. Research Exposure & Active Exploration (Evidence Tiers E1 – E2)
* **Near-Memory Computer Architecture & Bump-in-the-Wire Accelerators:** Microarchitectural modeling of front-end Ingress Processing Units (IPUs) designed to absorb 6G burst line-rate ingest (simulated in SimPy; not physical silicon).
* **Formal Verification & Neurosymbolic Invariants:** Exploring SMT-LIB constraints and Z3 theorem provers for automated API state machine assurance.
* **Agentic Orchestration & Distributed Cognition:** Designing runtime task managers that decouple task state from worker sessions (`FLEET-001`).

---

## 4. Systems Philosophy

1. **Deterministic Verification over Fragile Abstraction:** If code cannot be verified deterministically via unit tests, SMT solvers, or hardware scope captures, it remains a hypothesis, not an engineering asset.
2. **Hardware Realism:** Abstractions must account for physical hardware limits—DRAM latency, memory bus saturation, cache line fills, and interrupt latency jitter.
3. **Epistemic Transparency:** Explicitly state what is implemented, what is simulated, and what is hypothesized. Proving the wrong formalization with mathematical rigor is still an error.
4. **The Three-Output Invariant:** Every architectural brainstorm or research cycle must terminate in at least one of: (1) a reproducible experiment (`INV-xxx`), (2) an executable implementation artifact, or (3) a falsifiable hypothesis card (`HYP-xxx`).

---

## 5. Selected Projects

### Project 1: SPARK (Smart Protection & Alerting Resilient Kit)
* **Purpose:** Two-layer wearable fall detection system providing real-time local alerts and clinician-legible explainability without cloud telemetry dependency.
* **Role:** Lead AI & Firmware Architect (BEI Major Capstone Project).
* **Status:** `IMPLEMENTED` & `EXPERIMENTALLY VERIFIED` (Evidence Tier E4).
* **Evidence:** 44-page thesis proposal; 56 passing CTest/Unity unit tests; functional ESP32-S3 + MPU-6050 prototype; FastAPI clinical dashboard.
* **Benchmark:** **18.5 KB INT8 CNN**, **0.9185 AUC-ROC** on SisFall dataset (38,420 temporal windows, zero-leakage subject-grouped cross-validation).
* **Limitations:** Tested primarily on public benchmark data; real-world motion artifacts (dropping device, running) require further ambient false-positive calibration.

### Project 2: STRANGLER-IPU / SIPU-6G
* **Purpose:** Microarchitectural concept modeling a bump-in-the-wire Ingress Processing Unit to decouple 6G Sub-THz burst line-rate ingest from host DRAM/HBM memory controllers.
* **Role:** Lead Researcher & Systems Modeler.
* **Status:** `RESEARCH_PROTOTYPE` (Evidence Tier E3 — Simulation Only).
* **Evidence:** Formal specifications (`ARCH-SPEC-001`, `ARCH-SPEC-002`); SimPy discrete-event simulation scripts (`sim/sweep_ipu_breakeven.py`, `sim/warehouse_mem_sim.py`).
* **Benchmark:** **4.12x tail-latency reduction** (p99) and **68% host memory bus contention relief** under 1.6 Tbps synthetic Poisson burst ingest.
* **Limitations:** Results are purely simulated using queueing models; not yet validated on physical FPGA or ASIC hardware.

### Project 3: BiasAperture
* **Purpose:** Regulatory-compliant demographic bias auditing and intersectional disparity evaluation framework for deep vision models.
* **Role:** Co-Lead Engineer (Fusemachines AI Fellowship Capstone).
* **Status:** `IMPLEMENTED` & `EXPERIMENTALLY VERIFIED` (Evidence Tier E4).
* **Evidence:** Python CLI; automated Jinja2 LaTeX-to-PDF audit certificate generation; test suite covering statistical boundary conditions.
* **Benchmark:** Audited 126 demographic intersectional bins; evaluated Disparate Impact Ratio (DIR) and Equalized Odds Difference (EOD) with BCa bootstrap confidence intervals.
* **Limitations:** Sensitive to small subgroup sample sizes ($N < 30$ bins are discarded, which can obscure sparse minority edge cases).

### Project 4: NovaOptimizer
* **Purpose:** Ultra-lightweight Windows OS tuner optimizing system memory before heavy compute workloads without third-party telemetry bloat.
* **Role:** Creator & Maintainer.
* **Status:** `IMPLEMENTED` & `EXPERIMENTALLY VERIFIED` (Evidence Tier E4).
* **Evidence:** C# .NET 10 repository calling Win32 NT kernel APIs via P/Invoke.
* **Benchmark:** Reclaims **1.2 GB – 3.4 GB working-set RAM** via Win32 `EmptyWorkingSet` and trims standby cache.
* **Limitations:** Flushing working sets forces subsequent memory access to page-fault from disk/paging file, introducing transient warmup latency.

### Project 5: Super-NLM Hub
* **Purpose:** Multi-account Google NotebookLM aggregator providing unified research synthesis and MCP agent integration.
* **Role:** Creator & Systems Developer.
* **Status:** `IMPLEMENTED` (Evidence Tier E3).
* **Evidence:** FastMCP server in Python with token-ring router and session cooldown manager.
* **Benchmark:** Unlocks 6x parallel research and synthesis quota headroom across accounts.
* **Limitations:** Dependent on reverse-engineered web session tokens; vulnerable to upstream Google authentication changes.

### Project 6: GCSBR (Gesture Controlled Self-Balancing Robot)
* **Purpose:** Inverted pendulum two-wheeled robot controlled via real-time computer vision hand gestures.
* **Role:** Lead Hardware & Control Developer (BEI Minor Project).
* **Status:** `IMPLEMENTED` & `EXPERIMENTALLY VERIFIED` (Evidence Tier E4).
* **Evidence:** Arduino firmware, PID control loops, MATLAB dynamic modeling, MediaPipe vision bridge; rated **9.6/10** by academic examiners.
* **Benchmark:** Maintained stable upright equilibrium with $\pm 2.5^\circ$ tilt tolerance under real-time gesture commands.
* **Limitations:** Tuning was performed manually for smooth surfaces; stability degrades on irregular inclines.

---

## 6. Technical Toolchain

* **Languages:** C / C++ (Embedded), Python 3.11+, C# (.NET 10), Kotlin 2.2, SQL (PostgreSQL), Bash / PowerShell 7, LaTeX.
* **Embedded & Hardware:** ESP32-S3, Arduino, MPU-6050 (6-axis IMU), Logic Analyzers, Oscilloscopes, ESP-IDF, FreeRTOS, TFLite Micro.
* **AI & Statistics:** PyTorch, TensorFlow Lite, Fairlearn, AIF360, SHAP, SimPy, Scikit-learn, NumPy, Pandas.
* **Protocols & Architecture:** Model Context Protocol (FastMCP), REST (FastAPI), CXL 3.0/4.0 specifications, BLE GATT, Win32 NT APIs.
* **Tooling & CI/CD:** Git, CMake, Pandoc, Docker, Vite, Chrome Extensions (MV3).

---

## 7. Current R&D Directions

1. **Headless Invariant Assurance Engine:** Formalizing candidate software state invariants into SMT-LIB constraints and verifying them via SMT solvers (Z3) and isolated execution sandboxes.
2. **Worker Session Runtime (WSR):** Developing an autonomous orchestrator that treats LLM worker sessions as stateless, disposable compute instances while maintaining persistent task state across quota limits.
3. **Reproducibility Benchmarking:** Converting all simulation scripts and experimental sweeps into one-click pinned reproducible artifacts.

---

## 8. Verification Philosophy

Every major claim made in this dossier is backed by:
- **A machine-readable capability manifest** (`schemas/capability-registry.yaml`).
- **An explicit Evidence Tier ($E0$–$E5$)** (`schemas/evidence-policy.md`).
- **An audited empirical methodology record** (`report/quantitative-claims-audit.md`).
- **A transparent accounting model** (`report/economic-model.md`).
