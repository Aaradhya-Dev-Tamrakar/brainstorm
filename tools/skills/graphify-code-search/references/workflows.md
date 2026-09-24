# Developer Workflows: Fast Implementation Search with Graphify

Accelerate coding and eliminate duplicate code by querying the Graphify knowledge graph before writing new implementations.

---

## Workflow 1: "Before Writing New Code" (Zero-Duplicate Rule)

Before creating a new utility, helper, algorithm, or data processor, check if an existing implementation already exists in the repository.

### Procedure:
1. **Search by Concept or Action Keyword**:
   ```bash
   python <skill_dir>/scripts/find_implementation.py "<concept_keyword>" --snippet
   ```
   *Example*: `python <skill_dir>/scripts/find_implementation.py "debounce" --snippet`
2. **Review Existing Implementations**:
   - Inspect the returned function/class definitions and their source locations (`source_file:Lxx`).
   - Look at the `--snippet` output to verify if the parameters, behavior, and edge cases meet your requirements.
3. **Check Community Context**:
   - Note the community cluster (e.g. `utils`, `audio.js`, `access.js`).
   - If a matching implementation exists, import or reuse it instead of writing a new one.

---

## Workflow 2: "Understanding How to Call an API" (Usage Pattern Discovery)

When you find a function you need to call, but want to see real-world usage examples in the codebase:

### Procedure:
1. **Inspect Incoming Callers**:
   ```bash
   python <skill_dir>/scripts/find_implementation.py callers <function_name>
   ```
   *Example*: `python <skill_dir>/scripts/find_implementation.py callers decryptHexPayload`
2. **Jump to Calling Lines**:
   - The output displays the caller function name, source file, and line number where the call occurs (e.g. `updateGatedContentVisibility() in assets/js/modules/access.js:L614`).
3. **View Real Call Site**:
   - Open the caller file at that line to see how arguments are prepared, error handling is configured, and return values are consumed.

---

## Workflow 3: "Safe Refactoring & Signature Modification" (Impact Analysis)

Before modifying a function signature, changing return types, or renaming a method, determine the blast radius:

### Procedure:
1. **Find All References & Callers**:
   ```bash
   python <skill_dir>/scripts/find_implementation.py callers <function_name> --limit 50
   ```
2. **Review Call Dependencies**:
   - Check every module that has a `calls` or `references` relation to the symbol.
3. **Update All Call Sites**:
   - Use the exact file and line locations returned by the tool to update all callers atomically.

---

## Workflow 4: "Tracing Control / Data Flow Between Two Points"

To understand how high-level UI triggers propagate down to low-level engines, storage, or APIs:

### Procedure:
1. **Run Pathfinding**:
   ```bash
   python <skill_dir>/scripts/find_implementation.py path <start_symbol> <target_symbol>
   ```
   *Example*: `python <skill_dir>/scripts/find_implementation.py path initBackgroundAnimations PCBTraces`
2. **Analyze the Intermediate Steps**:
   - Each hop shows the intermediate function/class, the relationship type (`calls`, `implements`, `contains`), and the file/line coordinates.

---

## Workflow 5: "Deep Component Analysis"

When onboarding to an unfamiliar module or preparing architectural design changes:

### Procedure:
1. **Run Explain Mode**:
   ```bash
   python <skill_dir>/scripts/find_implementation.py explain <component_symbol>
   ```
2. **Output Provided**:
   - Component classification (function, class, module).
   - Exact source file and starting line.
   - Associated architectural community cluster.
   - Top 5 incoming callers (who relies on this).
   - Top 5 outgoing dependencies (what this relies on).
   - Initial code snippet preview.
