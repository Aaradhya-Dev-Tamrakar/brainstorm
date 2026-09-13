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

---

## 4. Operational Recognition & Automation Criteria

How does the repository automatically distinguish a **"significant architectural session"** from casual banter or quick syntax questions?

A session is classified as **Significant / Archival-Mandatory** if it satisfies **ANY** of these three deterministic conditions:

1. **Explicit Directive Trigger:**
   - The user or assistant mentions keywords: `"log this"`, `"archive this"`, `"record verbatim"`, or assigns a project `"codename"` / `"codeword"`.
2. **Architectural Artifact Genesis:**
   - Any commit that creates or updates a document in `research/architectures/` (`ARCH-SPEC-xxx`), `research/invariants/` (`INV-xxx`), or `sim/`.
3. **Cognitive Density Threshold:**
   - The dialogue exceeds $\ge 5$ user turns and contains $\ge 3$ domain architectural keyword hits (`"architect"`, `"channel"`, `"capacity"`, `"chasm"`, `"6G"`, `"IPU"`, `"coalescing"`).

### Automated Archival Utility
The repository maintains [`sim/transcript_archiver.py`](../../sim/transcript_archiver.py) to automatically inspect the current conversation, evaluate significance against these thresholds, and export the verbatim Markdown record with one command:

```powershell
python .\sim\transcript_archiver.py --auto
```

