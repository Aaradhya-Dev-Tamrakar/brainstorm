# Known Limitations, Failure Modes & Epistemic Risks

```text
Artifact ID:          LIM-001-KNOWN-LIMITATIONS
Version:              1.0.0
Status:               CANONICAL
Principal Architect:  Aaradhya Dev Tamrakar (ADT)
Evidence Tier:        E1 — DESIGN SPECIFICATION
Reconciliation Ref:   report/repository-audit.md
```

---

## 1. Motivation & Policy

A hallmark of rigorous engineering is the explicit disclosure of boundaries, failure modes, and epistemic risks. This document articulates the **known limitations and failure surfaces** of the Aaradhya Dev Tamrakar (ADT) ecosystem. It prevents over-claiming and ensures that researchers, collaborators, and evaluators understand the precise boundaries of current capabilities.

---

## 2. Core Architectural & Systemic Limitations

### 2.1 Formalization Error (The Intent-Specification Gap)
* **Description:** An automated or human-assisted formalizer (e.g., using LLMs to convert natural language API documentation into SMT-LIB constraints) can introduce subtle specification errors.
* **Failure Mode:** The SMT solver (Z3/CVC5) mathematically proves that the model satisfies the specification (UNSAT), but the specification itself was an incorrect translation of the real-world invariant.
* **Mitigation:** Closed-loop counterexample testing and execution of candidate invariants against real, instrumented execution sandboxes with planted bugs.

### 2.2 Benchmark Dependence & Distribution Shifts
* **Description:** Key empirical metrics in the ecosystem (e.g., SPARK's 0.9185 AUC-ROC on the SisFall dataset) are derived from controlled laboratory datasets.
* **Failure Mode:** In real-world patient ambulation, unexpected acceleration spikes (dropping a cane, aggressive sitting, vehicle bumps) can cause false positives not represented in the SisFall distribution.
* **Mitigation:** Two-layer interrupt threshold gating paired with localized SHAP feature attribution to allow clinicians to inspect attribution rationale.

### 2.3 Model Non-Determinism in Autonomous Orchestration Loops
* **Description:** Multi-model cognitive councils and LLM-powered code generators exhibit stochastic outputs even at temperature $\tau = 0$.
* **Failure Mode:** An autonomous orchestration loop that succeeds on Monday may fail on Tuesday if an upstream model updates its weights or produces an alternative AST representation.
* **Mitigation:** Zero-token deterministic verification gates (`reconciliation_engine.py`, SMT solvers, unit tests) serve as absolute hard barriers. No agent output is accepted without deterministic validation.

### 2.4 Integration Complexity Debt & Maintenance Burden
* **Description:** Maintaining 26 Git branches, 18 active projects, and 23 tool modules across heterogeneous stacks (C/C++, C# .NET 10, Python, Kotlin, Svelte, TypeScript, Node.js) imposes severe cognitive and temporal maintenance overhead.
* **Failure Mode:** "Platform sprawl" where developer time is consumed maintaining bindings, updating dependencies, and reconciling schemas rather than producing net-new research findings.
* **Mitigation:** The **Rule of Two** (prohibiting three-way composition before pairwise reliability is proven) and the **Integration-Cost equation** in `report/economic-model.md`.

### 2.5 API & Upstream Vendor Dependencies
* **Description:** Core components such as `Super-NLM` and `screen-qa-extension` rely on reverse-engineered web session tokens, Chrome extension APIs, and consumer AI subscriptions.
* **Failure Mode:** Upstream changes by Google, Anthropic, or OpenAI (e.g., modifying NotebookLM endpoints, altering family plan terms, or rate-limit tightening) can instantly break automation harnesses.
* **Mitigation:** Decoupling worker backends from task state (`FLEET-001`), ensuring that local models (via LM Studio / Ollama) or alternative API sockets can be swapped in without modifying task contracts.

### 2.6 Economic Replacement Valuation Uncertainty
* **Description:** The central replacement-equivalent asset valuation of ~$25,000 USD is derived from bottom-up reconstructed labor hours (~850 net hours) multiplied by a junior-to-mid engineering contracting rate ($25/hr).
* **Failure Mode:** Interpreting replacement cost as commercial enterprise value or liquid cash worth. A codebase costing $25k in labor to write may have zero market liquidity if there is no commercial entity monetizing it.
* **Mitigation:** Explicitly labeling the figure as *Replacement-Equivalent Labor Reconstruction*, with bounded sensitivity ranges ($15.5k – $37k).

### 2.7 Potential Survivorship Bias & Retrospective Coherence
* **Description:** Viewing 3.5 years of student projects retrospectively as a unified "4-tier Jarvis capability mesh" risks projecting post-hoc intentionality onto what originated as disparate, exploratory university assignments.
* **Failure Mode:** Treating accidental alignments as deliberate foundational architecture.
* **Mitigation:** Documenting the true evolutionary timeline: early projects were standalone course deliverables; the unified architectural mesh was formulated in late 2026.

### 2.8 False-Negative Pruning Risk in Invariant Discovery
* **Description:** In multi-stage invariant filtering (AST $\to$ SMT $\to$ Sandbox), aggressive early pruning heuristics can discard subtle, non-obvious invariants.
* **Failure Mode:** High pruning throughput achieving high precision on trivial invariants while systematically missing complex, cross-contract exploit invariants (false negatives).
* **Mitigation:** Continuous validation against benchmark suites of planted historical bugs with mandatory 100% recall enforcement.

### 2.9 Discrepancy Between Simulation Models and Physical Silicon
* **Description:** The STRANGLER-IPU results (4.12x tail-latency reduction, 68% memory bus contention relief) are simulated via SimPy discrete-event queueing models.
* **Failure Mode:** Idealized simulation assumptions (uniform packet distributions, simplified CXL 3.0 protocol transaction overhead, zero physical wire parasitics) may not translate directly to physical ASIC/FPGA performance.
* **Mitigation:** Labeling STRANGLER-IPU strictly as an *E3 Discrete-Event Simulation Prototype* rather than physical silicon.

### 2.10 Main-Thread Synchronization Boundary in CAD Actuation
* **Description:** Autodesk Fusion 360's internal C++ object model cannot be manipulated directly from background Python worker threads without risking immediate application crashes (`INV-FUS-001`).
* **Failure Mode:** Race conditions or thread blocking if long-running geometry calculations occur inside the `CustomEvent` handler.
* **Mitigation:** Fast asynchronous event queuing with brief execution slices and dedicated response channels.

### 2.11 LAN Peer Discovery and Multicast Broadcast Limits
* **Description:** LocalSend protocol actuation relies on UDP multicast (224.0.0.167:53317) and local subnet TCP connectivity (port 53318).
* **Failure Mode:** Corporate Wi-Fi client isolation, host firewalls, or multi-subnet routing prevent automatic peer discovery.
* **Mitigation:** Static peer IP fallback configuration and persistent favorite peer caching.

### 2.12 QA Authorization & Lease Mutation Boundary
* **Description:** In distributed DAG runtimes, QA reviews trigger state transitions (advancing tasks from QA to merge/formatting and unblocking dependent DAG stages).
* **Failure Mode:** If `/tasks/{task_id}/qa-review` does not enforce caller lease ownership and claim-token verification, any client holding an API key could prematurely finalize or reject tasks without owning the execution lease.
* **Mitigation:** Enforcing strict worker lease binding (`INV-WSR-002 Invariant E`): QA review submission requires the reviewer to hold the active lease and submit the cryptographically unique `claim_token`.

### 2.13 Headless Copilot API Contract Boundary vs Full Agent Tool-Calling
* **Description:** The headless GitHub Copilot worker adapter (`FLEET-002`) automates session token exchange and non-GUI REST completions (`POST /chat/completions`) for text generation and formatting.
* **Failure Mode:** Conflating the current REST text completion adapter (M1–M4) with fully autonomous agent mode that executes local sandboxed tools (`read_file`, `write_file`, `run_command`).
* **Mitigation:** Explicitly bounding M1–M4 to REST Text-Completion and scheduling multi-turn tool-calling loop as Phase 2 / M6 target capability.

### 2.14 Multi-Worker Fleet Authentication Header Propagation
* **Description:** In multi-provider fleet setups (`fleet_supervisor.py`), multiple worker loops run concurrently across different backends.
* **Failure Mode:** When orchestrator security requires API tokens (`X-API-Key`), worker launch daemons that instantiate HTTP clients without global credentials receive HTTP 401 Unauthorized responses on all task polling attempts.
* **Mitigation:** Standardizing credential ingestion via `API_AUTH_KEY` / `ORCHESTRATOR_API_KEY` across all client daemons and passing unified headers in `httpx.AsyncClient`.

### 2.15 Telemetry Failure Semantics vs Synthetic Placeholders
* **Description:** Distributed worker supervisors sample host CPU and RAM utilization for load-aware task arbitration.
* **Failure Mode:** Masking telemetry exceptions by returning synthetic `{"cpu_percent": 0.0, "memory_percent": 0.0}` placeholders, which tricks the orchestrator into treating an uninstrumented machine as having 100% free capacity.
* **Mitigation:** Strictly enforcing `null` (`None`) reporting and typed telemetry error states when OS performance counters are unreachable (`INV-WSR-002 Invariant C`).

### 2.16 Knowledge Graph Semantic Retrieval Evaluation Boundaries
* **Description:** BMK-MEMORY-001 measures signal density and precision@5 before and after memory stratification across Graphify communities.
* **Failure Mode:** Over-generalizing internal benchmark results (0.880 graded P@5 on a curated 5-query architectural suite) as a universal claim for arbitrary external knowledge graphs or independent corpora.
* **Mitigation:** Explicitly labeling the benchmark as a within-system diagnostic evaluation, preserving failed cohesion criteria (0.230 vs 0.45 target), and marking overall status as `QUALIFIED_PARTIAL_PASS`.

