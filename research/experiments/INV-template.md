# Experiment Log: INV-[ID]

- **Date / Time:** YYYY-MM-DD HH:MM
- **Target System:** [e.g., Mock REST API v1.2 / ERC-20 Ledger]
- **Target Invariant:** [e.g., "Account balance can never be negative under concurrent transfer"]
- **Cognitive Workers:** 
  - Reasoning Lead: Gemini Pro ($5/mo baseline)
  - Generator: Free Gemini Flash / Local Qwen 2.5 (LM Studio)
- **Deterministic Verifiers:** Z3 SMT Solver v4.13 + Local Python Async Sandbox

## Quantitative Metrics
| Metric | Value |
|---|---|
| Hypotheses Generated | [e.g., 42] |
| Pruned by Syntax / AST Checker | [e.g., 28] |
| Pruned by SMT Solver (Unsat) | [e.g., 11] |
| Counterexamples Submitted to Sandbox | [e.g., 3] |
| Empirically Verified Divergences | [e.g., 1] |
| False Positive Pruning Ratio | [e.g., 97.6%] |
| Total Inference Spend | $0.00 (within $5/mo quota) |
| Human Cognitive Minutes | [e.g., 12 mins] |

## Findings & Epistemic Classification
- **Classification:** `TIER 2: EMPIRICALLY_VERIFIED`
- **Violation Description:** [Exact sequence of operations triggering the unintended state]
- **Counterexample Trace:** [Machine-readable execution trace]
- **Identified Bottleneck:** [e.g., "LLM struggled to formulate non-linear modular arithmetic constraints in Z3; required 2 prompt mutations"]
- **Actionable Next Hypothesis:** [Follow-up experiment based on this result]
