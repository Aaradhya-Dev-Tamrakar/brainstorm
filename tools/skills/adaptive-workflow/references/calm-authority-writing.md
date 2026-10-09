# Calm Authority Engineering Standard

This document codifies the technical writing philosophy, editorial mechanics, and publication standards of **Anthropic** across technical communication, documentation, PR descriptions, and system cards.

---

## 1. Core Philosophy: The Whiteboard Test & Empirical Proof

The foundation of calm authority communication is:
> **Write like you are explaining a real system to a smart colleague at a whiteboard, or submitting an unredacted technical disclosure to a discerning safety auditor. Not selling. Not performing. Just explaining.**

$$\text{Trust} = \text{Precision} + \text{Scope Boundaries} + \text{Empirical Proof}$$

### The Three Pillars:
1. **Functional Precision**: Define mechanisms by what they mechanically *are* and *do*, never with promotional adjectives.
2. **Explicit Scope Boundaries**: Proactively declare what the system *cannot* do. Stating non-goals, failure modes, and out-of-scope configurations is the ultimate signal of technical credibility.
3. **Empirical Proof & Dog-Fooding**: Replace superlatives with verifiable operational metrics, standard pinned benchmark comparison tables, or 95% bootstrap confidence intervals.

---

## 2. Fast-Path Pre-Flight Decision Gate (Tiers L1–L5)

| Tier | Surface & Intent | Word Count | Action & Loaded Reference |
| :--- | :--- | :--- | :--- |
| **`L1`** | **Micro-Surface**: PR descriptions, README intros, portfolio project blurbs, commit notes. | 100–300 | **Fast-Path**: Execute directly using the 10 Invariants. Load 0 reference files. |
| **`L2`** | **Editorial Narrative**: Engineering blog posts, internal dog-fooding case studies, GA product launches. | 800–1,500 | Load `references/narrative-and-case-studies.md`. |
| **`L3`** | **Technical Spec**: Developer tutorials, SDK architecture, model migration guides, API payloads. | 1,000–3,000 | Load `references/migration-and-developer-specs.md`. |
| **`L4`** | **Model Launch Dossier**: Frontier model releases, benchmark evaluations, Pareto cost tradeoffs. | 2,000–5,000 | Load `references/model-reports-and-benchmarks.md`. |
| **`L5`** | **Exhaustive System Card**: Formal safety cards, RSP catastrophic risk evaluations, behavioral audits. | 5,000–30,000+ | Load `references/system-cards-and-safety.md`. |

---

## 3. The 10 Universal Invariant Writing Rules

1. **Title = Statement of Factual State**: Complete declarative sentence or precise noun phrase declaring what happened or what exists. Never use clickbait, numbered listicles, or emotional teases.
2. **1-Sentence Empirical Thesis**: The opening sentence must be a self-contained thesis stating the complete factual takeaway or quantifiable breakthrough.
3. **Strict Hype Blacklist & Active Verbs**: Total prohibition of marketing superlatives (`revolutionary`, `game-changing`, `groundbreaking`, `unleash`, `supercharge`, `seamless`, `cutting-edge`, `magic`, `effortlessly`, `next-gen`).
4. **Functional Precision in Definition**: Define any mechanism, feature, or tool in 10 to 15 concrete, mechanical words.
5. **Explicit Scope Boundaries & Non-Goals**: Dedicate explicit prose to what the system *does not* do. Declare non-goals, unsupported configurations, and failure modes prominently.
6. **Standardized Empirical Grounding**: Back every claim with verifiable data. In model reports, use standardized Pinned Benchmark Grids with explicit qualifiers.
7. **Multi-Objective Tradeoff & Pareto Transparency**: Acknowledge operational friction and costs. Present dual-axis Pareto frontiers (accuracy vs. cost on log scale) and effort setting curves.
8. **Sentence & Paragraph Geometry**: One idea per paragraph (1–4 sentences max). One action per sentence. Favor active voice with simple subjects.
9. **Deterministic, Verifiable Artifacts**: Code blocks must be copy-pasteable and runnable. Migration guides must contain before/after JSON request diffs. Reports must cite formal system cards.
10. **Actionable Next Steps over Redundant Summaries**: Never restate the introduction in the conclusion. Conclude with model IDs, CLI commands, documentation links, or open research questions.

---

## 4. Banned Hype Blacklist & Calibrated Substitutions

| Prohibited Marketing Superlative | Anthropic Calm-Authority Replacement |
| :--- | :--- |
| `Revolutionary` / `Groundbreaking` | Factual functional description (*"A diagnostic framework for..."*) |
| `Game-changing` / `Paradigm shift` | Quantified capability delta (*"Reduces evaluation latency by 75%"*) |
| `Seamless` / `Seamlessly` | Explicit protocol specification (*"Connects via REST API and prediction CSVs"*) |
| `Unleash` / `Supercharge` / `Turbocharge` | Measurable operational action (*"Enables", "Processes", "Evaluates"*) |
| `Next-generation` / `Next-gen` / `Cutting-edge` | Specific model ID or release version (*"Claude Haiku 5.5"*) |
| `State-of-the-art` (`SOTA`) | Pinned benchmark citation (*"Scored 72.4% on OSWorld 2.1 offline subset"*) |
| `Magic` / `Effortlessly` | Deterministic operational logic (*"Executes via non-blocking async event loops"*) |
| `Ultra-fast` / `Lightning-fast` | Exact empirical metric (*"Processes 10,000 tokens in 1.4 seconds"*) |
| `Eliminates all bias` / `100% safe` | Empirical boundary definition (*"Quantifies disparity across four demographic metrics"*) |
| `We are thrilled` / `excited to announce` | Factual declarative state change (*"[Feature] is now generally available"*) |
| `Unprecedented power` / `Boasts performance` | Verifiable score (*"Scores 45.9% on Humanity's Last Exam (no tools)"*) |

---

## 5. Deterministic Verification CLI

Audit markdown documents against calm authority invariants and regex patterns using `audit_calm_writing.py`:

```powershell
# Audit a single file enforcing a specific depth tier
python "F:\Aaradhya-Dev-Tamrakar\brainstorm\.agents\skills\writing-like-claude\scripts\audit_calm_writing.py" --tier L1 <path-to-file.md>

# Batch audit all markdown files in a directory
python "F:\Aaradhya-Dev-Tamrakar\brainstorm\.agents\skills\writing-like-claude\scripts\audit_calm_writing.py" --all <path-to-dir>
```
*Note: Code blocks, inline backticks, and markdown table definitions are stripped before prose scanning to prevent false-positive self-violations in reference guides.*
