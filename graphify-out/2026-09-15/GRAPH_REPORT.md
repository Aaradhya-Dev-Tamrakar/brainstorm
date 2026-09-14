# Graph Report - brainstorm  (2026-09-15)

## Corpus Check
- 36 files · ~93,892 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 292 nodes · 325 edges · 28 communities (20 shown, 7 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 3 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c2efedea`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- properties
- properties
- properties
- AI-Constraint-Solver.contract.json
- ecosystem.registry.json
- ARCH-RFC-003: Capstone Defense Standard
- capability.contract.v1.json
- enum
- enum
- sync.ps1
- Experiment Log: INV-[ID]
- properties
- warehouse_mem_sim.py
- enum
- enum
- yt-dlp-live.contract.json
- sweep_ipu_breakeven.py
- STRANGLER-IPU
- transcript_archiver.py
- Canonical Capability Registry
- reconciliation_engine.py
- Jarvis Cognitive Interface
- Headless Orchestration Substrate
- Hypothesis HYP-001
- BiasAperture
- Worker Session Runtime (WSR)
- YouTube Transformer Cluster

## God Nodes (most connected - your core abstractions)
1. `enum` - 9 edges
2. `enum` - 9 edges
3. `ARCH-SPEC-002: Ingestion Processing Unit (IPU)` - 9 edges
4. `ARCH-RFC-003: Capstone Defense Standard` - 9 edges
5. `Research Architectures Hub` - 9 edges
6. `required` - 8 edges
7. `INV-EPI-001: Verbatim Epistemic History Invariant` - 8 edges
8. `required` - 7 edges
9. `Write-Status()` - 7 edges
10. `ARCH-SPEC-001: ECIE Systems Architect Paradigm` - 7 edges

## Surprising Connections (you probably didn't know these)
- `STRANGLER-IPU` --implements--> `ARCH-SPEC-002 (IPU)`  [INFERRED]
  schemas/capability-registry.yaml → research/architectures/README.md
- `Personal Tool Ecosystem` --references--> `Canonical Capability Registry`  [EXTRACTED]
  README.md → schemas/capability-registry.yaml
- `GPU & RAM Architecture Spec` --conceptually_related_to--> `STRANGLER-IPU`  [INFERRED]
  research/experiments/GPU_RAM_ARCHITECTURE_SPEC.md → schemas/capability-registry.yaml
- `Personal Tool Ecosystem` --references--> `ARCH-SPEC-001: ECIE Systems Architect Paradigm`  [EXTRACTED]
  README.md → research/architectures/ARCH-SPEC-001-ECIE-COMPUTE-MEMORY.md
- `Personal Tool Ecosystem` --references--> `ARCH-SPEC-002: Ingestion Processing Unit (IPU)`  [EXTRACTED]
  README.md → research/architectures/ARCH-SPEC-002-INGESTION-PROCESSING-UNIT.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **4-Tier Jarvis Capability Mesh** — tool_super_nlm, tool_spark, tool_claude_fleet, tool_bias_aperture, tool_strangler_ipu [EXTRACTED 1.00]
- **Adversarial Invariant Assurance Flow** — research_hypotheses_hyp_001, research_hypotheses_hyp_002, research_experiments_fleet_001 [INFERRED 0.80]

## Communities (28 total, 7 thin omitted)

### Community 0 - "properties"
Cohesion: 0.07
Nodes (30): description, items, minItems, type, $ref, description, type, type (+22 more)

### Community 1 - "properties"
Cohesion: 0.07
Nodes (27): properties, description, type, description, type, description, type, description (+19 more)

### Community 2 - "properties"
Cohesion: 0.06
Nodes (32): http, sse, stdio, stream, transport, type, items, type (+24 more)

### Community 3 - "AI-Constraint-Solver.contract.json"
Cohesion: 0.11
Nodes (18): -m, solver.mcp_server, capabilities, location, mcp_endpoint, args, command, transport (+10 more)

### Community 4 - "ecosystem.registry.json"
Cohesion: 0.12
Nodes (15): modules, name, orchestration_root, branch, local_path, repository, role, $schema (+7 more)

### Community 5 - "ARCH-RFC-003: Capstone Defense Standard"
Cohesion: 0.22
Nodes (21): ARCH-RFC-001, Project STRANGLER-IPU, Personal Tool Ecosystem, ARCH-RFC-001: Record Keeping Standard, ARCH-RFC-002: Multi-Model Council Protocol, ARCH-RFC-003: Capstone Defense Standard, ARCH-SPEC-001: ECIE Systems Architect Paradigm, ARCH-SPEC-002: Ingestion Processing Unit (IPU) (+13 more)

### Community 6 - "capability.contract.v1.json"
Cohesion: 0.08
Nodes (24): capabilities, category, deterministic, id, inputs, location, module, outputs (+16 more)

### Community 7 - "enum"
Cohesion: 0.17
Nodes (12): actuation, cognition, compute, formal_verification, hardware_interop, ingestion, orchestration, presentation (+4 more)

### Community 8 - "enum"
Cohesion: 0.17
Nodes (12): audit, execute, find_counterexample, maximize, minimize, synthesize, transform, verify_invariant (+4 more)

### Community 9 - "sync.ps1"
Cohesion: 0.32
Nodes (7): Ensure-RemoteConfigured(), Provision-NewTool(), Switch-ToBranch(), Write-Fail(), Write-Notice(), Write-Status(), Write-Success()

### Community 10 - "Experiment Log: INV-[ID]"
Cohesion: 0.50
Nodes (3): Experiment Log: INV-[ID], Findings & Epistemic Classification, Quantitative Metrics

### Community 11 - "properties"
Cohesion: 0.18
Nodes (11): type, format, type, type, properties, author, last_updated, license (+3 more)

### Community 12 - "warehouse_mem_sim.py"
Cohesion: 0.29
Nodes (9): main(), Warehouse Logistics Memory Simulator (Lightweight GPU-to-DRAM Discrete Event…, Upgrade v+2: Near-Memory Streaming Accumulator Instead of hauling 4096 elements…, Baseline (Naive): Every thread's request is dispatched independently without…, Upgrade v+1: Smart Coalescer & Bank-Aware Schedular 1. Deduplicates memory…, run_baseline_uncoalesced(), run_upgrade_v1_smart_coalescer(), run_upgrade_v2_near_memory_reduction() (+1 more)

### Community 13 - "enum"
Cohesion: 0.22
Nodes (9): free_tier_api, heavy_compute, paid_api, zero_token_local, default, description, enum, type (+1 more)

### Community 14 - "enum"
Cohesion: 0.25
Nodes (8): empirical_sandbox, formal_smt, heuristic_unverified, statistical_audit, verification_tier, description, enum, type

### Community 15 - "yt-dlp-live.contract.json"
Cohesion: 0.25
Nodes (7): capabilities, location, module, runtime, $schema, tracking_branch, version

### Community 16 - "sweep_ipu_breakeven.py"
Cohesion: 0.43
Nodes (7): evaluate_conventional_pipeline(), evaluate_ipu_pipeline(), sweep_ipu_breakeven.py ---------------------- Implementation of EXP-001:…, Ingress -> Bus -> Host DRAM -> Host GPU -> Compute -> Result, Ingress -> IPU (In-Flight Stream Transform) -> Interconnect (rho * data) -> Host, run_parameter_sweep(), SweepConfig

### Community 17 - "STRANGLER-IPU"
Cohesion: 0.40
Nodes (5): ARCH-SPEC-002 (IPU), Aaradhya Dev Tamrakar (ADT), GPU & RAM Architecture Spec, SPARK Wearable Gateway, STRANGLER-IPU

### Community 18 - "transcript_archiver.py"
Cohesion: 0.43
Nodes (6): evaluate_significance(), export_verbatim(), find_latest_transcript_path(), main(), transcript_archiver.py ---------------------- Deterministic utility to identify…, Evaluates whether a transcript meets the criteria for permanent archival.…

### Community 19 - "Canonical Capability Registry"
Cohesion: 0.40
Nodes (5): Experiment FLEET-001, Hypothesis HYP-002, Canonical Capability Registry, Claude Worker Fleet (v2), Super-NLM Hub

## Knowledge Gaps
- **165 isolated node(s):** `$schema`, `$id`, `title`, `description`, `type` (+160 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 184 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `properties` connect `properties` to `properties`, `capability.contract.v1.json`, `enum`, `enum`, `enum`, `enum`?**
  _High betweenness centrality (0.210) - this node is a cross-community bridge._
- **Why does `properties` connect `properties` to `properties`, `capability.contract.v1.json`?**
  _High betweenness centrality (0.173) - this node is a cross-community bridge._
- **Why does `capability` connect `capability.contract.v1.json` to `properties`?**
  _High betweenness centrality (0.152) - this node is a cross-community bridge._
- **What connects `$schema`, `$id`, `title` to the rest of the system?**
  _165 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `properties` be split into smaller, more focused modules?**
  _Cohesion score 0.06666666666666667 - nodes in this community are weakly interconnected._
- **Should `properties` be split into smaller, more focused modules?**
  _Cohesion score 0.07407407407407407 - nodes in this community are weakly interconnected._
- **Should `properties` be split into smaller, more focused modules?**
  _Cohesion score 0.0625 - nodes in this community are weakly interconnected._