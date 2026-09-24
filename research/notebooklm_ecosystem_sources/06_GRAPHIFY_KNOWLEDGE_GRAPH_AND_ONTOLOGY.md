# Document 6: Graphify Knowledge Graph & Capability Contracts

## 1. Graphify Knowledge Graph Topology

The entire 22-module ecosystem is indexed into a persistent **Graphify Knowledge Graph** stored under `graphify-out/` in `brainstorm`. This graph models the interconnections between computational modules, RFC specifications, research logs, hardware interfaces, and academic disciplines.

### God Nodes & Central Bridges
- **`brainstorm`**: Central architectural root, ontology holder, and verification supervisor.
- **`super-nlm`**: Primary cognitive ingestion and multi-account query aggregator.
- **`sync.ps1`**: Unified Git operational backbone orchestrating 25 remote tracking branches.
- **`md2pdf-desktop`**: Universal compilation and academic rendering bridge for reports and dossiers.
- **`schemas/capability-registry.yaml`**: Single source of truth defining module inputs, outputs, and evidence tiers.

### Knowledge Graph Traversal & Querying
The graph can be traversed deterministically using Graphify CLI commands:
- `graphify query "<question>"`: Broad breadth-first search across all modules.
- `graphify query "<question>" --dfs`: Deep causal trace through dependency chains.
- `graphify path "<ModuleA>" "<ModuleB>"`: Discovers the shortest inter-tool communication path.
- `graphify explain "<NodeName>"`: Plain-language architectural summary of any component.

---

## 2. Formal Capability Contracts Specification

Every tool module adheres to the formal JSON capability schema defined in `schemas/capability.contract.v1.json`.

### Contract Structure
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "contract_version": "1.0.0",
  "id": "module-identifier",
  "name": "Human-Readable Name",
  "category": "computational_engine | actuation | ingestion | presentation",
  "execution_context": "Local Desktop | Edge Hardware | Cloud / Hybrid",
  "interfaces": [
    {
      "type": "mcp | cli | rest_api | win32_api",
      "endpoint": "tool_name or cli command",
      "inputs": { ... },
      "outputs": { ... },
      "latency_p95_ms": 150
    }
  ],
  "evidence_tier": "E0 | E1 | E2 | E3 | E4 | E5",
  "invariants": [
    "Determinism invariant",
    "Zero-data-loss invariant"
  ]
}
```

### Dynamic Reconciliation Mechanics
Whenever capability files, RFCs, or module contracts change:
- `sim/reconciliation_engine.py` dynamically scans all local directories, reads JSON schemas, reconciles counts across `schemas/ecosystem.registry.json`, `schemas/capability-registry.yaml`, and `README.md`, and validates contract compliance with **zero manual editing**.
