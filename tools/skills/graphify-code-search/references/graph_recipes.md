# Advanced Graph Query Recipes

For specialized graph explorations beyond the standard CLI, use these deterministic Python / NetworkX recipes against `graphify-out/graph.json`.

---

## 1. Finding God Nodes (Architectural Hubs)

God nodes are functions or classes with the highest degree of connectivity (most imported, most called, or calling the most components):

```python
import json
from pathlib import Path

data = json.loads(Path('graphify-out/graph.json').read_text(encoding='utf-8'))
nodes = {n['id']: n for n in data['nodes']}
degrees = {}

for link in data['links']:
    src, tgt = link['source'], link['target']
    degrees[src] = degrees.get(src, 0) + 1
    degrees[tgt] = degrees.get(tgt, 0) + 1

top = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:10]
for nid, deg in top:
    n = nodes.get(nid, {})
    print(f"{n.get('label')} ({n.get('source_file')}:{n.get('source_location')}) -> {deg} connections")
```

---

## 2. Finding Isolated or Dead Implementations

Find functions that have 0 incoming calls in the AST:

```python
import json
from pathlib import Path

data = json.loads(Path('graphify-out/graph.json').read_text(encoding='utf-8'))
nodes = {n['id']: n for n in data['nodes'] if n.get('_callable')}
incoming = {n['id']: 0 for n in data['nodes']}

for link in data['links']:
    tgt = link['target']
    if tgt in incoming:
        incoming[tgt] += 1

unreferenced = [nodes[nid] for nid, count in incoming.items() if count == 0 and nid in nodes]
print(f"Functions with 0 recorded callers: {len(unreferenced)}")
for n in unreferenced[:10]:
    print(f"  - {n.get('label')} in {n.get('source_file')}:{n.get('source_location')}")
```

---

## 3. Extracting All Functions in a Specific Community / Module

```python
import json
from pathlib import Path

data = json.loads(Path('graphify-out/graph.json').read_text(encoding='utf-8'))
community_name = 'access.js'

community_nodes = [
    n for n in data['nodes']
    if n.get('community_name') == community_name and n.get('_callable')
]

print(f"Functions in {community_name}: {len(community_nodes)}")
for n in community_nodes:
    print(f"  - {n.get('label')} ({n.get('source_location')})")
```

---

## 4. Exporting Subgraph as Markdown Documentation

```python
import json
from pathlib import Path

def export_module_markdown(module_file: str, out_path: str):
    data = json.loads(Path('graphify-out/graph.json').read_text(encoding='utf-8'))
    module_nodes = [n for n in data['nodes'] if n.get('source_file') == module_file]
    
    md = [f"# Architecture: {module_file}\n"]
    for n in module_nodes:
        badge = "[CLASS]" if n.get('_callable_class') else ("[FUNC]" if n.get('_callable') else "[ITEM]")
        md.append(f"### {badge} {n.get('label')}")
        md.append(f"- **Location**: `{n.get('source_file')}:{n.get('source_location')}`")
        md.append(f"- **Community**: `{n.get('community_name')}`\n")
    
    Path(out_path).write_text('\n'.join(md), encoding='utf-8')
    print(f"Wrote module architecture to {out_path}")
```
