# 🧭 LLM Model Recommendation, Benchmarking & MoE Routing Matrix

> **Dataset Identifier:** `research/datasets/llm_models.yaml`  
> **Documentation Version:** `1.0.0` (`dataset.llm.v1`)  
> **Data Snapshot Date:** `October 2026`  
> **Governance Invariants:** [`ARCH-RFC-001`](../architectures/ARCH-RFC-001-RECORD-KEEPING-STANDARD.md) (Calibrated Evidence Tiers) & [`ARCH-RFC-002`](../architectures/ARCH-RFC-002-MULTI-MODEL-COUNCIL.md) (Multi-Model Council)  
> **Total Models Cataloged:** `34` across `4` operational tiers  

---

## 1. Executive Summary & Navigation Index

This document provides a **navigable, multi-dimensional decision matrix** for evaluating, selecting, and auto-routing queries across frontier proprietary LLMs, open-weight foundation models, small edge models, and Mixture-of-Experts (MoE) architectures.

### Quick Navigation
1. [Master Model Matrix (All 34 Models)](#2-master-model-matrix)
2. [Mixture-of-Models (MoM) Auto-Routing & Triage Matrix](#3-mixture-of-models-mom-auto-routing--triage-matrix)
3. [Benchmark Comparison Matrix](#4-benchmark-comparison-matrix)
4. [Token Economics & Pricing Matrix](#5-token-economics--pricing-matrix)
5. [Hardware Sizing & Local VRAM Deployment Guide](#6-hardware-sizing--local-vram-deployment-guide)
6. [Architectural MoE Analysis (Total vs. Active Parameters)](#7-architectural-moe-analysis)
7. [Strengths, Weaknesses & Real-World Quirks](#8-strengths-weaknesses--real-world-quirks)
8. [Mermaid Decision Flowchart](#9-mermaid-decision-flowchart)
9. [Mapping to ARCH-RFC-002 Multi-Model Council](#10-mapping-to-arch-rfc-002-multi-model-council)

---

## 2. Master Model Matrix

| # | Model Name | Provider | Tier | Architecture | Context | Input / Output (per 1M) | Primary Benchmark SOTA | Primary Cascade Role |
|:---|:---|:---|:---|:---|:---:|:---:|:---|:---|
| **1** | [Claude Opus 4](#claude-opus-4) | Anthropic | Frontier Proprietary | Dense | 200k | \$15.00 / \$75.00 | SWE-bench: 72.5% | Tier 3 (Escalation) |
| **2** | [Claude Sonnet 4](#claude-sonnet-4) | Anthropic | Frontier Proprietary | Dense | 200k | \$3.00 / \$15.00 | Aider: 84.5% | Tier 1 (Worker) |
| **3** | [Claude Sonnet 3.5 v2](#claude-sonnet-3-5-v2) | Anthropic | Frontier Proprietary | Dense | 200k | \$3.00 / \$15.00 | Aider: 82.0% | Tier 1 (Worker) |
| **4** | [Claude Haiku 3.5](#claude-haiku-3-5) | Anthropic | Frontier Proprietary | Dense | 200k | \$0.80 / \$4.00 | MMLU-Pro: 69.2% | Tier 0 (Triage) |
| **5** | [GPT-4.1](#gpt-4-1) | OpenAI | Frontier Proprietary | Dense | 1,000k | \$2.50 / \$10.00 | Needle Recall: 99.8% | Tier 1 (Worker) |
| **6** | [o3](#o3) | OpenAI | Frontier Proprietary | Dense (CoT) | 200k | \$20.00 / \$80.00 | MATH 500: 96.7% | Tier 3 (Escalation) |
| **7** | [o4-mini](#o4-mini) | OpenAI | Frontier Proprietary | Dense (CoT) | 128k | \$1.10 / \$4.40 | MATH 500: 90.0% | Tier 1 (Worker) |
| **8** | [GPT-4o](#gpt-4o) | OpenAI | Frontier Proprietary | Dense | 128k | \$2.50 / \$10.00 | Arena: 1330 | Tier 1 (Worker) |
| **9** | [Gemini 2.5 Pro](#gemini-2-5-pro) | Google | Frontier Proprietary | Dense | 1,000k | \$1.25 / \$5.00 | GPQA: 73.0% | Tier 2 (Verifier) |
| **10** | [Gemini 2.5 Flash](#gemini-2-5-flash) | Google | Frontier Proprietary | Dense | 1,000k | \$0.15 / \$0.60 | Latency: <250ms | Tier 0 (Triage) |
| **11** | [DeepSeek R1](#deepseek-r1) | DeepSeek | Open-Weight Frontier | MoE (671B/37B) | 128k | \$0.55 / \$2.19 | MATH 500: 97.3% | Tier 3 (Escalation) |
| **12** | [DeepSeek V3](#deepseek-v3) | DeepSeek | Open-Weight Frontier | MoE (671B/37B) | 128k | \$0.14 / \$0.28 | MMLU-Pro: 75.9% | Tier 1 (Worker) |
| **13** | [Llama 4 Maverick](#llama-4-maverick) | Meta | Open-Weight Frontier | MoE (400B/17B) | 128k | \$0.40 / \$1.20 | SWE-bench: 61.5% | Tier 1 (Worker) |
| **14** | [Llama 4 Scout](#llama-4-scout) | Meta | Open-Weight Frontier | MoE (109B/17B) | 10,000k | \$0.30 / \$0.90 | Context: 10M tokens | Tier 1 (Worker) |
| **15** | [Qwen 2.5 72B Instruct](#qwen-2-5-72b-instruct) | Alibaba | Open-Weight Frontier | Dense (72.7B) | 128k | \$0.35 / \$0.70 | Arena: 1315 | Tier 1 (Worker) |
| **16** | [Qwen 2.5 Coder 32B](#qwen-2-5-coder-32b) | Alibaba | Open-Weight Frontier | Dense (32.5B) | 128k | \$0.20 / \$0.40 | HumanEval+: 88.0% | Tier 1 (Worker) |
| **17** | [Mistral Large 2](#mistral-large-2) | Mistral AI | Open-Weight Frontier | Dense (123B) | 128k | \$2.00 / \$6.00 | MMLU: 84.0% | Tier 1 (Worker) |
| **18** | [Command R+](#command-r-plus) | Cohere | Open-Weight Frontier | Dense (104B) | 128k | \$2.50 / \$10.00 | Grounded RAG | Tier 2 (Verifier) |
| **19** | [Grok 3](#grok-3) | xAI | Open-Weight Frontier | Dense | 128k | \$3.00 / \$15.00 | Real-Time X/Live | Tier 2 (Verifier) |
| **20** | [DBRX](#dbrx) | Databricks | Open-Weight Frontier | MoE (132B/36B) | 32k | \$0.75 / \$2.25 | SQL Execution | Tier 1 (Worker) |
| **21** | [Phi-4](#phi-4) | Microsoft | Small / Edge | Dense (14.7B) | 16k | \$0.10 / \$0.20 | MATH 500: 80.4% | Tier 1 (Worker) |
| **22** | [Gemma 3 27B](#gemma-3-27b) | Google | Small / Edge | Dense (27.2B) | 128k | \$0.20 / \$0.40 | Multimodal Edge | Tier 1 (Worker) |
| **23** | [Gemma 3 12B](#gemma-3-12b) | Google | Small / Edge | Dense (12.1B) | 128k | \$0.08 / \$0.16 | Vision on 8GB | Tier 1 (Worker) |
| **24** | [Gemma 3 4B](#gemma-3-4b) | Google | Small / Edge | Dense (4.3B) | 128k | \$0.04 / \$0.08 | Mobile Edge | Tier 0 (Triage) |
| **25** | [Qwen 2.5 7B](#qwen-2-5-7b) | Alibaba | Small / Edge | Dense (7.6B) | 128k | \$0.05 / \$0.10 | MMLU: 74.3% | Tier 0 (Triage) |
| **26** | [Qwen 2.5 3B](#qwen-2-5-3b) | Alibaba | Small / Edge | Dense (3.1B) | 32k | \$0.03 / \$0.06 | Speed: >120 tps | Tier 0 (Triage) |
| **27** | [Llama 3.2 3B](#llama-3-2-3b) | Meta | Small / Edge | Dense (3.2B) | 128k | \$0.03 / \$0.06 | Mobile Tool Use | Tier 0 (Triage) |
| **28** | [Mistral Small 3.1](#mistral-small-3-1) | Mistral AI | Small / Edge | Dense (24B) | 32k | \$0.10 / \$0.30 | Fast Code Review | Tier 1 (Worker) |
| **29** | [SmolLM2 1.7B](#smollm2-1-7b) | HuggingFace | Small / Edge | Dense (1.7B) | 8k | \$0.02 / \$0.04 | WebGPU/Client | Tier 0 (Triage) |
| **30** | [Mixtral 8x22B](#mixtral-8x22b) | Mistral AI | MoE Reference | MoE (176B/39B) | 65k | \$0.60 / \$1.80 | Sparse Reference | Tier 1 (Worker) |
| **31** | [Mixtral 8x7B](#mixtral-8x7b) | Mistral AI | MoE Reference | MoE (46.7B/12.9B)| 32k | \$0.25 / \$0.50 | 12.9B Active | Tier 1 (Worker) |
| **32** | [DeepSeek MoE 16B](#deepseek-moe-16b) | DeepSeek | MoE Reference | MoE (16.4B/2.8B) | 4k | N/A (Research) | 2.8B Active | Tier 0 (Triage) |
| **33** | [Snowflake Arctic](#snowflake-arctic) | Snowflake | MoE Reference | MoE (480B/17B) | 4k | \$0.80 / \$2.40 | Dense+Sparse Top-1 | Tier 1 (Worker) |
| **34** | [Jamba 1.5](#jamba-1-5) | AI21 Labs | MoE Reference | SSM-MoE (398B/94B)| 256k | \$2.00 / \$8.00 | Mamba-Attention | Tier 1 (Worker) |

---

## 3. Mixture-of-Models (MoM) Auto-Routing & Triage Matrix

For designing autonomous routers (like RouteLLM, FrugalGPT cascades, or Unify gateways), models must be mapped by **Complexity Score (1–10)** and **Domain Specialization**.

| Complexity (1-10) | Task Archetype | Primary Dispatch Model | Zero-Cost / Offline Alternative | Fallback Escalation Model |
|:---:|:---|:---|:---|:---|
| **1 – 2** | Regex parsing, intent classification, PII masking, language detection | **SmolLM2 1.7B** / **Qwen 2.5 3B** | Local in-process CPU / WebGPU | Claude Haiku 3.5 |
| **2 – 3** | JSON schema field extraction, text summarization, simple translation | **Gemini 2.5 Flash** / **DeepSeek V3** | Qwen 2.5 7B (Ollama) | Claude Sonnet 4 |
| **4 – 6** | Unit test drafting, standard API tool dispatch, bug triage, docstrings | **Qwen 2.5 Coder 32B** / **DeepSeek V3** | Gemma 3 27B / Mistral Small 3.1 | Claude Sonnet 4 |
| **6 – 8** | Multi-file AST refactoring, database migration scripts, RAG synthesis | **Claude Sonnet 4** / **Llama 4 Maverick** | Qwen 2.5 72B (Dual GPU) | Claude Opus 4 |
| **8 – 9** | Whole repository architectural planning, protocol invariants, RFC creation | **Claude Opus 4** / **Gemini 2.5 Pro** | DeepSeek R1 (API) | o3 |
| **9 – 10** | Formal verification, Olympiad-grade math, cryptographic proof analysis | **o3** / **DeepSeek R1** | DeepSeek R1 671B | o3 (Max Compute) |

### Domain Routing Signatures

* **AST & Code Diff Patches**: Route directly to `Claude Sonnet 4` or `Qwen 2.5 Coder 32B`. These models exhibit superior bracket-balance retention and rarely emit malformed diff headers.
* **Massive Sequences (>200k tokens)**: Route to `Gemini 2.5 Pro` (up to 2M) or `Llama 4 Scout` (10M context window). Dense models with standard 128k windows fail with context-overflow errors.
* **Grounded Citations / RAG**: Route to `Command R+` or `Gemini 2.5 Pro` with search grounding. These generate inline citation indices directly mapped to retrieval chunks.
* **Zero-Leakage Air-Gapped Privacy**: Route to `Phi-4` (14B), `Gemma 3` (12B/27B), or `Qwen 2.5 72B` running locally via Ollama/vLLM.

---

## 4. Benchmark Comparison Matrix

> All benchmark numbers are categorized under calibrated evidence tiers: `[E]` = `EMPIRICALLY_VERIFIED`, `[S]` = `STATISTICALLY_OBSERVED`.

| Model Name | SWE-bench Verified (%) | Aider Polyglot (%) | GPQA Diamond (%) | MATH 500 (%) | MMLU-Pro (%) | Chatbot Arena ELO |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **o3** | 71.7 `[S]` | 88.0 `[S]` | **87.7** `[S]` | 96.7 `[S]` | **87.5** `[S]` | **1375** `[S]` |
| **Claude Opus 4** | 72.5 `[S]` | 86.2 `[S]` | 74.9 `[S]` | 96.4 `[S]` | 84.1 `[S]` | 1362 `[S]` |
| **DeepSeek R1** | 49.2 `[E]` | 79.2 `[S]` | 71.5 `[E]` | **97.3** `[E]` | 84.0 `[E]` | 1360 `[S]` |
| **Grok 3** | 62.0 `[S]` | 81.5 `[S]` | 72.0 `[S]` | 92.5 `[S]` | 82.0 `[S]` | 1355 `[S]` |
| **Claude Sonnet 4** | **72.8** `[E]` | 84.5 `[E]` | 71.2 `[E]` | 92.4 `[E]` | 82.5 `[E]` | 1350 `[S]` |
| **Gemini 2.5 Pro** | 63.8 `[E]` | 81.0 `[S]` | 73.0 `[E]` | 93.0 `[E]` | 81.0 `[E]` | 1345 `[S]` |
| **Llama 4 Maverick** | 61.5 `[S]` | 80.2 `[S]` | 67.4 `[S]` | 91.0 `[S]` | 81.2 `[S]` | 1340 `[S]` |
| **GPT-4.1** | 55.0 `[S]` | 79.5 `[S]` | 68.0 `[S]` | 89.2 `[S]` | 79.4 `[S]` | 1335 `[S]` |
| **Claude Sonnet 3.5 v2** | 65.0 `[E]` | 82.0 `[E]` | 65.0 `[E]` | 88.0 `[E]` | 78.0 `[E]` | 1330 `[S]` |
| **GPT-4o** | 38.8 `[E]` | 72.0 `[E]` | 53.6 `[E]` | 76.6 `[E]` | 72.5 `[E]` | 1330 `[S]` |
| **DeepSeek V3** | 42.0 `[E]` | 76.5 `[S]` | 59.1 `[E]` | 90.2 `[E]` | 75.9 `[E]` | 1320 `[S]` |
| **Qwen 2.5 72B** | 46.5 `[E]` | 76.0 `[E]` | 58.5 `[E]` | 83.1 `[E]` | 76.8 `[E]` | 1315 `[S]` |
| **o4-mini** | 49.0 `[S]` | 78.0 `[S]` | 72.0 `[S]` | 90.0 `[S]` | 76.5 `[S]` | 1310 `[S]` |
| **Gemini 2.5 Flash** | 48.0 `[E]` | 74.0 `[S]` | 58.0 `[E]` | 85.0 `[E]` | 74.0 `[E]` | 1290 `[S]` |
| **Gemma 3 27B** | 41.0 `[S]` | 72.0 `[S]` | 51.0 `[S]` | 79.0 `[S]` | 71.5 `[S]` | 1290 `[S]` |
| **Qwen 2.5 Coder 32B** | 47.6 `[E]` | 73.7 `[E]` | 51.0 `[E]` | 80.0 `[E]` | 71.0 `[E]` | 1285 `[S]` |
| **Phi-4 (14B)** | 34.0 `[E]` | 69.5 `[E]` | 54.0 `[E]` | 80.4 `[E]` | 69.5 `[E]` | 1260 `[S]` |
| **Mixtral 8x22B** | 36.0 `[E]` | 68.0 `[E]` | 48.0 `[E]` | 72.0 `[E]` | 69.0 `[E]` | 1265 `[S]` |
| **Gemma 3 12B** | 32.0 `[S]` | 66.0 `[S]` | 44.0 `[S]` | 72.0 `[S]` | 64.0 `[S]` | 1250 `[S]` |
| **Qwen 2.5 7B** | 28.0 `[E]` | 62.0 `[E]` | 41.0 `[E]` | 74.3 `[E]` | 62.0 `[E]` | 1240 `[S]` |
| **Gemma 3 4B** | 22.0 `[S]` | 54.0 `[S]` | 35.0 `[S]` | 60.0 `[S]` | 53.0 `[S]` | 1195 `[S]` |
| **SmolLM2 1.7B** | 8.0 `[E]` | 35.0 `[E]` | 24.0 `[E]` | 38.0 `[E]` | 36.0 `[E]` | 1120 `[S]` |

---

## 5. Token Economics & Pricing Matrix

> Pricing is quoted in **USD per 1 Million Tokens** for Standard API access.

| Model | Standard Input | Standard Output | Cached Input | Batch Input (50% Off) | Cache Savings (%) | Free Tier Available? |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **DeepSeek V3** | **\$0.14** | **\$0.28** | **\$0.07** | N/A | 50% | No |
| **Gemini 2.5 Flash** | \$0.15 | \$0.60 | \$0.0375 | \$0.075 | **75%** | **Yes (AI Studio)** |
| **Qwen 2.5 Coder 32B** | \$0.20 | \$0.40 | \$0.05 | \$0.10 | 75% | No (Self-hostable) |
| **Llama 4 Scout** | \$0.30 | \$0.90 | \$0.05 | \$0.15 | 83% | No (Self-hostable) |
| **Qwen 2.5 72B** | \$0.35 | \$0.70 | \$0.08 | \$0.175 | 77% | No (Self-hostable) |
| **Llama 4 Maverick** | \$0.40 | \$1.20 | \$0.10 | \$0.20 | 75% | No (Self-hostable) |
| **DeepSeek R1** | \$0.55 | \$2.19 | \$0.14 | N/A | 75% | No |
| **Claude Haiku 3.5** | \$0.80 | \$4.00 | \$0.08 | \$0.40 | **90%** | No |
| **o4-mini** | \$1.10 | \$4.40 | \$0.55 | \$0.55 | 50% | No |
| **Gemini 2.5 Pro (<=128k)**| \$1.25 | \$5.00 | \$0.3125 | \$0.625 | 75% | **Yes (AI Studio)** |
| **Claude Sonnet 4** | \$3.00 | \$15.00 | \$0.30 | \$1.50 | **90%** | No |
| **GPT-4.1** | \$2.50 | \$10.00 | \$1.25 | \$1.25 | 50% | No |
| **GPT-4o** | \$2.50 | \$10.00 | \$1.25 | \$1.25 | 50% | **Yes (Free web UI)** |
| **Claude Opus 4** | \$15.00 | \$75.00 | \$1.50 | \$7.50 | **90%** | No |
| **o3** | \$20.00 | \$80.00 | \$10.00 | \$10.00 | 50% | No |

---

## 6. Hardware Sizing & Local VRAM Deployment Guide

For local, air-gapped, or privacy-sensitive workloads, use this matrix to size hardware requirements across quantization tiers.

| Model | Parameters | FP16 VRAM (Full) | Q8_0 VRAM | Q4_K_M VRAM (Recommended) | Target Hardware Tier | CLI Command (Ollama) |
|:---|:---:|:---:|:---:|:---:|:---|:---|
| **SmolLM2 1.7B** | 1.7B | 3.5 GB | 2.0 GB | **1.1 GB** | CPU / WebGPU / Raspberry Pi | `ollama run smollm2:1.7b` |
| **Qwen 2.5 3B** | 3.1B | 6.5 GB | 3.5 GB | **2.1 GB** | Ultra-thin Laptop / Integrated GPU | `ollama run qwen2.5:3b` |
| **Llama 3.2 3B** | 3.2B | 6.8 GB | 3.6 GB | **2.2 GB** | Mobile / Laptop CPU | `ollama run llama3.2:3b` |
| **Gemma 3 4B** | 4.3B | 9.0 GB | 4.8 GB | **2.8 GB** | Laptop GPU (4GB VRAM) | `ollama run gemma3:4b` |
| **Qwen 2.5 7B** | 7.6B | 16.0 GB | 8.5 GB | **4.8 GB** | Entry GPU (RTX 3060 6GB/8GB) | `ollama run qwen2.5:7b` |
| **Gemma 3 12B** | 12.1B | 25.0 GB | 13.5 GB | **7.5 GB** | Standard Laptop GPU (8GB VRAM) | `ollama run gemma3:12b` |
| **Phi-4 (14B)** | 14.7B | 30.0 GB | 16.0 GB | **9.5 GB** | Mid Desktop GPU (RTX 4070 12GB) | `ollama run phi4:14b` |
| **Mistral Small 3.1**| 24.0B | 48.0 GB | 26.0 GB | **14.5 GB** | Single RTX 4080 (16GB VRAM) | `ollama run mistral-small:24b` |
| **Gemma 3 27B** | 27.2B | 55.0 GB | 30.0 GB | **16.5 GB** | RTX 3090/4090 or Apple M-series | `ollama run gemma3:27b` |
| **Qwen 2.5 Coder 32B**| 32.5B | 65.0 GB | 36.0 GB | **19.5 GB** | **Single RTX 3090/4090 (24GB VRAM)**| `ollama run qwen2.5-coder:32b` |
| **Mixtral 8x7B** | 46.7B | 95.0 GB | 50.0 GB | **28.0 GB** | Dual RTX 3060/4060 or Mac 36GB | `ollama run mixtral:8x7b` |
| **Qwen 2.5 72B** | 72.7B | 145.0 GB | 80.0 GB | **42.0 GB** | **Dual RTX 3090/4090 (48GB VRAM)** | `ollama run qwen2.5:72b` |
| **Llama 4 Scout** | 109.0B | 220.0 GB | 120.0 GB | **65.0 GB** | Workstation (2x-3x 24GB GPUs / Mac 64GB)| `ollama run llama4:scout` |
| **Mixtral 8x22B** | 176.0B | 350.0 GB | 190.0 GB | **105.0 GB** | Quad RTX 3090/4090 (96GB+) / Mac 128GB | `ollama run mixtral:8x22b` |
| **Llama 4 Maverick**| 400.0B | 800.0 GB | 440.0 GB | **240.0 GB** | Multi-GPU Server (4x A100 80GB) | `ollama run llama4:maverick` |
| **DeepSeek R1 / V3**| 671.0B | 1340.0 GB| 720.0 GB | **400.0 GB** | Server Cluster (8x H100 80GB) | `ollama run deepseek-r1:671b` |

---

## 7. Architectural MoE Analysis

A common misconception in model evaluation is conflating **total parameters** with **active parameters per token**. Sparse Mixture-of-Experts models decouple memory capacity (total knowledge) from compute latency (FLOPs per forward pass).

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        SPARSE MIXTURE-OF-EXPERTS (MoE) ROUTING                         │
├─────────────────────┬──────────────┬──────────────┬──────────┬──────────────┬──────────┤
│ MODEL NAME          │ TOTAL PARAMS │ ACTIVE PARAMS│ EXPERTS  │ ROUTED / PASS│ EFFICIENCY│
├─────────────────────┼──────────────┼──────────────┼──────────┼──────────────┼──────────┤
│ DeepSeek V3 / R1    │ 671.0 B      │ 37.0 B       │ 256 + 1  │ 8 + 1 shared │ 18.1x    │
│ Llama 4 Maverick    │ 400.0 B      │ 17.0 B       │ 128      │ 8 active     │ 23.5x    │
│ Snowflake Arctic    │ 480.0 B      │ 17.0 B       │ 128      │ 1 (+10B base)│ 28.2x    │
│ Llama 4 Scout       │ 109.0 B      │ 17.0 B       │ 32       │ 4 active     │ 6.4x     │
│ Mixtral 8x22B       │ 176.0 B      │ 39.0 B       │ 8        │ 2 active     │ 4.5x     │
│ DBRX                │ 132.0 B      │ 36.0 B       │ 16       │ 4 active     │ 3.6x     │
│ Mixtral 8x7B        │ 46.7 B       │ 12.9 B       │ 8        │ 2 active     │ 3.6x     │
│ DeepSeek MoE 16B    │ 16.4 B       │ 2.8 B        │ 64 + 2   │ 6 + 2 shared │ 5.8x     │
└─────────────────────┴──────────────┴──────────────┴──────────┴──────────────┴──────────┘
```

### Architectural Takeaways for MoE Designers
1. **The Shared Expert Invariant**: Models like DeepSeek V3 and DeepSeek MoE 16B isolate core lexical and linguistic representations into 1–2 **shared experts** that activate on every token, while dynamically routing remaining capacity across 64–256 fine-grained sub-experts. This prevents routing instability and token drop.
2. **Top-K Saturation**: Increasing active experts beyond $Top\text{-}8$ yields diminishing returns in perplexity while causing high GPU memory-bus thrashing.
3. **KV Cache Bottleneck**: While MoE reduces feed-forward compute, the attention KV cache scales with sequence length regardless of sparsity. DeepSeek's Multi-head Latent Attention (MLA) addresses this by compressing keys and values into low-dimensional latent spaces.

---

## 8. Strengths, Weaknesses & Real-World Quirks

### Claude Family (Anthropic)
* **Claude Opus 4**:
  * *Strengths*: Top-tier autonomous agentic multi-file refactoring; dismantles subtle edge-case bugs; writes production-ready code with zero shortcuts.
  * *Weaknesses*: Premium price point (\$75/M output); high latency during extended thinking.
  * *Quirk*: Proactively audits and refactors surrounding scaffolding if it spots architectural flaws.
* **Claude Sonnet 4**:
  * *Strengths*: Perfect sweet spot for daily engineering; flawless diff/patch application; 90% prompt caching discount.
  * *Weaknesses*: Overly cautious on system administration scripts that trigger malware heuristics.
  * *Quirk*: Natural affinity for functional programming paradigms and Markdown table formatting.

### OpenAI Family
* **o3 / o4-mini**:
  * *Strengths*: Undisputed champion on formal mathematics, Olympiad competitions, and cryptographic proofs; self-corrects invalid deductive steps.
  * *Weaknesses*: Cannot turn off extended thinking; reasoning tokens burn output budget rapidly; high latency.
  * *Quirk*: Internal reasoning trace is summarized by OpenAI; can reject clean simple solutions in search of non-existent complexity.
* **GPT-4.1 / GPT-4o**:
  * *Strengths*: 1M token context; native multimodal vision/audio; strict JSON schema mode guarantees zero parse failures.
  * *Weaknesses*: Coding scores lag behind Claude Sonnet 4; prompt caching discount is limited to 50%.
  * *Quirk*: Enthusiastic conversational default unless calibrated via system prompt.

### Google Gemini Family
* **Gemini 2.5 Pro**:
  * *Strengths*: 1M–2M context window with near-perfect needle retrieval; native multimodal processing of multi-hour audio and video files; free tier in Google AI Studio.
  * *Weaknesses*: Pricing doubles once prompts exceed 128k tokens; can wrap code in conversational narrative.
  * *Quirk*: Excels at synthesizing entire books, PDF dossiers, and repositories into structured Obsidian wikilinks.
* **Gemini 2.5 Flash**:
  * *Strengths*: Sub-250ms TTFT; \$0.15/M input pricing; optional toggleable extended thinking.
  * *Weaknesses*: Can miss subtle negative constraints in deeply nested prompts.
  * *Quirk*: The optimal zero-cost prototype engine via Google AI Studio.

### Open-Weight Leaders
* **DeepSeek R1 / V3**:
  * *Strengths*: World-class reasoning and coding at 1/30th the API cost of proprietary competitors; open weights under MIT license; transparent `<think>` traces in R1.
  * *Weaknesses*: Requires an 8-GPU cluster for self-hosting; censorship triggers on Chinese political topics.
  * *Quirk*: R1 frequently 'talks to itself' across languages inside its thinking tokens before emitting final English answers.
* **Qwen 2.5 Coder 32B**:
  * *Strengths*: The definitive offline coding model; fits entirely on a single 24GB GPU (RTX 3090/4090); matches GPT-4o on HumanEval+.
  * *Weaknesses*: Context degrades past 40k tokens without careful position encoding.
  * *Quirk*: Completely fluff-free code generation; outputs raw, usable code immediately.
* **Phi-4 (14B)**:
  * *Strengths*: Unmatched mathematical and logical density under 10GB VRAM; fits on a 12GB RTX 3060/4070; MIT license.
  * *Weaknesses*: 16k context window is narrow; not suited for multi-file repo refactors.
  * *Quirk*: Explains technical concepts with the formal rigor of a university textbook.

---

## 9. Mermaid Decision Flowchart

Use this deterministic flowchart to route incoming queries to the optimal model:

```mermaid
flowchart TD
    START([User Query or Agent Task]) --> PRIVACY{Air-Gapped / Private Local Policy?}
    
    PRIVACY -->|Yes| VRAM_CHECK{Local Hardware VRAM Available?}
    VRAM_CHECK -->|>= 40 GB Dual GPU| QWEN72[Qwen 2.5 72B Instruct]
    VRAM_CHECK -->|>= 20 GB Single 3090/4090| QWEN_CODER[Qwen 2.5 Coder 32B]
    VRAM_CHECK -->|8 - 16 GB Mid GPU| PHI4[Phi-4 14B / Gemma 3 12B]
    VRAM_CHECK -->|<= 4 GB CPU/Mobile| GEMMA4[Gemma 3 4B / Qwen 2.5 3B]
    
    PRIVACY -->|No: API Allowed| MODALITY{Requires Vision, Audio, or Video?}
    MODALITY -->|Audio / Video Native| GEMINI_PRO[Gemini 2.5 Pro]
    MODALITY -->|Images / UI Screenshots| SONNET4[Claude Sonnet 4 / GPT-4o]
    
    MODALITY -->|Text Only| CTX{Prompt Sequence Length?}
    CTX -->|> 200k Tokens| GEMINI_CTX[Gemini 2.5 Pro / Llama 4 Scout]
    
    CTX -->|Standard <= 200k| TASK_TYPE{Task Nature & Complexity?}
    
    TASK_TYPE -->|Formal Math / Crypto / Proofs| O3[o3 / DeepSeek R1]
    TASK_TYPE -->|Autonomous Coding / Multi-File Refactor| CODING_BUDGET{Budget Sensitivity?}
    CODING_BUDGET -->|High Quality Benchmark SOTA| CLAUDE_OPUS[Claude Opus 4]
    CODING_BUDGET -->|Production Workhorse ($3/M)| CLAUDE_SONNET[Claude Sonnet 4]
    CODING_BUDGET -->|Lowest Cost ($0.14/M)| DEEPSEEK_V3[DeepSeek V3]
    
    TASK_TYPE -->|High Volume Triage / JSON Extraction| FAST_CHEAP[Gemini 2.5 Flash / Haiku 3.5]
    TASK_TYPE -->|Real-Time Web / Social Sentiment| GROK[Grok 3]
    TASK_TYPE -->|Grounded RAG / Multi-Hop Citations| COMMAND[Command R+]
```

---

## 10. Mapping to ARCH-RFC-002 Multi-Model Council

Under the [ARCH-RFC-002 Cognitive Council Protocol](../architectures/ARCH-RFC-002-MULTI-MODEL-COUNCIL.md), frontier models are assigned to their natural comparative advantages:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        THE MULTI-PERSPECTIVE COGNITIVE COUNCIL                         │
├──────────────────────┬──────────────────────┬──────────────────────────────────────────┤
│ MODEL FAMILY         │ COUNCIL ROLE         │ PRIMARY RESPONSIBILITY IN ECOSYSTEM      │
├──────────────────────┼──────────────────────┼──────────────────────────────────────────┤
│ 1. ChatGPT Think     │ The Adversarial      │ Searing peer review, literature sanity,  │
│    (o3 / o4-mini)    │ Skeptic / Reviewer   │ dismantling unearned claims & benchmarks │
├──────────────────────┼──────────────────────┼──────────────────────────────────────────┤
│ 2. Claude (Anthropic)│ The Systems & Code   │ Refined systems coding, clean abstraction│
│    (Sonnet 4 / Opus) │ Craftsman            │ layers, diff patches & architectural RFCs│
├──────────────────────┼──────────────────────┼──────────────────────────────────────────┤
│ 3. Perplexity /      │ The Empirical Fact-  │ Live academic paper retrieval, citation  │
│    Command R+        │ Checker & Grounder   │ verification & conference tracking       │
├──────────────────────┼──────────────────────┼──────────────────────────────────────────┤
│ 4. Grok (xAI)        │ The Unfiltered First-│ Contrarian stress-testing, unconventional│
│                      │ Principles Provocateur│ physics boundary checks & live trends   │
├──────────────────────┼──────────────────────┼──────────────────────────────────────────┤
│ 5. Gemini /          │ The Synthesizer &    │ Large-context orchestration, Git / tool  │
│    Antigravity       │ Living Repository    │ execution, invariant codification & sync │
└──────────────────────┴──────────────────────┴──────────────────────────────────────────┘
```
