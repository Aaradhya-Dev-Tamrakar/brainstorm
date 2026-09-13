# 📜 Architectural Invariant: INV-EPI-001 (Verbatim Conversational Logging)

> **Document ID:** `INV-EPI-001`  
> **Status:** Permanent Repository Invariant (`FORMALLY_ENFORCED`)  
> **Domain:** Epistemic Governance & Conversation History Preservation  
> **First Codified:** 2026-09-13  
> **Applies To:** `F:\Aaradhya-Dev-Tamrakar\brainstorm` and all interconnected tool modules  

---

## 1. The Core Invariant Statement

> **"In the `brainstorm` repository, every significant architectural brainstorming session, strategic pivot, and conceptual breakthrough MUST be exported verbatim from the engine's raw execution transcript and committed to `research/transcripts/` before the session is closed."**

---

## 2. Rationale & Epistemic Grounding

1. **Loss Prevention:** AI chat sessions across web interfaces, desktop clients, or IDE agents are ephemeral and vulnerable to truncation, deletion, or platform lock-in.
2. **Provenance & Defensibility:** High-level architectural discoveries (such as the ECIE Systems Architect paradigm, the Strangler-IPU 6G transition, or the $25k asset balance sheet) require an immutable audit trail to prove original authorship, human intent, and chronological genesis.
3. **Anti-Hallucination & Continuity:** Future agent sessions and subagents can read exact past dialogues rather than degraded, lossy summaries.

---

## 3. Mandatory Invariant Protocol

At the conclusion or major milestone of any significant conversation:
1. **Target Directory:** `research/transcripts/`
2. **File Naming Convention:** `YYYY-MM-DD_<PROJECT_OR_TOPIC_CODENAME>_CONVERSATION.md`
3. **Format Requirement:** Verbatim extraction of both User (`USER_INPUT`) and Assistant (`PLANNER_RESPONSE`) messages, complete with ISO timestamps.
4. **Index Requirement:** The new transcript must be linked in [`research/transcripts/README.md`](README.md) and referenced in the corresponding architectural spec (`research/architectures/`).
5. **Git Sync:** Must be staged, committed, and pushed to remote origin via `sync.ps1`.
