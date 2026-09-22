# yt-dlp-live — Brainstorm Ecosystem Branch

> **Ecosystem Branch**: `yt-dlp-live`
> **Canonical Repo**: [Aaradhya-Dev-Tamrakar/yt-dlp-live](https://github.com/Aaradhya-Dev-Tamrakar/yt-dlp-live)
> **Archetype**: Sensory Organ — Live Media Capture & RTMP Relay Daemon
> **Role in Jarvis**: Resilient live stream recording, lossless remuxing, and real-time RTMP broadcast relay

---

## Tool Summary

A production-grade automation suite for capturing, relaying, and broadcasting YouTube Live streams with zero CPU re-encoding (pure stream copy), resilient MPEG-TS container protection against network dropouts, automatic DVR backlog recovery, and simultaneous tee-muxed RTMP relay + local archive recording.

| Field | Value |
|---|---|
| **Registry Index** | 11 |
| **Branch ID** | `yt-dlp-live` |
| **Tech Stack** | PowerShell, yt-dlp, FFmpeg, streamlink |
| **Execution Context** | Local Daemon |
| **Core Superpower** | Resilient live stream capture daemon, RTMP relay, and autonomous lossless media transformer |
| **Local Path** | `F:\Aaradhya-Dev-Tamrakar\yt-dlp-live` |

---

## Ecosystem Position

```
[Jarvis Architecture]
  ┌─────────────────────────────┐
  │      SENSORY ORGANS         │
  │                             │
  │  ● Screen Q&A               │  DOM scanning, question detection, Gemini overlay
  │  ● SPARK                    │  Hardware telemetry & BLE fall detection
  │  ● yt-dlp-live  ◄── THIS    │  Live stream capture & RTMP relay
  └─────────────────────────────┘
```

**Integration with Jarvis**:
- `yt-dlp-live` is a **raw media ingestion engine** — it captures the live world into structured local archives.
- Future: Pipe captured stream metadata into **Super-NLM** for automated research synthesis, or trigger **Alpha-SuperApp** mobile notifications on stream completion.

---

## Files in This Branch

| File | Purpose |
|---|---|
| `record_live.ps1` / `record_live.bat` | Interactive YouTube Live recorder — MPEG-TS capture + auto MP4 remux |
| `relay_live.ps1` / `relay_live.bat` | Simultaneous RTMP relay + local archive via FFmpeg tee muxer |
| `stream_file_live.bat` | Local video file broadcaster to YouTube RTMP ingest |
| `yt-dlp.conf` | Portable config: network resilience, 480p cap, safe Windows filenames |
| `AGENTS.md` | Agent rules: secrets/stream key invariants, lossless copy principle |
| `sync.ps1` | Ecosystem sync engine with stream key & credential pre-commit guards |

---

## Security Rules

The following are **strictly gitignored** — never commit these:
- `stream_key.txt` — private YouTube RTMP ingest key
- `cookies.txt` — YouTube session authentication
- `downloads/` — captured recordings and raw streams
- `yt-dlp.exe` — binary executable

---

## 📌 Ecosystem Architecture

See [`ECOSYSTEM_ARCHITECTURAL_BRAINSTORM.md`](ECOSYSTEM_ARCHITECTURAL_BRAINSTORM.md) for the full Jarvis capability mesh.