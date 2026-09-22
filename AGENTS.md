# AGENTS.md — Agent Directives for yt-dlp-live

Welcome, Agent. This repository provides operational tooling for high-resilience YouTube live recording, RTMP relays, and automated remuxing.

---

## 1. Version Control Enforcement

- **Strict Rule**: Never execute manual `git add`, `git commit`, or `git push` directly.
- **Use `sync.ps1` exclusively**:
  ```powershell
  .\sync.ps1                               # Automated sync
  .\sync.ps1 -m "feat(scope): summary"     # Semantic commit
  .\sync.ps1 -PullOnly                     # Safe pull
  ```

---

## 2. Secrets & Safety Invariants

1. **Credentials & Stream Keys**:
   - `stream_key.txt` and `cookies.txt` contain high-entropy private credentials and must **NEVER** be committed or un-ignored.
   - `sync.ps1` runs a mandatory regex pre-commit scan for tokens and keys.

2. **Binary & Media Isolation**:
   - Never commit `yt-dlp.exe`, `.ts`, `.mp4`, `.mkv`, or any captured media to git tracking.
   - Store all media outputs in the gitignored `downloads/` folder.

3. **Lossless Video Operations**:
   - Prefer stream copying (`-c copy` / `-c:v copy`) over transcoding to preserve CPU/GPU cycles and eliminate generational loss.
