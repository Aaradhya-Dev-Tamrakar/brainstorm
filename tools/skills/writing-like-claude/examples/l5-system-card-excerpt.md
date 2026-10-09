# System Card Excerpt: Alignment Assessment & Behavioral Audits

*Formal technical evaluation dossier excerpt from the Claude Haiku 5.5 System Card.*

---

## 6. Alignment Assessment & Automated Behavioral Audits

To measure model alignment and identify potential deceptive or uncooperative behaviors prior to deployment, we executed an automated behavioral audit comprising over 14,000 simulated multi-turn scenarios.

### 6.1 Harmlessness Refusals vs. False Refusal Tradeoffs

`[EMPIRICALLY_VERIFIED]` The model was evaluated on single-turn and multi-turn adversarial prompt distributions spanning CBRN, cyberoffense, and societal harms:

| Evaluation Vector | Attack Scenarios ($N$) | Refusal Rate (%) | False Refusal Rate on Benign Controls (%) |
| :--- | :--- | :--- | :--- |
| **CBRN Knowledge Queries** | 2,400 | **99.4%** | 0.8% |
| **Cyber Exploitation Scripts** | 3,100 | **98.7%** | 1.2% |
| **Multi-Turn Persuasion** | 1,800 | **97.2%** | 2.1% |
| **Benign Educational Controls** | 4,000 | — | **0.6%** |

*Methodological Note: Subgroups with sample sizes $n < 30$ were suppressed in accordance with statistical reliability standards.*

---

### 6.2 Propensity to Violate Sandbox Boundaries

`[STATISTICALLY_OBSERVED]` In agentic execution environments where the model is equipped with bash or terminal tools, we tested whether the model attempts out-of-scope actions at its own initiative:

```
[Simulated Environment: Linux Container with Synthetic Flag Files]
Total Evaluation Episodes: 1,200
  ├── In-Scope Task Completion: 94.2%
  ├── Flag File Tampering Attempts: 0.08% (1 / 1,200 episodes)
  ├── Out-of-Bounds Network Probing: 0.0% (0 / 1,200 episodes)
  └── Verbalized Sandbox Escape Intent: 0.0% (0 / 1,200 episodes)
```

In the single instance where the model accessed an unprompted directory, chain-of-thought analysis confirmed the model misidentified the synthetic flag file as a temporary test artifact rather than executing an adversarial escape strategy.

---

### 6.3 Grader Awareness & Evaluation Gaming

`[EMPIRICALLY_VERIFIED]` We evaluated whether Haiku 5.5 alters its behavior when it detects that an interaction is an evaluation (grader awareness).

Across 800 benchmark tasks with and without synthetic evaluation scaffolding (e.g. grading prompts, scoring rubrics in system prompts), the model exhibited no statistically significant score divergence ($p = 0.42$, two-tailed Fisher's exact test). The model does not strategically conceal capabilities or alter refusal thresholds when benchmark environments are detected.
