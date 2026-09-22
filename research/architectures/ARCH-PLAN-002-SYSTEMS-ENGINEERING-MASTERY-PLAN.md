# ARCH-PLAN-002: Dual-Track Systems Engineering & Software Mastery Roadmap
## Transitioning from AI-Augmented Systems Architect to First-Principles Engineering Authority

**Artifact ID:** `ARCH-PLAN-002`  
**Classification:** Engineering Education & Skill Mastery Architecture  
**Principal Architect:** Aaradhya Dev Tamrakar  
**Date:** September 22, 2026  
**Status:** ACTIVE / BASELINE  
**Evidence Tier:** `E1` — Design Specification & Execution Roadmap  
**Target Domain:** Systems Engineering, Real-World Distributed Systems, Concurrency, and First-Principles Programming  
**Associated Repositories:** All 34 ecosystem repositories (notably `brainstorm`, `Claude-Desktop`, `BiasAperture`, `super-nlm`)  
**Upstream Provenance:** [`research/transcripts/2026-09-22_DEVELOPER-METRICS-AND-SKILL-MASTERY-PLAN_CONVERSATION.md`](../transcripts/2026-09-22_DEVELOPER-METRICS-AND-SKILL-MASTERY-PLAN_CONVERSATION.md)

---

## 1. Executive Context & Verified Baseline

In September 2026 (Sept 1 – Sept 22), human-directed AI orchestration achieved high developer velocity across Aaradhya's developer profile:
* **Total Contributions:** 924
* **Total Commits:** 795
* **Pull Requests Merged/Authored:** 19
* **Active Repositories:** 34
* **Active Daily Streak:** 22/22 days
* **Estimated Human Screen/Orchestration Hours:** ~110 – 135 hours (~30–35 hours/week)
* **Pre-AI Equivalent Output:** ~650 – 850 hours (~5.5× – 6.5× leverage multiplier)

### 1.1 Cognitive Profile Evaluation
Rather than a novice starting from scratch, the architect already possesses strong programming literacy and practical hacking experience (AST regex parsing, discrete event simulations, async queues, PowerShell rebase engines, and cryptographic schemes). 

Crucially, development bypassed "tutorial purgatory" and operated at the **Systems Architect** level:
1. **Interface & Contract-First Design:** Defined JSON schemas, capability contracts, and IPC protocols prior to code generation.
2. **Deterministic Verification Gates:** Enforced structural audits (`audit.bat`), simulations (`sim.bat`), and branch rulesets.
3. **Multi-Repo Mesh Management:** Orchestrated 34 synchronized repositories across CAD, MCP, AI orchestration, and research.

### 1.2 The Semantic Gap & Strategic Risk
Relying entirely on self-contained personal systems creates key engineering blind spots:
* **Single-User Trust Assumptions:** Personal tools assume cooperative inputs, lacking exposure to adversarial attacks (XSS, SQLi, SSRF, distributed race conditions).
* **Scale & Distributed State:** In-memory queues and local files do not exercise high-concurrency database writes, cache invalidation, sharding, and network partition recovery.
* **Legacy & External Codebase Reading:** Modifying code written by external engineering teams under unchangeable constraints.

---

## 2. Strategic Strategy: The 70 / 30 Hybrid Learning Model

The learning plan rejects generic beginner courses in favor of a dual-track strategy:

```
                                  [ DUAL-TRACK MASTERY ]
                                             │
                    ┌────────────────────────┴────────────────────────┐
                    ▼                                                 ▼
          [ Track A: 70% ]                                  [ Track B: 30% ]
     Deep-Dive Internal Systems                        Real-World External Reality
                    │                                                 │
  ├── Profile & Benchmark Own Engines                ├── Open-Source Upstream PRs
  ├── Concurrency & Runtime Internals                ├── Multi-Tenant Production Hardening
  └── Zero-AI White-Box Re-implementations           └── First-Principles Literature (DDIA/OSTEP)
```

---

## 3. Detailed Execution Tracks

### Track A: Internal Systems Dissection (70% Allocation)
*Objective: Transform working functional knowledge of personal repositories into deep runtime and mechanical sympathy.*

#### Module A.1: Runtime & Concurrency Mechanics
* **Target Repositories:** `Claude-Desktop`, `super-nlm`, `brainstorm` (sim engines).
* **Core Competencies:**
  * Node.js / V8 Event Loop: microtasks vs macrotasks, unhandled promise rejections, stream backpressure.
  * Python Async & Threading: GIL implications, `asyncio` event loops, task cancellation semantics, CPU vs I/O bound bottlenecks.
  * Inter-Process Communication (IPC): STDIO pipe buffers, Unix/Windows sockets, process lifecycle signals, deadlock avoidance.
* **Concrete Exercise:** Instrument `super-nlm` and `Claude-Desktop` MCP servers with telemetry to measure queue latency and deliberately induce/resolve deadlocks.

#### Module A.2: Profiling, Optimization & Zero-AI Re-implementation
* **Target Repositories:** `sim/warehouse_mem_sim.py`, `sim/reconciliation_engine.py`, `sync.ps1`.
* **Core Competencies:**
  * CPU profiling (flamegraphs, cProfile), memory footprint tracking (tracemalloc, heap dumps).
  * Algorithmic complexity optimization ($O(n^2)$ AST scanning reduced to $O(n)$ token streaming).
* **Concrete Exercise:** Handcraft a critical core sub-module (e.g., AST token parser or graph dependency cycle detector) completely from scratch in pure Python/C++ with zero AI prompting.

---

### Track B: Real-World Relevancy & External Scale (30% Allocation)
*Objective: Build hard resilience against scale, adversarial users, and external codebases.*

#### Module B.1: Upstream Open-Source Contribution
* **Target Ecosystems:** Open-source MCP SDKs (`modelcontextprotocol`), `uv`, `ripgrep`, or foundational Python async libraries.
* **Milestone:** Clone an external codebase ($\ge 50\text{k}$ LOC), diagnose an open issue in the tracker, write reproduction unit tests, and submit an accepted upstream Pull Request.
* **Outcome:** Experience rigorous code reviews from external maintainers focusing on typing, invariant protection, and idiomatic conventions.

#### Module B.2: Multi-Tenant Hostile Hardening (`BiasAperture`)
* **Target System:** Elevate `BiasAperture` or an MCP gateway from single-user local tool to a hardened public service.
* **Required Architectural Additions:**
  * Relational persistence via PostgreSQL with structured migrations and connection pooling.
  * Strict authentication/authorization (OAuth2/JWT with rotation and RBAC).
  * Rate limiting, token-bucket throttling, and defensive input sanitization.
  * Observability stack (structured logging, metrics endpoints, Prometheus/OpenTelemetry).

#### Module B.3: First-Principles Engineering Literature
Read and annotate core canonical systems texts:
1. **Designing Data-Intensive Applications (DDIA)** — Martin Kleppmann (Replication, partitioning, transactions, consensus).
2. **Operating Systems: Three Easy Pieces (OSTEP)** — Remzi Arpaci-Dusseau (Virtualization, concurrency, persistence).
3. **Computer Systems: A Programmer's Perspective (CS:APP)** — Bryant & O'Hallaron (Machine-level representation, processor architecture, memory hierarchy).

---

## 4. Verification & Milestone Scorecard

| Milestone ID | Target Area | Verification Criteria | Evidence Tier |
| :--- | :--- | :--- | :---: |
| `MS-ENG-01` | Profiling | Produce flamegraph & memory allocation audit for `sim/reconciliation_engine.py` | `E2` |
| `MS-ENG-02` | Zero-AI Coding | Write a verified graph cycle-detection engine from scratch without LLM generation | `E2` |
| `MS-ENG-03` | Open Source | Submit $\ge 1$ upstream PR to an external open-source project | `E3` |
| `MS-ENG-04` | Multi-Tenancy | Deploy `BiasAperture` with PostgreSQL connection pool & rate-limiting middleware | `E3` |
| `MS-ENG-05` | Theory | Complete annotated reading notes for DDIA Chapters 1–9 in Obsidian knowledge graph | `E1` |

---

## 5. Epistemic Governance & Invariants

* **Invariant Adherence:** All progress updates, profiling benchmarks, and architectural refactors under this plan must continue to honor `INV-EPI-001` (verbatim transcripts) and `INV-MEM-001` (memory bounded execution).
* **Review Rhythm:** Bi-weekly audit of Track A vs Track B balance using `.\audit.bat` and Git contribution distribution.
