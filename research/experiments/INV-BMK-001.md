# 🏛️ RESEARCH EXPERIMENT: INV-BMK-001 (Headless Invariant Assurance & Sandbox Replay Benchmark)

```text
Artifact ID:          INV-BMK-001
Title:                Headless Invariant Assurance: SMT Inductive Verification & Sandbox Replay Benchmark
Version:              1.0.0
Status:               EMPIRICALLY_VERIFIED
Principal Architect:  Aaradhya Dev Tamrakar (ADT)
Domain:               Neurosymbolic Verification, SMT Solvers & Automated Counterexample Replay
Created Date:         2026-09-24
Evidence Tier:        E4 — EXPERIMENTALLY VERIFIED
Upstream Specs:       schemas/capability-ontology.md, schemas/capability-registry.yaml (headless-invariant-assurance)
Implementation Ref:   sim/invariant_engine/ (smt_encoder.py, sandbox_replay.py, state_machine.py, benchmark_runner.py)
Evidence Dossier:     research/results/INV-BMK-001_results.json
```

---

## 1. Executive Summary & Objective

The repository's 2026-09-24 architectural audit identified a critical gap between mature infrastructure (Layer 1/2 verification, registries, ontologies) and the flagship research capability—the **Headless Invariant Assurance Engine**, which remained a Tier E1 design specification.

This benchmark (`INV-BMK-001`) transitions the engine from `PROPOSED` to `EMPIRICALLY_VERIFIED` (Tier E4). It constructs a multi-domain testbed of formal state machines, validates true safety invariants inductively via Z3 SMT-LIB2, isolates deliberately planted boundary violations, flags vacuous/contradictory negative controls, and replays mathematical counterexamples in isolated Python sandboxes to confirm runtime contract violations.

---

## 2. Formal Architecture & Mathematical Formulation

The engine executes an inductive verification loop:

```text
                       Candidate Invariant P(s)
                                  │
                                  ▼
                     ┌──────────────────────────┐
                     │ Vacuity & Contradiction  │
                     │  Negative Control Gate   │
                     └────────────┬─────────────┘
                                  │
              ┌───────────────────┴───────────────────┐
              ▼                                       ▼
    [Contra: P UNSAT]                       [Tautology: ¬P UNSAT]
  ──> REJECT_CONTRADICTION                ──> REJECT_VACUOUS
              │                                       │
              └───────────────────┬───────────────────┘
                                  │ (Passed Controls)
                                  ▼
                     ┌──────────────────────────┐
                     │   Base Case Check (Z3)   │
                     │     I(s) ∧ ¬P(s)         │
                     └────────────┬─────────────┘
                                  │
                                  ├──[SAT]──► Counterexample Found (Base)
                                  │
                           [UNSAT: Holds]
                                  │
                                  ▼
                     ┌──────────────────────────┐
                     │  Inductive Step Check    │
                     │ P(s) ∧ T(s,a,s') ∧ ¬P(s')│
                     └────────────┬─────────────┘
                                  │
                                  ├──[SAT]──► Counterexample Model (s, a, s')
                                  │                 │
                           [UNSAT: Proved]          ▼
                                  │       ┌──────────────────────────┐
                                  ▼       │  Python Sandbox Replay   │
                            FORMAL PROOF  │ machine.step(a, **model) │
                            CERTIFICATE   └────────────┬─────────────┘
                                                       │
                                                       ▼
                                              REPLAY_CONFIRMED (E4)
```

### 2.1 Inductive Invariant Property
For a state machine $M = \langle S, S_0, A, T \rangle$ and candidate invariant $P$:
1. **Base Case:** $\forall s \in S_0, P(s)$
2. **Inductive Step:** $\forall s, s' \in S, \forall a \in A, [P(s) \land T(s, a, s')] \implies P(s')$

### 2.2 Replay Ground Truth Invariant
To eliminate formalization divergence (where a solver proves a model that does not match real code), the counterexample model values are injected into an unmocked Python runtime state machine:
$$\text{ReplayConfirmed} \iff \neg P(\text{machine}.\text{step}(a, \text{model}(s)))$$

---

## 3. Benchmark Testbed Composition

The suite tests 12 distinct invariant scenarios across 4 domain state machines:

| Machine ID | Domain | Variables | Actions | Tested Properties | Planted Bugs |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **`CXL_ALLOCATOR`** | 6G Sub-THz Ingress CXL pooled memory controller | `credits_total`, `credits_free`, `credits_allocated`, `req` | `allocate`, `release` | 4 | Double-free credit inflation |
| **`TOKEN_BUCKET`** | Distributed rate limiter & API token bucket | `tokens`, `capacity`, `fill_rate`, `consumed`, `dt`, `amount` | `refill`, `consume` | 3 | Unbounded refill leak |
| **`WORKER_SESSION_RUNTIME`** | Autonomous worker lifecycle coordinator | `pending`, `running`, `completed`, `failed` | `dispatch`, `complete`, `fail` | 3 | Phantom task duplication |
| **`SEQUENCE_NONCE_TRACKER`** | Cryptographic replay prevention stream | `current_nonce`, `replays_detected`, `incoming_nonce` | `receive` | 2 | Monotonicity replay bypass |

---

## 4. Empirical Evaluation Results

The benchmark was executed deterministically via `sim/invariant_engine/benchmark_runner.py`:

```text
=====================================================================================
   HEADLESS INVARIANT ASSURANCE BENCHMARK ENGINE (INV-BMK-001)
   Domain State Machines: 4 | Formal Verification: Z3 SMT-LIB2 | Execution: Python Sandbox
=====================================================================================
Prop ID       | Machine            | Classification      | Prover Status         | Replay Status     | Time(ms)
---------------------------------------------------------------------------------------------------------------
INV-CXL-01    | CXL_ALLOCATOR      | VALID_INVARIANT     | PROVED_INVARIANT      | SKIPPED_HOLDS     | 19.85   
INV-CXL-02    | CXL_ALLOCATOR      | VALID_INVARIANT     | PROVED_INVARIANT      | SKIPPED_HOLDS     | 13.69   
INV-CXL-03    | CXL_ALLOCATOR      | PLANTED_VIOLATION   | COUNTEREXAMPLE_FOUND  | REPLAY_CONFIRMED  | 15.05   
INV-CXL-04    | CXL_ALLOCATOR      | VACUOUS_TAUTOLOGY   | VACUOUS_REJECTED      | SKIPPED_HOLDS     | 3.41    
INV-TB-01     | TOKEN_BUCKET       | VALID_INVARIANT     | PROVED_INVARIANT      | SKIPPED_HOLDS     | 16.71   
INV-TB-02     | TOKEN_BUCKET       | PLANTED_VIOLATION   | COUNTEREXAMPLE_FOUND  | REPLAY_CONFIRMED  | 8.81    
INV-TB-03     | TOKEN_BUCKET       | CONTRADICTORY_SPEC  | CONTRADICTION_REJECTED | SKIPPED_HOLDS     | 2.24    
INV-WSR-01    | WORKER_SESSION_RUNTIME | VALID_INVARIANT     | PROVED_INVARIANT      | SKIPPED_HOLDS     | 20.86   
INV-WSR-02    | WORKER_SESSION_RUNTIME | VALID_INVARIANT     | PROVED_INVARIANT      | SKIPPED_HOLDS     | 19.39   
INV-WSR-03    | WORKER_SESSION_RUNTIME | PLANTED_VIOLATION   | COUNTEREXAMPLE_FOUND  | REPLAY_CONFIRMED  | 16.33   
INV-NONCE-01  | SEQUENCE_NONCE_TRACKER | VALID_INVARIANT     | PROVED_INVARIANT      | SKIPPED_HOLDS     | 8.76    
INV-NONCE-02  | SEQUENCE_NONCE_TRACKER | PLANTED_VIOLATION   | COUNTEREXAMPLE_FOUND  | REPLAY_CONFIRMED  | 6.02    
=====================================================================================
 EMPIRICAL RESEARCH BENCHMARK SUMMARY (INV-BMK-001)
=====================================================================================
  * Total Evaluated Properties : 12
  * Planted Bug Recall         : 100.0% (4/4 violations found) [Target: 100%]
  * Counterexample Replay Conf.: 100.0% (4/4 confirmed in sandbox)
  * Vacuous Negative Controls  : 1/1 flagged & rejected
  * Contradictory Specs        : 1/1 flagged & rejected
  * False Discovery Rate (FDR) : 0.0% on valid invariants
  * Mean Solver Latency        : 12.59 ms
  * Mean Sandbox Replay Latency: 0.01 ms
[+] Evidence dossier recorded: research/results/INV-BMK-001_results.json
=====================================================================================
```

---

## 5. Falsification & Key Findings

1. **100% Discovery Recall on Planted Bugs:** All 4 planted boundary bugs across CXL memory, token bucket, worker runtime, and nonce sequencing were flagged by Z3 SMT without human assistance.
2. **100% Counterexample Replay Confirmation:** Every generated counterexample successfully executed in the concrete Python state machine runtime, producing real invariant violations and confirming zero formalization divergence.
3. **Robust Negative Control Gating:** Tautological invariants (e.g. $x \ge 0 \lor x < 0$) and contradictory constraints (e.g. $x > 100 \land x < 0$) were isolated and rejected before inductive checks.
4. **Sub-20ms Execution Speed:** Across all 12 properties, mean Z3 solver latency was $12.59\text{ ms}$, enabling continuous real-time CI enforcement.

---

## 6. Epistemic Certification

* **Evidence Tier:** **E4 — EXPERIMENTALLY VERIFIED**
* **Verification Command:** `python -m unittest sim/test_invariant_engine.py` (incorporated into `audit.bat`).
* **Artifact Output:** [INV-BMK-001_results.json](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/results/INV-BMK-001_results.json).
