# Claude Blog Post Skeletons & Templates

Ready-to-use structural skeletons for the three canonical post archetypes.

---

## Template 1: Internal Case Study / Dog-Fooding

```markdown
# How [Team] [Solved Problem / Rebuilt Workflow] with [Tool/System]

> *[One-sentence thesis: how an internal system now does X, and how that changed how the team works]*

---

## The Baseline Problem

[Describe the state before the change in 2-3 short paragraphs. Include concrete numbers: hours wasted, error rates, queue backlogs.]

## What We Built

[Explain the architecture in functional terms. Define what the system IS in 15 words or fewer.]

```
[System Diagram or ASCII flow]
```

Key technical components:
- **[Component A]**: [One-sentence functional description]
- **[Component B]**: [One-sentence functional description]

## What We Measured

[Share empirical results. Specific numbers, percentages, and latency figures. Include honest qualification: "most", "on average", "in 74% of runs".]

- **[Metric 1]**: [Baseline] -> [New value]
- **[Metric 2]**: [Baseline] -> [New value]

## Where It Struggled (Warts & Edge Cases)

[Document where early prototypes failed and how the architecture was adjusted. This is the primary trust signal.]

## How This Changed How We Work

[Reflect on workflow shifts, cultural changes, or operational freed capacity.]

---

## Getting Started / Next Steps

[Concrete CLI command or documentation link.]
```

---

## Template 2: Product / Feature Announcement

```markdown
# [Product/Feature] is now [generally available / in early access]

> *[One-sentence thesis stating the release and secondary capability]*

---

Today we are releasing [Product/Feature], a [functional 10-word definition].

## Core Capabilities

- **[Active Verb] [feature]**: [1-2 sentences of functional precision]
- **[Active Verb] [feature]**: [1-2 sentences of functional precision]
- **[Active Verb] [feature]**: [1-2 sentences of functional precision]

## Scope & Availability

| Capability | Status | Availability |
| :--- | :--- | :--- |
| **[Core Feature]** | General Availability (GA) | Available to all users |
| **[Advanced Feature]** | Early Access / Preview | Opt-in via flag |
| **[Deferred Roadmap]** | Planned | Next quarter |

## Working Example

[Syntactically valid, runnable code snippet or CLI command]

```bash
# Example command
run-tool --target config.json
```

## How to Get Started

[Exact link or terminal command to install and begin.]
```

---

## Template 3: Developer Tutorial / Guide

```markdown
# How to [Accomplish Specific Task] with [Tool]

> *[One-sentence description of the task and runtime requirements]*

---

[Tool] allows you to [task]. In this guide, you will set up [component] and run [operation].

## Prerequisites

- [Runtime requirement, e.g. Python 3.11+]
- [Library or CLI tool version]

## 1. [First Step: Configuration or Setup]

[1-2 sentences explaining rationale]

```python
# Runnable code block with imports
import tool
```

## 2. [Second Step: Implementation]

[1-2 sentences explaining mechanics]

```python
# Core logic
result = tool.run()
```

## Common Guardrails & Failure Modes

- **[Edge case 1]**: [How the system reacts and how to prevent it]
- **[Edge case 2]**: [Validation error and resolution]

## Next Steps

[Links to full documentation, repository, or related tutorials.]
```
