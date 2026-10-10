---
description: "This skill should be used when the user asks to 'write like claude', 'write an engineering blog post', 'write a model release report', 'draft a system card', 'create a technical announcement', 'write a developer migration guide', 'audit technical writing', 'write a case study', or mentions drafting publications, benchmarks, or safety dossiers in the calm-authority Anthropic voice."
---

# Writing Like Claude — The Calm Authority Engineering Standard

This skill codifies the technical writing philosophy, editorial mechanics, and publication standards of **Anthropic** across the full spectrum of technical communication: from engineering blog posts and developer tutorials (`claude.com/blog`, `platform.claude.com/docs`) to frontier model release reports, threat intelligence disclosures, and formal 144-page system cards (`anthropic.com/claude-haiku-5-5`, `Haiku 5.5 System Card`).

---

## 1. Core Philosophy: The Whiteboard Test & Empirical Proof

The foundation of Anthropic-style communication is **calm authority**:
> **Write like you are explaining a real system to a smart colleague at a whiteboard, or submitting an unredacted technical disclosure to a discerning safety auditor. Not selling. Not performing. Just explaining.**

Trust is governed by an immutable relationship:
$$\text{Trust} = \text{Precision} + \text{Scope Boundaries} + \text{Empirical Proof}$$

### The Three Pillars
1. **Functional Precision**: Define mechanisms by what they mechanically *are* and *do*, never with promotional jargon.
2. **Explicit Scope Boundaries**: Proactively declare what the system *cannot* do. Stating non-goals, failure modes, and out-of-scope tasks is the ultimate signal of technical credibility.
3. **Empirical Proof & Dog-Fooding**: Replace adjectives with verifiable operational metrics, standard pinned benchmark comparison tables, or 95% bootstrap confidence intervals.

---

## 2. Fast-Path Pre-Flight Decision Gate (Zero-Thinking Route)

Before drafting, identify the task requirement:

| Tier | Surface & Intent | Word Count | Action & Loaded Reference |
| :--- | :--- | :--- | :--- |
| **`L1`** | **Micro-Surface**: PR descriptions, README intros, portfolio project blurbs, commit notes. | 100–300 | **Fast-Path**: Execute directly using the 10 Invariants below. **Load 0 reference files**. |
| **`L2`** | **Editorial Narrative**: Engineering blog posts, internal dog-fooding case studies, GA product launches. | 800–1,500 | Load `references/narrative-and-case-studies.md`. |
| **`L3`** | **Technical Spec**: Developer tutorials, SDK architecture, model migration guides, API payloads. | 1,000–3,000 | Load `references/migration-and-developer-specs.md`. |
| **`L4`** | **Model Launch Dossier**: Frontier model releases, benchmark evaluations, Pareto cost tradeoffs. | 2,000–5,000 | Load `references/model-reports-and-benchmarks.md`. |
| **`L5`** | **Exhaustive System Card**: Formal safety cards, RSP catastrophic risk evaluations, behavioral audits. | 5,000–30,000+ | Load `references/system-cards-and-safety.md`. |

---

## 3. The 10 Universal Invariant Writing Rules

Every document drafted or audited under this skill must comply with these ten invariants:

1. **Title = Statement of Factual State**: Complete declarative sentence or precise noun phrase declaring what happened or what exists. Never use clickbait, numbered listicles, or emotional teases (*"Claude Haiku 5.5 is now available"* or *"How our sales team rebuilt inbound with Claude Managed Agents"*, not *"10 Incredible Features in Our New Release"*).
2. **1-Sentence Empirical Thesis**: The opening sentence must be a self-contained thesis stating the complete factual takeaway or quantifiable breakthrough.
3. **Strict Hype Blacklist & Active Verbs**: Total prohibition of marketing superlatives (*revolutionary, game-changing, groundbreaking, unleash, supercharge, seamless, cutting-edge, magic, effortlessly, next-gen*). Replace with measurable nouns and active verbs. Consult `references/vocabulary_cheatsheet.md`.
4. **Functional Precision in Definition**: Define any mechanism, feature, or tool in 10 to 15 concrete, mechanical words (*"Mods are small TypeScript functions that change CLI behavior"*).
5. **Explicit Scope Boundaries & Non-Goals**: Dedicate explicit prose to what the system *does not* do. Declare non-goals, unsupported configurations, and failure modes prominently.
6. **Standardized Empirical Grounding**: Back every claim with verifiable data. In model reports, use standardized Pinned Benchmark Grids (Subject, Predecessor, Competitor, Frontier Reference) with explicit qualifiers (`offline subset`, `no tools`, `with tools`, `Xhigh`).
7. **Multi-Objective Tradeoff & Pareto Transparency**: Acknowledge operational friction and costs. Present dual-axis Pareto frontiers (accuracy vs. cost on log scale) and effort setting curves (Low/Medium/High/Max).
8. **Sentence & Paragraph Geometry**: One idea per paragraph (1–4 sentences max). One action per sentence. Favor active voice with simple subjects.
9. **Deterministic, Verifiable Artifacts**: Code blocks must be copy-pasteable and runnable. Migration guides must contain before/after JSON request diffs. Reports must cite formal system cards.
10. **Actionable Next Steps over Redundant Summaries**: Never restate the introduction in the conclusion. Conclude with model IDs, CLI commands, documentation links, or open research questions.

---

## 4. Adaptive Execution Postures (Capability, Not Fundamentality)

Orchestration is an opt-in execution capability, not an inescapable overhead:

```
[Task Scope]
  ├── Default (90% of tasks) ──> Solo Direct Execution (Immediate, zero subagents)
  ├── Explicit /agent-teams ───> Multi-Agent Team (Scout -> Reviewer -> Writer -> Lead)
  └── Explicit /fleet-orch  ───> Headless Batch Swarm (SKU DAG -> Pooled Workers -> Drive Sync)
```

1. **Mode 1: Solo Direct Execution (Default)**:
   - For all L1 micro-tasks, standard blog posts, migration guides, and report drafts.
   - Executed directly by the primary agent with zero multi-agent coordination latency.
2. **Mode 2: Multi-Agent Team Capability (`/agent-teams-orchestration`)**:
   - For high-stakes research dossiers and system cards requiring independent adversarial audit.
   - Dispatches **Scout** (`research`, `flash`) for raw data $\rightarrow$ **Reviewer** (`self`, `pro`) for adversarial checks $\rightarrow$ **Writer** for synthesis.
   - Consult `references/swarm-and-fleet-capabilities.md`.
3. **Mode 3: Fleet Swarm Capability (`/fleet-orchestrator`)**:
   - For high-throughput batch evaluation suites and multi-model document pipelines.
   - Enqueues declarative SKU DAG `assets/sku-templates/model_report_pack.json` into `orchestrator-state/tasks/`.
   - Consult `references/swarm-and-fleet-capabilities.md`.

---

## 5. Ecosystem Compatibility Fast-Pointers

- **`compliance-report-harmonizer`**: When authoring Tier L5 compliance dossiers, adhere to the 5-section hierarchy and suppress cohorts with $n < 30$ using `.badge-guard` and `<details class="insufficient-block">`.
- **`portfolio-project-manager`**: When onboarding tools via `scripts/add_project.py`, generate exactly 3 active-verb, zero-hype bullet points matching Tier L1 format.
- **`github-workflow`**: Use Tier L1 format for PR descriptions (declarative title, 1-sentence thesis, test proof, non-goals) with authentic commit SHAs.
- **`super-nlm`**: Include `schema.org` JSON-LD and KaTeX math blocks to ensure clean ingestion into Google NotebookLM fleets.
- **`graphify`**: Ground research findings into the local Obsidian graph using `[[wikilinks]]`.
- Consult `references/ecosystem-compatibility.md` for complete cross-tool SOPs.

---

## 6. Deterministic Style Verification

Audit any document against calm authority standards using the local Python CLI:
```powershell
python "C:\Users\Aaradhya\.gemini\config\skills\writing-like-claude\scripts\audit_calm_writing.py" --tier L1 <path-to-file.md>
```

---

## 7. Additional Resources

### Modular Reference Guides (`references/`)
- **`references/adaptive-depth-guide.md`** — Comprehensive recipes and word counts for Tiers L1 through L5.
- **`references/vocabulary_cheatsheet.md`** — Complete banned hype list and calm authority replacements.
- **`references/narrative-and-case-studies.md`** — Structural formulas for engineering blogs and GA announcements.
- **`references/migration-and-developer-specs.md`** — API diffs, model ID syntax, and migration checklists.
- **`references/model-reports-and-benchmarks.md`** — Pinned benchmark tables, Pareto frontiers, and effort scaling.
- **`references/system-cards-and-safety.md`** — The 9-part System Card blueprint based on the 144p Haiku 5.5 release.
- **`references/governance-and-threat-models.md`** — Shared responsibility, grant tiers, and 30-day offline monitoring.
- **`references/swarm-and-fleet-capabilities.md`** — Execution protocols for `/agent-teams` and `/fleet-orchestrator`.
- **`references/ecosystem-compatibility.md`** — Complete integration SOPs across the 8 interacting ecosystem skills.

### Worked Reference Examples (`examples/`)
- **`examples/l1-portfolio-and-pr.md`** — Tier L1: Portfolio project manifest & PR description.
- **`examples/l2-blog-case-study.md`** — Tier L2: Engineering blog post & dog-fooding case study.
- **`examples/l3-migration-guide.md`** — Tier L3: Developer migration guide with JSON request diffs.
- **`examples/l4-model-launch-report.md`** — Tier L4: Haiku 5.5-style model release announcement.
- **`examples/l5-system-card-excerpt.md`** — Tier L5: Formal system card capability & alignment audit.
