---
name: graphify-code-search
description: This skill should be used when the user asks to "search for implementation", "find function definition", "find how X is implemented", "find callers of", "who calls this function", "what does this function call", "check if we already have a helper for", "trace call chain", "search implementation with graphify", or when looking to speed up coding by discovering and reusing existing codebase implementations via the Graphify knowledge graph.
version: 1.0.0
---

# Graphify Code Search: Implementation Discovery Engine

Use the repository's Graphify knowledge graph (`graphify-out/graph.json`) to rapidly locate existing function/class definitions, callers, callees, and real-world usage patterns in milliseconds before writing new code.

---

## 1. Purpose & Core Advantage

Coding in medium-to-large codebases is slowed down by:
1. **Linear file hunting**: Guessing filenames or running slow, noisy grep searches across dozens of files.
2. **Reinventing the wheel**: Writing redundant utilities, helpers, or data transforms that already exist in other modules.
3. **API uncertainty**: Not knowing which functions call an implementation or what arguments and side effects are expected.

**The Graphify Solution**:
Instead of reading files blindly, query the pre-extracted AST knowledge graph (`graphify-out/graph.json`). It provides:
- **Instant symbol resolution**: Exact file paths and line numbers (`file.ext:Lxx`).
- **Dependency context**: Who calls the symbol (callers) and what the symbol depends on (callees).
- **Direct snippet previews**: Reads and displays the live source code around the definition line.
- **Dependency paths**: Shortest execution/call chains between any two components.

---

## 2. Quick Command Reference

All commands run through the bundled zero-dependency Python search engine:
`python C:\Users\Aaradhya\.gemini\config\skills\graphify-code-search\scripts\find_implementation.py`

*(Or simply `find_implementation.py` when in the skill directory or added to PATH).*

### Search for Implementations & Functions
```bash
# General keyword / concept search
python <skill_dir>/scripts/find_implementation.py "decrypt"

# Search with live code preview (first 15 lines)
python <skill_dir>/scripts/find_implementation.py "decrypt" --snippet --lines 15

# Search with callers and callees displayed
python <skill_dir>/scripts/find_implementation.py "decrypt" --callers --callees

# Filter by node type (function or class)
python <skill_dir>/scripts/find_implementation.py "modal" --type func
python <skill_dir>/scripts/find_implementation.py "animation" --type class

# Filter by file path or pattern
python <skill_dir>/scripts/find_implementation.py "init" --file "assets/js/*"
```

### Trace Callers (Who Calls This?)
```bash
# Find all functions and modules that call or reference a symbol
python <skill_dir>/scripts/find_implementation.py callers decryptHexPayload
```

### Trace Callees (What Does This Call?)
```bash
# Find all outgoing dependencies and function calls made by a symbol
python <skill_dir>/scripts/find_implementation.py callees decryptHexPayload
```

### Trace Call Paths (How Does A Connect to B?)
```bash
# Shortest call chain between two functions or components
python <skill_dir>/scripts/find_implementation.py path updateGatedContentVisibility getDecryptionKey
```

### Explain Component Context
```bash
# Comprehensive architectural summary: location, cluster, callers, callees, code snippet
python <skill_dir>/scripts/find_implementation.py explain PCBTraces
```

### Machine-Readable JSON Output (For Agents & Automation)
```bash
python <skill_dir>/scripts/find_implementation.py "auth" --snippet --json
```

---

## 3. Standard Agent Workflow for Coding Tasks

When tasked with implementing a feature, fixing a bug, or adding a utility:

### Step 1: Pre-Code Search (Zero Duplication)
1. Formulate 1-3 search keywords describing the functionality needed (e.g. `toast`, `debounce`, `cache`, `dialog`, `encrypt`, `sanitize`).
2. Run `find_implementation.py "<keyword>" --snippet`.
3. If an existing implementation is found:
   - Check if it can be directly imported or reused.
   - If not directly reusable, use its structure, conventions, and error handling as a blueprint.

### Step 2: Signature & Caller Inspection
1. Before invoking or modifying a function, run `find_implementation.py callers <symbol>`.
2. Review the calling lines to see actual invocation examples (e.g., arguments passed, async/await handling).

### Step 3: Refactoring Impact Check
1. When modifying or deprecating a symbol, run `find_implementation.py callers <symbol> --limit 50`.
2. Inspect every caller location returned and update all call sites atomically.

---

## 4. Graph Availability & Freshness Gate

The search engine automatically locates `graphify-out/graph.json` by searching the current working directory and traversing up parent directories to the repository root.

- If `graphify-out/graph.json` is missing or out-of-date after significant code changes:
  - In repositories with `sync.ps1` (e.g. `AaradhyaDT.github.io`):
    ```powershell
    .\sync.ps1 -SkipPush -PullOnly   # or graphify update .
    ```
  - In standard repositories:
    ```bash
    graphify .
    ```

---

## 5. Additional Documentation

For deeper procedures and specialized graph analyses:
- **`references/workflows.md`**: Step-by-step developer workflows for API discovery, refactoring impact analysis, and control-flow tracing.
- **`references/graph_recipes.md`**: Advanced NetworkX & Python scripts for architectural hub detection, dead-code elimination, and subgraph documentation export.
