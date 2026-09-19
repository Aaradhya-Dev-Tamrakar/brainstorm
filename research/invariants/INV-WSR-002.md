# 📜 Architectural Invariant: INV-WSR-002 (Worker Protocol Completeness & Truthful Telemetry)

> **Artifact ID:** `INV-WSR-002`  
> **Title:** Worker Protocol Completeness, Push/Pull Dispatch & Truthful Telemetry Invariant  
> **Version:** `1.0.0`  
> **Status:** `ACTIVE_SPECIFICATION`  
> **Principal Architect:** Aaradhya Dev Tamrakar  
> **Discipline:** Distributed Orchestration & Multi-Agent Session Architecture  
> **Domain:** Worker Lifecycle, Task Leasing & Epistemic Telemetry  
> **Created Date:** 2026-09-19  
> **Evidence Tier:** `E1` — `DESIGN SPECIFICATION`  
> **Applies To:** `Claude-Desktop`, `brainstorm`, and all fleet worker daemons  
> **Upstream Trace:** [`ARCH-RFC-001`](../architectures/ARCH-RFC-001-RECORD-KEEPING-STANDARD.md), [`ARCH-SPEC-003`](../architectures/ARCH-SPEC-003-HEADLESS-ORCHESTRATION-SUBSTRATE.md), [`FLEET-001`](../experiments/FLEET-001.md)  

---

## 1. The Core Invariant Statements

### 1.1 Invariant A: Closed-Loop Worker Dispatch (No Orphaned Leases)
> **"A central scheduler SHALL NEVER mutate task lease ownership to an assigned worker without an explicit, verifiable protocol mechanism through which that worker ingests and executes the leased task."**

In a distributed task state machine, task acquisition must adhere strictly to one of two valid communication contracts:
1. **Pull-with-Scheduler-Arbitration (Recommended):** The worker explicitly calls `POST /tasks/acquire` (or `REQUEST_WORK`), and the central scheduler atomically matches, leases, and returns the assigned task directly to the requester in a single atomic database transition.
2. **Push-with-Dedicated-Queue:** If the scheduler assigns a task asynchronously to `owner_worker_id = W`, worker `W` MUST poll `GET /tasks?owner_worker_id=W&status=claimed` rather than browsing generic pending tasks.

*Failure Mode Avoided:* Scheduler claims task for Worker A while Worker A only browses pending tasks, causing tasks to freeze until lease timeout.

---

### 1.2 Invariant B: Strict Separation of Real Execution and Simulation
> **"An execution adapter SHALL NEVER catch an unhandled provider failure or HTTP 4xx/5xx exception and silently substitute synthetic output with `success = True`."**

1. **Simulation Containment:** Simulation/demo mock paths must be explicitly declared at worker startup (`EXECUTION_MODE = SIMULATION`).
2. **Epistemic Honesty:** A failed API call or CDP disconnection MUST emit a typed error event (`EXECUTION_FAILED`, `RATE_LIMIT_429`, or `AUTH_ERROR`), decrementing worker health and releasing the lease back to the orchestrator.
3. **Evidence Invariant:** Synthetic outputs must never be recorded into production checkpoints or satisfy evidence verification gates.

---

### 1.3 Invariant C: Telemetry Truthfulness & Quota Headroom
> **"Heartbeat metrics emitted by worker daemons MUST reflect empirical system/provider states rather than constant synthetic placeholders."**

Worker heartbeat payloads must decouple and report:
- `rate_limit_headroom`: Provider-specific remaining requests/tokens per window (or explicit cooldown timer upon HTTP 429).
- `system_resources`: Actual CPU/RAM utilization via OS performance counters.
- `active_leases`: Count of currently executing tasks (strictly bounded by worker concurrency limits).

---

### 1.4 Invariant D: Atomic Checkpoint & DAG Advancement
> **"Task state completion, checkpoint persistence, worker quota accounting, and downstream DAG stage instantiation MUST occur within a single atomic database transaction."**

To prevent post-commit crash inconsistencies (where a task is marked `done` but the process crashes before the next pipeline stage task is created), the orchestrator must wrap state finalization and successor task generation in an atomic transaction or durable transactional outbox.

---

## 2. Mathematical Formalization

Let $T$ be a task, $W$ be a registered worker, and $\mathcal{S}$ be the orchestrator state.

$$\text{Lease}(T, W, \tau) \implies \left( \text{State}(T) = \text{CLAIMED} \land \text{Owner}(T) = W \land \text{Token}(T) = \tau \right)$$

The valid state transition sequence is:

$$\mathcal{S}_0 \xrightarrow{\text{Acquire}(W)} \mathcal{S}_1 \xrightarrow{\text{Execute}(W, \text{REAL})} \mathcal{S}_2 \xrightarrow{\text{AtomicCommit}(C_T, \text{DONE}, T_{\text{next}})} \mathcal{S}_3$$

If $\text{Execute}(W)$ raises error $E$:

$$\mathcal{S}_1 \xrightarrow{\text{Error}(E)} \mathcal{S}_{\text{recover}} \implies \left( \text{State}(T) = \text{PENDING} \land \text{Cooldown}(W) = \Delta t \right)$$

Under no circumstances may:

$$\text{Error}(E) \to \text{State}(T) = \text{DONE} \quad (\text{VIOLATION})$$

---

## 3. Verification & Compliance Gate

Compliance with `INV-WSR-002` is verified by:
1. Unit and integration tests in `Claude-Desktop` testing zero-fallthrough on simulated Anthropic API failures.
2. Adversarial concurrency suites verifying pull-based task acquisition and atomic DAG advancement.
3. Static audit asserting zero synthetic heartbeat hardcoding in worker daemons.
