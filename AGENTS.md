# AGENTS.md — Agent & Contributor Directives for Downloader Scripts

Welcome, Agent. This repository houses the desktop downloader automation suite for `downloader-scripts`.

---

## 1. Version Control & Synchronization

- **Strict Rule**: Never run raw `git add`, `git commit`, or `git push` directly.
- **Always use `sync.ps1`**:
  ```powershell
  .\sync.ps1                               # Auto commit & push with secret scan
  .\sync.ps1 -m "feat(scope): message"     # Explicit conventional message
  .\sync.ps1 -PullOnly                     # Safe pull with rebase
  ```

---

## 2. Secrets, Binaries & Media Hygiene

1. **Credentials & Tokens**:
   - `cookies.txt` contains active browser session tokens and must **NEVER** be committed.
   - `sync.ps1` runs regex pre-commit filters to detect keys and credentials.

2. **Binaries & Large Files**:
   - Never commit `yt-dlp.exe`, `.exe`, or ffmpeg binaries to the repository.
   - Never commit downloaded media files (`.mp3`, `.mp4`, `.flac`, `.wav`, `.mkv`, etc.).

3. **UX Directives**:
   - Desktop WPF cards in `scripts/clipboard-downloader.ps1` must maintain responsive UI threads (using `BackgroundWorker` or `Start-Job` for background tasks).
