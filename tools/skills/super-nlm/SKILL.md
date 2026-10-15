---
name: super-nlm
description: This skill should be used when interacting with Google NotebookLM fleets, querying notebooks via Super-NLM MCP, downloading and managing Studio artifacts (videos, mind maps, reports, audio overviews, quizzes), syncing Google Drive or local folders with code adapters, scheduling batch generation, and running cross-notebook synthesis.
version: 1.2.0
---

# Super-NLM Orchestrator & Fleet Management Skill

This skill provides comprehensive instructions for operating **Super-NLM**, a multi-account unified orchestrator and Model Context Protocol (MCP) server for Google NotebookLM.

---

## 1. Architectural Overview

Super-NLM enables parallel AI agents and developers to interact with $N$ Google NotebookLM accounts without hitting single-account query quotas or rate limits.

```mermaid
flowchart TD
    Agent["AI Agent / Antigravity / Claude"] -->|MCP / CLI| SuperNLM["Super-NLM Orchestrator"]
    SuperNLM --> Rotator["Round-Robin Account Rotator"]
    SuperNLM --> Scheduler["Studio Batch Scheduler"]
    SuperNLM --> DriveSync["Drive & Folder Ingestion Engine"]
    SuperNLM --> CalendarSync["Academic Calendar Copilot"]
    
    Rotator --> Acc1["Google Account 1 (Standard)"]
    Rotator --> Acc2["Google Account 2 (Standard)"]
    Rotator --> AccPro["Google Account Pro (Pro AI Model)"]
    
    Scheduler --> Artifacts["Studio Artifacts (Video, Audio, Reports, Mindmaps)"]
    DriveSync --> Storage["Ingested Sources (PDF, Code Adapter, Sheets)"]
```

### Core Engine Capabilities
1. **Round-Robin Multi-Account Rotation**: Distributes notebook queries evenly across registered accounts.
2. **Two-Tiered Rate Limiting & Cooldown**:
   - **Burst Concurrency (429 / RPM)**: 120-second cooldown while token bucket refills.
   - **Daily Quota Exhaustion (RPD)**: Automatic cooldown until 00:00 UTC midnight.
   - **Automatic Fallback**: Pending queries immediately retry on the next available account.
3. **Studio Artifact Generation & Bulk Downloads**: Batch generation of video overviews, audio deep-dives, reports, mind maps, quizzes, and flashcards with deduplicated downloads.
4. **Hybrid Folder Mapping & Drive Sync**: Ingests local files or Google Drive web folders with automatic code adapters (`.ipynb` markdown extraction, `.py`, `.c`, `.m`, `.xlsx`).
5. **Academic Calendar & Course Copilot**: Auto-matches upcoming syllabus exams/deadlines to course codes (`CT653`, `CT704`, `EX751`, `EX752`, `ME708`, `EX725`).

---

## 2. Model Context Protocol (MCP) Reference

When `super-nlm` MCP server is active, use the following tools:

### Querying & Synthesis
- **`query_notebook(notebook_id, query, conversation_id?, source_ids?, timeout?, new_conversation?, use_pro?)`**:
  Query a notebook with automatic fleet rotation and optional Pro AI routing (`use_pro=True`).
- **`cross_query(notebook_ids[], query, synthesizer_profile_id?)`**:
  Query across multiple notebooks in parallel and synthesize unified insights using Pro AI.
- **`list_notebooks(search?, profile_id?, category?)`**:
  Search and list notebooks from local cache without consuming API quota (`category`: `'study'`, `'projects'`, or `'all'`).
- **`list_profiles()`**:
  List all connected Google profiles, their tiers (`pro` vs `standard`), and status.
- **`rotation_status()`**:
  Check fleet diagnostics, active query cooldowns, and round-robin counter.

### Studio Artifact Operations & Scheduling
- **`schedule_batch_creation(notebook_ids[], artifact_type, format_option?, style?, custom_prompt?, quantity?, difficulty?, preferred_profile_id?)`**:
  Queue background studio artifact creation across multiple notebooks.
  - `artifact_type`: `'video'`, `'audio'`, `'quiz'`, `'flashcards'`, `'mind_map'`, `'report'`, `'infographic'`, `'data_table'`, `'slide_deck'`.
- **`get_scheduled_queue(status_filter?)`**:
  Inspect queue items (`pending`, `running`, `completed`, `failed`).
- **`cancel_scheduled_job(job_id)`**:
  Cancel an active or queued generation task.

### Fleet operations

#### Hub notebook and Fleet batch controls

The notebook grid shows at most **8 notebooks per page** with a visible range/total counter (for example, `1–8/51`); selections persist while paging. Each card identifies the creator account from verified owner-role metadata. Shared collaborators appear as colored account dots plus `+N`; pending invitations are visually faded. `+?` means sharing metadata is unknown, not that the notebook is unshared. Sync to refresh metadata and never infer ownership from the profile used to query the notebook. Press **F** to open Fleet Batches, **Esc** to close it, and `?` to view the shortcut reference. The selected-notebook **Batch Download** action opens Fleet Batches with those IDs prefilled for review.


`download_mode="auto"` starts at one transfer and probes up to six using completed transfer windows (bytes / elapsed time, including CLI/server overhead). It backs off after failures or absent throughput gains, ignores tiny/incomplete samples for tuning, and shows observed MiB/s plus concurrency. This is a heuristic, not an internet line-speed test. Manual concurrency remains available. Paused batches can select Auto on resume.

Notebooks download sequentially in input order. `artifact_concurrency` controls simultaneous artifacts within the current notebook (1-6, default 1 for slow connections). The GUI offers sequential or parallel modes; a paused batch can change concurrency when resumed.

Clean filenames use the artifact title and extension (for example `Evolution of Context.mp4`). Add a short ID suffix only for name collisions; keep full IDs in the local catalog and batch manifests. Recognize and safely rename legacy type/title/UUID filenames without re-downloading. The scheduler also uses the actual artifact title when available.

Downloads always use the `default` account; generation retains fleet rotation. The download CLI has no `--profile` option: set `NLM_PROFILE=default` only in the child process environment, removing inherited `NOTEBOOKLM_COOKIES`. Never switch the saved CLI default for each download.


- In the Hub Fleet batch dialog, paste notebook URLs/UUIDs or include selected, filtered, or all notebooks. Download all Studio artifact types by default; preview notebook folders and set an external destination.
- `get_notebook_share_status` inspects collaborators and roles without sending invitations. `list_notebook_sources` returns source IDs/titles. `preflight_studio_generation` checks access and source scope without creation.
- Generation accepts explicit `source_ids`, per-notebook ID maps, filename/ID exclusions, multiple prompts separated by `---`, `{notebook_title}` expansion, and idempotency keys. NotebookLM UI checkboxes are not read. Exclude `seed.sql` explicitly when intended.
- Pause/resume scheduler dispatch and clean selected terminal history through the MCP tools. Submitted Studio work continues when dispatch is paused.
- `batch_download_artifacts` accepts notebook URLs/IDs, optional artifact type filters, external root and per-notebook folder overrides. It saves persistent progress/manifests, skips nonempty files indexed by artifact ID, and supports pause/resume without regeneration. `download_batch_results` fetches only exact artifacts from a generation batch.
- Download types: video, audio, report, quiz, flashcards, mindmap, slides, infographic, data-table. Paths are on the Super-NLM host; the default scheduler output is `~/Downloads/Super-NLM/Generated`.
- OS leases enforce one scheduler writer; MCP forwards queue controls to the Hub loopback API when the Hub owns the queue. Use `SUPER_NLM_HUB_URL` to configure its loopback address.
- Generation stores accepted artifact IDs before polling and resumes those IDs after restart. Legacy interrupted jobs without IDs stop for inspection instead of automatic duplicate creation. Finish old-worker generations before restarting; old workers do not honor leases.
- Failure records retain stage, notebook, profile, process output and available provider detail. If the CLI reports only a generic source error, the cause is marked unavailable.
- Automated tests isolate data and mock CLI calls. Provider quota and fleet throughput are not benchmarked.

### Folder Mapping & Ingestion
- **`map_notebook_folder(notebook_id, target_path, folder_type?, display_name?, auto_sync?, recursive?)`**:
  Map a local filesystem path or Google Drive folder URL/ID to a notebook.
- **`get_folder_status(notebook_id)`**:
  Inspect mapped folder diffs (new, ingested, stale, unsupported) and 300-source capacity meter.
- **`sync_notebook_folder(notebook_id, action?, selected_files?)`**:
  Trigger sequential, rate-limited ingestion of new or stale sources.

### Calendar & Sharing
- **`get_agenda(days?)`**:
  Fetch upcoming schedule matched against registered course notebooks.
- **`batch_share_notebooks(notebook_ids[], target_profile_ids?, role?, auto_sync?)`**:
  Share notebooks across accounts with automatic editor permission caching.
- **`auto_share_study_courses(role?, auto_sync?)`**:
  Auto-detect all academic course notebooks and share across the fleet.

---

## 3. Direct CLI Workflows (`nlm`)

The `nlm` unified CLI can be executed directly for high-throughput batch operations:

### Studio Artifact Downloads & LocalSend Sharing
For automated URL resolution, folder routing outside the repo, and LocalSend transfers, activate the companion skill **`super-nlm-downloads`**:
```powershell
node $env:USERPROFILE\.gemini\config\skills\super-nlm-downloads\scripts\download_and_share.mjs "<notebook_url_or_id>" [--share] [--files-only] [--to "V2029"]
```
> [!IMPORTANT]
> **Zero Repo Pollution Rule**: Never download or stage artifacts inside the repository working tree. Always route to subject folders directly under `$env:USERPROFILE\Downloads\<Subject> Exam`.

To download manually into a subject folder without duplicates:
```powershell
nlm download all <notebook_id> --output-dir "$env:USERPROFILE\Downloads\<Subject> Exam" --skip-existing --interactive-format markdown
```

To download specific artifact types:
```powershell
# Download video overviews
nlm download video <notebook_id> --id <artifact_id> --output "video_title.mp4"

# Download reports/study guides
nlm download report <notebook_id> --id <artifact_id> --output "report_title.md"

# Download mind maps
nlm download mind-map <notebook_id> --id <artifact_id> --output "mindmap_title.json"
```

### Inspecting Studio Status
```powershell
nlm studio status <notebook_id> --json
```

---


## 4. Academic Course Mappings & Notebook IDs

For reference, the primary course notebooks in the ecosystem include:

| Course Code | Subject / Notebook Title | Key Notebook ID |
|---|---|---|
| **ME708** | ME708 - Organization and Management | *Resolve locally* |
| **CT653** | Artificial Intelligence | *Resolve locally* |
| **CT704** | Digital Signal Analysis and Processing | *Resolve locally* |
| **EX751** | Energy Management & Audit | *Fleet Managed* |
| **EX752** | RF & Microwave Engineering | *Resolve locally* |
| **EX725** | Embedded Systems Design | *Fleet Managed* |
| **Personal** | ⚙️ Personal Notebook | *Resolve locally* |
| **SPARK** | SPARK Research | *Resolve locally* |
| **BiasAperture** | BiasAperture Study | *Resolve locally* |

---

## 5. Ingestion Rules & Adapters

When preparing source files for ingestion via Super-NLM:
- **Direct Gemini Notebook folder preparation**: Check the current official supported-source list. Keep supported originals in their native format and create a Markdown copy only for a source type that Gemini Notebook does not accept. Preserve the original beside the copy; do not convert an entire folder or create redundant Markdown copies for supported PDFs, Office documents, Google Workspace files, images, audio, or video. This rule applies to Drive folders prepared for direct Notebook ingestion; Super-NLM's own adapters below may transform inputs within its separate ingestion flow.
- **Jupyter Notebooks (`.ipynb`)**: Never ingested raw. Super-NLM's code adapter converts markdown cells and executable code blocks into clean markdown text before uploading.
- **Source Code (`.py`, `.c`, `.cpp`, `.m`, `.ts`, `.js`, `.json`, `.sql`)**: Wrapped in code fences with syntax headers.
- **Spreadsheets (`.xlsx`, `.xls`)**: Transformed into structured CSV / Markdown data tables.
- **Unsupported Executables / Archives (`.zip`, `.exe`, `.dll`, `.iso`)**: Automatically filtered out by the ingestion scanner.
- **Capacity Gates**: Ingestion verifies target capacity (Standard: 50 sources, Pro AI: 300 sources) before triggering batch uploads.
