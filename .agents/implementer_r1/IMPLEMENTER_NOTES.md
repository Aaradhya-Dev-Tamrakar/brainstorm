# Continuous Synchronization Pipeline: Local/GitHub -> Google Drive -> NotebookLM

## 1. Summary of Completed Deliverables

### R1. Drive Manifest & Sync Engine
- **Engine:** `scripts/sync_drive.py`
  - Deterministic synchronization engine with zero third-party dependencies (uses Python standard library `urllib`).
  - Seamless OAuth2 credential resolution across:
    1. GitHub Actions environment variables (`GDRIVE_CLIENT_ID`, `GDRIVE_CLIENT_SECRET`, `GDRIVE_REFRESH_TOKEN`, `GDRIVE_CLIENT_SECRET_JSON`).
    2. Local file fallbacks (`~/.gdrive-credentials.json` and `~/.gdrive-server-credentials.json`).
  - Automatic Google Doc conversion (`mimeType: application/vnd.google-apps.document`) on initial creation, which is required for native Google NotebookLM Drive ingestion without `SOURCE_STATUS_ERROR`.
  - In-place updates via Google Drive API `PATCH /upload/drive/v3/files/{file_id}?uploadType=media` with `Content-Type: text/plain; charset=utf-8`, preserving permanent Google Drive `fileId`s across repeated updates.
  - SHA256 content hashing to ensure idempotent zero-duplicate updates when files are unchanged.
  - Automatic existing-file adoption by filename to prevent duplicates.
  - Comprehensive CLI options: `--dry-run`, `--manifest`, `--file`, `--sync-notebook`, `--force`.
- **Manifest:** `drive-manifest.json`
  - Maps Google Drive folder `1GmbXBjMaVKdfa_NSC_l67RdPaiwBw5YC` and NotebookLM notebook `95a79d26-2f87-42cd-8cb9-8361a1e56059`.
  - Tracks all 7 required curated Markdown documents with fixed permanent `drive_file_id`s and SHA256 hashes:
    1. `PROFILE.md` -> `1K4Ve8huc9KFURX3y1i9jIC9RRQmmFN_QNqQYKKAbLLg`
    2. `AARADHYA_MASTER_v165.md` -> `1PXvkqE9ZeT6-bhb20jhMRP1cCNsqcFnNp0XKm80QH7g`
    3. `README.md` -> `1fk81kT5Y9szz5l3-jduqqNHmGTaeHx31aE9zn9eOGC8`
    4. `AGENTS.md` -> `1u4p1ZvjOtqDr6-zYxcTGdImVdrxQOnVRmSHoZ8_WPww`
    5. `ECOSYSTEM_ARCHITECTURAL_BRAINSTORM.md` -> `1ogGFwfL6OwPAXI2I7f5NEe-ZmnIWNdrOusuOd26_eh4`
    6. `report/quantitative-claims-audit.md` -> `1ZvHwSjiwR5ZI34RFCw-cQL8ZIiyxe6ec8tGMDsiNeWg`
    7. `graphify-out/GRAPH_REPORT.md` -> `1K5BBmRzLXOq6dh-7iZE1XV7u2M9B1qdE_zqymnNTfjk`

### R2. GitHub Actions Automation Workflow
- **Workflow:** `.github/workflows/sync-drive.yml`
  - Triggered on push to `main` when tracked Markdown files or sync configuration change (`'**.md'`, `'report/**'`, `'research/**'`, `'drive-manifest.json'`, `'scripts/sync_drive.py'`).
  - Sets up Python 3.12 and runs `python scripts/sync_drive.py`.
  - Uses repository secrets `GDRIVE_CLIENT_ID`, `GDRIVE_CLIENT_SECRET`, `GDRIVE_REFRESH_TOKEN`, `GDRIVE_CLIENT_SECRET_JSON`.
  - Automatically commits manifest updates with `[skip ci]` if new file IDs are registered.

### R3. NotebookLM Ingestion & In-Place Embedding Refresh
- Ingested all 7 permanent Drive documents into NotebookLM notebook `95a79d26-2f87-42cd-8cb9-8361a1e56059`:
  - `AARADHYA_MASTER_v165.md` -> `8a560c22-0a1d-4e06-9c1f-cd84979dc173`
  - `ECOSYSTEM_ARCHITECTURAL_BRAINSTORM.md` -> `913c511e-5873-4bc4-9055-fd5bc1453693`
  - `brainstorm_AGENTS.md` -> `323fc823-891a-4fd4-abb0-8749109e5a3f`
  - `brainstorm_GRAPH_REPORT.md` -> `37dd6d5b-b120-4a12-8548-4ba2e7d82e4f`
  - `brainstorm_PROFILE.md` -> `c7e4d24f-f973-416d-8fd3-9af35970f677`
  - `brainstorm_README.md` -> `59e77658-f973-4b58-b5c5-9278d7564a25`
  - `quantitative-claims-audit.md` -> `8658284e-2f11-4479-9b20-ef40f52b9d81`
- Replaced the 7 old static/pasted `generated_text` source uploads by deleting them via `nlm source delete`.
- Performed end-to-end delta refresh verification:
  - Added new section with `Delta Sync Verification Token: AUDIT-SYNC-TOKEN-2026-09-15-INPLACE-REFRESH-OK` to `report/quantitative-claims-audit.md`.
  - Ran `python scripts/sync_drive.py` -> PATCH succeeded (HTTP 200 OK) preserving Drive ID `1ZvHwSjiwR5ZI34RFCw-cQL8ZIiyxe6ec8tGMDsiNeWg`.
  - NotebookLM flagged source `8658284e-2f11-4479-9b20-ef40f52b9d81` as `stale: true`.
  - Executed delta sync (`source_sync_drive`) -> source transitioned to `stale: false` while retaining exact source ID `8658284e-2f11-4479-9b20-ef40f52b9d81`.
  - Queried NotebookLM -> retrieved the exact verification token citing source `8658284e-2f11-4479-9b20-ef40f52b9d81` with 100% grounding.

## 2. Verification Gates
- `.\audit.bat`: 0 Discrepancies Found across 132 files.
- `.\sim.bat`: Simulation completed without regressions.
- `python scripts/sync_drive.py --dry-run`: Verified.
- `python scripts/sync_drive.py`: Live execution verified.
- NotebookLM live query: Verified.
