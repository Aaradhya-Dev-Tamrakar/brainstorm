# Calibrated Evidence Policy & Epistemic Verification Standard

```text
Artifact ID:          POL-001-EVIDENCE-POLICY
Version:              1.0.0
Status:               CANONICAL
Principal Architect:  Aaradhya Dev Tamrakar (ADT)
Evidence Tier:        E1 — DESIGN SPECIFICATION
Reconciliation Ref:   schemas/capability-ontology.md
```

---

## 1. Motivation & Policy Scope

A common failure mode in ambitious technical portfolios is **epistemic inflation**: reporting architectural proposals, mathematical sketches, and uncalibrated benchmark targets as if they were experimentally demonstrated realities.

This document establishes the **Calibrated Evidence Policy** for all repositories, projects, capabilities, and claims across the Aaradhya Dev Tamrakar (ADT) ecosystem. Every headline metric, quantitative benchmark, capability status, and research finding MUST be tagged with a verifiable Evidence Tier and Epistemic Classification.

---

## 2. The Six Evidence Tiers ($E0$ – $E5$)

```text
E0 (IDEA) ──> E1 (DESIGN) ──> E2 (IMPLEMENTED) ──> E3 (LOCALLY VERIFIED) ──> E4 (EXPERIMENTALLY VERIFIED) ──> E5 (REPRODUCIBLY VERIFIED)
```

| Tier | Tier Name | Qualifying Criteria & Artifact Requirements | Permitted Claim Wording |
| :---: | :--- | :--- | :--- |
| **$E0$** | **IDEA** | Unformalized hypothesis, conversational brainstorming transcript, or high-level strategic note without architectural specification. | "Proposed", "Hypothesized", "Aspirational", "Concept" |
| **$E1$** | **DESIGN** | Formal architectural RFC (`ARCH-RFC-xxx`), schema specification (`schemas/*.json`), or machine-readable interface contract (`capability.contract.v1.json`). | "Designed", "Formally specified", "Architected" |
| **$E2$** | **IMPLEMENTED** | Buildable, syntax-checked code committed to an ecosystem repository or microcontroller firmware tree. No dangling dependencies. | "Implemented", "Built", "Executable" |
| **$E3$** | **LOCALLY VERIFIED** | Unit test suite passing (`pytest`, `ctest`), discrete-event simulation model executed (`sim/*.py`), or zero-drift static audit passing (`reconciliation_engine.py`). | "Locally verified", "Simulated", "Tested" |
| **$E4$** | **EXPERIMENTALLY VERIFIED** | Executed on target physical hardware (e.g., ESP32-S3 microcontroller, Win32 NT kernel, live network stream) or validated against public benchmark datasets (e.g., SisFall dataset, 38k windows). | "Empirically demonstrated", "Benchmarked", "Observed" |
| **$E5$** | **REPRODUCIBLY VERIFIED** | End-to-end reproducible by an independent third party via deterministic seed scripts, automated docker/virtualenv recipes, and pinned public dataset hashes. | "Reproducibly proven", "Rigidly benchmarked", "Production-verified" |

---

## 3. The Four Epistemic Classifications

In addition to evidence maturity tiers, every analytical claim must specify its epistemic truth mechanism:

```text
FORMALLY_PROVEN       ── Deterministic mathematical proof or SMT solver guarantee
EMPIRICALLY_VERIFIED  ── Observed via physical hardware execution or test-suite run
STATISTICALLY_OBSERVED── Measured across distribution samples with confidence bounds
HEURISTIC_HYPOTHESIS  ── Reasonable inductive rule-of-thumb awaiting experimental test
```

### 3.1 `FORMALLY_PROVEN`
* Grounded in formal logic, SMT solvers (Z3, CVC5), or closed-form mathematical proofs.
* Requires verifiable solver input script (SMT-LIB, Python Z3 binding) and counterexample absence.

### 3.2 `EMPIRICALLY_VERIFIED`
* Grounded in deterministic physical execution (e.g., Win32 `EmptyWorkingSet` API reducing working set RAM, or ESP-IDF ISR firing at 200 Hz).
* Requires deterministic setup instructions, log outputs, or hardware scope captures.

### 3.3 `STATISTICALLY_OBSERVED`
* Grounded in empirical distribution testing (e.g., AUC-ROC scores across SisFall, chi-squared disparity tests, BCa bootstrap confidence intervals).
* **Mandatory Invariant:** Must report sample size ($N$), baseline comparison, confidence interval, and variance. Never report point estimates alone.

### 3.4 `HEURISTIC_HYPOTHESIS`
* An educated working assumption, inductive architectural rule, or unverified rule-of-thumb.
* Must be explicitly flagged as a hypothesis awaiting falsification via an experiment card (`INV-xxx`).

---

## 4. The Epistemic Triad: Distinguishing Correctness Layers

A critical failure mode in formal systems and AI verification is confusing solver guarantees with real-world correctness. The ecosystem strictly enforces the separation of three distinct correctness layers:

```text
Natural-Language Intent / Real-World Invariant
         ↓ (Formalization Step)
Formal SMT / Logical Specification
         ↓ (Solver Step)
Solver SAT / UNSAT / Proof Result
         ↓ (Compilation & Execution Step)
Physical Hardware / Runtime Behavior
```

```
┌────────────────────────────────────────────────────────────────────────┐
│                        THE THREE CORRECTNESS LAYERS                    │
├──────────────────────────┬─────────────────────────────────────────────┤
│ Correctness Layer        │ Meaning & Verification Surface              │
├──────────────────────────┼─────────────────────────────────────────────┤
│ 1. Formalization         │ Does the formal specification correctly     │
│    Correctness           │ capture the real-world natural-language     │
│                          │ requirement or domain intent?               │
├──────────────────────────┼─────────────────────────────────────────────┤
│ 2. Solver Correctness    │ Did the SMT/theorem solver execute without  │
│                          │ internal soundness or completeness bugs?    │
├──────────────────────────┼─────────────────────────────────────────────┤
│ 3. Empirical / Runtime   │ Does the compiled machine code or physical  │
│    Correctness           │ hardware behave identically to the verified │
│                          │ model under physical operating noise?       │
└──────────────────────────┴─────────────────────────────────────────────┘
```

> [!CAUTION]
> **Core Architecture Invariant:**  
> *A solver successfully proving a formally encoded constraint does NOT establish that the formalization correctly represents the original system requirement.*  
> Proving the wrong specification with 100% mathematical rigor is still a failure. Every formal proof must be complemented by empirical execution in a real runtime sandbox.

---

## 5. External Reference & Benchmark Citation Policy

When comparing ecosystem capabilities against external research or commercial frameworks:
1. **Forbidden Language:** Do not use "validated by", "proven by", or "equivalent to" unless direct, identical benchmark parity has been executed in-repo.
2. **Mandatory Calibrated Language:**
   - *"Informed by"* (e.g., "Architecture informed by DARPA AIxCC autonomous vulnerability synthesis").
   - *"Inspired by"* (e.g., "Strangler Fig migration pattern inspired by Martin Fowler's telecom evolution model").
   - *"Consistent with"* (e.g., "Latency reduction bounds consistent with CXL 3.0 pooling literature").
   - *"Externally demonstrated by"* (e.g., "Neurosymbolic invariant pruning externally demonstrated by DeepMind AlphaCode 2").
