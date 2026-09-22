# Screen Q&A — Brainstorm Ecosystem Branch

> **Ecosystem Branch**: `screen-qa-extension`
> **Canonical Repo**: [Aaradhya-Dev-Tamrakar/screen-qa-extension](https://github.com/Aaradhya-Dev-Tamrakar/screen-qa-extension)
> **Archetype**: Sensory Organ — Ambient Browser Intelligence
> **Role in Jarvis**: Real-time DOM question extraction and zero-click Gemini Flash overlay responses

---

## Tool Summary

Screen Q&A is a Manifest V3 Chrome Extension that monitors every web page for question-like text via `MutationObserver`, queries the Google Gemini Flash API, and renders non-intrusive floating answer overlays anchored precisely to the question source element. Runs continuously in the content script context — immune to MV3 service worker idle termination.

| Field | Value |
|---|---|
| **Registry Index** | 9 |
| **Branch ID** | `screen-qa-extension` |
| **Tech Stack** | Chrome MV3 (JS), Gemini Flash |
| **Execution Context** | Ambient Browser |
| **Core Superpower** | Ambient browser intelligence, instant question extraction and zero-click overlay response |
| **Local Path** | `F:\Aaradhya-Dev-Tamrakar\screen-qa-extension` |

---

## Ecosystem Position

```
[Jarvis Architecture]
  ┌─────────────────────────────┐
  │      SENSORY ORGANS         │
  │                             │
  │  ● Screen Q&A  ◄── THIS     │  DOM scanning, question detection, Gemini overlay
  │  ● SPARK                    │  Hardware telemetry & BLE fall detection
  │  ● yt-dlp-live              │  Live stream capture & RTMP relay
  └─────────────────────────────┘
```

**Compound Pipeline A — Rapid Learning Loop**:
```
Screen Q&A (extract) ──► Super-NLM (synthesize) ──► md2pdf (render) ──► RSVP Reader (flash)
```

---

## Files in This Branch

| File | Purpose |
|---|---|
| `manifest.json` | Manifest V3 extension config (background, content scripts, options) |
| `background.js` | Stateless MV3 service worker — Gemini Flash API relay |
| `content.js` | MutationObserver DOM watcher + TreeWalker anchor + overlay injector |
| `overlay.css` | Dark-theme ambient floating UI styles |
| `options.html` / `options.js` | User API key configuration via `chrome.storage.local` |
| `icons/` | Extension icon set (16×16, 48×48, 128×128) |
| `AGENTS.md` | Agent operating rules (MV3 constraints, secret hygiene) |
| `sync.ps1` | Ecosystem sync engine with Gemini key secret guard |

---

## 📌 Ecosystem Architecture

See [`ECOSYSTEM_ARCHITECTURAL_BRAINSTORM.md`](ECOSYSTEM_ARCHITECTURAL_BRAINSTORM.md) for the full Jarvis capability mesh.