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
* **Description:** Maintaining 18 Git branches, 14 active projects, and 13 computational capabilities across heterogeneous stacks (C/C++, C# .NET 10, Python, Kotlin, Svelte, TypeScript) imposes severe cognitive and temporal maintenance overhead.
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
