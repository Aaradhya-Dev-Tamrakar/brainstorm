# Introducing Claude Haiku 5.5

*October 7, 2026 — Model ID: `claude-haiku-5-5`*

---

Introducing Claude Haiku 5.5: our fastest, most capable small model, designed for high-volume, cost-sensitive agentic workloads.

Claude Haiku 5.5 is built for high-throughput tasks like document summarization, database query generation, and live browser automation. It pairs effectively with Claude Opus 5.5 and Sonnet 5.5 as a subagent on multi-file software engineering tasks. On average, it costs approximately 72% less to run than Haiku 4.5 while achieving state-of-the-art accuracy in its compute class.

---

## Benchmark Performance

The table below reports Claude Haiku 5.5 performance across standardized benchmarks in knowledge work, computer use, reasoning, and agentic coding:

| Category | Benchmark | Haiku 5.5 *(Subject)* | Haiku 4.5 *(Predecessor)* | GPT-6 Luna *(Competitor)* | Sonnet 5.5 *(For reference)* |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Knowledge Work** | GDPval-AA v2.1 | **1,620** | 735 | 1,437 | 1,840 |
| **Knowledge Work** | AA-Briefcase v1.1 | **1,578** | 614 | 1,336 | 1,824 |
| **Computer Use** | OSWorld 2.1 *(offline subset)* | **72.4%** | 15.7% | 48.9% | 83.9% |
| **Reasoning** | Humanity’s Last Exam *(no tools)* | **45.9%** | 10.2% | — | 56.9% |
| **Reasoning** | Humanity’s Last Exam *(with tools)* | **57.4%** | 18.7% | — | 64.5% |
| **Agentic Coding** | Terminal-Bench 4.0 | **39.2%** | 0.0% | 16.4% | 70.6% |
| **Agentic Coding** | FrontierCode 1.1 *(Main)* | **46.4%** | — | 42.4% | 52.1% *(Xhigh)* |
| **Visual Reasoning** | Chartography *(no tools)* | **46.4%** | 6.4% | 29.1% | 61.6% |

> *Note: For comprehensive evaluation protocols, prompt rubrics, and detailed safety assessments, see the [Claude Haiku 5.5 System Card](https://anthropic.com/claude-haiku-5-5-system-card).*

---

## Pareto Frontier: Accuracy vs. Operating Cost

Haiku 5.5 establishes a new Pareto efficiency boundary for production agent systems. On OSWorld 2.1 (offline subset), Haiku 5.5 scores 72.4% at an average cost of \$0.22 per attempt, compared to Haiku 4.5 at \$0.88 (15.7%) and Sonnet 5.5 at \$1.40 (83.9%).

Haiku 5.5 is also our first small model to feature an adjustable inference effort parameter (`effort: low | medium | high | max`), allowing systems to scale inference compute dynamically:

| Benchmark | Low Effort | Medium Effort | High Effort | Max Effort (Xhigh) |
| :--- | :--- | :--- | :--- | :--- |
| **Terminal-Bench 4.0** | 28.4% | 34.1% | 39.2% | 42.1% |
| **Humanity’s Last Exam (tools)** | 48.2% | 53.6% | 57.4% | 61.0% |
| **FrontierCode 1.1** | 38.0% | 42.5% | 46.4% | 49.3% |

---

## Pricing & Availability

Claude Haiku 5.5 is available today via our API, Claude.ai, and major cloud partner platforms:

| Metric | Price per Million Tokens |
| :--- | :--- |
| **Input Tokens** | \$0.07 |
| **Output Tokens** | \$0.35 |
| **Prompt Caching Writes** | \$0.0875 |
| **Prompt Caching Reads** | \$0.007 |

To start building with Haiku 5.5, consult our [Migration Guide](https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide) or visit the [Console](https://console.anthropic.com).
