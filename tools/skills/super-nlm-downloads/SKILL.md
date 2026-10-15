---
name: super-nlm-downloads
description: This skill should be used when the user pastes a Google NotebookLM link or notebook ID to download all studio artifacts (videos, quizzes, mind maps, slides, reports), requires files saved directly to the subject's downloads folder outside the repository, or asks to share downloaded folders/files via LocalSend (sharing the whole folder, or bundling files into a date-appended subfolder).
version: 1.3.0
---

# Super-NLM Studio Artifact Downloads & LocalSend Sharing Skill

This skill governs the automated downloading of Google NotebookLM Studio artifacts into dedicated external subject folders and seamless P2P sharing via LocalSend.

---

### Fleet operations

`download_mode="auto"` starts at one transfer and probes up to six using completed transfer windows (bytes / elapsed time, including CLI/server overhead). It backs off after failures or absent throughput gains, ignores tiny/incomplete samples for tuning, and shows observed MiB/s plus concurrency. This is a heuristic, not an internet line-speed test. Manual concurrency remains available. Paused batches can select Auto on resume.

Notebooks download sequentially in input order. `artifact_concurrency` controls simultaneous artifacts within the current notebook (1-6, default 1 for slow connections). The GUI offers sequential or parallel modes; a paused batch can change concurrency when resumed.

Clean filenames use the artifact title and extension (for example `Evolution of Context.mp4`). Add a short ID suffix only for name collisions; keep full IDs in the local catalog and batch manifests. Recognize and safely rename legacy type/title/UUID filenames without re-downloading. The scheduler also uses the actual artifact title when available.

### File enumeration (ascending, oldest-generated first)

Downloaded artifacts are automatically numbered in ascending order by creation time (oldest-generated first). The numbering adapts to single vs multi-notebook layouts:

- **Single-notebook** (files only, no subfolders): Files get flat sequential prefixes `1 - Title.ext`, `2 - Title.ext`, `3 - Title.ext`, ...
- **Multi-notebook** (one subfolder per notebook): Folders are numbered `0. FolderName`, `1. FolderName`, ... sorted by the oldest file creation time inside each folder. Files within each folder get hierarchical prefixes `0.1 - Title.ext`, `0.2 - Title.ext`, `1.1 - Title.ext`, ...

Already-numbered files (matching the `N - ` or `N.M - ` prefix pattern) are skipped when all files in a directory already have prefixes. Use `--no-enumerate` to skip auto-numbering, or `--enumerate-output <path>` to number files/folders in an existing directory post-hoc.

Example (multi-notebook `D:\Super-NLM FUSE AIF`):
```
0. AIF 2026 WK2 - Database & API Architecture/
   0.1 - Mastering Concurrency.mp4
   0.2 - Modern API Architecture.mp4
   0.3 - Relational SQL & AI Lifecycle.mp4
1. AIF 2026 WK4-5 - Supervised Tabular ML/
   1.1 - Bagging vs Boosting.mp4
   1.2 - ERM & The Telco Accuracy Trap.mp4
```

Downloads always use the `default` account; generation retains fleet rotation. The download CLI has no `--profile` option: set `NLM_PROFILE=default` only in the child process environment, removing inherited `NOTEBOOKLM_COOKIES`. Never switch the saved CLI default for each download.


- Use the Hub **Fleet batch** dialog to paste notebook URLs/UUIDs or include selected, filtered, or all notebooks. Download all Studio artifacts by default, optionally filter types, preview per-notebook folders, and choose an external destination.
- `get_notebook_share_status(notebook_id, profile_id?)` reads collaborators, roles and pending invitations without sharing. Unlisted accounts remain unknown. `list_notebook_sources` returns IDs/titles; `preflight_studio_generation(notebook_ids, exclude_sources?)` checks access and scope without creation.
- `schedule_batch_creation` accepts `source_ids`, `source_ids_by_notebook`, `exclude_sources`, `prompts`, and `request_key`. Notebooks multiply by prompts; `{notebook_title}` expands titles. Source exclusions can include `seed.sql`. Browser source checkboxes are not read. Explicit source IDs are validated and passed to creation.
- `pause_scheduler_dispatch` retains submitted work; `resume_scheduler_dispatch` resumes new submissions. `cleanup_scheduled_jobs(statuses?, batch_id?)` deletes terminal history only. Retry existing jobs with `run_scheduled_job_now`.
- `batch_download_artifacts(notebook_ids, artifact_types?, output_root?, notebook_folders?, skip_existing?, request_key?)` starts persistent bulk downloads. Omit types for all supported types: video, audio, report, quiz, flashcards, mindmap, slides, infographic, data-table.
- Inspect with `get_download_batch(batch_id)` / `list_download_batches()`. `resume_download_batch` retries/re-scans without generation; `pause_download_batch` pauses a locally owned batch. `download_batch_results(batch_id, output_root?)` restricts downloads to exact IDs from a generation batch.
- Output paths are on the Super-NLM host, outside repositories. Default scheduler output is `~/Downloads/Super-NLM/Generated`. Bulk batches export manifests; nonempty files indexed by artifact ID are skipped. Keep the same request key for retrying an identical submission; changed settings require a new key.
- OS leases enforce one scheduler writer. MCP forwards queue controls to the owning Hub at loopback `SUPER_NLM_HUB_URL` (default port 8000), with its configured access key. Download batch/profile/folder leases coordinate processes.
- Accepted artifact IDs persist before polling; restart resumes those IDs. Legacy interrupted jobs without IDs fail for inspection rather than automatic regeneration. Finish old-worker generations before upgrading/restarting Hub and MCP, since old workers ignore the new leases.
- Errors retain stage, notebook, profile, exit code, stdout/stderr and provider details. A generic upstream source error marks the cause unavailable; do not invent an explanation. Sharing status alone does not prove generation permission or remaining quota.
- Automated coverage uses isolated storage and mocked CLI calls. Fleet throughput and provider quotas have not been benchmarked.

### Fleet downloads through MCP

For mass generation/download, use the Hub Fleet batch GUI or Super-NLM MCP. Paste many notebook URLs/UUIDs, select all supported artifact types or filter by type, preview notebook-specific folders, and set an external output root. MCP: `batch_download_artifacts`; inspect using `get_download_batch` / `list_download_batches`; use `resume_download_batch` after interruption. Resume does not regenerate Studio artifacts. Outputs are stored on the Super-NLM host and include a batch manifest. Use this workflow when managing a large fleet; keep the script below for one-notebook downloads and authorized LocalSend sharing.

The notebook-selection bar's **Batch Download** action preloads the selected IDs into Fleet Batches; review settings and start explicitly. The grid is paginated at eight notebooks per page, and selection persists across pages. Use the **F** shortcut to open Fleet Batches and **Esc** to close it. Cards show the verified creator account and shared accounts as colored dots with a `+N` count; pending invitations are faded and `+?` means sharing status is unverified.

For mass generation/download, use the Hub Fleet batch GUI or Super-NLM MCP. Paste many notebook URLs/UUIDs, select all supported artifact types or filter by type, preview notebook-specific folders, and set an external output root. MCP: `batch_download_artifacts`; inspect using `get_download_batch` / `list_download_batches`; use `resume_download_batch` after interruption. Resume does not regenerate Studio artifacts. Outputs are stored on the Super-NLM host and include a batch manifest. Use this workflow when managing a large fleet; keep the script below for one-notebook downloads and authorized LocalSend sharing.

## ⚡ Core Operational Principles

1. **Zero Repository Pollution**:
   - Studio artifact media (videos `.mp4`, slide decks `.pdf`/`.pptx`, quizzes `.md`, mind maps `.json`) must **NEVER be saved or committed inside the active git repository** (e.g. `super-nlm` or workspace root).
   - All files must be saved directly to the subject's downloads folder under:
     `C:\Users\Aaradhya\Downloads\<SubjectFolder>` (e.g. `C:\Users\Aaradhya\Downloads\EX725 Exam`).

2. **Automated URL & Subject Resolution**:
   - Extract the notebook UUID from any Google NotebookLM link:
     `https://notebook.google.com/notebook/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})`
   - Retrieve the notebook title and identify the course or subject code (e.g. `EX725`, `ME708`, `CT653`, `CT704`, `EX751`, `EX752`).
   - Map to the canonical subject directory:
     | Course Code | Canonical Subject Directory |
     | :--- | :--- |
     | **EX725** | `C:\Users\Aaradhya\Downloads\EX725 Exam` |
     | **ME708** | `C:\Users\Aaradhya\Downloads\ME708 Exam` |
     | **CT653** | `C:\Users\Aaradhya\Downloads\CT653 Exam` |
     | **CT704** | `C:\Users\Aaradhya\Downloads\CT704 Exam` |
     | **EX751** | `C:\Users\Aaradhya\Downloads\EX751 Exam` |
     | **EX752** | `C:\Users\Aaradhya\Downloads\EX752 Exam` |
     | *Other* | `C:\Users\Aaradhya\Downloads\<SanitizedTitle>` |

3. **Deterministic LocalSend Sharing Modes**:
   - **Mode A: Share Whole Folder**:
     - When instructed to "share folder", "share everything", or "send to [Device]", send the entire subject directory (`C:\Users\Aaradhya\Downloads\<SubjectFolder>`).
     - LocalSend automatically preserves the relative directory hierarchy (e.g. `EX725 Exam/Chapter 1_ ...`).
   - **Mode B: Share Files Only**:
     - When asked to "share files only", "share the files", or send a filtered subset of artifacts:
       1. Compute today's date formatted as `YYYY-MM-DD` (e.g. `2026-10-02`).
       2. Create a dedicated date-appended subfolder inside the subject directory:
          `C:\Users\Aaradhya\Downloads\<SubjectFolder>\<SubfolderName>_<YYYY-MM-DD>`
          *(e.g. `C:\Users\Aaradhya\Downloads\EX725 Exam\EX725_2026-10-02`)*
       3. Copy the selected/requested files into that subfolder.
       4. Dispatch that newly created dated folder via LocalSend.

---

## 🛠️ Automated Execution Workflow

### Single-notebook companion script

The skill bundles an automated script at `scripts/download_and_share.mjs` that executes the full pipeline end-to-end:

```powershell
# 1. Download all artifacts from URL directly to subject downloads folder:
node C:\Users\Aaradhya\.gemini\config\skills\super-nlm-downloads\scripts\download_and_share.mjs "https://notebook.google.com/notebook/56cdad30-13d3-4621-a0b7-8f841858476b"

# 2. Download and share the entire subject folder to V2029:
node C:\Users\Aaradhya\.gemini\config\skills\super-nlm-downloads\scripts\download_and_share.mjs "https://notebook.google.com/notebook/56cdad30-13d3-4621-a0b7-8f841858476b" --share --to "V2029"

# 3. Share the existing folder only (without re-downloading):
node C:\Users\Aaradhya\.gemini\config\skills\super-nlm-downloads\scripts\download_and_share.mjs "56cdad30-13d3-4621-a0b7-8f841858476b" --share-only --to "V2029"

# 4. Share files only (automatically creates <Folder>_YYYY-MM-DD subfolder and shares):
node C:\Users\Aaradhya\.gemini\config\skills\super-nlm-downloads\scripts\download_and_share.mjs "56cdad30-13d3-4621-a0b7-8f841858476b" --files-only --to "V2029"

# 5. Share files only with keyword filter:
node C:\Users\Aaradhya\.gemini\config\skills\super-nlm-downloads\scripts\download_and_share.mjs "56cdad30-13d3-4621-a0b7-8f841858476b" --files-only --filter "Chapter" --to "V2029"

# 6. Number files/folders in an existing multi-notebook output directory:
node C:\Users\Aaradhya\.gemini\config\skills\super-nlm-downloads\scripts\download_and_share.mjs --enumerate-output "D:\Super-NLM FUSE AIF"

# 7. Download without auto-numbering:
node C:\Users\Aaradhya\.gemini\config\skills\super-nlm-downloads\scripts\download_and_share.mjs "56cdad30-13d3-4621-a0b7-8f841858476b" --no-enumerate
```

---

### Option 2: Step-by-Step CLI Execution

If executing step-by-step manually:

#### Step 1: Identify Notebook & Resolve Path
```powershell
nlm notebook get <notebook_id> --json
# Read title -> Map to C:\Users\Aaradhya\Downloads\<Subject> Exam
```

#### Step 2: Download Outside Repository
```powershell
# Stage outside repo in a temporary staging folder
$staging = "C:\Users\Aaradhya\Downloads\_nlm_staging_$([guid]::NewGuid().ToString().Substring(0,8))"
nlm download all <notebook_id> --output-dir "$staging" --skip-existing --interactive-format markdown

# Move all files into the subject folder
$dest = "C:\Users\Aaradhya\Downloads\<Subject> Exam"
Get-ChildItem -Path "$staging" -Recurse -File | Move-Item -Destination "$dest" -Force
Remove-Item -Path "$staging" -Recurse -Force
```

#### Step 3: LocalSend Sharing via `localsend-mcp`

Use `F:\Aaradhya-Dev-Tamrakar\Utility-MCPs\localsend-mcp` client:

- **For Whole Folder**:
  ```javascript
  const payloads = collectPayloads(['C:\\Users\\Aaradhya\\Downloads\\<Subject> Exam']);
  await sendFiles(config, { peer, payloads });
  ```

- **For Files Only (Dated Subfolder)**:
  ```javascript
  const dateStr = new Date().toISOString().slice(0, 10);
  const subfolder = path.join('C:\\Users\\Aaradhya\\Downloads\\<Subject> Exam', `<Subject>_${dateStr}`);
  fs.mkdirSync(subfolder, { recursive: true });
  // Copy files to subfolder
  for (const f of selectedFiles) {
    fs.copyFileSync(path.join(sourceDir, f), path.join(subfolder, f));
  }
  const payloads = collectPayloads([subfolder]);
  await sendFiles(config, { peer, payloads });
  ```

---

## 🔒 Verification & Safety Gates

1. **Repo Cleanliness Check**:
   Immediately run `git status --short` after downloads to verify no files were placed in the repo working tree.
2. **LocalSend Peer Reachability**:
   Confirm the target device (e.g. `V2029`) is discovered on LAN before dispatching file transfers.
