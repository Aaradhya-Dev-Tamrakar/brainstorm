# Swarm & Fleet Capabilities: Multi-Agent Delegation Workflows

This reference defines the operational procedures for activating **Mode 2: Multi-Agent Teams (`/agent-teams-orchestration`)** and **Mode 3: Headless Swarm Pools (`/fleet-orchestrator`)** when authoring high-complexity technical publications.

---

## 1. Mode 2: Multi-Agent Team Capability (`/agent-teams-orchestration`)

Use when drafting an intricate, high-stakes system card, benchmark report, or research dossier where verification requires independent adversarial skepticism.

### The Cognitive Division of Labor
- **Scout** (`TypeName: "research"`, `Model: "flash"`): Read-only codebase and literature explorer. Extracts raw benchmark logs, tables, and API endpoints into `research/scratch/scout_<task>.md`. Zero theorizing.
- **Reviewer** (`TypeName: "self"`, `Model: "pro"`): Adversarial skeptic. Audits the Scout's extraction, hunts unearned promotional hype, checks 95% bootstrap confidence intervals, and records flagged risks in `research/scratch/review_<task>.md`.
- **Writer** (`TypeName: "self"`, `Model: "inherit"`): Synthesizes strictly from reviewed evidence into the final deliverable.
- **Lead** (*Main Thread*): Orchestrates handoffs, verifies style via `scripts/audit_calm_writing.py`, and links files into Obsidian.

### Step-by-Step Subagent Dispatch Commands

#### 1. Dispatch Scout:
```json
{
  "Subagents": [
    {
      "TypeName": "research",
      "Model": "flash",
      "Role": "Scout: Benchmark & Metric Extractor",
      "Prompt": "Extract raw evaluation scores, sample sizes, and baselines for <target_model>. Write unadorned tables to research/scratch/scout_<task>.md. Never speculate or add adjectives. Stop once complete."
    }
  ]
}
```

#### 2. Dispatch Reviewer (Upon Scout Completion):
```json
{
  "Subagents": [
    {
      "TypeName": "self",
      "Model": "pro",
      "Role": "Reviewer: Adversarial Writing Auditor",
      "Prompt": "Audit the findings in research/scratch/scout_<task>.md. Check every claim against the banned hype list in references/vocabulary_cheatsheet.md. Verify that benchmark scores include standard baseline reference columns and qualifiers. Record approved facts in research/scratch/review_<task>.md."
    }
  ]
}
```

---

## 2. Mode 3: Fleet Swarm Capability (`/fleet-orchestrator`)

Use for batch reporting, multi-model evaluation pipelines, or high-throughput documentation generation across heterogeneous compute accounts ($N \times 200$ Copilot credits).

### Declarative SKU Pipeline DAG
Fleet tasks are executed via dependency-ordered DAGs:
```json
{
  "sku_id": "model_report_pack_v1",
  "pipeline": [
    "extract_benchmark_logs",
    "draft_calm_dossier",
    "adversarial_audit",
    "drive_notebooklm_sync"
  ]
}
```

### Execution Steps
1. **Enqueue Task JSON**:
   Place task payload in `F:\Aaradhya-Dev-Tamrakar\Fleet-Orchestrator\orchestrator-state\tasks\<task_id>.json` with status `"pending"`.
2. **Worker Pool Execution**:
   Launch headless queue workers in isolated `.worktrees/`:
   ```powershell
   python F:\Aaradhya-Dev-Tamrakar\Fleet-Orchestrator\tools\copilot_queue_worker.py --workers 4
   ```
3. **Google Drive & NotebookLM Sync**:
   Push finished markdown dossiers to Google Drive, preserving file IDs:
   ```powershell
   python F:\Aaradhya-Dev-Tamrakar\Fleet-Orchestrator\scripts\sync_drive.py --push
   ```
