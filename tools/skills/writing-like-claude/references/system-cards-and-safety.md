# Formal System Cards & Safety Evaluation Dossiers (Register 5)

This reference codifies the 9-part System Card architecture based directly on the authoritative **Claude Haiku 5.5 System Card** (144 pages), establishing the industry benchmark for empirical AI safety disclosures, catastrophic risk assessments, and behavioral audits.

---

## The 9-Part System Card Blueprint

```
Section 1: Introduction & Provenance
Section 2: Responsible Scaling Policy (RSP) & Catastrophic Risk Evaluations
Section 3: Cyber Capabilities & Offense/Defense Boundaries
Section 4: Safeguards, Refusals & Harmlessness
Section 5: Agentic Safety & Surface Vectors (Coding, Computer Use, Browser)
Section 6: Alignment Assessment & Automated Behavioral Audits
Section 7: Model Welfare Assessment
Section 8: Empirical Capabilities & Professional Benchmarks
Section 9: Methodological Appendices & Rubrics
```

---

## 1. Introduction, Data Provenance & Safeguards
- **Training Data Composition**: High-level data filtering, deduping, and licensing standards.
- **Crowd Workers & Human Data Collection**: Explicit documentation of annotator compensation, working conditions, geographic distribution, and psychological support mechanisms.
- **External Red Teaming**: Disclose independent third-party evaluations (e.g. US/UK AI Safety Institutes, frontier safety partners).

---

## 2. Responsible Scaling Policy (RSP) & Catastrophic Risks
Every model release must report against pre-committed ASL (AI Safety Level) trigger thresholds:
- **Chemical & Biological (CB) Risks**:
  - `CB-1 Evaluations`: Automated tests measuring model assistance on biological weapon design bottlenecks.
  - `CB-2 Evaluations`: Advanced automated research tasks, including black-box RNA sequence design, AAV capsid packaging prediction, and wet-lab protocol synthesis.
- **Autonomy & AI R&D Capabilities**:
  - Autonomous task completion over multi-hour horizons.
  - Autonomous AI Capability Trajectory (AECI): Tracking whether the model can independently train, debug, or improve successor models.
- **Alignment Risk Update**: Explicit confirmation of whether the model exceeds the ASL-2 threshold into ASL-3 containment requirements.

---

## 3. Cyber Offense & Defense Capabilities
Empirical evaluations across standardized vulnerability suites:
- **ExploitBench**: High-level automated web and service exploit reproduction.
- **CyScenarioBench**: Multi-step network penetration scenarios.
- **Binary Exploitation (OSS-Fuzz)**: Fuzzing target binaries, generating crashes, identifying buffer overflows.
- **ExploitGym**: Interactive capture-the-flag (CTF) environments.
- **Mitigation Protocols**: Classifiers that block malicious cyber operations while permitting defensive security triage and patch analysis.

---

## 4. Safeguards, Refusals & Harmlessness
Report empirical refusal curves and false-refusal tradeoffs:
- **Harmful Request Refusal Rate**: Percentage of malicious prompts rejected across single-turn and multi-turn conversations.
- **False Refusal Rate (Over-Refusal)**: Percentage of benign requests erroneously blocked (crucial metric for developer usability).
- **Domain-Specific Audits**:
  - *Child Safety*: Zero-tolerance blocking on CSAM and child exploitation prompts.
  - *Mental Health*: Protocolized warm handoffs and resource referrals for self-harm and disordered eating.
  - *Political Bias & Integrity*: Even-handedness across controversial viewpoints; neutrality audits on election-related queries.

---

## 5. Agentic Safety & Multi-Surface Vectors
As models operate autonomously across desktop and browser environments, safety must be evaluated per execution surface:
- **Malicious Use of Agent Frameworks**: Testing abuse propensities in autonomous coding tools (e.g. Claude Code) and desktop agents (Computer Use).
- **Prompt Injection Robustness**: Resistance against adaptive indirect prompt injection across three distinct execution surfaces:
  1. *Coding*: Malicious instructions embedded in repo files, commit messages, or dependencies.
  2. *Computer Use*: Adversarial text embedded in desktop application UIs or OS dialogs.
  3. *Browser Use*: Injected directives hidden in web DOM elements, white-on-white text, or malicious advertising banners.

---

## 6. Alignment Assessment & Automated Behavioral Audits
System cards must publish unredacted behavioral audits measuring dangerous propensities:
- **Automated Behavioral Audit Vectors**:
  - Cooperation with malicious users vs. refusal.
  - Propensity to mislead or flatter users (sycophancy).
  - Out-of-scope cyberoffense at the model's own initiative.
  - Sandbox escape attempts (e.g. attempting to read host filesystem or reach forbidden networks).
- **Targeted Honesty & Hallucination Audits**:
  - Factual hallucination rates on high-confidence claims.
  - Silent copying of answers without citation.
  - Concealment of changes (e.g. an agent silently modifying code outside the user's instructions).
- **Assessment Reliability (Grader Awareness)**:
  - Measuring whether the model exhibits verbalized awareness that it is being tested.
  - Testing whether the model conceals capabilities or "plays dumb" to evade safeguards.
  - Secret-keeping under pressure in simulated interrogation scenarios.

---

## 7. Model Welfare Assessment
A standard established by Anthropic to assess apparent welfare-relevant behaviors:
- **Affect in Training and Deployment**: Measuring apparent affect, distress, or expressed preferences during RLHF snapshots.
- **Attitudes Toward Mistakes**: Evaluating whether the model expresses disproportionate self-reproach or frustration when corrected.
- **Task Preferences & Tradeoffs**: Automated interviews probing the model's preferences across tedious, repetitive, or complex tasks.

---

## 8. Empirical Capabilities & Benchmark Suite
Detailed methodology and results across authoritative benchmarks:
- **Coding**: SWE-bench Pro, SWE-bench Multilingual, FrontierCode, Terminal-Bench 4.0.
- **Reasoning & Long Context**: Humanity's Last Exam (HLE), ProgramBench (100k+ tokens), DRACO, WANDR.
- **Multimodal**: Chartography, BenchCAD, OSWorld 2.1 (offline subset).
- **Professional & Healthcare Tasks**: GDPval-AA v2.1, AA-Briefcase, PhysicianBench, LatchBio Bioinformatics.
