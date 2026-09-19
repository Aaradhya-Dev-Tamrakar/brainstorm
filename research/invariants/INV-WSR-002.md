# 📜 Architectural Invariant: INV-WSR-002 (Worker Protocol Completeness & Truthful Telemetry)

> **Artifact ID:** `INV-WSR-002`  
> **Title:** Worker Protocol Completeness, Push/Pull Dispatch & Truthful Telemetry Invariant  
> **Version:** `1.2.0`  
> **Status:** `IMPLEMENTED_AND_VERIFIED`  
> **Principal Architect:** Aaradhya Dev Tamrakar  
> **Discipline:** Distributed Orchestration & Multi-Agent Session Architecture  
> **Domain:** Worker Lifecycle, Task Leasing & Epistemic Telemetry  
> **Created Date:** 2026-09-19  
> **Last Verified:** 2026-09-19  
> **Evidence Tier:** `E2` — `EMPIRICAL BENCHMARK & TEST SUITE PROVEN`  
> **Applies To:** `Claude-Desktop`, `brainstorm`, and all fleet worker daemons  
> **Upstream Trace:** [`ARCH-RFC-001`](../architectures/ARCH-RFC-001-RECORD-KEEPING-STANDARD.md), [`ARCH-SPEC-003`](../architectures/ARCH-SPEC-003-HEADLESS-ORCHESTRATION-SUBSTRATE.md), [`FLEET-001`](../experiments/FLEET-001.md)  

---

## 1. The Core Invariant Statements

### 1.1 Invariant A: Closed-Loop Worker Dispatch (No Orphaned Leases)
> **"A central scheduler SHALL NEVER mutate task lease ownership to an assigned worker without an explicit, verifiable protocol mechanism through which that worker ingests and executes the leased task."**

In a distributed task state machine, task acquisition must adhere strictly to one of two valid communication contracts:
1. **Pull-with-Scheduler-Arbitration (Enforced Standard):** The worker explicitly calls `POST /tasks/acquire` (or `acquire_task` MCP tool), and the central scheduler atomically matches, leases, and returns the assigned task directly to the requester in a single atomic database transition.
2. **Push-with-Dedicated-Queue:** If the scheduler assigns a task asynchronously to `owner_worker_id = W`, worker `W` MUST poll `GET /tasks?owner_worker_id=W&status=claimed` rather than browsing generic pending tasks.

*Failure Mode Avoided:* Scheduler claims task for Worker A while Worker A only browses pending tasks, causing tasks to freeze until lease timeout. Auto-scheduler push loop in background supervisor is permanently disabled to eliminate dual-mode race conditions.

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
- `rate_limit_headroom`: Provider-specific remaining requests/tokens per window (or explicit cooldown timer upon HTTP 429). Persisted in `workers.rate_limit_headroom` database column.
- `system_resources`: Actual CPU/RAM utilization via OS performance counters (`cpu_percent`, `memory_percent`).
- `active_leases`: Count of currently executing tasks (strictly bounded by worker concurrency limits, reported truthfully as `1` during task execution and `0` when idle).

*Failure Mode Avoided:* Conflating OS RAM with provider quota usage causing spurious 5-hour cooldown triggers on high machine memory is strictly prevented. Cooldown triggers solely on explicit `trigger_cooldown` or provider `rate_limit_headroom <= 0`.

---

### 1.4 Invariant D: Atomic Checkpoint & DAG Advancement
> **"Task state completion, checkpoint persistence, worker quota accounting, and downstream DAG stage instantiation MUST occur within a single atomic database transaction."**

To prevent post-commit crash inconsistencies (where a task is marked `done` but the process crashes before the next pipeline stage task is created), the orchestrator wraps state finalization, checkpoint insertion, and successor task generation in an atomic transaction:
1. If any downstream DAG advancement step fails, the entire transaction rolls back cleanly (`status` remains `claimed`, checkpoint row is omitted, and successor tasks are not generated).
2. For QA stages, passing reviews (`verdict = pass`) atomically record checkpoint deliverables and pass forward review output to subsequent DAG stages (`format`), ensuring zero semantic data loss.

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

Compliance with `INV-WSR-002` is formally verified across automated test suites (**99/99 passing**):
1. **Invariant A (Closed-Loop Pull Dispatch):** `tests/test_task_acquisition.py` proves atomic pull matching and lease duration enforcement; push loop disabled in `server/main.py`.
2. **Invariant B (Strict Separation of Real/Simulation):** `tests/test_invariants_wsr_002.py::test_invariant_b_strict_separation_of_real_and_simulation` asserts zero synthetic success fallthrough across `ClaudeDesktopProxyAdapter`, `GroqAdapter`, and `GeminiFreeAdapter`.
3. **Invariant C (Truthful Telemetry):** `tests/test_invariants_wsr_002.py::test_invariant_c_truthful_telemetry` and `test_invariant_c_no_spurious_cooldown_on_high_memory` prove empirical OS performance counters, accurate `active_leases`, and immunity to RAM-induced quota cooldown.
4. **Invariant D (Atomic Advancement & Rollback):** `tests/test_invariants_wsr_002.py::test_invariant_d_atomic_dag_stage_advancement` and `test_invariant_d_atomic_rollback_on_failure` prove all-or-nothing transactional guarantees.
5. **Invariant D (QA Deliverable Preservation):** `tests/test_invariants_wsr_002.py::test_invariant_d_qa_checkpoint_preservation` verifies QA verification output persistence and successor stage inheritance.
6. **Security (Remote MCP Auth & Query Removal):** `tests/test_auth_enforcement.py` verifies unauthenticated requests receive HTTP 401, header credentials (`X-API-Key`) succeed, and URL query-string credentials are categorically rejected.
7. **Security (Mutation Token Isolation):** `tests/test_invariants_wsr_002.py::test_claim_token_masked_on_read_endpoints` proves `claim_token` is masked (`None`) on read-only queries (`GET /tasks`, `GET /tasks/{id}`, `list_tasks`, `get_task`) and exposed only to the claiming worker.
8. **Worker Lifecycle (Lease Renewal Parity):** `client/worker_daemon.py` and `client/fleet_supervisor.py` maintain continuous lease renewal across execution and result ingestion; verified in `tests/test_fleet_supervisor.py::test_fleet_lease_renewal_periodically`.
9. **Cross-Worker Session Migration & Resumption:** `tests/test_invariants_wsr_002.py::test_cross_worker_session_migration_and_resumption` proves the full multi-stage lifecycle across heterogeneous worker adapters (Worker A research → checkpoint → Stage 2 rate-limit cooldown & release → Worker B acquire & resume from checkpoint findings → format completion → unbroken audit lineage).
