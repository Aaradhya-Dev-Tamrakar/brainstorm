# Research Program Charter: Nepal Information Systems Research (NISR)

**ID:** `PLAN-NISR-001`  
**Date:** 2026-09-28  
**Status:** Approved / Active Research Program  
**Principal Investigator & System Architect:** Aaradhya Dev Tamrakar  
**Context:** Sovereign Information Infrastructure, Adaptive Multi-Modal Ingestion, Document Intelligence & Open-Ended Scientific R&D  
**Decoupling Relation:** Independent Research Laboratory (Formally decoupled from undergraduate major project `SPARK`)  
**Ecosystem Modules Referenced:** `nepali-ocr-ai` (Module #19), `super-nlm` (Module #1), `brainstorm` (Orchestration Root)  
**Parent / Evolution Link:** Evolved from [`PLAN-NEP-DATA-001`](PLAN-NEP-DATA-001_SOVEREIGN_KNOWLEDGE_GRAPH_AND_IDBFS_INGESTION.md) following 65-turn adversarial peer review ([`2026-09-28_REVIEW-NEPAL-DATA-WORK_CONVERSATION.md`](../transcripts/2026-09-28_REVIEW-NEPAL-DATA-WORK_CONVERSATION.md))

---

## 1. Program Mission & Paradigm Shift

The **Nepal Information Systems Research (NISR)** program addresses a fundamental systems problem: **Nepal's public information ecosystem is radically fragmented, unindexed, multi-modal, and encumbered by legacy font encodings.**

### The Core Paradigm Shift
Previous plans framed this work as a software scraper (*"building an autonomous crawler to collect all data about Nepal"*). Following extensive multi-model adversarial peer review, the program has pivoted to a scientific laboratory model:

> **"Characterizing and ingesting an unknown national information substrate through adaptive, evidence-driven systems engineering."**

The project does not begin by assuming an optimal crawling or OCR algorithm. Instead, **the unknown itself is treated as the primary research object**. The acquisition machinery is engineered to discover, characterize, and adapt to the actual access topology of Nepal's digital and archival surface.

### The Central Research Question
> *"How can an adaptive, multi-modal ingestion architecture minimize computational and network overhead while maximizing textual recovery accuracy across Nepal's legacy-encoded, heterogeneous public information ecosystem?"*

---

## 2. Decoupling from SPARK (Academic vs. Research Lab)

To prevent premature scope reduction, NISR is formally decoupled from Aaradhya's academic undergraduate major project:

| Attribute | SPARK | NISR (This Program) |
|---|---|---|
| **Organizational Role** | Formally bounded academic Major Project (BEI) | Independent open-ended research laboratory |
| **Domain** | Embedded wearable sensor + TinyML fall detection | National information systems, NLP, & distributed ingestion |
| **Timeline Boundary** | Fixed semester deliverables and university viva | Multi-phase empirical program driven by discovery |
| **Deliverable** | Single integrated hardware-software prototype | Reusable research substrate, datasets, and publications |
| **Design Driver** | Rubric and syllabus adherence | Empirical reproducibility and epistemic ground truth |

---

## 3. The 6 Emergent Contribution Tracks

Rather than committing prematurely to a single paper narrative, NISR collects rigorous, reproducible evidence across **six independent tracks**. Whichever track produces the highest empirical anomaly or systems breakthrough will form the basis of formal publication:

```text
                                  NISR PROGRAM ROOT
                                          │
    ┌──────────────┬──────────────┬───────┴──────┬──────────────┬──────────────┐
    ▼              ▼              ▼              ▼              ▼              ▼
[Track 001]    [Track 002]    [Track 003]    [Track 004]    [Track 005]    [Track 006]
  Source         Adaptive       Document       Synthetic      Sovereign        Legal
Landscape       Ingestion     Intelligence      Flywheel     Provenance      Knowledge
  Study        Architecture    & Transcoding      OCR        & Integrity       Graph
```

### Track NISR-001: Source Landscape Study
- **Objective:** Construct a machine-readable census (`source_registry.json`) mapping the accessibility, darkness, CMS frameworks, and modality distribution across all 25 ministries, constitutional bodies, and departments.
- **Publication Target:** *Empirical Software Engineering / Web Science / Dataset Paper.*

### Track NISR-002: Adaptive Ingestion Architecture
- **Objective:** Design an adaptive ingestion scheduler that selects traversal primitives (static crawler vs. headless browser vs. API enumerator vs. PDF harvester) based on observed source characteristics.
- **Publication Target:** *Distributed Systems / Systems Software Architecture.*

### Track NISR-003: Nepali Document Intelligence & Font Recovery
- **Objective:** Build an automated font-table inspection and path router that intercepts legacy Latin-1 mapped glyph fonts (Preeti, Kantipur, Himali) and transcodes them to Unicode NFC, proving that optical OCR is an unnecessary overhead for $>80\%$ of legacy digital PDFs.
- **Publication Target:** *Document Analysis and Recognition (ICDAR / DAS).*

### Track NISR-004: Synthetic OCR Flywheel
- **Objective:** Bootstrap high-accuracy neural OCR models for low-resource Devanagari by generating authentic synthetic training patches from clean digital statutory seeds, unlocking historical 1950–2000 scanned Nepal Gazettes.
- **Publication Target:** *Applied Machine Learning / Computer Vision / NLP.*

### Track NISR-005: Sovereign Provenance & Cryptographic Lineage
- **Objective:** Engineer a zero-drift, tamper-evident audit ledger pairing atomic storage, `os.fsync()` physical re-read assertions, and multi-tier cryptographic hashes for sovereign public records.
- **Publication Target:** *Information Systems / Digital Forensics / Open Data Governance.*

### Track NISR-006: Legal Knowledge Graph & Temporal Reasoning
- **Objective:** Formulate a bi-directional 125-year Bikram Sambat $\leftrightarrow$ Gregorian temporal normalization engine and statutory relation graph capturing legislative lifecycles (`AMENDS`, `REPEALS`, `PARTIALLY_REPEALS`, `CITES`).
- **Publication Target:** *Legal Informatics / AI & Law (JURIX / ICAIL).*

---

## 4. The 5-Phase Execution Sequence

Execution proceeds strictly in a gated, evidence-driven sequence:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: Program Grounding & Invariant Locking (Current Phase)         │
│  • Formalize PLAN-NISR-001 and establish operational invariants.        │
│  • Enforce single-node constraint and strict TLS quarantine rules.      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ PHASE 2: Step 0 Empirical Reconnaissance (EXP-NISR-001)                │
│  • Probe 10 representative Nepal public authorities.                   │
│  • Measure real-world accessibility, TLS, CMS types, and modalities.   │
│  • Validate or falsify initial traversal hypotheses.                   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ PHASE 3: Stratified 50-Document Extraction Benchmark (EXP-NISR-002)    │
│  • Assemble 50 ground-truth documents (Unicode, Preeti, Scanned).      │
│  • Implement font-table inspector and DocumentRouter.                  │
│  • Benchmark Transcoder vs. Tesseract 5 vs. PaddleOCR on RTX 3060.     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ PHASE 4: Controlled Single-Source Ingestion Pilot                      │
│  • Execute full vertical slice harvest against Nepal Law Commission.   │
│  • Ingest ~400 active Acts with post-write verification and B.S. dates.│
│  • Produce verified digital legal corpus + SQLite WAL ledger.         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ PHASE 5: Synthesis & Publication Candidate Selection                   │
│  • Evaluate empirical metrics across Tracks 001–006.                   │
│  • Select dominant scientific contribution and author formal paper.    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Bounded Architectural Invariants

The NISR program operates under five non-negotiable architectural invariants:

### `INV-SEC-TLS-001`: Strict TLS Certificate Verification & Quarantine
- **Rule:** The ingestion crawler must **never disable TLS certificate verification** (`verify=False` is strictly prohibited).
- **Enforcement:** If a government domain presents an expired certificate, self-signed root, or broken chain, the engine must:
  1. Record an `EPOS_TLS_CERT_INVALID` event with the server's x509 fingerprint in the ledger.
  2. Apply backoff retry according to domain policy.
  3. Quarantine the endpoint for human review.
- **Rationale:** Never silently lower cryptographic trust boundaries to compensate for poorly maintained public infrastructure.

### `INV-FLEET-001`: Single-Node Workstation Execution Constraint
- **Rule:** All Phase 1, Phase 2, and Phase 3 operations must execute on a **single local workstation** (host PC with RTX 3060 12GB + NVMe storage).
- **Enforcement:** Multi-node cluster orchestration (Jetson Nano, secondary PC, Mac mini) is deferred until single-node processing limits are empirically reached.
- **Rationale:** Prevents distributed systems overhead (RPC serialization, network leases, distributed deadlocks) from consuming engineering bandwidth during discovery.

### `INV-DOC-ROUTER-001`: Font-Table Inspection Before Visual OCR
- **Rule:** Optical character recognition (OCR) is the **last resort**, not the default response to unreadable PDF text.
- **Enforcement:** Every digital PDF must undergo font-table and encoding inspection via PyMuPDF. If legacy Latin-1 glyph mappings (Preeti, Kantipur) are detected, text is routed to the AST transcoder (`nepali-ocr-ai`), bypassing GPU OCR entirely.
- **Rationale:** Transcoding achieves $>50\times$ faster throughput and near $0\%$ character error rate compared to running visual OCR on digital vector text.

### `INV-TRAVERSAL-001`: Provisional Traversal Invariant
- **Rule:** Iterative Deepening Breadth-First Search (IDBFS) is a **traversal hypothesis**, not foundational dogma.
- **Enforcement:** The crawl engine must treat traversal algorithms as pluggable policies. Depth-based prioritization must be balanced against source importance, content modality, and document density.

### `INV-LEGAL-SEP-001`: Separation of Ingestion from Relational Extraction
- **Rule:** Raw document acquisition and cryptographic verification must be strictly decoupled from semantic relationship extraction.
- **Enforcement:** Ingestion preserves immutable byte payloads and primary metadata (`published_date`, `status`). Relationship parsing (`AMENDS`, `REPEALS`, `CITES`) operates as an asynchronous, offline NLP enrichment pass.

---

## 6. Component Architecture Boundary

To prevent reinventing commodity engineering, the boundary between proprietary research and third-party tools is strictly demarcated:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ PROPRIETARY NEPAL DOMAIN LAYER (Aaradhya's Research Core)              │
│  • CrawlPolicy & Domain Pacing Engine                                  │
│  • DocumentRouter & Preeti/Kantipur AST Font Transcoders               │
│  • Devanagari Unicode NFC Normalization & Varnavinyas Grammar Engine   │
│  • 125-Year Bikram Sambat ↔ Gregorian Bi-directional Calendar Engine   │
│  • Multidimensional Legal Chronology & Gazette Hierarchy Parsers       │
│  • Immutable Provenance Ledger & SHA-256 fsync Assertion Gate          │
├────────────────────────────────────────────────────────────────────────┤
│ SWAPPABLE COMMODITY PLUGINS (Mature Open-Source Engines)               │
│  • HTTP Traversal & Scheduling: Scrapy (~64k ⭐) / Crawlee (~26k ⭐)     │
│  • Document Parsing & Metadata: Apache Tika 4.1 / PyMuPDF              │
│  • Baseline OCR Engines: Tesseract 5 (`tessdata_best`)                 │
│  • Neural Layout & Vision OCR: PaddleOCR (~90k ⭐) / docTR             │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Immediate Phase 2 Deliverable: Step 0 Protocol

Phase 1 completes with the formalization of this charter. Immediate execution transitions to **Phase 2 (Step 0 Reconnaissance Probe)** as defined in [`research/experiments/EXP-NISR-001_RECON_PROBE.md`](../experiments/EXP-NISR-001_RECON_PROBE.md).
