# NotebookLM Grounding Source 07: BRL Fellowship, Guild Quest Engine & Onboarding

**Category:** Governance, Contributor Onboarding & Operational Protocol  
**Authority:** [`PLAN-BRL-001`](../plans/PLAN-BRL-001_BRAINSTORM_RESEARCH_LAB_CHARTER.md)  
**Laboratory Director:** Aaradhya Dev Tamrakar  
**Context:** Central Handbook for BRL Cohort 0 Fellows  

---

## 1. Laboratory Philosophy & The Artifact Standard

The **Brainstorm Research Laboratory (BRL)** is an independent research collective dedicated to sovereign systems engineering, formal invariant verification, and reproducible open-source tools.

At BRL, **credibility is defined by verifiable artifacts rather than nominal titles**. Every fellow's work is recorded in permanent cryptographic Git commits, signed release tags, and peer-reviewed technical dossiers.

---

## 2. The Guild Rank & Quest Engine

Contributors advance through five distinct ranks based strictly on deterministic proof of competence:

1. **Rank E (Research Scout):**
   - Focus: Baseline reproduction, raw dataset acquisition, environment sanity.
   - Core Quest: `QUEST-C0-00` (Dry-Run PR), `QUEST-C0-01` (Memory Simulator verification), `QUEST-C0-02` (Source census).
   - Gate: 100% bit-exact match with established golden outputs and schema validity.
2. **Rank D (Research Analyst):**
   - Focus: Failure-mode taxonomies, dataset cleaning, edge-case probing.
   - Core Quest: `QUEST-C0-03` (Devanagari legacy font transcoding corpus).
   - Gate: Zero schema violations, clean data normalization scripts.
3. **Rank C (Research Engineer):**
   - Focus: Tool adapters, module features, pipeline integrations.
   - Core Quest: `QUEST-C0-04` (Module telemetry profiling).
   - Gate: Passing `.\audit.bat` with 0 discrepancies, clean code review.
4. **Rank B (Research Fellow):**
   - Focus: SMT/Z3 formal invariant proofs, mathematical verification.
   - Gate: Formally proved invariants with 0% false discovery rate.
5. **Rank A (Senior Fellow):**
   - Focus: Architectural synthesis, conference authorship (IEEE/ACM).
   - Gate: Camera-ready LaTeX paper and accepted peer-reviewed artifact.

---

## 3. Git Workflow & The Branch Protection Invariant

1. **Never push to `main`:** All work must take place on isolated feature branches formatted as:
   `c0/<github_username>/<quest-id>`
2. **Branch Convention Examples:**
   - `c0/roshan-kc/quest-0`
   - `c0/anita-shrestha/quest-c0-02`
3. **The Zero-Discrepancy Audit Gate:**
   Before submitting any Pull Request, every contributor must run:
   ```powershell
   .\audit.bat
   ```
   If discrepancies or broken links exist, the PR will not be merged.
4. **Pull Requests:** All submissions must use the GitHub PR Template (`.github/PULL_REQUEST_TEMPLATE.md`), attaching a terminal snippet of the passing audit gate.

---

## 4. Communication & The "No-Guilt" Pause Protocol

1. **Zero Technical DMs:** All technical questions, environment setup bugs, and Git questions must be asked in the public group chat or opened as GitHub Issues. This ensures peer learning and prevents 1-on-1 tutoring bottlenecks.
2. **The `[PAUSE]` Rule:** If university coursework, midterm exams, or final semester vivas become overwhelming, fellows simply type `[PAUSE]` in the group chat. The quest is frozen immediately without penalty, guilt, or awkwardness. Lifetime credit for completed commits is permanently preserved.

---

## 5. Frequently Asked Questions (FAQ)

### Q: Can I use ChatGPT / Claude / Gemini for my quests?
**A:** Yes, as productivity tools. However, you are evaluated on **problem decomposition, data integrity, edge-case analysis, and deterministic execution**. Submitting unverified AI-generated text, fake citations, or unrunnable code constitutes an immediate failure of the audit gate.

### Q: What tools can I share or redistribute?
**A:** Datasets and benchmark papers you author under open research tracks are public. However, BRL's internal 23-module orchestration core and automation scripts are proprietary ecosystem assets and cannot be redistributed without written permission.

### Q: What happens if I fail an audit check?
**A:** Run `.\audit.bat` locally. The terminal output will point out the exact file and line number causing the issue (e.g., broken markdown link, syntax error, or failing unit test). Fix the reported issue and re-run.
