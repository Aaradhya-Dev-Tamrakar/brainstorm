# Narrative Engineering & Case Studies (Registers 1 & 2)

This reference defines the structural formulas, narrative progression, and voice calibration for **Register 1 (Internal Dog-Fooding Case Studies)** and **Register 2 (Product & Feature GA Announcements)** modeled after `claude.com/blog` and `anthropic.com/news`.

---

## 1. Register 1: The Internal Case Study / Dog-Fooding Formula

Used for deep-dive engineering articles, architecture retrospectives, and internal tool adoption stories (*e.g. "How Anthropic's sales team rebuilt inbound with Claude Managed Agents"*).

### The Narrative Arc
1. **Title**: *"How [Team] [Solved/Rebuilt X] with [System/Tool]"*
   - Avoid hyping the outcome in the title. State the operational action plainly.
2. **1-Sentence Thesis Subtitle**:
   - Must state the before/after operational change and why it matters.
   - Example: *"How a Claude-powered buying agent now answers most inbound customers, and how that changed the way our sales team works."*
3. **The Before State (Friction & Baseline Metrics)**:
   - Establish the baseline with unflinching honesty.
   - Include exact operational friction metrics: ticket response times, error rates, queue backlog, developer hours spent.
4. **The Architecture (Concrete System Components)**:
   - Describe what was built in mechanical, functional terms.
   - Avoid hand-waving abstract diagrams. Show actual component boundaries, message queues, API handoffs, and storage backends.
   - Include a concise Mermaid flowchart:
     ```mermaid
     flowchart LR
         Inbound["Inbound Request"] --> Filter["Classifier Filter"]
         Filter --> Agent["Buying Agent Loop"]
         Agent --> DB[("CRM Datastore")]
         Agent --> Output["Customer Response"]
     ```
5. **Empirical Outcomes & Measured Impact**:
   - Report exact measured figures: *"Answers 68% of inbound inquiries with zero human handoff"*, *"Reduced average triage latency from 4.2 hours to 45 seconds"*.
   - Never say *"all inquiries"* or *"100% automated"*; precision requires nuanced qualifiers (*"most inbound inquiries"*).
6. **Warts, Edge Cases & Failure Modes**:
   - Document what failed during early iterations.
   - Explain how the team identified prompt drift, hallucinated tool calls, or rate-limit saturation, and the concrete mitigations implemented.
7. **How It Changed How We Work**:
   - Conclude with the cultural or workflow shift resulting from the tool.
   - What do the humans do now that the routine task is automated?

---

## 2. Register 2: Product & Feature GA Announcements

Used for official release notes, framework milestones, and platform feature launches (*e.g. "Claude for Government is now generally available"* or *"Customize Claude Code with mods"*).

### The Structural Blueprint
1. **Title**: *"[Product/Feature] is now [generally available / in early access]"*
   - Factual declarative state change.
2. **1-Sentence Thesis**:
   - Complete takeaway summarizing release scope and user benefit.
3. **Core Capabilities (3–4 Imperative Bullets)**:
   - Every bullet must begin with an active imperative verb:
     - *"Rewrite and refactor multi-file workspaces using isolated worktrees."*
     - *"Block malicious prompt injections across browser and terminal surfaces."*
     - *"Add custom tool endpoints via standard Model Context Protocol (MCP) servers."*
4. **Scope & Availability Matrix**:
   - Explicitly differentiate release states to set accurate customer expectations:
     | Feature | General Availability (GA) | Early Access / Beta | Deferred Roadmap |
     | :--- | :--- | :--- | :--- |
     | Core CLI & Terminal | All Pro / Team Plans | — | — |
     | Browser Use SDK | — | Enterprise Waitlist | Q1 2027 |
     | Fine-Tuning Console | — | Select Partners | Under Evaluation |
5. **Minimal Functional Code / Configuration Example**:
   - Provide a copy-pasteable configuration file or runnable CLI snippet.
   - Must be syntactically complete with no placeholders.
6. **Getting Started & Concrete Next Steps**:
   - Direct link to documentation, installation commands, or console signups.
   - Zero redundant summary conclusion.
