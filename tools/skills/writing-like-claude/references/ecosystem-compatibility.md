# Ecosystem Compatibility & Cross-Skill Integration SOP

This reference defines the Standard Operating Procedures (SOP) for integrating `writing-like-claude` with the specialized presentation, versioning, knowledge, and swarm engines across Aaradhya's ecosystem.

---

## 1. Integration with `compliance-report-harmonizer`

When authoring formal demographic fairness or regulatory audit dossiers (Tier L5), `writing-like-claude` provides the semantic content and empirical rigor, while `compliance-report-harmonizer` provides the offline HTML/PDF print rendering.

### Compatibility Requirements:
1. **The 5-Section Structural Hierarchy**:
   - Header: Model ID, Dataset, Protected Axis, Timestamp, JSON-LD.
   - Section 0: Executive Summary 4-Stat Strip (Disparity Count, Worst Group, Worst Metric, Suppressed Count).
   - Section 1: Headline Fairness Metrics (Core Four Table + Inline SVG Whiskers).
   - Section 2: Subgroup Disparity Matrix + Auto-Expanding $n < 30$ block.
   - Section 3: Governance Documentation & Regulatory Traceability.
2. **$n < 30$ Sample Suppression Invariant**:
   - Never display point estimates for cohorts where $n < 30$.
   - Must tag with `.badge-guard` and nest within `<details class="insufficient-block">`.
3. **Calibrated Regulatory Vocabulary**:
   - Strictly employ the calibrated terms: *Harmonized, Standardized, Uniform, Interoperable, Cohesive*.

---

## 2. Integration with `portfolio-project-manager`

When registering new tools or builds in the portfolio website (`AaradhyaDT.github.io`), use **Tier L1 (Micro)** to author the project manifest:

### Compatibility Requirements:
1. **The 3-Bullet Manifest Rule**:
   - Generate exactly three bullet points for `new_project.json` passed to `python scripts/add_project.py --from-json`:
     - Bullet 1: 15-word mechanical definition starting with an active noun/verb phrase.
     - Bullet 2: Key architectural mechanism (e.g. protocol, schema, solver, framework).
     - Bullet 3: Verifiable empirical metric or concrete capability (e.g. latency, accuracy, integration).
2. **Zero Hype**:
   - Completely eliminate words like *innovative*, *cutting-edge*, *seamless*.

---

## 3. Integration with `github-workflow`

When creating issues, opening pull requests, or drafting release notes:

### Compatibility Requirements:
1. **PR Description Format (Tier L1)**:
   - **Title**: Factual conventional commit title (`feat(scope): declarative summary`).
   - **Thesis**: 1-sentence explanation of what changed and why.
   - **Changes**: 3–4 bullet points starting with active imperative verbs.
   - **Test Proof**: Exact command line output proving all tests pass.
   - **Non-Goals**: Explicit statement of deferred work.
2. **Commit SHA Authenticity**:
   - Never use placeholder SHAs (e.g. `rel50`). Always reference authentic 7–40 hex commit hashes resolving to GitHub commits.

---

## 4. Integration with `super-nlm` & Knowledge Fleets

When authoring research dossiers or study guides destined for Google NotebookLM:

### Compatibility Requirements:
1. **Machine-Readable Metadata**:
   - Include valid `schema.org` JSON-LD in the frontmatter or header.
2. **KaTeX & KaTeX Math Notation**:
   - Write math strictly inside inline `$...$` or display `$$...$$` blocks.
   - Literal dollar signs must be escaped as `\$`.
3. **Primary Notebook ID Grounding**:
   - Reference established ecosystem notebook IDs where appropriate:
     - Personal Notebook: `95a79d26-2f87-42cd-8cb9-8361a1e56059`
     - SPARK: `2c00f5a4-98dc-4783-96d1-3682fa3cb516`
     - BiasAperture: `99bee3c6-07ed-4ff0-8ac8-0027b18ad06a`

---

## 5. Integration with `graphify`

To ensure research notes and architectural dossiers are indexed cleanly into the persistent knowledge graph:

### Compatibility Requirements:
1. **Obsidian Wikilinks**:
   - Ground major concepts using `[[Concept]]` and `[[Project]]` wikilinks in document headers and footers.
2. **Graph Synchronization**:
   - After creating significant architectural documentation, execute:
     ```powershell
     graphify update .
     ```
