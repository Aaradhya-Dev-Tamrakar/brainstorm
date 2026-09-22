# AGENTS.md — Agent & Contributor Guidelines for Screen Q&A

Welcome, Agent. This repository contains the Chrome Extension Manifest V3 implementation for `screen-qa-extension`.

---

## 1. Version Control & Synchronization

- **Strict Enforcement**: Do not execute raw `git commit`, `git push`, or `git add`.
- Always use `.\sync.ps1`:
  ```powershell
  .\sync.ps1                                    # Auto commit & push
  .\sync.ps1 -m "feat(scope): message"         # Explicit semantic message
  .\sync.ps1 -PullOnly                          # Safe pull
  ```

---

## 2. Extension Architecture Directives

1. **Manifest V3 Constraints**:
   - `background.js` is an ephemeral Service Worker. It must remain stateless.
   - Do not store long-running timers or state in `background.js`.
   - Continuous DOM observation belongs in `content.js` via `MutationObserver`.

2. **Security & Privacy**:
   - Never commit Google Gemini API keys or hardcode credentials into any source file.
   - API keys are exclusively entered by the user via `options.html` and saved in `chrome.storage.local`.

3. **DOM Overlay Hygiene**:
   - Always ensure overlays use pointer-events management (`pointer-events: none` unless interactive) to prevent breaking underlying web application inputs.
