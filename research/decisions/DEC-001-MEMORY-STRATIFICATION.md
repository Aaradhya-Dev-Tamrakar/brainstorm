# 🏛️ DECISION RECORD: DEC-001 (Memory Stratification & Retrieval Pruning)

```text
Decision ID:          DEC-001
Title:                Stratification of Knowledge Graph Ingestion to Decouple Verbatim History from Operational Retrieval
Status:               RATIFIED
Decision Date:        2026-09-19
Principal Architect:  Aaradhya Dev Tamrakar (ADT) & Multi-Model Cognitive Council
Governing RFC:        research/architectures/ARCH-RFC-005-MEMORY-STRATIFICATION.md
Benchmark Ref:        research/experiments/BMK-MEMORY-001.md
Evidence Tier:        E4 — EXPERIMENTALLY VERIFIED
Source Transcripts:   research/transcripts/2026-09-19_RATE-WORKFLOW_CONVERSATION.md, research/transcripts/2026-09-19_GITHUB-UPDATE-SUMMARY_CONVERSATION.md
```

---

## 1. Context & Problem

The 2026-09-19 external workflow audit rated personal R&D workflow at **8.7/10** with memory externalization at **9.7/10**, but identified acute retrieval noise in Graphify:
- `graphify-out/GRAPH_REPORT.md` revealed 2,246 nodes, 222 communities, and mean cohesion of only 0.03–0.06.
- Top God nodes were dominated by dialogue turns (`Turn 3` @ 45 edges, `Turn 5` @ 24 edges, `Antigravity Session Transcript`).
- 1,659 isolated schema symbols were fragmenting modularity.

---

## 2. Decision

1. **Establish Four Memory Layers:**
   - **Layer 0 (Verbatim Vault):** `research/transcripts/*.md` permanently stored on disk per `INV-EPI-001`.
   - **Layer 1 (Canonical Decisions):** `research/decisions/` containing high-signal, distilled architectural cards.
   - **Layer 2 (Knowledge Mesh):** `graphify-out/` ingesting specs, contracts, simulations, and decisions (excluding raw transcripts).
   - **Layer 3 (Working State):** `sim/task_telemetry.py` recording active task vectors.

2. **Exclude Transcripts from Graphify:**
   - Create `.graphifyignore` excluding `research/transcripts/*`.
   - Execute `graphify update . --force` to purge 1,441 conversational nodes.

---

## 3. Consequences & Empirical Verification

- **Node Count:** Reduced by **55.5%** (from 2,246 to 1,000 nodes).
- **Edge Count:** Reduced by **52.9%** (from 2,335 to 1,101 dense semantic edges).
- **Communities:** Consolidated by **61.3%** (from 222 fragmented clusters to 86 cohesive modules).
- **God Nodes:** 100% of conversational markers (`Turn X`, `Assistant`, `User`) were eliminated. Top hubs are now architectural registers (`Granular Claims Audit`, `Quantitative Claims`, `ARCH-RFC-003`, `reconciliation_engine`).
- **Benchmark Certification:** Formally validated in `research/experiments/BMK-MEMORY-001.md` and recorded in `research/results/BMK-MEMORY-001_results.json`.
