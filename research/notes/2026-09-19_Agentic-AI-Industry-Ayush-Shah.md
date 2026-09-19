# 2026-09-19 — Guest Lecture: Agentic AI in Industry (Ayush Kumar Shah, Meta)

**Date & Time:** 2026-09-19 09:45 – 10:36 NPT (GMT+5:45)  
**Speaker:** Ayush Kumar Shah (Software Engineer, Meta)  
**Contacts:** `aykumars07@gmail.com` | `shahayush@meta.com` | [LinkedIn](https://linkedin.com/in/ayush7) | [Website](https://shahayush.com)  
**Host / Program:** Fusemachines AI Fellowship / Community Guest Lecture (68 Slides Total)  
**Linked Projects:** [[research/architectures/ARCH-RFC-003-CAPSTONE-DEFENSE-STANDARD|BiasAperture (Fuse AI)]] | [[research/architectures/ARCH-RFC-001-RECORD-KEEPING-STANDARDS|Ecosystem Provenance]]  
**Verification Gate (Slide 37):** PASSED — Full slide deck captured (Slides 32–68), timestamps verified, code/skill artifacts compiled, linked to Obsidian graph.

---

## 1. Executive Summary
Ayush Kumar Shah presented practical patterns for implementing **Agentic AI workflows in personal and industrial engineering**, bridging Andrej Karpathy's compiled knowledge base concept with Tiago Forte's PARA framework and Obsidian-based automation loops.

---

## 2. Key Frameworks & Architecture Covered

### A. Karpathy's LLM-Maintained Personal Wiki (Slide 32)
* **Moving Beyond Ephemeral RAG:** Traditional vector RAG breaks on cross-document synthesis. Karpathy proposes treating the LLM as an **autonomous librarian** that compiles raw sources (papers, web, articles) into a persistent, interconnected Markdown wiki using `[[wikilinks]]`.
* **The Compounding Loop:** *"Useful answers become new pages."* Non-trivial insights generated in Q&A sessions are synthesized back into the wiki as first-class concept nodes.
* **Human-in-the-loop Grounding:** Obsidian serves as the local visual inspection layer (interactive graph view).

### B. PARA Organizes Knowledge Around Action (Slide 33)
* Organizing by *topic* ("AI", "Physics") creates digital graveyards. Knowledge must be organized by **actionability and time-horizon**:
  1. **Projects:** Active efforts with deadlines and completion criteria (e.g. *Fuse fellowship session*, *BiasAperture defense*).
  2. **Areas:** Ongoing responsibilities with standards to maintain (e.g. *Research practice*, *Ecosystem health*).
  3. **Resources:** Reference materials, tools, datasets, techniques.
  4. **Archive:** Completed, inactive, or superseded assets.

### C. Obsidian as the Shared Markdown Workspace (Slide 34)
* **Readable files:** Both human and AI agents read/write the identical plain `.md` files. Zero vendor lock-in.
* **Connected context:** Graph view and bidirectional links expose emergent relationships.
* **Reusable structure:** Templater + Daily Notes automate scaffolding.

### D. The Daily Automation Loop (Slide 35 & 36)
$$\text{Daily Note (Template)} \longrightarrow \text{Meeting Notes} \longrightarrow \text{Route to Projects} \longrightarrow \text{Daily Learnings} \longrightarrow \text{Tomorrow's Context}$$
* **Invariant:** *"Source links stay beside imported claims."* (Matches `ARCH-RFC-001` epistemic provenance).

### E. The Three Daily Guardrail Jobs (Slide 37)
| Trigger | Concrete Output | Check Before Finishing |
| :--- | :--- | :--- |
| **Start of day** | Today's note + schedule draft | Correct local date and timezone |
| **After meetings** | Notes linked to matching project | Source ID, owner, and duplicate check |
| **End of day** | Learning summary + tomorrow's context | Evidence links and unresolved questions |

### F. High-Bandwidth Input & Remote Control (Slides 41–44)
* **Voice-to-Agent Bandwidth (Slide 43):** Dictation into CLI prompts (`Claude Code /voice`, Superwhisper, Wispr Flow) leaps from 60 WPM (typing) to 150 WPM (speech).
* **Remote Session Telemetry (Slide 44):** `claude remote-control` allows starting an agent session on desktop, scanning a QR code, and monitoring/guiding from mobile while compute stays on bare-metal local hardware.

### G. Asynchronous Overnight Execution & Multi-Agent Swarms (Slides 45–47)
* **"I sleep. The machine stays awake" (Slide 45):** Bounded overnight tasks. Decoupling human hours from progress requires: (1) Evening task briefing, (2) Bounded execution, (3) Morning human review.
* **The Multi-Agent Triad Prompt (Slide 47):**
  - **Scout:** Find papers, code symbols, source IDs.
  - **Reviewer:** Adversarial skeptic challenging claims and limitations.
  - **Writer:** Drafts strictly from reviewed evidence.
  - **Lead:** Owns final delivery, arbitrates conflicts, enforces hard stop criteria.
  - **Invariant:** *"Use separate working files."* / isolated worktrees to prevent concurrency race conditions.

### H. Deterministic Security & Sandboxing (Slide 52)
* **"Permissions live outside CLAUDE.md":** Never rely on LLM prompts for security. Hard runtime enforcement outside the prompt (`settings.json` / `config.json`):
  - `allow`: Non-destructive commands (`npm test`, `pytest`).
  - `ask`: Mutating / external actions (`git push`, schema migration).
  - `deny`: Hard block on sensitive files (`.env`, credentials, private keys).

### I. Agent Self-Learning & Edge Realities at Meta (Slides 54 & 56)
* **"Changed behavior does not imply changed model weights" (Slide 54):** Production agent improvement happens by updating externalized memory, prompts, and skills (`preferences.md`, `SKILL.md`), followed by regression replay—NOT expensive, destabilizing weight retraining.
* **Edge Inference via ExecuTorch (Slide 56):** Billion-user scale cannot stream all frames/audio to cloud GPUs. On-device models (Instagram Cutouts via ExecuTorch, WhatsApp bandwidth estimators) minimize latency and compute bills. Direct mirror to our `SPARK` 18.5 KB INT8 CNN on ESP32-S3.

### J. Industrial Rollout & Production Failure Matrix (Slides 57–60)
* **The 5 Rollout Stages (Slide 57):** `Offline` $\rightarrow$ `Shadow` (dark launch) $\rightarrow$ `Canary` (1%) $\rightarrow$ `Staged` ($10\% \rightarrow 50\%$) $\rightarrow$ `Everyone` (behind feature flag). *"Every stage can stop the rollout."*
* **"An offline win is only a hypothesis" (Slide 58):**
  - Eval accuracy $\rightarrow$ Must prove distribution hasn't drifted.
  - Average quality $\rightarrow$ Must prove important cohorts stay within guardrails (**`BiasAperture`** thesis).
  - Model quality $\rightarrow$ Must fit physical latency & memory budgets (**`SPARK`** / **`NovaOptimizer`**).
* **Meta HawkEye Testing Matrix (Slide 60):**
  - *Model Quality:* Regression tests and slice/cohort audits.
  - *Device/Traffic:* p95/p99 latency, weak networks, bursts.
  - *Data/Dependencies:* Stale features, timeouts, schema drift.
  - *Agent Behavior:* Tool selection failures, looping actions, ungrounded claims.
  - *Recovery:* Kill-switch rehearsals, automated rollbacks, and graceful degradation.

### K. Pre-Release Risk Scoring & Bounded Triage Agents (Slides 61 & 63)
* **Meta Diff Risk Score (Slide 61):** Code diff + metadata $\rightarrow$ AI-predicted risk score and suspect snippets. Focuses human reviewer attention on high-risk blast radiuses. Enabled 10,000+ changes during sensitive 2024 events without outages. *"Risk prediction does not certify a change."*
* **Bounded Triage Agent Architecture (Slide 63):**
  - *Sandbox Guards:* Strictly **read-only tools**, hard time/step budget, complete audit logging.
  - *Parallel SRE Investigation:* Alert $\rightarrow$ Route $\rightarrow$ parallel fetch of `Logs`, `Recent Diffs`, and `Runbooks` $\rightarrow$ Evidence Synthesis $\rightarrow$ Triage Report.
  - *The Human Boundary:* *"Autonomous investigation ends at a reviewable report" $\rightarrow$ "Engineer decides."*
  - *Closed Loop:* Human's reviewed resolution feeds back into updated runbooks.

### L. Karpathy's `autoresearch` Experiment Loop (Slides 65–67)
* **Autonomous Research Engine (`github.com/karpathy/autoresearch`):**
  $$\text{program.md (Brief)} \longrightarrow \text{Hypothesis} \longrightarrow \text{Edit train.py} \longrightarrow \text{Train 5 mins} \longrightarrow \text{Eval val\_bpb} \longrightarrow \begin{cases} \text{Keep improvement} \\ \text{Revert otherwise} \end{cases}$$
* **Empirical Run Dynamics (Slide 67):**
  - **83 Total Experiments $\rightarrow$ 15 Kept (18%) vs. 68 Discarded (82%).**
  - Validation BPB dropped systematically from `0.998` to `0.978`.
  - Discovered breakthroughs: batch-size halving, LR warmup/warmdown schedules, decoupled embedding/unembedding LRs, sliding window attention, and RoPE base frequency scaling ($10\text{k} \rightarrow 200\text{k}$).
* **Core Takeaways:**
  1. *Failure is the baseline (82% failure rate).* The differentiator is automated, costless `git revert`.
  2. *Human owns objective, budget, and held-out test.*
* **Ecosystem Parallels:** Directly matches our repository structure:
  - `research/hypotheses/` (Falsifiable hypothesis cards)
  - `research/experiments/` (Executed empirical results)
  - `research/failures/` (Documented regressions and negative results)
  - Three-Output Rule in `AGENTS.md` (mandatory termination in executable artifacts).

---

## 3. Integration into the `brainstorm` Capability Mesh

1. **Templates Deployed:**
   - Daily Note: `[[templates/daily-note]]`
   - Meeting Note: `[[templates/meeting-note]]`
2. **Persistent Antigravity Skill Activated:**
   - Saved `[[C:/Users/Aaradhya/.gemini/config/skills/agent-teams-orchestration/SKILL.md|agent-teams-orchestration]]` and wired it into `/teamwork-preview` globally across all workspaces.
3. **Graph Connection:**
   - This note integrates directly into the `brainstorm` Obsidian graph, connecting industrial Meta engineering practices directly to our **`ARCH-RFC-001`** provenance standard, **`ARCH-RFC-002`** Multi-Model Council, and **`ARCH-RFC-003`** Fuse capstone defense.

---

## 4. Q&A Exchange: Aaradhya Dev Tamrakar & Ayush Kumar Shah

### Aaradhya's Question:
> *"What use cases do you think locally hosted models shine as of now? And if it's a part of your workflow, where do you use them? And what is your usual workflow, in day-to-day life in and out of work—with and without AI?"*

### Ayush's Ground-Truth Answer & Core Takeaways:

1. **On Locally Hosted vs. Frontier Cloud Models:**
   - **Rarely uses local models compared to frontier LLMs:** For non-trivial reasoning, literature synthesis, and systems engineering, frontier cloud models remain substantially superior.
   - **The Strict Air-Gap Scenario:** Local models are deployed primarily for simple tasks or sensitive scenarios where private/confidential files cannot be legally or ethically sent to third-party cloud APIs due to zero privacy guarantees.

2. **Daily Workflow — With AI:**
   - **High-Velocity Aggregation:** Daily catch-ups, paper overviews, routine script automations, and structuring meeting notes.
   - **Variance Generation:** Using agents as broad idea engines that propose multiple implementation pathways.

3. **Daily Workflow — Without AI (Manual Deep Work):**
   - **Human Taste & Discernment:** Manually reviews AI output digests and **cherry-picks the viable ideas**, discarding the noise.
   - **First-Principles Ideation:** Generating original architectural ideas independently before consulting models.
   - **Deep Domain Mastery:** Invested deep manual study into **video codecs** (essential for WhatsApp calling, Instagram media, and bandwidth optimization). *Insight:* Without deep underlying domain mastery, an engineer cannot evaluate whether an AI's proposed solution is sound or catastrophic.
   - **Reward Engineering:** Spends manual cognitive effort designing **reward functions and feedback signals for Reinforcement Learning (RL)**—framing the objective so models improve iteratively rather than manually coding algorithmic edge cases.
