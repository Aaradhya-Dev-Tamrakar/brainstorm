# Week 16: Agentic Loop & Evaluation Harness

---
relevancy_tier: CALIBRATED_REFERENCE
mentor_score: 85/100
classroom_id: 878032079298
quiz_id: 884690483126
local_path: F:\FuseAIF2026\M4\WK16
github_repo: https://github.com/AaradhyaDT/fuseAiF_wk16_agentic_assistant
---

## 1. Overview & Evaluation Goals
- **Objective**: Construct an autonomous agentic decision loop with structured context engineering and a from-scratch evaluation harness over the Week 15 RAG assistant.
- **Core Modules**:
  - ReAct (Reasoning + Acting) execution state machine.
  - Multi-tool calling interface with parameter coercion and schema checking.
  - Context engineering: dynamic scratchpad memory compaction and sliding history windows.
  - Automated evaluation harness: LLM-as-a-judge scoring, tool selection accuracy, and step latency.

---

## 2. SOTA Industry Best Practices & Production Standards
- **Deterministic Eval Harness (`INV-AGENT-EVAL`)**: Never evaluate agentic systems using unstructured free-form questions. Use a golden dataset with strict assertions:
  1. **Tool Invocation Parity**: Did the agent invoke the exact required tool (`expected_tool == actual_tool`)?
  2. **Parameter Correctness**: Did the extracted arguments match the schema?
  3. **Step Budget Limit**: Did the agent resolve the task within $\le 5$ turns without looping?
  4. **Faithfulness**: Did the final response stay grounded in retrieved context without hallucinating?
- **Context Firebreaks**: Prune intermediate tool execution output from the active prompt window once verified; summarize bulky data to prevent attention dilution and quadratic token costs.

---

## 3. Mentor Evaluation & Quality Rating
- **Assignment Grade**: **85 / 100** ("Week 16 Assignment").
- **Quiz Status**: Handed in ("Quiz Assignment (Agentic AI)").
- **Mentor Commentary**: Strong agentic state machine design; recommended tighter programmatic safeguards against edge-case loop timeouts.

---

## 4. Local-First & GitHub Fallback Resolution (`INV-RESOLVE-FUSE`)
- **Local Directory**: [`F:\FuseAIF2026\M4\WK16`](file:///F:/FuseAIF2026/M4/WK16)
- **GitHub Remote Fallback**:
  - `https://github.com/AaradhyaDT/fuseAiF_wk16_agentic_assistant`
  - Clone: `gh repo clone AaradhyaDT/fuseAiF_wk16_agentic_assistant`

---

## 5. Golden Implementation Snippets

### Deterministic Agentic Evaluation Harness
```python
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class EvalTestCase:
    prompt: str
    expected_tools: List[str]
    forbidden_tools: List[str]
    max_steps: int

class AgentEvalHarness:
    def __init__(self, agent_fn):
        self.agent_fn = agent_fn

    def run_eval(self, test_cases: List[EvalTestCase]) -> Dict[str, Any]:
        results = []
        for tc in test_cases:
            execution_trace = self.agent_fn(tc.prompt)
            tools_used = [step["tool"] for step in execution_trace.get("steps", [])]
            
            tool_match = all(t in tools_used for t in tc.expected_tools)
            safe_match = not any(t in tools_used for t in tc.forbidden_tools)
            budget_ok = len(execution_trace.get("steps", [])) <= tc.max_steps
            
            passed = tool_match and safe_match and budget_ok
            results.append({
                "prompt": tc.prompt,
                "passed": passed,
                "steps": len(execution_trace.get("steps", [])),
                "tools_used": tools_used
            })
            
        pass_rate = sum(r["passed"] for r in results) / len(results)
        return {"pass_rate": pass_rate, "details": results}
```

---

## 6. Classroom Quiz Analysis & Conceptual Traps
- **Quiz ID**: `884690483126`.
- **Infinite Loop Circuit Breaker**: If an agent encounters repeated tool errors (e.g. invalid query syntax), an uncapped retry loop will cycle infinitely. Enforce a monotonic step counter (`max_iterations = 5`) and return a structured fallback message when breached.
