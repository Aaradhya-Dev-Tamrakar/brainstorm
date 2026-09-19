# 🧠 RESEARCH BENCHMARK: BMK-MEMORY-001 (Memory Stratification & Graph Density)

```text
Artifact ID:          BMK-MEMORY-001
Title:                Graphify Knowledge Graph Signal Density Benchmark Before and After Memory Stratification
Version:              1.0.0
Status:               PROPOSED_PROTOCOL
Principal Architect:  Aaradhya Dev Tamrakar (ADT) & Multi-Model Cognitive Council
Domain:               Knowledge Representation, Graph Modularity & Retrieval Precision
Created Date:         2026-09-19
Evidence Tier:        E3 — LOCALLY VERIFIED PROTOCOL
Upstream Specs:       research/architectures/ARCH-RFC-005-MEMORY-STRATIFICATION.md, schemas/capability-ontology.md
Target Subsystem:     Graphify Knowledge Graph (`graphify-out/`)
```

---

## 1. Objective & Hypothesis

### 1.1 Objective
To empirically measure and quantify the structural degradation of the Graphify knowledge graph caused by conversational transcript ingestion, and to validate the signal-density improvements achieved by applying **ARCH-RFC-005 Memory Stratification** (excluding raw conversational transcripts from operational retrieval while preserving them in the Layer 0 epistemic vault).

### 1.2 Core Hypothesis (HYP-MEM-001)
> *Excluding raw conversational transcripts (`research/transcripts/`) from Graphify graph extraction and restricting Layer 2 extraction to architecture specifications, capability contracts, and verified experiment records will:*
> 1. Eliminate 100% of conversational artifact God nodes (`Turn X`, `Assistant`, `User`).
> 2. Reduce total node clutter by $\ge 40\%$ while increasing mean community cohesion from $< 0.10$ to $\ge 0.45$.
> 3. Improve architectural concept retrieval precision@5 by $\ge 50\%$ on benchmark queries.

---

## 2. Experimental Topology & Baseline Snapshot (Pre-Stratification)

### 2.1 Baseline State (Recorded from `graphify-out/GRAPH_REPORT.md` @ commit `2a70bcd6`)

| Graph Metric | Baseline Value (Pre-Stratification) | Target Value (Post-Stratification) |
| :--- | :---: | :---: |
| **Total Ingested Files** | 81 files (~317,261 words) | ~45 curated architecture/contract/spec files |
| **Total Graph Nodes** | **2,246 nodes** | **$\le 1,200$ nodes** (Pruned clutter) |
| **Total Graph Edges** | **2,335 edges** | **$\ge 1,500$ dense semantic edges** |
| **Detected Communities** | **222 communities** | **$15 - 30$ cohesive modules** |
| **Mean Community Cohesion** | **$0.03 - 0.06$** (Extremely fragmented) | **$\ge 0.50$** (High modularity) |
| **Isolated Schema Symbols** | **1,659 symbol nodes** ($\le 1$ edge) | Pruned via AST/JSON schema filtering |

### 2.2 Top Baseline God Nodes (Pathological Clutter)

```text
1. "Antigravity Session Transcript — Governance Rulesets & v1.0 Ecosystem Freeze" (78 edges)
2. "Turn 3" (4 distinct disjoint nodes, 45 edges each)
3. "Turn 5" (4 distinct disjoint nodes, 24 edges each)
4. "7. Verify the actual enforcement" (18 edges)
```

*Pathology:* The central hubs of the semantic graph represent conversational turn counters rather than fundamental architectural components (`reconciliation_engine`, `SPARK`, `Super-NLM`, `Fusion 360 MCP`).

---

## 3. Stratification Protocol (ARCH-RFC-005 Enforcement)

### 3.1 Layer Partitioning
1. **Layer 0 (Verbatim Epistemic Vault):** `research/transcripts/*.md` remain permanently stored on disk with ISO timestamps per `INV-EPI-001`. They are added to `.graphifyignore`.
2. **Layer 1 (Distilled Decisions):** Structured decision cards in `research/decisions/` and `report/` are ingested.
3. **Layer 2 (Operational Retrieval Mesh):** Graphify ingests:
   - `research/architectures/` (System charters, specs, and RFCs)
   - `research/experiments/` (Empirical protocols and result records)
   - `research/invariants/` (Mathematical and system invariants)
   - `schemas/` (Capability contracts, registries, ontology)
   - `sim/` (Deterministic verification and simulation engines)

### 3.2 Execution Commands

```powershell
# Step 1: Configure Graphify exclusion for raw transcripts
echo "research/transcripts/*" >> .graphifyignore

# Step 2: Re-run Graphify extraction
graphify update .

# Step 3: Extract post-stratification graph metrics
graphify report
```

---

## 4. Benchmark Retrieval Evaluation (Precision@5)

To evaluate retrieval signal density, 5 canonical architectural queries are evaluated before and after stratification:

| Query ID | Evaluation Query Prompt | Target Ground-Truth God Nodes |
| :---: | :--- | :--- |
| **Q1** | "How does the Fusion 360 MCP bridge execute CAD geometry without UI thread deadlocks?" | `ARCH-SPEC-006`, `INV-FUS-001`, `EXP-FUSION360-MCP-001` |
| **Q2** | "What is the mathematical definition of Human Intervention Ratio and how is it logged?" | `task_telemetry.py`, `ARCH-RFC-004`, `economic-model.md` |
| **Q3** | "Explain the two-layer fall detection architecture on ESP32-S3." | `SPARK`, `ARCH-SPEC-001`, `PROFILE.md` |
| **Q4** | "What are the six emergent compound workflows in the ecosystem?" | `schemas/capability-ontology.md`, `README.md` |
| **Q5** | "What are the calibrated evidence tiers and their solver/runtime requirements?" | `schemas/evidence-policy.md`, `ARCH-RFC-001` |

### Scoring Formula:
$$\text{Precision@5} = \frac{\sum_{i=1}^5 \mathbb{I}(\text{result}_i \in \text{Target Nodes})}{5}$$

---

## 5. Falsification & Acceptance Criteria

* **PASS / ACCEPT:** 
  1. Top 5 God Nodes contain zero occurrences of `Turn`, `Assistant`, `User`, or raw transcript titles.
  2. Mean community cohesion across top 10 communities increases by $\ge 300\%$ over baseline ($> 0.25$).
  3. Average Precision@5 across Q1–Q5 reaches $\ge 0.80$.
* **FAIL / REJECT:**
  1. Conversational artifacts remain in top 10 God Nodes.
  2. Critical architectural cross-references are broken by transcript exclusion.

---

## 6. Execution Status & Next Steps

* **Current Status:** Protocol codified and ready for execution.
* **Next Action:** Update `.graphifyignore`, execute Graphify re-indexing pass, and record empirical results in `BMK-MEMORY-001_results.json`.
