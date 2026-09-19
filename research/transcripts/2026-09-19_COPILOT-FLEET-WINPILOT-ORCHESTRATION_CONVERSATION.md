# Copilot Fleet & WinPilot Orchestration Architecture Dialogue

- **Archived Date:** 2026-09-19
- **Topic:** Multi-Account Headless GitHub Copilot Fleet, WinPilot Subsystem Integration, Model/Thinking Automation, and Batched Serial Dispatch
- **Target Repositories:** `brainstorm`, `Claude-Desktop`, `windows-pilot`
- **Epistemic Provenance:** `INV-EPI-001`

---

## Turn 1

### User
just like claude fleet, can i make a copilot fleet?

### Assistant
Explored existing fleet orchestration and agent-teams patterns across repositories.

---

## Turn 2

### User
github -copilot is what I mean

### Assistant
Reviewed GitHub Copilot multi-agent features, `/fleet` CLI mode, and custom agent capabilities.

---

## Turn 3

### User
i meant worker fleet like claude-desktop that i have

### Assistant
Identified the core architecture:
> **Multiple account profiles → multiple Electron instances → unique CDP ports → programmatic fleet control**

Mapped the Claude Desktop fleet layer to a GitHub Copilot fleet equivalent using isolated VS Code user data directories (`--user-data-dir`) and remote debugging ports.

---

## Turn 4

### User
also do we need the whole app running? I want to abstract everything with minimal RAM usage. Like if we could just route it without opening VS code , then we could do the same parallelly with minimal ram and cpu footprint

### Assistant
Analyzed the weight stack from heavy GUI to headless API:
- **Full VS Code Electron:** ~400–500 MB per worker
- **VS Code headless (`serve-web`):** ~150–200 MB per worker
- **Copilot LSP Server only:** ~50–80 MB per worker
- **Direct Asynchronous Python Client (`httpx` + Local Tool Executor):** **~10–20 MB per worker**

Formulated the zero-GUI, headless Copilot worker fleet reducing RAM by 20–50× across concurrent instances inside a single Python event loop.

---

## Turn 5

### User
also note that copilot free plan auto selects model.

### Assistant
Incorporated Copilot Free tier economics into fleet role design:
- Free Copilot workers assigned to grunt tasks (`researcher`, `formatter`, `overflow_worker`).
- Claude Desktop workers preserved for heavy reasoning (`orchestrator`, `writer`, `qa_reviewer`).
- Implemented `model_used` metadata extraction from API headers for quality-aware adaptive QA routing.

---

## Turn 6

### User
log this plan to repo for now

### Assistant
Drafted and logged [`research/experiments/FLEET-002.md`](../experiments/FLEET-002.md), verified repository audit gates (`.\audit.bat`), and synchronized via `.\sync.ps1`.

---

## Turn 7

### User
i am thinking of connecting windows-pilot to these too so that they can control one another flawlessly.

### User
F:\Aaradhya-Dev-Tamrakar\windows-pilot

### Assistant
Analyzed `windows-pilot` (`F:\Aaradhya-Dev-Tamrakar\windows-pilot`) and designed the 3-Layer Interconnection Topology:
1. **Logical & Task Layer:** FastAPI DAG Orchestrator.
2. **Cognitive & Compute Layer:** Claude Desktop Fleet (CDP) + Copilot Headless Fleet (API).
3. **Physical / OS Reality Layer (`windows-pilot`):**
   - Out-of-band watchdog & modal auto-dismissal.
   - Cross-model delegation and physical window control.
   - Multimodal ground truth verification (screenshot diffs for UI QA).

---

## Turn 8

### User
Also when quota exhaustion occurs who should take control

### Assistant
Established the Authority Hierarchy for Quota Exhaustion:
- **The Dying Worker:** Flushes latest checkpoint $C_k$ to disk and yields lease.
- **The FastAPI Orchestrator:** Absolute decision authority. Re-assigns task lease to standby worker and manages cooldown pools.
- **WinPilot:** Physical switchboard actuator. Detects UI lockouts, extracts exact reset timestamps, uncloaks standby profiles on Virtual Desktop 2, and starts new chats.

---

## Turn 9

### User
claude desktop quota cannot be explicilty known as it is not shown. There will be a non obstructive popup above chat box when around 90% of limit is hit. and sometimes even that is not shown if a heavy session drains whole 5hr quota in 1 message

### Assistant
Engineered a Dual-Signal Forensic Telemetry Strategy:
1. **Early Canary Sniffing:** Detecting the 90% warning toast in DOM and tagging the profile as `DRAINING`.
2. **Sudden 1-Turn Blowout Forensic Parser:** Dead-man watchdog triggering WinPilot to inspect UI tree, parse `resets at HH:MM` via regex, and update exact cooldown timers.
3. **Pre-flight context throttling:** Pre-processing large diffs with Copilot Free workers before handing to Claude.

---

## Turn 10

### User
My plan is to run 3claude+3copilot accounts in the first test

### Assistant
Specified the 6-worker hybrid fleet topology:
- **3 Claude Desktop workers (`claude-1`, `claude-2`, `claude-3`):** CDP ports 9222–9224 on Virtual Desktop 2 (~1.2 GB RAM).
- **3 Copilot Free workers (`copilot-1`, `copilot-2`, `copilot-3`):** Zero-GUI async tasks (~45 MB RAM).
- **Total RAM:** ~1.25 GB.
- Outlined 5-stage validation pipeline (`Research` $\rightarrow$ `Decompose` $\rightarrow$ `Implement` $\rightarrow$ `Format` $\rightarrow$ `QA Review`).

---

## Turn 11

### User
Also model selection should be done by winpilot itself like clicking a series of buttons to get to the required model, and shortcut Ctrl+Shift+E can toggle thinking

*(User provided 5 screenshots of Claude Desktop UI, showing model selector menu, Effort submenu, Thinking toggle switch, and official keyboard shortcuts modal)*

### Assistant
Implemented and validated enhancements in `windows-pilot`:
1. Updated `VK_MAP` in `winpilot/core/input.py` with `VK_OEM_PERIOD` (`0xBE`) for shortcut reliability.
2. Added `ClaudeDesktopRecipe.toggle_thinking()` using `Ctrl+Shift+E`.
3. Added `ClaudeDesktopRecipe.open_model_menu()` (`Ctrl+Shift+.` with button fallback) and `set_model()` (`Sonnet 5`, `Haiku 4.5`, `Opus 5`, `Fable 5.1`).
4. Added `ClaudeDesktopRecipe.set_effort()` navigating the nested `Effort` submenu (`Low`, `Medium`, `High`, `Extra`, `Max`).
5. Upgraded `detect_cooldown()` to return structured forensic reset timestamps.
6. Exposed all actions via FastMCP in `winpilot/mcp_server.py`.
7. Created unit tests in `tests/test_claude_recipe.py` (15/15 tests passed) and synced repository.

---

## Turn 12

### User
My mental model for orchestrator to worker input method-
1. orchestrator plans task , worker and model selection.
2. calls winpilot's specific functions for each of 3 action
3. functions are predefined to select/execurthe the required series of manual tasks and also have access to clipboard history.

tally with reality

### Assistant
Audited the mental model against physical OS constraints:
- **Step 1:** 100% matched.
- **Step 2:** Matched, with the constraint that window focus is a single global OS singleton requiring sequential dispatch (~1s per window).
- **Step 3:** Predefined recipes match 100%. Highlighted that the Windows clipboard is a global shared buffer requiring mutex isolation rather than raw `Win+V`.

---

## Turn 13

### User
that I meant that tasks are batched and called through winpilot for a worker one by one

### Assistant
Confirmed that batched sequential dispatch ("Revolving Turnstile") provides:
- **Serial Injection (~1.2s per window, ~3.6s total for 3 workers) $\rightarrow$ Zero clipboard races, zero focus collisions.**
- **Parallel Background Execution $\rightarrow$ All 3 Claude instances generate simultaneously for minutes.**
- Internal clipboard history per `(task_id, worker_id)` enables instant atomic retries on UI glitches.
