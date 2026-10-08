---
name: cold-storage-archiver
description: Autonomous cold-storage packaging, pre-compressed dataset/game repack archiving, and cloud offloading engine. Enforces zero-recompression Store Mode (-m0), self-healing recovery records (-rr3% - -rr5%), 10GB cloud-volume slicing, pre-flight disk headroom triage, and offline shadow indexing into OmniVault (~/.omnivault/catalog.db).
category: storage-management
---

# Cold Storage Archiver — Large Payload & Game Repack Packaging Engine

This skill guides agents in packaging massive datasets, game installers, pre-compressed repacks, and media libraries for long-term cold storage (External HDDs, Google Drive 5TB, NAS, Glacier) without wasting CPU cycles, exhausting disk space, or risking unrecoverable bit-rot corruption.

---

## 1. Core Operating Invariants

When a user requests to archive, backup, or cloud-offload a large folder (> 10 GB) or game repack:

1. **Pre-Flight Drive Triage (`INV-CSA-001`)**:
   - Always run `Get-PSDrive -PSProvider FileSystem` before initiating an archive.
   - Never write an archive to the source drive if the remaining free space is less than `SourceSize * 1.15`.
   - Select the staging drive with the largest available headroom (e.g. `C:\` vs `D:\`).

2. **Zero-Recompression on Pre-Compressed Media (`INV-CSA-002`)**:
   - Inspect files in the target directory. If it contains game installer archives (`.bin`, `.pak`, `.ucas`, `.vpk`), media archives (`.zip`, `.rar`, `.7z`, `.gz`, `.tar.zst`), or compressed video (`.mp4`, `.mkv`), **NEVER** use standard/ultra compression (`-mx9`, `-m5`).
   - Re-compressing already compressed assets consumes 100% CPU for hours and yields $< 0.05\%$ compression.
   - **Always enforce Store Mode (`-m0`)**. This streams directly at hardware SSD/NVMe speeds (minutes instead of hours).

3. **Bit-Rot Self-Healing Invariant (`INV-CSA-003`)**:
   - A single flipped bit in an 80+ GB binary corrupts the entire installation (`ISDone.dll / Unarc.dll error`).
   - Always append a **3% to 5% Reed-Solomon Recovery Record (`-rr3%` or `-rr5%`)** or generate `.par2` parity files.

4. **Cloud-Resilient Volume Slicing (`INV-CSA-004`)**:
   - Uploading a single monolithic 80+ GB file via web or intermittent network drops is fragile.
   - Split large archives into **10 GB slices (`-v10g`)** or **20 GB slices (`-v20g`)** for Google Drive / cloud uploads. If an upload fails, only a single chunk needs to be re-uploaded.

5. **Header Encryption for Cloud Storage (`INV-CSA-005`)**:
   - For sensitive data or game repacks uploaded to Google Drive / OneDrive, use header encryption (`-hp`) with a password to prevent automated cloud content hash-scanning.

6. **Offline Catalog Registration (`INV-CSA-006`)**:
   - Before deleting local source files to reclaim disk space, register the archive metadata into **OmniVault** (`~/.omnivault/catalog.db`). This preserves instant searchability and metadata tracking even when the payload is exclusively stored in Google Drive or a disconnected drive.

---

## 2. Standard Packaging Pipeline

### A. Pre-Flight Headroom Check
```powershell
Get-PSDrive -PSProvider FileSystem | Select-Object Name, @{Name="FreeGB";Expression={[math]::Round($_.Free/1GB, 2)}}
```

### B. High-Speed Headless CLI Packaging (WinRAR `Rar.exe`)
```powershell
# Store mode (-m0), 3% recovery record (-rr3%), 10 GB cloud split (-v10g), recursive (-r)
& "C:\Program Files\WinRAR\Rar.exe" a -m0 -rr3% -v10g -r "C:\Staging_Archive\Payload.rar" "D:\SourceFolder\*"
```

*(To add header encryption against cloud scanner inspection: append `-hp"YourPassphrase"`).*

### C. 7-Zip Alternative (`7z.exe` Store Mode)
```powershell
# Copy mode (-mx=0), split into 10000m volumes (-v10g)
7z a -mx=0 -v10g "C:\Staging_Archive\Payload.7z" "D:\SourceFolder\*"
```

---

## 3. OmniVault Integration

OmniVault (`F:\Aaradhya-Dev-Tamrakar\omnivault`) is the authoritative cold-vault manager. Agents can run:

```bash
# Automated pack, split, parity, and catalog registration
omnivault pack "D:\Games\Black Myth - Wukong [FitGirl Repack]" --staging "C:\Wukong_Archive" --split 10G --parity 3% --cloud gdrive
```

### Post-Upload Lifecycle:
1. Verify MD5 / CRC checksums.
2. Upload chunks to cloud storage (Google Drive 5TB quota).
3. Purge local staging directory on `C:\`.
4. Delete source folder on `D:\` to reclaim space.
5. OmniVault shadow catalog retains complete file listing and searchability.
