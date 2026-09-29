# Brainstorm Research Laboratory (BRL) — Contributor Agreement

**Version:** 1.0.0  
**Effective Date:** 2026-09-29  
**Authority:** [`PLAN-BRL-001`](PLAN-BRL-001_BRAINSTORM_RESEARCH_LAB_CHARTER.md)  
**Laboratory Director:** Aaradhya Dev Tamrakar  

---

## Preamble

The **Brainstorm Research Laboratory (BRL)** is an independent, artifact-driven engineering and scientific research collective. BRL operates on the principle that **technical credibility is earned through reproducible evidence, cryptographic commit history, and peer-reviewed outputs**, rather than nominal or unverified titles.

This Contributor Agreement establishes the rights, responsibilities, intellectual property boundaries, and operational standards for all contributors, research fellows, and student researchers participating in BRL research tracks and cohorts.

---

## 1. Permanent Public Attribution Invariant

1. **Authorship Guarantee:** Any code, dataset, simulation script, formal invariant proof, or technical report authored by a contributor will permanently bear their name and contribution record in:
   - Git commit history and signed release tags.
   - Project documentation and technical reports.
   - Academic papers, conference submissions, and workshop proceedings where the contributor met standard IEEE/ACM co-authorship criteria.
2. **Verification & Portfolio Rights:** Contributors retain the irrevocable right to cite their completed Quests, authored artifacts, and official BRL fellowship designation on their CVs, personal portfolios, and academic/employment applications. BRL will provide formal verification of completed deliverables upon request.

---

## 2. Tooling Boundary & Tripartite Asset Classification

To eliminate ambiguity between collaborative open science and laboratory infrastructure, all repository contents are categorized into three distinct operational asset tiers:

1. **Category I: OPEN RESEARCH ASSETS (`OPEN_RESEARCH_ASSETS`)**
   - **Scope:** Public research datasets (e.g. Nepali government corpus, Devanagari OCR samples), benchmark datasets, public domain state-machine models, and academic preprint drafts.
   - **License & Rights:** Released under permissive open licenses (Apache 2.0 / MIT / CC-BY 4.0). Contributors retain permanent co-authorship and public attribution.

2. **Category II: BRL INTERNAL OPERATING ASSETS (`BRL_OPERATING_ASSETS`)**
   - **Scope:** The central orchestration framework of `brainstorm`, the 23-module capability mesh, private automation engines (`sync.ps1`, `sync.bat`, `reconciliation_engine.py`, `audit.bat`, `audit.sh`), multi-account MCP bridges (`super-nlm`), and formal verification harnesses.
   - **Governance & Terms:** Proprietary laboratory infrastructure governed by BRL. Contributors receive a non-exclusive, non-transferable license to utilize these tools solely for executing authorized BRL Quests. Forking, mirroring, redistributing, or commercially rebranding core automation assets without express written consent from the Laboratory Director is strictly prohibited.

3. **Category III: PUBLIC VERIFICATION ARTIFACTS (`PUBLIC_VERIFICATION_ARTIFACTS`)**
   - **Scope:** Zero-discrepancy audit ledgers (`research/results/`), cryptographic verification certificates (`AaradhyaDT.github.io/verify/`), CI provenance logs, and the public merit ledger.
   - **Integrity & Access:** Irrevocably public, immutable, and cryptographically auditable for third-party verification of student competencies.

---

## 3. Epistemic Rigor & The "AI Trap" Policy

1. **Calibrated Evidence Tiers:** All technical statements must adhere to calibrated epistemic tiers (`ARCH-RFC-001`):
   - `FORMALLY_PROVEN`: Mechanically verified via SMT/Z3 solvers.
   - `EMPIRICALLY_VERIFIED`: Confirmed via deterministic, reproducible scripts.
   - `STATISTICALLY_OBSERVED`: Supported by benchmark runs with confidence intervals.
   - `HEURISTIC_HYPOTHESIS`: Plainly marked as unverified design or intuition.
2. **AI Tooling Guidelines:** Generative AI tools (LLMs, code assistants) are recognized as productivity enhancers. However, contributors are evaluated on **problem decomposition, data integrity, edge-case analysis, and deterministic verification**. Submitting unverified AI-generated text, fabricated citations, unrunnable code, or hallucinated benchmarks constitutes an immediate epistemic violation.

---

## 4. Conduct, Meritocracy & Culture

1. **Absolute Meritocracy:** All evaluations, quest assignments, rank promotions, and authorship orders are determined strictly by objective technical performance, code quality, and deliverable reproducibility.
2. **Universal Non-Discrimination:** BRL is committed to an open, merit-based environment free from identity politics, tokenism, or bias. Advancement is strictly decoupled from gender, ethnicity, or social standing; execution is the sole metric.
3. **Academic Integrity:** Plagiarism, data fabrication, intentional omission of prior art, or credential misrepresentation will result in immediate termination of fellowship standing and revocation of contributor status.

---

## 5. Bandwidth, Communication & The "No-Guilt" Pause

1. **Time Commitment:** Fellows commit to a realistic, self-selected bandwidth (typically 5–8 hours/week for active cohorts).
2. **Shared Communication:** Technical inquiries, environment bugs, and quest questions must be posted in the designated shared laboratory channel rather than private direct messages, ensuring transparent peer learning.
3. **Graceful Exit / Pause:** Contributors experiencing academic overloads, exam periods, or personal emergencies may invoke a `[PAUSE]` at any time without penalty or social friction. Completed work remains attributed; unfinished quests are safely reassigned.

## 6. Zero-Cost Merit Rewards & Progression Rights

1. **Deterministic Merit Ledger:** Contributor progress and Quest evaluations are recorded deterministically in [`research/fellows/merit_ledger.json`](../fellows/merit_ledger.json).
2. **Reward Eligibility:** Fellows who complete quests and demonstrate epistemic rigor earn verified institutional rewards at zero financial cost:
   - Official **Metric-Backed Letters of Recommendation (LOR)** signed by the IEEE KEC KTM Vice-Chair & BRL Director.
   - Publicly verifiable **Cryptographic Digital Certificates** hosted on `AaradhyaDT.github.io/verify/`.
   - Named **Academic Co-Authorship** or formal acknowledgments on research publications and datasets.
   - 1-on-1 systems architecture and debugging reviews for the fellow's personal/academic major projects.
   - **Cohort 1 Quest Lead** appointments.
3. **Zero Financial Obligations:** Fellows are never required to purchase software subscriptions, cloud credits, or specialized hardware. All tools and compute options are designed to function on generous free tiers (Kaggle 30h/wk GPU, Google AI Studio free tier, Google Colab).
4. **Physical Maker Space Policy:** In-person sprints hosted at KEC Makerspace adhere strictly to the college's First-Come, First-Served (FCFS) rules. All BRL quests remain 100% laptop-native and asynchronous, ensuring fellows are never bottlenecked by physical bench availability.

---

## 7. Acknowledgment & Sign-Off

By submitting the BRL Intake Form, executing Quest 0, or contributing code to BRL repositories, the contributor affirms that they have read, understood, and agreed to be bound by the terms of this Agreement.
