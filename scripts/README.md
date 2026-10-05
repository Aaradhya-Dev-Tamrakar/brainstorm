# 🛠️ Ecosystem Scripts & Local Automation Suite

This directory contains standalone PowerShell, Python, and Batch utilities that automate local development, media processing, cross-drive synchronization, hotkey bindings, and OS-level environment routing.

---

## 📂 Catalog of Scripts

### 0. Deterministic Environment Bootstrap & Antigravity Setup
- **File:** [`bootstrap-environment.ps1`](bootstrap-environment.ps1) — Single-command reproducible setup script for new machines or clean OS installations.
- **Actions Executed:**
  1. Validates Python runtime (3.10+) and installs core dependencies (`requirements.txt`, `beautifulsoup4`, `pyyaml`, `simpy`).
  2. Deploys global CLI tools (`save-chat`, `save-doc`) to Python Scripts / User `PATH`.
  3. Synchronizes all 19 Antigravity custom skills from `tools/skills/` into `$HOME/.gemini/config/skills/`.
  4. Runs deterministic verification audit (`audit.bat`) to guarantee zero-discrepancy operational readiness.

---

### 1. Windows Environment & User Shell Folders (Selective OneDrive Bypass)
- **Files:**
  - [`setup-user-shell-folders.ps1`](setup-user-shell-folders.ps1) — Idempotent PowerShell script to verify folder structures, expand variables, and set registry keys.
  - [`user_shell_folders.reg`](user_shell_folders.reg) — Direct registry export of `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders`.
- **Architectural Rationale:**
  - **Decoupled Local Media / Zero-Latency Capture:**
    - `Pictures / Images`: `%USERPROFILE%\Images`
    - `Screenshots`: `%USERPROFILE%\Images\Screenshots`
    - `Downloads`: `%USERPROFILE%\Downloads`
    - `Videos / Music`: `%USERPROFILE%\Videos`, `%USERPROFILE%\Music`
    - *Purpose:* Prevents screenshots and bulky local media from relying on OneDrive cloud connectivity, eliminating network sync latency, quota exhaustion, and offline capture errors.
  - **Retained Cloud Sync:**
    - `Desktop`: `C:\Users\Aaradhya\OneDrive\Desktop`
    - `Personal / Documents`: `C:\Users\Aaradhya\OneDrive\Documents`
    - *Purpose:* Keeps lightweight daily productivity documents and desktop shortcuts continuously backed up and synchronized across devices automatically without manual handling.

---

### 2. Media Ingestion & YouTube Automation
- **[`clipboard-downloader.ps1`](clipboard-downloader.ps1):** WPF GUI and background daemon for zero-click clipboard URL auto-paste, audio/video extraction, and dual-directory routing.
- **[`yt-music.ps1`](yt-music.ps1):** High-bitrate audio extraction pipeline via `yt-dlp` and `ffmpeg` (flac/opus/mp3).
- **[`yt-video480.bat`](yt-video480.bat) / [`yt-video720.bat`](yt-video720.bat):** Low-overhead quick-download presets for reference videos and tutorials.
- **[`yt.ps1`](yt.ps1):** General-purpose YouTube download wrapper script.

---

### 3. Media Transcoding & Stream Copying (FFmpeg Engine)
- **[`convert-media.ps1`](convert-media.ps1):** Multi-mode converter engine with dark WPF GUI, clipboard auto-path detection, batch recursion, and toast notifications.
- **[`convert-media.bat`](convert-media.bat):** 1-click desktop/terminal launcher for the Media Converter GUI.
- **[`convert-ts.bat`](convert-ts.bat):** Ultra-fast stream-copy remuxing wrapper for `.ts` -> `.mp4` (drag-and-drop or active folder execution).

---

### 4. Local Cloud & Device Sync
- **[`sync_drive.py`](sync_drive.py):** Google Drive / local filesystem synchronizer with file hash comparison, rate limiting, and manifest tracking.
- **[`setup-hotkeys.ps1`](setup-hotkeys.ps1):** Configures ecosystem keyboard triggers and global execution hotkeys.

---

### 5. P2P Dataset Packaging, Headless Seeding & Swarm Marketplace
- **[`make_dataset_torrent.py`](make_dataset_torrent.py):** Standalone pure-Python (zero external dependencies) BitTorrent v1 packager and Magnet URI generator. Automatically computes optimal chunk sizes (512 KB–16 MB), embeds Tier-1 public trackers + AcademicTorrents announce tiers, and supports BEP 0019 HTTP web-seeds.
- **[`seed_dataset.ps1`](seed_dataset.ps1):** Automated PowerShell seeder utilizing `aria2c` with DHT, PEX, and Local Peer Discovery (LPD) for high-speed local LAN/campus swarming.
- **[`start_marketplace.ps1`](start_marketplace.ps1):** Launches the **Brainstorm & Campus Swarm Marketplace** web portal (`tools/swarm_marketplace/`) with automatic Wi-Fi/LAN IP detection for campus distribution, QR code generation, and Cohort Pro role gating (`cohort-pro-2026`).

---

## 🚀 Usage

### Applying Shell Folders Setup
```powershell
# Run PowerShell as User / Administrator
.\scripts\setup-user-shell-folders.ps1

# Restart Explorer to propagate changes across all running applications
Stop-Process -Name explorer -Force
```
