---
name: graphify-optimizer
description: >-
  Expert knowledge graph optimization, noise elimination, and relevancy calibration engine for Graphify.
  Use whenever analyzing or tuning graphify-out/, pruning leaf-node spur noise, configuring .graphifyignore,
  executing directed or code-only extractions, labeling semantic communities, or maximizing GraphRAG retrieval signal.
---

# Graphify Optimizer & Relevancy Engine

Turn raw Graphify extractions into high-signal, semantically cohesive knowledge graphs. This skill provides the operational playbooks, topological tuning flags, ignore filters, and metric gates to prevent low-cohesion graph bloat and eliminate "Fake God Nodes".

---

## 1. When to Use This Skill

Activate this skill when:
- **Graph Relevancy & Noise Audit:** A graph has thousands of nodes but low semantic utility, high leaf/spur ratio (>50% degree-1 nodes), or giant irrelevant God Nodes.
- **Ignore Filtering (`.graphifyignore`):** Static textbooks, academic syllabi, raw JSON data evaluation schemas, or verbose test fixtures are polluting the graph.
- **Topological Optimization:** You need causal dependency preservation (`--directed`), pure AST code analysis (`--code-only`), or fast re-clustering (`--cluster-only`).
- **Semantic Community Calibration:** Generic labels ("Community 0", "Community 1") need to be scored for cohesion and mapped into architectural domains via `.graphify_labels.json`.
- **Disk & Artifact Hygiene:** Cleaning dated snapshot folders, temporary chunk files (`.graphify_chunk_*.json`), and syncing with Obsidian vaults.

---

## 2. Core Operational Workflow

```
┌─────────────────────────────────┐
│ 1. Audit Degree & Top Nodes     │ Inspect graph.json for leaf spurs & fake God Nodes
└──────────────┬──────────────────┘
               ↓
┌─────────────────────────────────┐
│ 2. Configure .graphifyignore    │ Exclude static reference text & verbose payload schemas
└──────────────┬──────────────────┘
               ↓
┌─────────────────────────────────┐
│ 3. Execute Calibrated Rebuild   │ Run .\graphify.bat -Directed -Full
└──────────────┬──────────────────┘
               ↓
┌─────────────────────────────────┐
│ 4. Score Cohesion & Label       │ Filter communities < 0.08 cohesion; map semantic domains
└──────────────┬──────────────────┘
               ↓
┌─────────────────────────────────┐
│ 5. Verify & Export              │ Inspect graph.html & export Obsidian vault (--obsidian)
└─────────────────────────────────┘
```

---

## 3. Diagnostic Commands: Measuring Graph Health

Before tuning, evaluate the current graph's signal-to-noise ratio:

```powershell
# Quick Degree & File Contribution Audit
& "$HOME\AppData\Roaming\uv\tools\graphifyy\Scripts\python.exe" -c "
import json
from collections import Counter
from pathlib import Path

p = Path('graphify-out/graph.json')
if p.exists():
    data = json.loads(p.read_text(encoding='utf-8'))
    nodes = data.get('nodes', [])
    edges = data.get('links', []) or data.get('edges', [])
    degree = Counter()
    for e in edges:
        degree[e.get('source')] += 1
        degree[e.get('target')] += 1
    deg1 = sum(1 for n in nodes if degree[n.get('id')] <= 1)
    print(f'Nodes: {len(nodes)} | Edges: {len(edges)} | Degree <= 1: {deg1} ({deg1/max(1, len(nodes))*100:.1f}%)')
"
```

### Health Benchmarks:
* **Degree $\le 1$ Ratio:** Should be $< 45\%$. If $> 60\%$, the graph is heavily diluted with unreferenced leaf spurs.
* **Top God Node Connectivity:** Should represent a core architectural abstraction (e.g. `BaseStateMachine`, `Orchestrator`, `DatabaseEngine`), NOT a static reference doc or course syllabus.
* **Mean Community Cohesion:** Should be $\ge 0.10$. Large communities with cohesion $< 0.05$ indicate unclustered collections of leaf spurs.

---

## 4. Ingestion Hygiene: Rules for `.graphifyignore`

Graphify natively respects `.graphifyignore` in the project root. Apply these boundaries:

```gitignore
# 1. Epistemic Layer 0 Vaults (Preserved on disk, excluded from operational retrieval)
research/transcripts/
research/transcripts/*
*.transcript.jsonl
*.transcript_full.jsonl

# 2. External Static References (Avoid dumping massive syllabi or reference text)
research/references/
research/references/*

# 3. Verbose Data & Evaluation Payload Schemas (Keep ecosystem registry & contracts; exclude raw schemas)
schemas/*.evaluation.v1.json
schemas/horoscope.evaluation.v1.json
schemas/nepal-civic-service.v1.json
schemas/model_benchmark.schema.json
schemas/ecosystem.verification.schema.json

# 4. Ephemeral Caches & Scratch Space
.agents/
__pycache__/
*.pyc
scratch/
report/*.aux
report/*.log
report/*.out
report/*.toc
```

---

## 5. Execution Flags & Playbooks

Always execute via `.\graphify.bat` (or `.\graphify.ps1`) to ensure Python resolution and automatic stale-snapshot pruning:

### Playbook A: Full Calibrated Directed Rebuild
Preserves caller $\to$ callee causality and dependency order:
```powershell
.\graphify.bat -Directed -Full
```

### Playbook B: Pure Code AST Extraction (Zero Hallucination)
Skips all Markdown prose and documentation, extracting only runnable AST symbols (functions, classes, calls, imports):
```powershell
.\graphify.bat -CodeOnly -Full
```

### Playbook C: Incremental Ecosystem Sync (Routine)
Re-extracts only modified files since the last run and prunes deleted sources:
```powershell
.\graphify.bat -Update
```

### Playbook D: Re-Clustering without Re-Extraction
Recalculates Louvain community detection in $< 2$ seconds after editing `.graphify_labels.json`:
```powershell
.\graphify.bat -ClusterOnly
```

### Playbook E: Obsidian Knowledge Vault Generation
Exports native Obsidian canvas and bidirectional `[[wikilink]]` Markdown notes into `graphify-out/obsidian/`:
```powershell
.\graphify.bat -Obsidian
```

---

## 6. Semantic Community Labeling

Graphify stores persistent community labels in `graphify-out/.graphify_labels.json`. Overwrite generic labels (`"Community 0"`) with domain names:

```json
{
  "0": "Continuous Sync & Document Pipeline",
  "1": "Gemini Multimodal Media & GenAI SDK",
  "2": "Windows DFIR Forensics & Kernel ACL Vault",
  "3": "Deterministic Verification & Invariant Engine",
  "4": "Multi-Agent Fleet Coordination & MCP Bridges"
}
```

After updating `.graphify_labels.json`, immediately run `.\graphify.bat -ClusterOnly` to propagate the semantic labels to [graphify-out/GRAPH_REPORT.md](../../../graphify-out/GRAPH_REPORT.md) and [graphify-out/graph.html](../../../graphify-out/graph.html).
