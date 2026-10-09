# Calm Authority Writing Standards — Field Reference Guide

This guide codifies the Anthropic technical writing standard, editorial mechanics, and deterministic verification protocols defined in `writing-like-claude`.

---

## 1. Core Philosophy: The Whiteboard Test & Trust Equation

Anthropic-style technical communication is governed by **calm authority**:
> *Write like you are explaining a real system to a smart colleague at a whiteboard, or submitting an unredacted technical disclosure to a discerning safety auditor. Not selling. Not performing. Just explaining.*

### The Trust Equation
$$\text{Trust} = \text{Precision} + \text{Scope Boundaries} + \text{Empirical Proof}$$

### The Three Pillars
1. **Functional Precision**: Define mechanisms by what they mechanically *are* and *do*, never with promotional jargon or marketing abstraction.
2. **Explicit Scope Boundaries**: Proactively declare what the system *cannot* do. Stating non-goals, failure modes, and unsupported edge cases builds credibility.
3. **Empirical Proof & Dog-Fooding**: Replace subjective adjectives with verifiable operational metrics, pinned benchmark tables, or 95% bootstrap confidence intervals ($n \ge 30$).

---

## 2. Fast-Path Pre-Flight Decision Gate (Tiers L1–L5)

Select the target tier before drafting:

| Tier | Surface & Intent | Word Count | Action & Loaded Reference |
| :--- | :--- | :--- | :--- |
| **`L1`** | **Micro-Surface**: PR descriptions, README intros, portfolio project blurbs, commit notes. | 100–300 | **Fast-Path**: Zero reference files loaded. Enforce 1-sentence thesis, 3–4 imperative bullets, 1 minimal artifact, explicit non-goal. |
| **`L2`** | **Editorial Narrative**: Engineering blogs, internal dog-fooding case studies, GA product launches. | 800–1,500 | Load `references/narrative-and-case-studies.md`. Cover Before State, Architecture, Outcomes, and Warts/Failures. |
| **`L3`** | **Technical Spec**: Developer tutorials, SDK architecture, migration guides, API payloads. | 1,000–3,000 | Load `references/migration-and-developer-specs.md`. Include before/after JSON request diffs and migration checklist. |
| **`L4`** | **Model Launch Dossier**: Frontier model releases, benchmark evaluations, Pareto tradeoffs. | 2,000–5,000 | Load `references/model-reports-and-benchmarks.md`. Include Model ID pill, Pinned Benchmark Grid, Pareto curves, and pricing. |
| **`L5`** | **Exhaustive System Card**: Formal safety cards, RSP catastrophic risk evaluations, behavioral audits. | 5,000–30,000+ | Load `references/system-cards-and-safety.md`. Enforce 9-Part Safety Blueprint (RSP, Cyber, Harmlessness, Welfare, Benchmarks). |

---

## 3. The 10 Universal Invariant Writing Rules

All publications must strictly satisfy the 10 universal invariants:

1. **Title = Statement of Factual State**: Complete declarative sentence or precise noun phrase declaring what happened or exists (*"Claude Haiku 5.5 is now available"* or *"How our sales team rebuilt inbound with Claude Managed Agents"*). Never use clickbait, numbered listicles, or emotional teases.
2. **1-Sentence Empirical Thesis**: Opening sentence must be an autonomous factual takeaway or quantifiable breakthrough.
3. **Strict Hype Blacklist & Active Verbs**: Total prohibition of marketing superlatives. Replace with concrete nouns and active verbs.
4. **Functional Precision in Definition**: Define any mechanism, feature, or tool in **10 to 15 concrete, mechanical words** (*"Mods are small TypeScript functions that change CLI behavior"*).
5. **Explicit Scope Boundaries & Non-Goals**: Proactively declare what the system *does not* do, unsupported configurations, and failure modes.
6. **Standardized Empirical Grounding**: Back claims with verifiable data. In model reports, use standardized Pinned Benchmark Grids (Subject, Predecessor, Competitor, Frontier Reference) with explicit condition qualifiers (`offline subset`, `no tools`, `with tools`, `Xhigh`).
7. **Multi-Objective Tradeoff & Pareto Transparency**: Disclose operational friction. Present dual-axis Pareto frontiers (accuracy vs. cost on log scale) and effort scaling curves (`effort: low | medium | high | max`).
8. **Sentence & Paragraph Geometry**: One idea per paragraph (1–4 sentences maximum). One action per sentence. Favor active voice with simple subjects.
9. **Deterministic, Verifiable Artifacts**: Code blocks must be runnable and copy-pasteable. Migration guides must contain before/after request diffs. Reports must cite formal system cards.
10. **Actionable Next Steps over Redundant Summaries**: Never restate the introduction in the conclusion. Conclude with copyable model identifiers, CLI commands, documentation links, or open research questions.

---

## 4. Complete Banned Hype Words & Calibrated Lexicon

### Banned Hype Blacklist & Replacements

| Prohibited Superlative | Anthropic Calm-Authority Replacement |
| :--- | :--- |
| *Revolutionary / Groundbreaking* | Factual functional description (*"A diagnostic framework for..."*) |
| *Game-changing / Paradigm shift* | Quantified capability delta (*"Reduces evaluation latency by 75%"*) |
| *Seamless / Seamlessly* | Explicit protocol specification (*"Connects via REST API and prediction CSVs"*) |
| *Unleash / Supercharge / Turbocharge* | Measurable operational action (*"Enables", "Processes", "Evaluates"*) |
| *Next-generation / Next-gen / Cutting-edge* | Specific model ID or release version (*"Claude Haiku 5.5"*) |
| *State-of-the-art (SOTA)* | Pinned benchmark citation (*"Scored 72.4% on OSWorld 2.1 offline subset"*) |
| *Magic / Effortlessly* | Deterministic operational logic (*"Executes via non-blocking async event loops"*) |
| *Ultra-fast / Lightning-fast* | Exact empirical metric (*"Processes 10,000 tokens in 1.4 seconds"*) |
| *Eliminates all bias / 100% safe* | Empirical boundary definition (*"Quantifies disparity across four demographic metrics"*) |
| *We are thrilled / excited to announce* | Factual declarative state change (*"[Feature] is now generally available"*) |
| *Unprecedented power / Boasts performance* | Verifiable score (*"Scores 45.9% on Humanity's Last Exam (no tools)"*) |
| *Empowers developers to unlock* | Direct technical capability (*"Exposes typed interfaces for browser tool calls"*) |

### Calibrated Scientific & Regulatory Terminology
- **Harmonized**: Differing backend primitives or regulatory standards reconciled into unified point estimates.
- **Standardized**: Complies with immutable schema contracts ($n < 30$ suppression, 95% bootstrap CIs).
- **Uniform**: Visual geometry, card hierarchy, and badge semantics remain identical across formats.
- **Interoperable**: Operates simultaneously across web, paginated print PDF, and JSON-LD schema.
- **Cohesive**: Narrative text, empirical whiskers, and governance cards fit together without contradiction.
- **Refusal Rate**: Percentage of malicious requests correctly rejected by safety classifiers.
- **False Refusal Rate**: Percentage of benign requests erroneously blocked by over-cautious safeguards.
- **Grader Awareness**: Model telemetry detecting that an interaction is part of a benchmark evaluation.
- **Pareto Frontier**: Multi-objective tradeoff boundary where accuracy cannot improve without degrading cost.
- **Effort Setting**: Scalable computational budget allocation (`effort: low | medium | high | max`).

---

## 5. Deterministic Verification CLI

Audit markdown documents against calm authority invariants and regex patterns using `audit_calm_writing.py`:

```powershell
# Audit a single file enforcing a specific depth tier
python "F:\Aaradhya-Dev-Tamrakar\brainstorm\.agents\skills\writing-like-claude\scripts\audit_calm_writing.py" --tier L1 <path-to-file.md>

# Alternative path via Gemini configuration root
python "C:\Users\Aaradhya\.gemini\config\skills\writing-like-claude\scripts\audit_calm_writing.py" --tier L1 <path-to-file.md>

# Batch audit all markdown files in a directory
python "F:\Aaradhya-Dev-Tamrakar\brainstorm\.agents\skills\writing-like-claude\scripts\audit_calm_writing.py" --all <path-to-dir>
```

### Automated Invariant Checks
1. **Hype Word Scan**: Regex matching against prohibited words (`\brevolutionary\b`, `\bgame-changing\b`, `\bgroundbreaking\b`, `\bunleash(es|ing)?\b`, `\bsupercharged?\b`, `\bturbocharge\b`, `\bseamlessly\b`, `\bcutting-edge\b`, `\bnext-gen(eration)?\b`, `\beffortlessly\b`, `\bmagical\b`, `\bwe are (thrilled|excited)\b`, `\bunprecedented power\b`).
2. **Word Count Compliance**: Enforces tier budget limits (e.g., L1 $\le 500$ words).
3. **Structural Verification**:
   - **L1**: Requires imperative bullet points and non-goal statements.
   - **L2**: Enforces empirical operational metrics (`\d+%`, latency, volume).
   - **L3**: Enforces code blocks (`json`, `typescript`, `python`) and before/after diffs.
   - **L4**: Enforces Pinned Benchmark tables with baseline comparison columns.
   - **L5**: Enforces evaluation, audit, refusal, and safety sections.
