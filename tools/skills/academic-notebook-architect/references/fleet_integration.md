# Fleet Integration Reference: Super-NLM & Fleet-Orchestrator

## 1. Super-NLM Multi-Account Fleet Schema
- **Folder Mapping**: Configured in `data/folder_mappings.json`.
  ```json
  "<notebook_id>": {
    "notebook_id": "<notebook_id>",
    "folder_type": "local_folder",
    "target_path": "<absolute_local_path>",
    "display_name": "<CourseCode> Study Hub",
    "last_scanned": "<iso_timestamp>",
    "auto_sync": true,
    "recursive": true
  }
  ```
- **Source Capacity**: NotebookLM supports up to 300 sources per notebook. Prefer uploading high-yield summaries and syllabus extracts rather than hundreds of uncompressed raw slides.
- **Quota Safeguards**: Distribute cross-notebook queries using Super-NLM's round-robin rotator. Auto-share all course notebooks with Editor privileges across all registered fleet profiles.

## 2. Fleet-Orchestrator Swarm SKU Reference
- Define declarative DAG tasks in `Fleet-Orchestrator/sku-templates/`:
  - `pipeline`: `["research", "draft", "qa", "format"]`
  - Enqueue into `orchestrator-state/tasks/<task_id>.json`.
  - Copilot workers auto-claim tasks, execute worktrees, and commit structured markdown study outputs.
