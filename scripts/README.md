# 🛠️ Ecosystem Scripts & Local Automation Suite

This directory contains standalone PowerShell, Python, and Batch utilities that automate local development, media processing, cross-drive synchronization, hotkey bindings, and OS-level environment routing.

---

## 📂 Catalog of Scripts

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

### 3. Local Cloud & Device Sync
- **[`sync_drive.py`](sync_drive.py):** Google Drive / local filesystem synchronizer with file hash comparison, rate limiting, and manifest tracking.
- **[`setup-hotkeys.ps1`](setup-hotkeys.ps1):** Configures ecosystem keyboard triggers and global execution hotkeys.

---

## 🚀 Usage

### Applying Shell Folders Setup
```powershell
# Run PowerShell as User / Administrator
.\scripts\setup-user-shell-folders.ps1

# Restart Explorer to propagate changes across all running applications
Stop-Process -Name explorer -Force
```
