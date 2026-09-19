# ARCH-RFC-005: Memory Stratification & Knowledge Graph Signal Density

- **Artifact ID:** ARCH-RFC-005
- **Status:** IMPLEMENTED
- **Principal Architect:** Aaradhya Dev Tamrakar (ADT) & Multi-Model Cognitive Council
- **Evidence Tier:** E4 (Locally Verified)
- **Supersedes / Extends:** ARCH-RFC-001 (Record Keeping), INV-EPI-001 (Verbatim History)

---

## 1. Executive Summary & Problem Statement

As established in the 2026-09-19 external workflow audit ([`2026-09-19_RATE-WORKFLOW_CONVERSATION.md`](file:///F:/Aaradhya-Dev-Tamrakar/brainstorm/research/transcripts/2026-09-19_RATE-WORKFLOW_CONVERSATION.md)), the brainstorm ecosystem succeeded at eliminating information loss (**9.7/10 on externalized memory**) but created an information retrieval challenge.

Specifically:
- Verbatim multi-turn transcript logs (`research/transcripts/*.md`) injected thousands of conversational graph nodes into Graphify.
- God nodes were dominated by repeated strings like `Turn 3`, `Turn 5`, and conversational markers.
- Knowledge graph communities exhibited low modularity and cohesion (e.g., clusters ranging from 0.04 to 0.18 cohesion).

**Core Axiom**: *Verbatim archival memory and operational retrieval memory must not be the same structural layer.*

---

## 2. The Four-Tier Memory Stratification Hierarchy

To preserve complete epistemic provenance without degrading retrieval precision, the memory architecture is partitioned into four distinct layers:

```
┌────────────────────────────────────────────────────────────────────────┐
│ Layer 3: Working State (Ephemeral Task Vectors & Active DAGs)          │
│  - Active session checkpoints, tool buffers, memory scratchpad         │
├────────────────────────────────────────────────────────────────────────┤
│ Layer 2: High-Density Conceptual Knowledge Mesh (Graphify Graph)       │
│  - Architecture specs, capabilities, contracts, tools, hypotheses      │
│  - High cohesion (>0.75), typed cross-references, zero turn clutter    │
├────────────────────────────────────────────────────────────────────────┤
│ Layer 1: Canonical Event & Decision Records (`research/decisions/`)    │
│  - Distilled architectural pivots, evidence elevations, failure logs   │
│  - Structured metadata cards with exact pointers to Layer 0 sources    │
├────────────────────────────────────────────────────────────────────────┤
│ Layer 0: Verbatim Epistemic Vault (`research/transcripts/`)            │
│  - Raw transcripts preserved verbatim per INV-EPI-001                  │
│  - Read-on-demand for historical provenance, excluded from semantic AST│
└────────────────────────────────────────────────────────────────────────┘
```

### Layer 0: Verbatim Epistemic Vault
- **Path**: `research/transcripts/*.md`
- **Purpose**: Strict adherence to `INV-EPI-001` (Verbatim Epistemic History Invariant). Complete raw dialogues, peer reviews, and model transcripts exported via `save-chat` CLI.
- **Indexing Rule**: Excluded from raw sentence-level semantic node extraction; indexed only by file-level summary and provenance metadata.

### Layer 1: Canonical Event & Decision Extraction
- **Path**: `research/decisions/` and `research/daily/`
- **Purpose**: Distills key decisions, rejected alternatives, and quantitative pivots out of raw conversations.
- **Format**: Structured Markdown cards linking back to source transcripts.

### Layer 2: High-Density Conceptual Knowledge Mesh
- **Path**: `graphify-out/`
- **Purpose**: Semantic dependency graph of concepts, tools, capabilities, schemas, and invariants.
- **Invariant**: No conversational turn headers (`Turn X`, `User`, `Assistant`) may appear as independent semantic God nodes.

### Layer 3: Ephemeral Task State
- **Path**: `sim/task_telemetry.py` & active agent scratchpads.
- **Purpose**: Immediate working memory, resource telemetry, and task checkpointing.

---

## 3. Graphify Ingestion & Pruning Rules

1. **Transcript Summarization**: When archiving dialogues, `save-chat` outputs a structured title and turn count. Graphify extracts file-level summary tokens rather than generating an AST node per conversational turn.
2. **God Node Invariant**: A node with $>50$ degrees is only valid if it represents a core architectural entity (e.g., `Antigravity`, `sync.ps1`, `reconciliation_engine`, `CapabilityRegistry`, `SPARK`). Conversational markers are purged.
3. **Cluster Cohesion Threshold**: Knowledge graph community generation should target average cohesion $>0.60$ for architectural clusters.

---

## 4. Verification & Conformance

- **Deterministic Audit**: `sim/reconciliation_engine.py` validates that all RFCs and invariants conform to metadata standards without requiring Graphify to parse raw transcript turns.
- **Zero-Token Verification**: Memory stratification operates purely on deterministic file structure paths and explicit Markdown headers.
