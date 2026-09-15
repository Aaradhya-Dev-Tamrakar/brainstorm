# Original User Request

## 2026-09-15T14:34:55Z

This is a single self-contained fix; keep it small and focused. Build and deploy an automated continuous synchronization pipeline between the local/GitHub repository `brainstorm`, Google Drive (Folder ID: `1GmbXBjMaVKdfa_NSC_l67RdPaiwBw5YC`), and Google NotebookLM (`95a79d26-2f87-42cd-8cb9-8361a1e56059`).

Working directory: `F:\Aaradhya-Dev-Tamrakar\brainstorm`
Integrity mode: development

## Requirements

### R1. Drive Manifest & Sync Engine
Provide a deterministic Python synchronization utility (`scripts/sync_drive.py`) and a mapping manifest (`drive-manifest.json`) that uploads/updates curated Markdown files (`PROFILE.md`, `README.md`, `AGENTS.md`, `AARADHYA_MASTER_v165.md`, `ECOSYSTEM_ARCHITECTURAL_BRAINSTORM.md`, `report/quantitative-claims-audit.md`, `graphify-out/GRAPH_REPORT.md`) into Google Drive folder `1GmbXBjMaVKdfa_NSC_l67RdPaiwBw5YC`, preserving fixed Google Drive File IDs across updates.

### R2. GitHub Actions Automation Workflow
Create `.github/workflows/sync-drive.yml` in `brainstorm` triggered on push to `main` when tracked Markdown files change, using repository secrets (`GDRIVE_CLIENT_ID`, `GDRIVE_CLIENT_SECRET`, `GDRIVE_REFRESH_TOKEN` or equivalent credentials) to update the Drive files in-place.

### R3. NotebookLM Ingestion & Delta Refresh
Ingest the permanent Drive documents into NotebookLM notebook `95a79d26-2f87-42cd-8cb9-8361a1e56059` replacing static file uploads, and verify that updating a local file and syncing Drive triggers a successful in-place embedding refresh via Super-NLM / NotebookLM API without altering source IDs or breaking conversation citations.

## Verification Resources
- Google Drive Target Folder: `https://drive.google.com/drive/folders/1GmbXBjMaVKdfa_NSC_l67RdPaiwBw5YC`
- NotebookLM Target Notebook: `https://notebook.google.com/notebook/95a79d26-2f87-42cd-8cb9-8361a1e56059`
- Ecosystem Synchronization Script: `F:\Aaradhya-Dev-Tamrakar\brainstorm\sync.ps1`
- Super-NLM MCP Server & Python Tools: `F:\Aaradhya-Dev-Tamrakar\super-nlm`

## Acceptance Criteria

### Execution & In-Place Freshness
- [ ] `scripts/sync_drive.py` supports `--dry-run` and executes file updates against Google Drive API.
- [ ] `.github/workflows/sync-drive.yml` passes syntax verification and targets the correct manifest paths.
- [ ] Google Drive files in `1GmbXBjMaVKdfa_NSC_l67RdPaiwBw5YC` retain fixed `fileId`s after content updates.
- [ ] NotebookLM reflects the updated content on delta sync without creating duplicate sources or losing query grounding.
