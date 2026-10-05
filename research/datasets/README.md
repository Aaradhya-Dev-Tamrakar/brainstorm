# 📦 LLM Models Dataset & Routing Infrastructure

> **Dataset Root:** `research/datasets/llm_models.yaml`  
> **Human Navigation Table:** [`MODEL_RECOMMENDATION_TABLE.md`](MODEL_RECOMMENDATION_TABLE.md)  
> **Schema Version:** `dataset.llm.v1`  
> **Standard:** [`ARCH-RFC-001`](../architectures/ARCH-RFC-001-RECORD-KEEPING-STANDARD.md) & [`ARCH-RFC-002`](../architectures/ARCH-RFC-002-MULTI-MODEL-COUNCIL.md)  

---

## 1. Overview

This directory houses the machine-readable dataset and analytical documentation for **34 contemporary Large Language Models** across 4 operational tiers:
1. **Frontier Proprietary** (10 models: Claude Opus 4, Sonnet 4, GPT-4.1, o3, Gemini 2.5 Pro, etc.)
2. **Open-Weight Frontier** (10 models: DeepSeek R1/V3, Llama 4 Maverick/Scout, Qwen 2.5 72B/32B, etc.)
3. **Small & Edge Models** (9 models: Phi-4, Gemma 3 series, Qwen 2.5 7B/3B, Llama 3.2 3B, SmolLM2, etc.)
4. **MoE Reference Architectures** (5 models: Mixtral 8x22B, 8x7B, DeepSeek MoE 16B, Snowflake Arctic, Jamba 1.5)

The primary goal of this dataset is to supply **quantitative ground truth** and **actionable operational traits** for designing autonomous Mixture-of-Models (MoM) gateways, router networks (RouteLLM / FrugalGPT cascades), and local inference pipelines.

---

## 2. File Organization

```
research/datasets/
├── llm_models.yaml                # Authoritative machine-readable YAML dataset (34 models)
├── MODEL_RECOMMENDATION_TABLE.md  # Navigable comparison tables, MoE analysis & Mermaid flowchart
└── README.md                      # Dataset specifications and programmatic query guide
```

---

## 3. Schema Specification (`dataset.llm.v1`)

Each model entry in `llm_models.yaml` adheres to the following typed schema:

```yaml
id: string                       # Unique slug identifier (e.g. "claude-sonnet-4")
name: string                     # Formal display name
provider: string                 # Creator organization
family: string                   # Architecture lineage (Claude, GPT, Gemini, Llama, Qwen, etc.)
tier: string                     # frontier_proprietary | open_weight_frontier | small_edge | moe_reference
release_date: string             # ISO-8601 date (YYYY-MM-DD)

architecture:
  type: string                   # dense | moe | hybrid_ssm_moe
  total_params_b: float | null   # Total parameters in billions (null for closed weights)
  active_params_b: float | null  # Active parameters per forward pass (FLOPs equivalent)
  num_experts: int | null        # MoE total expert count
  top_k_experts: int | null      # Experts activated per token
  context_window: int            # Max input context length (tokens)
  output_limit: int              # Max single-turn generation length (tokens)
  training_cutoff: string        # ISO date or year-month

access:
  license: string                # proprietary | mit | apache-2.0 | llama-community | etc.
  open_weights: bool             # Can weights be downloaded directly?
  api_available: bool            # Is official hosted API available?
  local_runnable: bool           # Can it run locally on workstations/clusters?
  vram_fp16_gb: float | null     # Unquantized FP16 VRAM requirement (GB)
  vram_q4_gb: float | null       # Recommended 4-bit (Q4_K_M) VRAM requirement (GB)
  quantization_formats: list     # [gguf, awq, gptq, exl2, onnx, litert]
  ollama_tag: string | null      # Canonical Ollama pull identifier
  huggingface_id: string | null  # Canonical HuggingFace repository ID

pricing:
  input_per_m: float | null      # USD per 1M input tokens
  output_per_m: float | null     # USD per 1M output tokens
  cached_input_per_m: float | null # USD per 1M cached prompt tokens
  batch_input_per_m: float | null  # USD per 1M batch API input tokens
  batch_output_per_m: float | null # USD per 1M batch API output tokens
  free_tier: bool                # Zero-cost tier available?
  notes: string                  # Pricing caveats, context surcharges, etc.

benchmarks:
  swe_bench_verified: float | null # SWE-bench Verified (% resolved)
  aider_polyglot: float | null   # Aider 6-language benchmark (% pass)
  gpqa_diamond: float | null     # GPQA Diamond graduate STEM reasoning (%)
  math_500: float | null         # MATH 500 benchmark (%)
  mmlu_pro: float | null         # MMLU-Pro reasoning benchmark (%)
  arena_elo: int | null          # LMSYS Chatbot Arena ELO rating
  arc_agi: float | null          # ARC-AGI visual-spatial reasoning (%)
  humaneval_plus: float | null   # HumanEval+ Python execution benchmark (%)

capabilities:
  extended_thinking: bool        # Explicit test-time CoT reasoning mode
  tool_use: bool                 # Function calling support
  vision: bool                   # High-res image understanding
  audio_input: bool              # Native audio ingestion
  video_input: bool              # Native video understanding
  computer_use: bool             # OS/GUI automation capability
  code_execution: bool           # Sandboxed Python execution environment
  structured_output: bool        # Guaranteed JSON schema adherence
  streaming: bool                # Server-sent token streaming

routing_profile:
  complexity_range: [int, int]   # Min and max complexity (1–10 scale)
  best_domains: list[string]     # Optimal task specializations
  avoid_domains: list[string]    # Known failure modes / inefficient domains
  cascade_role: string           # tier_0_triage | tier_1_worker | tier_2_verifier | tier_3_escalation
  latency_tier: string           # ultra_fast (<300ms) | fast (<800ms) | standard | slow_cot
  tool_calling_reliability: float# Schema compliance rate (0.0 – 1.0)
  instruction_drift_threshold_k: int # Context length (k-tokens) before instruction drift
  cache_discount_pct: int        # Prompt caching percentage discount (0-90)
  cognitive_council_role: string # Assigned role per ARCH-RFC-002

strengths: list[string]          # Bulleted key capabilities
weaknesses: list[string]         # Known constraints or limitations
quirks: list[string]             # Operational behaviors, formatting traits, refusals
metadata:
  data_snapshot_date: string     # ISO date
  evidence_tier: string          # EMPIRICALLY_VERIFIED | STATISTICALLY_OBSERVED
  sources: list[string]          # Primary source documentation URLs
```

---

## 4. Programmatic Query Examples

### Python Query Script (Filter Local Models Under 20GB VRAM)

```python
import yaml

with open("research/datasets/llm_models.yaml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

# Find all local models with coding strength that fit in a 24GB VRAM GPU
local_coders = [
    m for m in data["models"]
    if m["access"]["local_runnable"]
    and m["access"]["vram_q4_gb"] is not None
    and m["access"]["vram_q4_gb"] <= 24.0
    and any("code" in d for d in m["routing_profile"]["best_domains"])
]

for m in sorted(local_coders, key=lambda x: x["access"]["vram_q4_gb"]):
    print(f"[{m['access']['vram_q4_gb']:4.1f} GB] {m['name']:<25} | Ollama: {m['access']['ollama_tag']}")
```

### RouteLLM Cascading Simulator

```python
import yaml

def route_query(task_complexity: int, requires_vision: bool, max_budget_usd_per_m: float):
    with open("research/datasets/llm_models.yaml", "r", encoding="utf-8") as f:
        models = yaml.safe_load(f)["models"]

    candidates = []
    for m in models:
        # Filter vision
        if requires_vision and not m["capabilities"]["vision"]:
            continue
        # Filter complexity
        c_min, c_max = m["routing_profile"]["complexity_range"]
        if not (c_min <= task_complexity <= c_max):
            continue
        # Filter cost
        price = m["pricing"]["input_per_m"] or 0.0
        if price > max_budget_usd_per_m:
            continue
        candidates.append(m)

    # Sort by benchmark score (SWE-bench or MATH-500)
    candidates.sort(
        key=lambda x: (x["benchmarks"]["swe_bench_verified"] or 0),
        reverse=True
    )
    return candidates[0] if candidates else None

# Example: High complexity (8), no vision, budget $5/M
best = route_query(task_complexity=8, requires_vision=False, max_budget_usd_per_m=5.0)
print(f"Selected: {best['name']} (${best['pricing']['input_per_m']}/M)")
```

---

## 5. Maintenance & Update Governance

1. **Monthly Reconciliation**: When new frontier models are released, update `llm_models.yaml` with calibrated numbers and execute `python scratch/validate_dataset.py`.
2. **Evidence Tier Tagging**:
   - `EMPIRICALLY_VERIFIED`: Directly from vendor model cards, pricing tables, or reproducible scripts.
   - `STATISTICALLY_OBSERVED`: Derived from third-party leaderboards (LMSYS Arena, Aider, LiveBench).
   - `HEURISTIC_HYPOTHESIS`: Community estimates or extrapolations.
3. **Repository Sync**:
   All changes must pass local automated schema verification prior to committing via `.\sync.bat`:
   ```powershell
   python scratch/validate_dataset.py
   .\sync.bat -m "docs(datasets): update LLM model recommendation table"
   ```
