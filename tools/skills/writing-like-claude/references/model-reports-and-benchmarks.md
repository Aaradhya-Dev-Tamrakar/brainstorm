# Frontier Model Launch Reports & Benchmark Methodology (Register 4)

This reference defines the evaluation reporting standards, pinned benchmark grid formatting, and Pareto frontier tradeoff analyses modeled after `anthropic.com/claude-haiku-5-5`.

---

## 1. Pinned Benchmark Comparison Grid Standard

Anthropic's model release reports present evaluations using a standardized 4-column comparative hierarchy. Every benchmark table must include:
1. **The Evaluated Subject (Pinned Column)**: Displayed first, bolded, and prominently styled.
2. **The Predecessor Baseline**: The direct previous model in the same class (*e.g. Haiku 4.5*).
3. **The Leading Competitor Baseline**: The direct competitive peer in the same capability/price bracket (*e.g. GPT-6 Luna*).
4. **The Frontier Reference Model**: The premier frontier flagship (*e.g. Sonnet 5.5*), explicitly annotated with a sub-label: **"For reference"**.

### Standard Benchmark Table Schema:

| Category | Benchmark Name | Haiku 5.5 (Subject) | Haiku 4.5 (Predecessor) | GPT-6 Luna (Competitor) | Sonnet 5.5 (For reference) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Knowledge Work** | GDPval-AA v2.1 | **1,620** | 735 | 1,437 | 1,840 |
| **Knowledge Work** | AA-Briefcase v1.1 | **1,578** | 614 | 1,336 | 1,824 |
| **Computer Use** | OSWorld 2.1 *(offline subset)* | **72.4%** | 15.7% | 48.9% | 83.9% |
| **Reasoning** | Humanity’s Last Exam *(no tools)* | **45.9%** | 10.2% | — | 56.9% |
| **Reasoning** | Humanity’s Last Exam *(with tools)* | **57.4%** | 18.7% | — | 64.5% |
| **Agentic Coding** | Terminal-Bench 4.0 | **39.2%** | 0.0% | 16.4% | 70.6% |
| **Agentic Coding** | FrontierCode 1.1 *(Main)* | **46.4%** | — | 42.4% | 52.1% *(Xhigh)* |
| **Visual Reasoning** | Chartography *(no tools)* | **46.4%** | 6.4% | 29.1% | 61.6% |

### Mandatory Evaluation Qualifiers:
Never report a bare percentage without its exact evaluation condition qualifier:
- `(no tools)` vs. `(with tools)`
- `(offline subset)` vs. `(live environment)`
- `(0-shot)` vs. `(5-shot)`
- `(Xhigh)`: Indicates extreme inference-time compute / maximum effort configuration.
- `—` (Em-dash): Indicates that the benchmark was un-run or un-reported by the competitor. Never guess or fabricate unreleased numbers.

---

## 2. Multi-Objective Tradeoff & Pareto Frontier Disclosure

Model capability cannot be evaluated in isolation from financial and latency costs. Reports must explicitly document tradeoff frontiers:

### 1. Cost vs. Accuracy on Log Scale
- Document the cost per task attempt (in USD, log scale) plotted against benchmark accuracy score.
- Highlight instances where the small model achieves frontier capability at an order of magnitude lower operating cost:
  > *"Haiku 5.5 achieves 72.4% on OSWorld 2.1 at \$0.22 per attempt, compared to Haiku 4.5 at \$0.88 (15.7%) and Sonnet 5.5 at \$1.40 (83.9%)."*

### 2. Effort Setting Scaling Curves
When models support scalable computational effort (`effort: low | medium | high | max`), present performance deltas across the spectrum:

| Benchmark | Low Effort | Medium Effort | High Effort | Max Effort (Xhigh) |
| :--- | :--- | :--- | :--- | :--- |
| **Terminal-Bench 4.0** | 28.4% | 34.1% | 39.2% | 42.1% |
| **Humanity’s Last Exam (with tools)** | 48.2% | 53.6% | 57.4% | 61.0% |
| **FrontierCode 1.1** | 38.0% | 42.5% | 46.4% | 49.3% |

---

## 3. Pricing & Token Economics Breakdown

Present pricing plainly, highlighting structural cost improvements such as cache reads:

| Model Tier | Input Tokens | Output Tokens | Prompt Caching Writes | Prompt Caching Reads |
| :--- | :--- | :--- | :--- | :--- |
| **Claude Haiku 5.5** | \$0.07 / MTok | \$0.35 / MTok | \$0.0875 / MTok | \$0.007 / MTok |
| **Claude Sonnet 5.5** | \$3.00 / MTok | \$15.00 / MTok | \$3.75 / MTok | \$0.30 / MTok |
| **Claude Opus 5.5** | \$15.00 / MTok | \$75.00 / MTok | \$18.75 / MTok | \$1.50 / MTok |

---

## 4. Mandatory System Card Citation & Footnote Standard

Every model release overview must conclude its performance section with an explicit, traceable citation pointing to the full evaluation methodology:

```markdown
> For comprehensive evaluation protocols, prompt rubrics, and detailed safety assessments, see the [Claude Haiku 5.5 System Card](https://anthropic.com/claude-haiku-5-5-system-card).
```
