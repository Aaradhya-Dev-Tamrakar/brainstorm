# Adaptive Depth Guide: Calibrating Tiers L1 Through L5

This guide defines the structural mechanics, word count constraints, required sections, and artifact requirements across the 5 Depth Tiers of the `writing-like-claude` engine.

---

## Tier Summary Matrix

| Tier | Name | Target Words | Primary Surface | Structural Focus | Artifact Requirement |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`L1`** | **Micro** | 100–300 | PR descriptions, README intros, portfolio blurbs | 1-Sentence Thesis, 3–4 Imperative Bullets, Explicit Scope Non-Goals | 1 Minimal code snippet or CLI command |
| **`L2`** | **Editorial** | 800–1,500 | Engineering blog posts, internal case studies | Whiteboard Test, Before State, Architecture, Warts & Failures | System interaction diagram (Mermaid) |
| **`L3`** | **Technical Spec** | 1,000–3,000 | Migration guides, API docs, SDK references | Request Before/After Payloads, Parameter Diffs, Checklist | Functional JSON request diffs & model IDs |
| **`L4`** | **Model Launch** | 2,000–5,000 | Frontier model release announcements | Model ID Pill, Pinned Benchmark Grid, Pareto Curves, Pricing | Markdown comparison table with standard baselines |
| **`L5`** | **System Card** | 5,000–30,000+ | Formal safety cards, regulatory compliance dossiers | 9-Part Safety Blueprint, RSP Thresholds, Behavioral Audits | Refusal curves, empirical confidence intervals |

---

## 1. Tier L1: Micro-Surface Specification (100–300 Words)

Used for rapid, high-impact surfaces: GitHub Pull Request descriptions, README overviews, portfolio project manifests (`add_project.py`), and conventional commit bodies.

### Structural Recipe:
1. **Title**: Complete declarative sentence or conventional commit scope (`feat(scope): declarative summary`).
2. **1-Sentence Thesis**: Exactly what changed, what was solved, or what was released.
3. **Core Capabilities / Changes**: 3 to 4 bullet points. Every bullet **must start with an active imperative verb** (*"Expose"*, *"Enforce"*, *"Suppress"*, *"Route"*, *"Compile"*).
4. **Minimal Runnable Artifact**: One 3-line CLI command or copy-pasteable configuration block.
5. **Explicit Non-Goals / Scope Cut**: One sentence explicitly stating what this change does **not** touch or solve.

---

## 2. Tier L2: Editorial Narrative Specification (800–1,500 Words)

Used for public engineering blogs (`claude.com/blog`), technical retrospectives, and internal dog-fooding case studies.

### Structural Recipe:
1. **Title**: *"How [Team] [Solved/Rebuilt X] with [System/Tool]"* or factual state change.
2. **1-Sentence Thesis Subtitle**: Concrete takeaway and organizational impact.
3. **The Before State**: Specific friction numbers (e.g. queue latency, failure rate, headcount hours).
4. **System Architecture**: High-level mechanical breakdown accompanied by a clean Mermaid diagram.
5. **Empirical Outcomes**: Quantifiable before/after metrics ($n$ inquiries handled, percentage speedup).
6. **Warts, Edge Cases & Iterations**: Candid disclosure of what broke during early testing and how the architecture adapted.
7. **Actionable Takeaways / Next Steps**: Concrete next steps or documentation links. Zero redundant summary conclusions.

---

## 3. Tier L3: Developer Technical Spec & Migration Guide (1,000–3,000 Words)

Used for platform documentation (`platform.claude.com/docs`), SDK integration manuals, and model version migration guides.

### Structural Recipe:
1. **Title**: *"[Model/Tool] Migration Guide"* or *"Integrating [Feature] via [SDK]"*.
2. **Exact Model Identifiers**: Dedicated code pills with copyable model strings (e.g. `claude-haiku-5-5-20261001`).
3. **Breaking Changes Matrix**: Clean tabular comparison of deprecated vs. replacement parameters.
4. **Before & After Request Diffs**: Side-by-side or consecutive JSON/TypeScript payloads showing exact payload changes.
5. **Parameter Migration Mechanics**: Explicit guidance on new capability parameters (e.g. `effort: low|medium|high`, prompt caching tokens).
6. **Step-by-Step Migration Checklist**: Checkbox list (`- [ ]`) categorized by starting baseline model.

---

## 4. Tier L4: Frontier Model Launch Dossier (2,000–5,000 Words)

Used for major model launch reports (`anthropic.com/claude-haiku-5-5`).

### Structural Recipe:
1. **Eyebrow & Date**: Factual release timestamp and model class badge.
2. **Model Name & ID Pill**: Canonical display name with copyable API identifier.
3. **1-Sentence Thesis**: Singular quantifiable advancement (e.g. *"Cheapest, fastest small model costing 75% less to run"*).
4. **Target Workloads & Subagent Pairing**: 2–3 paragraphs defining optimal use cases and orchestration pairings.
5. **Pinned Benchmark Comparison Grid**:
   - Pinned candidate column (highlighted).
   - Predecessor baseline column.
   - SOTA Competitor column.
   - Frontier reference column labeled *"For reference"*.
   - Explicit condition qualifiers (`offline subset`, `no tools`, `with tools`, `Xhigh`).
6. **Multi-Objective Tradeoffs & Pareto Frontier**:
   - Accuracy vs. Cost (USD per attempt on log scale).
   - Effort setting scaling curves across benchmarks.
7. **Pricing & Economic Structure**: Clear table detailing input tokens, output tokens, and prompt caching write/read pricing.
8. **Safety & Verification Program Access**: Summary of ASL status and access tiers (Standard vs. High-Risk).
9. **Mandatory System Card Citation**: Footnote or link pointing to the full underlying evaluation document.

---

## 5. Tier L5: Exhaustive System Card & Safety Evaluation (5,000–30,000+ Words)

Used for comprehensive regulatory filings, safety institute disclosures, and formal model system cards (modeled on the 144-page Haiku 5.5 release).

### Structural Recipe (The 9-Part Safety Blueprint):
1. **Executive Summary & Key Claims**: Core metrics, ASL level, and primary findings.
2. **Training Data, Crowd Workers & Provenance**: Human annotator compensation, data filtering, and usage policies.
3. **Responsible Scaling Policy (RSP) & Catastrophic Risks**:
   - Chemical & Biological (CB-1 and CB-2 evaluations).
   - Autonomy & AI R&D capabilities (AECI trajectories).
   - Alignment risk update and ASL determination.
4. **Cyber Offense & Defense Capabilities**:
   - ExploitBench, CyScenarioBench, OSS-Fuzz, and ExploitGym results.
5. **Harmlessness, Refusals & Societal Safeguards**:
   - Single-turn and multi-turn harmful request evaluation curves.
   - False refusal rates on benign prompts.
   - Child safety, mental health, political bias, and election integrity evaluations.
6. **Agentic Safety & Surface Vectors**:
   - Malicious use testing across coding and computer use surfaces.
   - Prompt injection robustness across coding, computer, and browser surfaces.
7. **Alignment Assessment & Automated Behavioral Audits**:
   - Propensity to mislead, uncooperative behavior, sandbox escape attempts.
   - Honesty and factual hallucination evaluations.
   - Reliability of assessment: verbalized grader awareness and secret-keeping under pressure.
8. **Model Welfare Assessment**:
   - Affect in training and deployment, attitudes toward mistakes, automated interview transcripts.
9. **Empirical Capabilities & Benchmark Dossier**:
   - Full evaluation breakdown across SWE-bench, Terminal-Bench, Humanity's Last Exam, Chartography, OSWorld, and specialized domain benchmarks.
