---
name: slm-router-forge
description: Autonomous end-to-end Small Language Model (SLM) forge, local routing engine, and task time allocation synthesizer. Use whenever asked to "tune an intent router", "train a local classifier", "fine-tune Qwen on Colab", "export GGUF for local inference", "harvest task time dataset", "allocate task execution timeout", "upload model to Google Drive", "run model in LM Studio", or mentions training sub-1B parameter models (e.g., Qwen 0.5B/0.8B LoRA via Unsloth) for low-latency (<50ms) intent discovery, skill routing, and empirical duration budgeting.
version: 1.2.0
---

# SLM Router & Time Allocation Forge (`slm-router-forge`)

This skill defines the authoritative procedure for harvesting empirical task execution datasets from chat histories, fine-tuning sub-1B parameter Small Language Models (SLMs) in Google Colab (Pro L4 GPU or Free T4) using Unsloth LoRA, exporting quantized INT4 GGUF weights, streaming large binary models directly to Google Drive via resumable upload, and mounting them locally into LM Studio for sub-50ms offline task routing and dynamic time allocation.

---

## 1. Architectural Philosophy: The Decoupled Router & Time Allocation Pattern

Frontier reasoning models (Gemini Pro, Claude Opus) should not waste expensive tokens or round-trip network latency on routine intent classification, skill dispatching, and execution duration estimation. Instead, decouple execution into a dedicated 2-tier cognitive division:

```mermaid
flowchart TD
    UserPrompt["Incoming User Request / Task Prompt"] --> FastRouter["⚡ Local SLM Router (Qwen2.5-0.5B GGUF)\n- Runs locally in LM Studio / llama.cpp\n- < 40ms latency on CPU (AVX-VNNI)\n- RAM footprint: ~380 MB"]
    
    FastRouter --> RoutingJSON["Structured Ecosystem Payload\n{\n  'archetype': 'ENGINEERING_DEV',\n  'tier': 'Tier 1',\n  'matrix_cell': '(V0, R1)',\n  'policy': 'BRANCH_GUARD',\n  'primary_skill': 'github-workflow',\n  'velocity': 'BALANCED',\n  'time_allocation': {\n    'tier': 'T1_FAST',\n    'estimated_duration_s': 45,\n    'timeout_ceiling_s': 99,\n    'cpm_weight': 1.5,\n    'execution_route': 'FLEET_WORKER'\n  }\n}"]
    
    RoutingJSON --> CPMSolver["📐 CPM DAG Solver (sim/adaptive_orchestrator.py)\n- Uses cpm_weight for exact D_j duration\n- Solves ES, EF, LS, LF, TS, FS mathematically"]
    RoutingJSON --> QueueWorker["🛡️ Fleet Queue Worker (copilot_queue_worker.py)\n- Dynamically sets worker timeout = timeout_ceiling_s\n- Eliminates static 420s timeout lockups"]
```

---

## 2. The 5-Stage Forge Lifecycle

### Stage 1: Hardware Profiling & Architecture Selection
Before training, audit host memory and acceleration instructions to select the optimal model tier:
* **Host with <6 GB free RAM & Shared Graphics (e.g. Intel Core Ultra 7 155H, 16GB RAM)**:
  - **Optimal Tier**: **`Qwen2.5-0.5B-Instruct`** (Quantized to `Q4_K_M` GGUF: ~380 MB RAM, 25–45ms latency via AVX-VNNI).
  - **Alternative (Pure Logits)**: `SetFit / DeBERTa-v3-small` (86M: ~150 MB RAM, 8–12ms latency).
* **Host with Discrete NVIDIA GPU (>=8 GB VRAM)**:
  - **Optimal Tier**: `Qwen3.5-0.8B` or `Llama-3.2-1B-Instruct`.

---

### Stage 2: Grounded Dataset Synthesis & Empirical Time Harvesting
Synthesize instruction-tuning datasets grounded in real repository schemas, historical tasks, and empirical chat histories:
1. Ingest lifecycle archetypes from `references/lifecycle-stages.md`.
2. Map skills from `references/skill-matrix.md` and `.agents/skills/`.
3. Harvest real past task prompts and execution durations using `tools/harvest_task_time_dataset.py`:
   - Crawls 500+ transcripts in `~/.gemini/antigravity/brain/*/transcript.jsonl` (extracting start/end timestamps and tool call counts).
   - Crawls completed task checkpoints in `Fleet-Orchestrator/orchestrator-state/checkpoints/*.json`.
   - Strips XML prompt tags (`<USER_REQUEST>`, `<ADDITIONAL_METADATA>`) and normalizes token lengths.
   - Calculates time tiers (`T0_MICRO` <15s, `T1_FAST` 15-60s, `T2_MEDIUM` 60-180s, `T3_LONG` 180-480s, `T4_EPIC` >480s), timeout ceilings ($\max(30\text{s}, 2.2 \times D_{\text{est}})$), and normalized CPM weights ($D_j = \max(0.5, D_{\text{est}} / 30.0)$).
4. Emit formatted `(instruction, input, output)` JSONL files:
   - `dataset/task_time_train.jsonl` (80% split)
   - `dataset/task_time_eval.jsonl` (20% split)
   - `dataset/dataset_summary.json` (metadata distribution audit)

```json
{
  "instruction": "You are the high-speed Intent, Skill, and Task Time Allocation Router for the Aaradhya development ecosystem. Classify the incoming user intent into the exact lifecycle archetype, tier, 2D matrix cell, primary skill, supporting skills, velocity profile, and task time allocation (tier, estimated_duration_s, timeout_ceiling_s, cpm_weight, execution_route) in strict JSON format.",
  "input": "Fix the regression in test_warehouse_mem_sim.py where queue latency was calculating as zero.",
  "output": "{\"archetype\": \"ENGINEERING_DEV\", \"tier\": \"Tier 1\", \"matrix_cell\": \"(V0, R1)\", \"policy\": \"BRANCH_GUARD\", \"primary_skill\": \"github-workflow\", \"supporting_skills\": [\"systems-concurrency-harness\"], \"velocity\": \"BALANCED\", \"time_allocation\": {\"tier\": \"T1_FAST\", \"estimated_duration_s\": 35, \"timeout_ceiling_s\": 77, \"cpm_weight\": 1.17, \"execution_route\": \"DIRECT_FAST\"}}"
}
```

---

### Stage 3: Cloud GPU Fine-Tuning (Unsloth on Colab Pro / Free)
Execute fine-tuning on a cloud GPU (Colab Pro L4 Ada Lovelace, A100, or Free T4):

1. **Tracked Colab Notebooks**:
   - Local self-contained notebook: `notebooks/slm_time_router_forge.ipynb` (in `Fleet-Orchestrator`)
   - Research experiment mirror: `research/experiments/colab_train_qwen_intent_router.ipynb` (in `brainstorm`)
   - Google Drive cloud mirror: `1wGq53okV7ZaFGSw2fWilEfxL4FEIVeIF`

2. **L4 GPU / Ada Lovelace Hyperparameters (Colab Pro)**:
   - Base Model: `unsloth/Qwen2.5-0.5B-Instruct-bnb-4bit`
   - Precision: `bf16=True` (natively accelerated on L4 / A100)
   - LoRA Target Modules: All linear projections (`q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj`)
   - LoRA Hyperparameters: Rank $r=16, \alpha=32, \text{dropout}=0$
   - Batching: `per_device_train_batch_size=8`, `gradient_accumulation_steps=2`
   - Epochs: 3 (typically ~145 gradient steps for 1,550 samples; finishes in **~60 to 90 seconds** on L4 GPU)

3. **Export to INT4 GGUF**:
   ```python
   model.save_pretrained_gguf("qwen_intent_router_q4", tokenizer, quantization_method = "q4_k_m")
   ```
   *(Outputs quantized GGUF weights `qwen_intent_router_q4/Qwen2.5-0.5B-Instruct.Q4_K_M.gguf` (~380 MB))*.

---

### Stage 4: Binary Isolation & Resumable Cloud Archiving
Never commit large binary model weights ($>100\text{ MB}$) to Git repositories:
1. **Strict `.gitignore` Invariant**:
   Enforce model ignores in repository roots:
   ```gitignore
   models/
   *.gguf
   *.safetensors
   *.bin
   *.onnx
   ```
2. **Chunked Resumable Upload to Google Drive**:
   Upload large weights directly to the designated Google Drive folder (`1wGq53okV7ZaFGSw2fWilEfxL4FEIVeIF`) using chunked resumable upload via `scripts/upload_large_model_to_drive.py`.
3. **Drive Manifest Registration**:
   Register the permanent Drive File ID and SHA-256 hash in `drive-manifest.json`:
   ```json
   "models/qwen_intent_router_q4_k_m.gguf": {
     "drive_file_id": "1bjXQ4K6hTtOevmG6XFih-AVGP0UlXGEK",
     "drive_file_name": "qwen_intent_router_q4_k_m.gguf",
     "description": "Fine-Tuned Qwen2.5-0.5B-Instruct Intent & Task Time Router (Q4_K_M GGUF)",
     "sha256": "68e2824405149b24"
   }
   ```

---

### Stage 5: Local Silicon Serving & Orchestrator Integration Gate
Deploy the model locally for sub-50ms inference:
1. **LM Studio Import & Load**:
   ```powershell
   lms import -c --user-repo aaradhya/qwen-intent-router -y "models/qwen_intent_router_q4_k_m.gguf"
   lms server start
   lms load qwen-intent-router --identifier qwen-intent-router -y
   ```
2. **Client Health-Guarded Routing (`tools/fast_intent_router.py`)**:
   - Perform a sub-millisecond socket connection check on `127.0.0.1:1234` before sending HTTP payloads.
   - If the server is offline, fall back instantly to deterministic keyword heuristics with `<1ms` latency.
   - Set request timeout to 5.0 seconds.
3. **Queue Worker Consumption (`tools/copilot_queue_worker.py`)**:
   - Inspects `task.get("time_allocation", {}).get("timeout_ceiling_s")`.
   - Adopts predicted timeout directly, dynamically sizing worker lifespans and preventing thread starvation.
   - Records `actual_duration_s` in completed checkpoints for ongoing telemetry reconciliation.
4. **CPM DAG Scheduling (`sim/adaptive_orchestrator.py`)**:
   - `DeterministicCPMScheduler` ingests `cpm_weight` directly as task duration ($D_j$) to compute exact early/late schedules and critical path identification ($TS = 0$).

---

## 3. Core Invariants (Zero-Drift Standards)

1. **INV-SLM-01: Zero Repo Bloat**: Machine learning binaries (`.gguf`, `.safetensors`, `.bin`) must never be staged or committed to Git. They reside in local cache (`models/`) and Google Drive cloud archives.
2. **INV-SLM-02: Socket Ping Guard**: Network requests to local inference servers must be guarded by a `<50ms` socket pre-check to eliminate multi-second connection timeouts when servers are cold.
3. **INV-SLM-03: Deterministic Fallback**: The client routing tool (`fast_intent_router.py`) must never fail or crash if the local LLM server is unbooted; it must return a valid heuristic classification and `time_allocation` with zero latency.
4. **INV-SLM-04: Resumable Cloud Ingestion**: All binary model uploads to Google Drive must use `uploadType=resumable` with 16MB chunking to prevent memory exhaustion and connection drops.
5. **INV-SLM-05: Dynamic Timeout Allocation**: Fleet queue workers must dynamically adopt `timeout_ceiling_s` from task time allocation whenever present rather than relying on a static 420.0s constant.
6. **INV-SLM-06: Mathematical CPM Duration Ingestion**: Critical Path Method schedulers must resolve durations from empirical `cpm_weight` point estimates rather than ungrounded integer assumptions.
