# Engineering Profile & Technical Dossier: Aaradhya Dev Tamrakar (ADT)

```text
Artifact ID:          PROF-001-ENGINEERING-PROFILE
Version:              2.1.0 (Evidence-Hardened Edition)
Status:               CANONICAL
Principal Architect:  Aaradhya Dev Tamrakar (ADT)
Evidence Tier:        E1 — SPECIFICATION
Verification Ref:     schemas/evidence-policy.md, report/quantitative-claims-audit.md
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
  - **Makerspace Ambassador — KEC Makerspace**

---

## 3. Four-Tier Status Classification & Technical Proficiencies

Every engineering capability in this dossier is mapped to an explicit status tier defined in [`schemas/evidence-policy.md`](schemas/evidence-policy.md):

```text
[EXPERIMENTALLY_VERIFIED] (E4) ── Physical hardware / public benchmark execution with measured metrics
[IMPLEMENTED]             (E2/E3)── Committed, buildable code with local unit tests / microservices
[RESEARCH_PROTOTYPE]      (E3)   ── Algorithmic or queue-theoretic simulation (SimPy / numerical sweep)
[PROPOSED]                (E0/E1)── Formal architectural specification or schema awaiting empirical test
```

### I. `[EXPERIMENTALLY_VERIFIED]` Domains (Tier E4)
* **Embedded Sensor Kinematics & INT8 Edge AI:** ESP-IDF C/C++ firmware on ESP32-S3 with continuous [200 Hz ISR threshold sampling](report/quantitative-claims-audit.md#1-fall-detection-classification-auc-roc); on-device post-training quantized INT8 neural networks.
* **Statistical Algorithmic Fairness:** Disparity auditing across [[126 demographic bins]](report/quantitative-claims-audit.md#8-intersectional-demographic-bins-audited-biasaperture) evaluating Disparate Impact Ratio and Equalized Odds Difference with BCa bootstrap confidence intervals.
* **Win32 OS & Memory Management:** Direct P/Invoke integration with Windows NT memory APIs (`EmptyWorkingSet`), reclaiming [[1.2 GB – 3.4 GB working-set RAM]](report/quantitative-claims-audit.md#6-working-set-ram-purge-novaoptimizer).
* **Client-Side Cryptography:** Browser-native WebCrypto AES-256-GCM encryption with [[600,000 SHA-256 PBKDF2 rounds]](report/quantitative-claims-audit.md#7-cryptographic-key-derivation-security-parameter).

### II. `[IMPLEMENTED]` Domains (Tier E3)
* **Agentic FastMCP Microservices:** FastMCP JSON-RPC servers in Python for multi-account session aggregation and CAD parametric automation.
* **Deterministic Repository Verification:** AST and regex-based repository auditors ([`sim/reconciliation_engine.py`](sim/reconciliation_engine.py)) enforcing zero-drift consistency across Markdown links, YAML schemas, and metadata headers.
* **Local Web Engines:** High-speed RSVP reading HUDs in Svelte/Vite operating at [[300 – 900 WPM]](report/quantitative-claims-audit.md#9-reading-speed-cadence-rsvp-reader).

### III. `[RESEARCH_PROTOTYPE]` Domains (Tier E3 — Simulation Only)
* **Near-Memory Compute & Bump-in-the-Wire Acceleration:** SimPy discrete-event queueing simulation modeling CXL pooled bus interfaces under burst line-rate ingest.

### IV. `[PROPOSED]` Domains (Tier E1 — Specification)
* **Headless Invariant Assurance:** Neurosymbolic translation of API specifications into SMT-LIB constraints verified via Z3 solvers and Docker execution sandboxes.

---

## 4. Systems Philosophy

1. **Deterministic Verification over Fragile Abstraction:** If code cannot be verified deterministically via unit tests, SMT solvers, or hardware scope captures, it remains an unverified hypothesis.
2. **Physical Hardware Realism:** High-level abstractions must acknowledge physical silicon bounds—DRAM bus saturation, cache line fills, interrupt jitter, and network packet buffers.
3. **Epistemic Honesty:** Never report simulation results as physical silicon measurements, and never report replacement labor reconstruction as liquid market valuation.
4. **The Three-Output Rule:** Every architectural brainstorm must terminate in at least one of: (1) a reproducible experiment ([`research/experiments/`](research/experiments/)), (2) an executable implementation artifact, or (3) a falsifiable hypothesis card ([`research/hypotheses/`](research/hypotheses/)).

---

## 5. Selected Projects

### Project 1: SPARK (Smart Protection & Alerting Resilient Kit)
* **Purpose:** Two-layer wearable fall detection architecture pairing microsecond interrupt threshold gating with quantized neural inference and clinician-legible SHAP explainability.
* **Role:** Lead AI & Firmware Architect (BEI Major Capstone Project).
* **Status:** `[EXPERIMENTALLY_VERIFIED]` (Evidence Tier E4).
* **Evidence:** 44-page thesis proposal; [[56 passing unit tests]](report/quantitative-claims-audit.md#3-unit-test-suite-volume-spark); functional ESP32-S3 + MPU-6050 hardware; FastAPI clinical dashboard.
* **Audited Benchmark:** [[18.5 KB INT8 CNN]](report/quantitative-claims-audit.md#2-edge-neural-network-footprint-int8) achieving [[0.9185 AUC-ROC]](report/quantitative-claims-audit.md#1-fall-detection-classification-auc-roc) on the SisFall dataset ([[38,420 temporal windows]](report/quantitative-claims-audit.md#1-fall-detection-classification-auc-roc), zero-leakage subject-grouped cross-validation).
* **Documented Limitations:** Evaluated primarily on laboratory dataset distributions; real-world ambient false-positive calibration requires continuous field wear testing.

### Project 2: STRANGLER-IPU / SIPU-6G
* **Purpose:** Microarchitectural discrete-event model of a bump-in-the-wire Ingress Processing Unit to decouple 6G Sub-THz burst line-rate ingest from host DRAM/HBM memory controllers.
* **Role:** Lead Systems Modeler & Author.
* **Status:** `[RESEARCH_PROTOTYPE]` (Evidence Tier E3 — Simulation Only; Not Physical Silicon).
* **Evidence:** Formal specifications ([`ARCH-SPEC-001`](research/architectures/ARCH-SPEC-001-ECIE-COMPUTE-MEMORY.md), [`ARCH-SPEC-002`](research/architectures/ARCH-SPEC-002-INGESTION-PROCESSING-UNIT.md)); discrete simulation scripts ([`sim/sweep_ipu_breakeven.py`](sim/sweep_ipu_breakeven.py), [`sim/warehouse_mem_sim.py`](sim/warehouse_mem_sim.py)).
* **Audited Benchmark:** [[4.12x tail-latency reduction]](report/quantitative-claims-audit.md#4-strangler-ipu-tail-latency-reduction) (p99) and [[68% host memory bus contention relief]](report/quantitative-claims-audit.md#5-strangler-ipu-host-memory-bus-contention-relief) under 1.6 Tbps synthetic Poisson burst ingest.
* **Documented Limitations:** Purely simulated in SimPy queueing models; not yet validated on physical FPGA testbeds or custom ASIC tape-outs.

### Project 3: BiasAperture
* **Purpose:** Intersectional demographic bias auditing and fairness evaluation framework for deep vision models, compiling regulator-legible PDF audit certificates.
* **Role:** Co-Lead Engineer (Fusemachines AI Fellowship Capstone).
* **Status:** `[EXPERIMENTALLY_VERIFIED]` (Evidence Tier E4).
* **Evidence:** Python CLI; automated Jinja2 LaTeX-to-PDF audit certificate generation; test suite covering statistical boundary conditions.
* **Audited Benchmark:** Audited [[126 demographic intersectional bins]](report/quantitative-claims-audit.md#8-intersectional-demographic-bins-audited-biasaperture); evaluated Disparate Impact Ratio and Equalized Odds Difference with BCa bootstrap confidence intervals.
* **Documented Limitations:** Statistical tests discard sparse subgroups ($N < 30$), which can mask edge-case disparities in underrepresented cohorts.

### Project 4: NovaOptimizer
* **Purpose:** Minimalist Windows OS memory management utility tuning process working sets before heavy computational tasks without telemetry bloat.
* **Role:** Creator & Developer.
* **Status:** `[EXPERIMENTALLY_VERIFIED]` (Evidence Tier E4).
* **Evidence:** C# .NET 10 repository calling Win32 NT kernel APIs via P/Invoke.
* **Audited Benchmark:** Reclaims [[1.2 GB – 3.4 GB working-set RAM]](report/quantitative-claims-audit.md#6-working-set-ram-purge-novaoptimizer) via Win32 `EmptyWorkingSet` and trims standby file cache.
* **Documented Limitations:** Trimming working sets forces subsequent memory access to page-fault from disk/paging file, introducing transient warmup latency.

### Project 5: Super-NLM Hub
* **Purpose:** Multi-account Google NotebookLM aggregator providing unified research synthesis and FastMCP agent integration.
* **Role:** Creator & Systems Developer.
* **Status:** `[IMPLEMENTED]` (Evidence Tier E3).
* **Evidence:** FastMCP server in Python with token-ring router and session cooldown manager.
* **Audited Benchmark:** Multi-account sharding provides 6x parallel research and synthesis quota headroom across accounts.
* **Documented Limitations:** Dependent on reverse-engineered web session tokens; vulnerable to upstream Google authentication updates.

### Project 6: GCSBR (Gesture Controlled Self-Balancing Robot)
* **Purpose:** Inverted pendulum two-wheeled robot maintaining equilibrium via real-time computer vision hand gestures.
* **Role:** Lead Hardware & Control Developer (BEI Minor Project).
* **Status:** `[EXPERIMENTALLY_VERIFIED]` (Evidence Tier E4).
* **Evidence:** Arduino firmware, PID control loops, MATLAB dynamic modeling, MediaPipe vision bridge; rated **9.6/10** by academic examiners.
* **Audited Benchmark:** Upright equilibrium with $\pm 2.5^\circ$ tilt tolerance under dynamic gesture commands.
* **Documented Limitations:** Tuned exclusively for flat indoor surfaces; dynamic stability degrades on irregular inclines.

---

## 6. Technical Toolchain

* **Languages:** C / C++ (Embedded), Python 3.11+, C# (.NET 10), Kotlin 2.2, SQL (PostgreSQL), Bash / PowerShell 7, LaTeX.
* **Embedded & Hardware:** ESP32-S3, Arduino, MPU-6050 (6-axis IMU), Logic Analyzers, Oscilloscopes, ESP-IDF, FreeRTOS, TFLite Micro.
* **AI & Statistics:** PyTorch, TensorFlow Lite, Fairlearn, AIF360, SHAP, SimPy, Scikit-learn, NumPy, Pandas.
* **Protocols & Architecture:** Model Context Protocol (FastMCP), REST (FastAPI), CXL 3.0/4.0 specifications, BLE GATT, Win32 NT APIs.
* **Tooling & CI/CD:** Git, CMake, Pandoc, Docker, Vite, Chrome Extensions (MV3).

---

## 7. Current R&D Directions

1. **Headless Invariant Assurance Engine:** Formalizing candidate software state invariants into SMT-LIB constraints and verifying them via SMT solvers (Z3) and isolated execution sandboxes ([`README.md`](README.md#flagship-research-wedge-headless-invariant-assurance-engine)).
2. **Worker Session Runtime (WSR):** Developing an autonomous orchestrator that treats LLM worker sessions as stateless, disposable compute instances while maintaining persistent task state across quota limits ([`FLEET-001`](research/experiments/FLEET-001.md)).
3. **Composition Experiment Benchmarks:** Empirically measuring compound pipeline latency, human intervention, and reproducibility across multi-capability workflows ([`research/experiments/`](research/experiments/)).

---

## 8. Verification Philosophy

Every major quantitative claim in this dossier is traceable directly to:
- **A machine-readable capability manifest:** [`schemas/capability-registry.yaml`](schemas/capability-registry.yaml).
- **An explicit Evidence Tier ($E0$–$E5$):** [`schemas/evidence-policy.md`](schemas/evidence-policy.md).
- **An audited empirical methodology record:** [`report/quantitative-claims-audit.md`](report/quantitative-claims-audit.md).
- **A defensible accounting model:** [`report/economic-model.md`](report/economic-model.md).
