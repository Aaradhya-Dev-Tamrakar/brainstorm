# Program Charter: Brainstorm Research Laboratory (BRL) & Contributor Fellowship

**ID:** `PLAN-BRL-001`  
**Date:** 2026-09-29  
**Status:** Approved / Active Program Charter  
**Director & Principal Architect:** Aaradhya Dev Tamrakar  
**Context:** Independent Scientific Research Collective, Empirical Apprenticeship, Guild & Quest Model, Sovereign Open-Source Tool Ecosystem  
**Institutional Positioning:** IEEE KEC KTM Student Branch (Vice-Chair), KEC Makerspace (Physical/Hybrid R&D Substrate)  
**Parent Provenance Link:** Grounded in transcript [`2026-09-29_CREATE-RESEARCH-OPPORTUNITIES_CONVERSATION.md`](../transcripts/2026-09-29_CREATE-RESEARCH-OPPORTUNITIES_CONVERSATION.md) (and baseline [`2026-09-28_CREATE-RESEARCH-OPPORTUNITIES_CONVERSATION.md`](../transcripts/2026-09-28_CREATE-RESEARCH-OPPORTUNITIES_CONVERSATION.md))  
**Related Programs:** [`PLAN-NISR-001_PROGRAM_CHARTER.md`](PLAN-NISR-001_PROGRAM_CHARTER.md), [`schemas/ecosystem.registry.json`](../../schemas/ecosystem.registry.json)  

---

## 1. Executive Summary & Paradigm Shift

The **Brainstorm Research Laboratory (BRL)** represents the formal transition of Aaradhya's personal 23-module tool ecosystem into an **autonomous, verifiable research and engineering collective**.

### The Core Problem: The "Internship" Illusion
In emerging engineering ecosystems, students and junior researchers frequently seek generic "internships" or attempt to manufacture superficial titles with vague, unverified duties. Such credentials demonstrate minimal technical capability and fail external scrutiny by elite academic laboratories or frontier engineering teams.

### The Paradigm Shift
BRL replaces title inflation with an **empirical, artifact-driven apprenticeship**:

> **"Credibility is not conferred by an organizational title; it is mathematically and empirically proven by reproducible artifacts, cryptographic commit history, and peer-reviewed technical dossiers."**

Rather than offering conventional "unpaid internships" (a legally ambiguous and pedagogically flawed term), BRL establishes a meritocratic **Research Fellowship & Guild System** where contributors earn verified standing (*Research Fellow*, *Research Contributor*, *Student Researcher*) backed by permanent, auditable deliverables.

---

## 2. Institutional Positioning & Operational Substrates

BRL operates across a calibrated hybrid model, combining high-trust physical touchpoints with fully asynchronous, zero-trust cryptographic workflows:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        BRAINSTORM RESEARCH LAB                         │
├──────────────────────────────────┬─────────────────────────────────────┤
│      PHYSICAL / HYBRID ROOT      │       DISTRIBUTED ASYNC ROOT        │
│    • KEC Makerspace / Hardware   │    • GitHub Organization Ecosystem  │
│    • IEEE KEC KTM Executive Hub  │    • Dual-Layer Verification Gates  │
│    • Direct Mentorship Sprints   │    • Graphify Topological Knowledge │
│    • Physical Sensor Benches     │    • NotebookLM Cognitive Grounding │
└──────────────────────────────────┴─────────────────────────────────────┘
```

1. **Academic Seniority & Institutional Leverage:** Directed by the final-year IEEE KEC KTM Vice-Chair, enabling cross-faculty engagement across Computer, Electronics, and Civil/Mechanical engineering faculties.
2. **Physical Maker Infrastructure:** Hands-on prototyping and sensor testbeds hosted at KEC Makerspace.
3. **Deterministic Digital Ground Truth:** All codebase contributions must pass through `sim/` regression suites and `.\audit.bat` before entering the canonical knowledge graph.

---

## 3. The Guild & Quest Progression Engine

To eliminate ambiguous expectations, contributor work is structured as a **Rank-Gated Quest Engine**. Contributors advance based on demonstrated technical proof, mirroring a `uv.lock` deterministic state lock:

```text
 [Rank E: Scout] ──► [Rank D: Analyst] ──► [Rank C: Builder] ──► [Rank B: Prover] ──► [Rank A: Scholar]
  Data Extraction     Sanity & Schema        Module Features      SMT / Formal Logic    Peer-Reviewed Papers
  Baseline Repro      Failure Taxonomies     Tool Adapters        Invariant Engines     Lead Fellowship
```

### Rank Tiers & Responsibilities

| Rank | Designation | Focus Domain | Minimum Deliverables | Gate Check |
|---|---|---|---|---|
| **Rank E** | *Research Scout* | Baseline reproduction, raw data scraping, sanity checks | Golden benchmark verification, source census | 100% deterministic match with existing baselines |
| **Rank D** | *Research Analyst* | Failure-mode classification, dataset cleaning, edge-case probing | Cleaned JSON/CSV corpora, negative control testbeds | Zero schema violations, validation scripts |
| **Rank C** | *Research Engineer* | Feature implementation, pipeline adapters, tool integrations | Pull request with unit tests, MCP tool integration | Zero-error `audit.bat`, code review sign-off |
| **Rank B** | *Research Fellow* | Formal verification, performance benchmarks, SMT solving | Formal invariant proofs (Z3/Python), latency profiles | Empirical evidence dossiers (`INV-xxx.json`) |
| **Rank A** | *Senior Fellow* | Architecture design, theoretical proofs, conference authorship | Complete IEEE/ACM format paper, camera-ready LaTeX | External peer review, artifact evaluation |

---

## 4. Cohort 0 (C0) Execution Blueprint

**Cohort 0** is the calibration cohort: a closed, high-trust circle of 3–5 pre-selected candidates designed to stress-test the guild system and establish baseline pedagogical efficiency.

### Scope-Lock Constraints
- **Team Size:** Strictly locked to $N \in [3, 5]$ contributors.
- **Duration:** 8-week structured cycle.
- **Teaching Tax Mitigation:** Onboarding is mediated through dedicated Google NotebookLM notebooks and deterministic CLI scripts, preventing 1-on-1 tutoring bottlenecks.
- **Evaluation against the "AI Trap":** In an era of pervasive LLMs, contributors are evaluated strictly on **problem decomposition, data integrity, edge-case analysis, and deterministic execution** rather than generative prose or boilerplate code.

---

## 5. Cohort 0 Launch Quest Catalog

The following four concrete quests are immediately available for Cohort 0 assignment:

### Quest C0-01: Baseline Reproduction & Execution Verification (Rank E)
- **Objective:** Clone the repository, execute the dual-layer verification engine, and verify the canonical discrete-event memory simulator output.
- **Target Subsystem:** [`sim/warehouse_mem_sim.py`](../../sim/warehouse_mem_sim.py), [`sim/run_all_reproducibility.py`](../../sim/run_all_reproducibility.py).
- **Deliverable:** Contributor-authored reproduction experiment report confirming identical hash/metric outputs across distinct hardware nodes.
- **Evaluation:** Bit-exact numerical alignment with established golden logs.

### Quest C0-02: Sovereign Source Census & Accessibility Probing (Rank E/D)
- **Objective:** Conduct a systematic accessibility and TLS inspection across 10 official Nepal public authority websites (aligned with [`PLAN-NISR-001_PROGRAM_CHARTER.md`](PLAN-NISR-001_PROGRAM_CHARTER.md)).
- **Target Subsystem:** Nepal Information Systems Research source registry.
- **Deliverable:** Machine-readable census (`source_census_c0.json`) documenting CMS frameworks, TLS protocols, broken links, and download rates.
- **Evaluation:** Adherence to JSON schema, absence of synthetic/hallucinated endpoints.

### Quest C0-03: Devanagari Legacy Glyph Transcoding Test Harness (Rank D)
- **Objective:** Assemble a ground-truth parallel corpus of 50 scanned/digital legacy-encoded sentences (Preeti/Kantipur) mapped to normalized Unicode NFC.
- **Target Subsystem:** Nepali OCR / Document Intelligence track.
- **Deliverable:** Test vector file (`legacy_transcode_vectors.json`) with edge cases (halfform ligatures, reph, nukta marks).
- **Evaluation:** 100% round-trip conversion accuracy through the transcoding harness.

### Quest C0-04: Tool Module Telemetry & Latency Profiling (Rank D/C)
- **Objective:** Benchmark execution latencies and memory footprints for one standalone module in the 23-module ecosystem.
- **Target Subsystem:** Selected from [`schemas/ecosystem.registry.json`](../../schemas/ecosystem.registry.json).
- **Deliverable:** Benchmark markdown report with p50/p95/p99 latency distributions and resource consumption graphs.
- **Evaluation:** Reproducibility across 100 sequential runs; proper statistical error bars.

---

## 6. Objective Evaluation Rubric

Every quest submission is evaluated across 5 objective axes, scored from 0 to 3:

| Score | Artifact Completeness | Reproducibility | Epistemic Honesty | Git & Sync Discipline | Autonomy |
|:---:|---|---|---|---|---|
| **0** | Missing core files or corrupted output | Fails execution entirely | Speculative claims disguised as empirical data | Direct force-pushes, unformatted commits | Abandoned task without notice |
| **1** | Partial output; key requirements omitted | Requires substantial manual patching to run | Mixed claims; missing baseline comparisons | Irregular commit history, broken branch rules | Required continuous hand-holding |
| **2** | All deliverables present and well-structured | Clean reproduction via single command | Strict calibrated epistemic tiers (RFC-001) | Clean conventional commits, passed `.\audit.bat` | Self-directed; asked targeted, high-clarity questions |
| **3** | Exceeds spec; includes edge-case stress suites | Fully automated containerized test suite | Discovered unstated edge cases / failure modes | Flawless PR history, authored docs update | Fully autonomous; unblocked peer contributors |

**Advancement Gate:** Contributor must score $\ge 8 / 15$ with zero 0-ratings to complete a Quest and qualify for promotion.

---

## 7. Governance, IP Boundary & Contributor Agreement

To maintain institutional integrity while protecting intellectual property, all participants adhere to the **BRL Contributor Agreement**:

1. **Permanent Attribution Invariant:**
   - Every contributor retains full public attribution for their authored code, datasets, and reports.
   - Authorship is permanently etched into Git history, release notes, and formal publications.
2. **Proprietary Tool Boundary:**
   - The Brainstorm orchestration core, multi-agent pipelines, automation scripts (`sync.ps1`, `reconciliation_engine.py`), and MCP servers remain proprietary ecosystem assets under BRL governance.
   - Contributor access to internal tooling is non-exclusive and non-transferable. Reverse-engineering, unauthorized re-licensing, or exfiltrating toolsets for uncredited commercial/personal repackaging constitutes an immediate, permanent revocation of standing.
3. **Strict Meritocracy & Non-Discrimination:**
   - BRL operates under absolute meritocratic evaluation.
   - Decisions regarding quests, promotions, authorship, and funding recommendations are strictly blind to gender, identity, or social politics. High-agency execution is the sole currency.
4. **Exit & Departure Protocol:**
   - Contributors who depart or are rotated off maintain all earned authorship, reference letters, and verifiable portfolio links.
   - Repository write access, internal API keys, and active lab communication channels are archived upon exit.

---

## 8. Multi-Phase Roadmap & Future Scaling

```text
┌────────────────────────────────────────────────────────────────────────┐
│ PHASE 0: Pre-Flight & Tool Lock (Weeks 0–2) [CURRENT]                  │
│  • Formalize PLAN-BRL-001 charter, Contributor Agreement, & Rubric.   │
│  • Finalize C0 candidate shortlist (3–5 individuals).                 │
│  • Prepare NotebookLM onboarding context package.                     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: Cohort 0 Operation & Calibration (Weeks 3–10)                 │
│  • Execute Quests C0-01 through C0-04.                                 │
│  • Measure empirical teaching tax and contributor retention.          │
│  • Publish first joint technical report / dataset archive.             │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ PHASE 2: Faculty Integration & Cohort 1 Expansion (Post-C0)            │
│  • Onboard select academic advisors and faculty mentors.               │
│  • Expand Guild Quests to Rank B/A (SMT solver proofs, papers).        │
│  • Initiate formal IEEE workshop / conference paper submissions.       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ PHASE 3: Institutionalization & Post-Graduation Continuity             │
│  • Transition BRL to an autonomous, distributed open-research engine.  │
│  • Seed spin-off opportunities / sovereign data infrastructure org.    │
└────────────────────────────────────────────────────────────────────────┘
```
