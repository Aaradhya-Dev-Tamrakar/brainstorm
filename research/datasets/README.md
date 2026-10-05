# 📦 2026 Realtime LLM Models Dataset & Routing Infrastructure

> **Dataset Root:** `research/datasets/llm_models.yaml`  
> **Human Navigation Table:** [`MODEL_RECOMMENDATION_TABLE.md`](MODEL_RECOMMENDATION_TABLE.md)  
> **Schema Version:** `dataset.llm.v2`  
> **Data Snapshot Date:** `October 2026`  
> **Ground Truth Provenance:** [Artificial Analysis Leaderboard](https://artificialanalysis.ai/leaderboards/models) & LMSYS Chatbot Arena  
> **Standards:** [`ARCH-RFC-001`](../architectures/ARCH-RFC-001-RECORD-KEEPING-STANDARD.md) & [`ARCH-RFC-002`](../architectures/ARCH-RFC-002-MULTI-MODEL-COUNCIL.md)  

---

## 1. Overview

This directory houses the authoritative machine-readable dataset and analytical documentation for **active 2026 frontier models** alongside high-speed MoE engines, edge architectures, and foundational predecessor baselines:

1. **Active 2026 Frontier Flagships**:
   - **Claude Opus 5.5** (Anthropic, AA Intelligence Index: **58** — World #1)
   - **Claude Sonnet 5.5** (Anthropic, AA Intelligence Index: **56**, 139 tokens/sec)
   - **GPT-6 Astra** (OpenAI, AA Intelligence Index: **53**)
   - **Gemini 4 Argon** (Google DeepMind, AA Intelligence Index: **53**, 2M context standard)
   - **Claude Fable 5.1** (Anthropic, AA Intelligence Index: **53**)
   - **GPT-6.1 Sol** (OpenAI, AA Intelligence Index: **52**, 96.2% on SWE-bench Verified)
   - **Muse Spark 1.3** (Meta, AA Intelligence Index: **48**, 152 tokens/sec)
   - **Grok 4.7** (xAI, AA Intelligence Index: **46**, live real-time X streaming)
   - **Kimi K3** (Moonshot, AA Intelligence Index: **44**, 2.8 Trillion parameter MoE)
   - **Qwen 3.8 Max** (Alibaba, AA Intelligence Index: **45**, 984k context)
2. **High-Speed MoE & Low-Cost Triage Engines**:
   - **Gemini 3.8 Flash** (Google, 249 tokens/sec)
   - **DeepSeek V4.1 Flash** (DeepSeek, 209 tokens/sec, only 13B active parameters)
   - **GPT-6 Luna** (OpenAI, 131 tokens/sec, $0.10/M tokens)
   - **Gemini 3.5 Flash-Lite** (Google, **360 tokens/sec**, $0.05/M tokens)
   - **MiMo-V2.6-Pro** (Xiaomi, $0.13/M tokens)
   - **Qwen 3.8 2.4T-A95B** (Alibaba, 2.4T MoE / 95B active)
3. **Local Edge & Workstation Models**:
   - **Qwen 3.6 35B-A3B** (Alibaba, 35B MoE / 3B active, fits on single RTX 3090/4090 24GB)
   - **Qwen 2.5 Coder 32B** (Alibaba, dense 24GB offline coding standard)
   - **Phi-4** (Microsoft, 14.7B dense math champion for 12GB laptop GPUs)
   - **SmolLM2 1.7B** (HuggingFace, in-browser / WebGPU classifier gate)
4. **Historical Predecessor Baselines**:
   - `DeepSeek R1` (671B RL reasoning)
   - `DeepSeek V3` (671B sparse MoE)
   - `Mixtral 8x22B` (176B sparse MoE reference)

---

## 2. File Organization

```
research/datasets/
├── llm_models.yaml                # Authoritative machine-readable YAML dataset (25 models)
├── MODEL_RECOMMENDATION_TABLE.md  # Navigable comparison tables, MoE analysis & Mermaid flowchart
└── README.md                      # Dataset specifications and programmatic query guide
```

---

## 3. Programmatic Query Examples

### Finding Sub-$1.00 Frontier Models with >100 Tokens/Sec Speed

```python
import yaml

with open("research/datasets/llm_models.yaml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

# Filter models with high speed and low cost
fast_budget_models = [
    m for m in data["models"]
    if m["pricing"]["input_per_m"] is not None
    and m["pricing"]["input_per_m"] <= 1.00
    and m["routing_profile"]["latency_tier"] in ["ultra_fast", "fast"]
]

print(f"Discovered {len(fast_budget_models)} fast budget models:")
for m in sorted(fast_budget_models, key=lambda x: x["pricing"]["input_per_m"]):
    price = m["pricing"]["input_per_m"]
    print(f"  [${price:5.2f}/M] {m['name']:<25} | Provider: {m['provider']:<10} | Role: {m['routing_profile']['cascade_role']}")
```

---

## 4. Maintenance & Ecosystem Synchronization

All changes must pass local automated schema verification prior to committing via `.\sync.bat`:

```powershell
python scratch/validate_dataset.py
.\sync.bat -m "feat(datasets): update realtime 2026 LLM frontier catalog"
```
