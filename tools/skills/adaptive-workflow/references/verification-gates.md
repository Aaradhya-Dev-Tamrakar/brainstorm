# Deterministic Verification Gates & Reality Layer

This document details the deterministic verification gates required before committing or finalizing work across the ecosystem. Speculative text is never ground truth; deterministic execution is.

---

## 1. Local Language & Runtime Verification

### Python Projects
```powershell
# Fast static linting and formatting check
uv run --extra dev ruff check src/
uv run --extra dev ruff format --check src/

# Test suite execution with coverage
uv run --extra dev pytest -v
```

### Node.js & TypeScript Projects
```bash
# Linter check
npm run lint

# Unit and component tests
npm test
```

### PowerShell & Automation Scripts
```powershell
# Pester unit tests
Invoke-Pester .\tests\ -Output Detailed
```

### Universal Makefile Targets (Where Present)
```bash
make lint       # Static analysis
make format     # Formatting verification
make test       # Test suites
make verify     # Combined verification gate
```

---

## 2. Central Ecosystem Verification (`brainstorm`)

The brainstorm repository maintains specific verification engines to ensure consistency across 27 modules, 31 branches, and formal LaTeX research reports.

### 1. Structural Consistency & Audit Gate (`audit.bat`)
```powershell
.\audit.bat
```
- Executes `sim/reconciliation_engine.py`.
- Validates JSON schemas against `schemas/capability.contract.v1.json` and `schemas/ecosystem.registry.json`.
- Enforces cross-branch inventory counts and doc synchronization.
- **Pass Criteria**: `0 errors`.
- **Auto-Repair**: Run `.\audit.bat --fix` to automatically synchronize physical counts.

### 2. Numerical Queue Simulation (`sim.bat`)
```powershell
.\sim.bat
```
- Executes `sim/warehouse_mem_sim.py` (discrete-event queue simulation).
- Confirms absence of regression in numerical or performance models.

### 3. LaTeX Research Dossier Compilation (`build_report.bat`)
```powershell
.\build_report.bat
```
- Compiles the formal LaTeX research report into `report/main.pdf`.

---

## 3. Portfolio Repository Verification (`AaradhyaDT.github.io`)

The canonical portfolio repository (`F:\AaradhyaDT\AaradhyaDT.github.io`) enforces a 26-category verification suite:

```powershell
python scripts/verify.py
```

### Critical Verification Invariants:
1. **Category 26 (Release SHAs)**:
   - Synthetic placeholder SHAs (e.g. `rel50`, `upg47`, `xtool20`) are strictly forbidden.
   - All commit references in `releases.js` must match `^[0-9a-f]{7,40}$` and resolve to authentic Git commits.
2. **Category 14 (Link Integrity)**:
   - Validates that every `id` referenced in navigation or deep links matches an existing element.
3. **Category 22 (Filter Pill Recounting)**:
   - Ensures project counts on UI filter pills match actual filtered project totals.

---

## 4. Formal SMT / Z3 Verification Gates

When designing protocol contracts, concurrency primitives, or invariant guarantees:
1. Model system states in Python Z3 (`import z3`).
2. Express safety invariants (`z3.ForAll`, `z3.Exists`, or state transition assertions).
3. Confirm satisfiability (`s.check() == z3.sat`) and absence of counterexamples.
4. Document the proof in the experiment log and assign the epistemic label `FORMALLY_PROVEN`.

---

## 5. CI Runner Bypass & Quota Protection

To prevent unnecessary GitHub Actions runner consumption on doc, research, and note changes:
- Use `-SkipCI` with `sync.bat`:
  ```powershell
  .\sync.bat -SkipCI -m "docs(notes): update research log"
  ```
- Make sure workflows define explicit `paths:` triggers and concurrency groups (`cancel-in-progress: true`).
