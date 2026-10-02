---
name: cp-archive-harvester
description: >-
  Autonomous competitive programming (CP) problem and optimal solution harvester using
  Chrome DevTools Protocol (CDP). Archives CS Academy, IEEEXtreme, and PreXtreme tasks with
  clean Markdown problem statements, KaTeX LaTeX math formulas, resource limits, sample I/O,
  and un-truncated 100-point solutions into IEEE-Xtreme-Archive.
---

# Competitive Programming Archive Harvester Skill (`cp-archive-harvester`)

Autonomous, high-throughput Competitive Programming problem and solution harvesting engine. Operates inside [`F:\Aaradhya-Dev-Tamrakar\IEEE-Xtreme-Archive`](file:///F:/Aaradhya-Dev-Tamrakar/IEEE-Xtreme-Archive) using Chrome DevTools Protocol (CDP) to extract client-rendered Single Page Application (SPA) data without truncated code or missing KaTeX formulas.

---

## 1. Operating Rules & Pre-Flight Checks

1. **Working Directory:** All harvesting runs must execute from `F:\Aaradhya-Dev-Tamrakar\IEEE-Xtreme-Archive`.
2. **Chrome CDP Verification:** Before running the harvester, check whether port `9222` is active:
   ```powershell
   python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:9222/json')"
   ```
3. **Starting Chrome with CDP (Safe Quoting):**
   When starting Chrome, **always use inner single quotes** around `--profile-directory` to prevent PowerShell array argument splitting:
   ```powershell
   Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList @(
       "--remote-debugging-port=9222",
       '--profile-directory=Profile 6',
       "--restore-last-session"
   )
   ```
   *(If an isolated CDP instance is preferred, pass `--user-data-dir="C:\Users\Aaradhya\.gemini\antigravity\chrome-cdp"`)*

---

## 2. Harvester CLI Commands

The engine is located at [`harvesters/csacademy_harvester.py`](file:///F:/Aaradhya-Dev-Tamrakar/IEEE-Xtreme-Archive/harvesters/csacademy_harvester.py).

### Mode A: Full Discovery & Indexing
Refreshes the catalog of all 669 tasks with difficulty, contest, solve ratio, and counts:
```powershell
python harvesters/csacademy_harvester.py --discover
```

### Mode B: Single Task Ingestion (Statement, Leaderboard & All Solutions)
Archives a single problem slug with full test case matrices:
```powershell
python harvesters/csacademy_harvester.py --slug <task_slug>
# Example:
python harvesters/csacademy_harvester.py --slug matrix_exploration
```

### Mode C: Controlled Batch Processing
Processes the next $N$ pending tasks from the catalog:
```powershell
python harvesters/csacademy_harvester.py --max-tasks 20
```

### Mode D: Full Autonomous Pipeline
Iterates over all pending cataloged tasks continuously with automated ledger checkpointing:
```powershell
python harvesters/csacademy_harvester.py
```

### Mode E: Repository Synchronization (`sync.ps1`)
All version control operations must run through `sync.ps1`:
```powershell
.\sync.ps1 -m "feat(scope): detailed summary"
```

---

## 3. Corpus Storage Schema

```text
F:\Aaradhya-Dev-Tamrakar\IEEE-Xtreme-Archive/
├── harvesters/
│   ├── cdp_engine.py                    # Lightweight WebSocket CDP client
│   └── csacademy_harvester.py           # Main extraction pipeline runner
├── ledger/
│   ├── tasks_index.json                 # Master list of all 669 tasks
│   ├── jobs_queue.json                  # Pending & completed submission jobs
│   └── archive_ledger.json              # Checkpoint ledger (completed tasks & jobs)
└── platforms/
    └── csacademy/
        ├── evaluation_environment.json  # Judge runtime specifications (Ubuntu 25.04)
        └── tasks/
            └── <task_slug>/             # e.g., addition, gcd, sorting_partition
                ├── problem.json         # Limits, score type, difficulty, ratio
                ├── statement.md         # Full Markdown with KaTeX math & I/O tables
                ├── statistics.json      # Solver count, top CPU & memory solutions
                └── submissions/
                    ├── index.json       # Registry of archived optimal solutions
                    └── <job_id>/        # e.g., 53192
                        ├── metadata.json# User, verdict, runtime, memory, language
                        ├── solution.<ext> # Clean un-truncated source code (cpp, py, java)
                        └── results.json # Granular per-test-case verification table
```

---

## 4. Invariant Quality Checks

Before completing or committing harvested batches, verify:
* **KaTeX Math Conversion:** `statement.md` must contain LaTeX math annotations (`$formula$` and `$$formula$$`), never stripped or raw unicode artifacts.
* **Un-truncated Source Code:** `solution.<ext>` must be read directly from the Ace editor buffer via `window.ace.edit(document.querySelector('.ace_editor')).getValue()`.
* **Zero Missing Test Cases:** `results.json` must be non-empty and capture granular test case numbers, CPU time, memory, and verdicts (`OK`, `WA`, `TLE`).
* **Resumability:** Ledgers must be updated atomically to prevent duplicate requests on resumption.
