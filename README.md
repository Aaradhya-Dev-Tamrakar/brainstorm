# Downloader Scripts Hub — Brainstorm Ecosystem Branch

> **Ecosystem Branch**: `downloader-scripts`  
> **Canonical Repo**: [Aaradhya-Dev-Tamrakar/downloader-scripts](https://github.com/Aaradhya-Dev-Tamrakar/downloader-scripts)  
> **Archetype**: Sensory / Ingestion Organ — Desktop Media Capture Engine  
> **Role in Jarvis**: 1-click & hotkey-driven zero-touch audio/video extraction, automated metadata embedding, and media routing  

---

## Tool Summary

Modular PowerShell and Windows Batch automation suite for batch audio/video extraction via `yt-dlp` with automatic tag and thumbnail embedding, deduplication archives, dedicated directory routing, and a modern zero-click dark card WPF UI:
- **Audio / Music**: `C:\Users\Aaradhya\Music`
- **Video**: `C:\Users\Aaradhya\Videos\yt-dlp`

| Field | Value |
|---|---|
| **Registry Index** | 22 |
| **Branch ID** | `downloader-scripts` |
| **Tech Stack** | PowerShell 7, WPF XAML, Windows Shell APIs, yt-dlp, Batch |
| **Execution Context** | Local Desktop |
| **Core Superpower** | Zero-click clipboard auto-paste downloader, 1-click WPF Audio vs Video selector dialog, dedicated routing to Music and Videos\yt-dlp, and Windows Toast notifications |
| **Local Path** | `F:\Aaradhya-Dev-Tamrakar\downloader-scripts` |

---

## ⚡ The Zero-Click Desktop Workflow

1. Copy any YouTube or YouTube Music URL (`Ctrl + C`).
2. Hit <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>D</kbd> (or double-click **`download.bat`** on your Desktop).
3. The URL is **automatically pasted** into a floating dark-mode card modal with a dedicated "Paste" button.
4. If a playlist parameter (`list=`) is detected, a dark **"Download full playlist"** checkbox appears.
5. Choose your stream:
   - **🎵 Audio Card**: Format dropdown (`MP3` *default*, `FLAC`, `M4A`, `OPUS`, `WAV`) $\to$ Click **Download Music** to save with album artwork and ID3 tags to `C:\Users\Aaradhya\Music`.
   - **🎬 Video Card**: Quality dropdown (`1080p` *default*, `4K / Max`, `720p`, `480p`, `360p`) $\to$ Click **Download Video** to save MP4 to `C:\Users\Aaradhya\Videos\yt-dlp`.

---

## Files in This Branch

```text
downloader-scripts/
├── scripts/
│   ├── clipboard-downloader.ps1 # Frameless WPF Dark UI + Toast notification download engine
│   ├── setup-hotkeys.ps1        # Desktop shortcut & hotkey installer
│   ├── yt.ps1                   # Parameterized CLI downloader (-Mode mp3|720p -Url <url>)
│   ├── yt-music.ps1             # Interactive YouTube Music downloader with tag/artwork embedding
│   ├── yt-video480.bat          # Fast 480p batch video download preset
│   └── yt-video720.bat          # 720p HD batch video download preset
├── download.bat                 # 1-click silent root launcher
├── sync.ps1                     # Automated Git synchronizer with pre-commit secret scanning
├── AGENTS.md                    # Contributor & Agent operating guidelines
├── LICENSE                      # MIT License
├── README.md                    # Ecosystem branch documentation
└── .gitignore                   # Ignores credentials, archives, executables, and media
```

---

## 📌 Ecosystem Architecture

See [`ECOSYSTEM_ARCHITECTURAL_BRAINSTORM.md`](ECOSYSTEM_ARCHITECTURAL_BRAINSTORM.md) for the full Jarvis capability mesh.
