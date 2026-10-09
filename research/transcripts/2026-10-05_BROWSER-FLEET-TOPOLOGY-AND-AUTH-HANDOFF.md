# Browser Fleet Topology & Authentication Verification Handoff

**Session Date**: 2026-10-05  
**Origin Conversations**:  
- Session 1: `7baac591-96ac-43a8-a614-257b84e08eed` (Bitwarden CLI/MCP setup & vault unlocking)  
- Session 2: `1381eba0-fa3d-4255-acf3-6e41b56442ac` (Single-login verification & browser fleet topology)  
**Author**: Aaradhya Dev Tamrakar & Antigravity  
**Repository**: `f:\Aaradhya-Dev-Tamrakar\brainstorm`  
**Epistemic Tier**: `EMPIRICALLY_VERIFIED`  

---

## 1. Verified Single-Login Baselines (Completed in Session 2)

All three target authentication types were empirically tested, verified, and certified:

| Service | Active Account | Verification Command / Gate | Result & Proof | Vault Status |
| :--- | :--- | :--- | :--- | :--- |
| **GitHub Copilot CLI** (`copilot`) | `AaradhyaDT` (keyring) | `copilot -p "echo Copilot active" --allow-all` | **Exit 0**, returned `Copilot active`, 0.63 AI credits consumed, 31.1k tokens in / 99 tokens out | Keyring present in Windows Credential Manager |
| **Antigravity CLI** (`agy`) | `primary-auth@account.internal` | `agy -p "PONG" --dangerously-skip-permissions` | **Exit 0**, returned `PING! Ready when you are. What would you like to work on?` | Active token cache in `~/.gemini/antigravity-cli` |
| **Google AI Studio API Key** | `primary-auth@account.internal` | `Invoke-RestMethod -Uri "https://generativelanguage.googleapis.com/v1beta/models?key=$env:GEMINI_API_KEY"` | **HTTP 200 OK**, retrieved models `gemini-2.5-flash`, `gemini-2.5-pro`, `gemini-2.5-flash-preview-tts` | Saved in Bitwarden: `Google AI Studio API Key` (`eab48399-6626-4c91-9e45-b4da00fb824f`), cloud synced |
| **WinPilot Engine** | N/A | `winpilot.core.screen.Screen.capture_window()` | Verified silent Win32 GDI BitBlt capture (2584x1624) and UIA tree discovery | Operational in `F:\Aaradhya-Dev-Tamrakar\Utility\windows-pilot` |

---

## 2. Authoritative 5-Browser Fleet Architecture

Transcribed and cross-verified directly from user desktop screen captures (`media_1791214286317.png` through `media_1791214355691.png`):

| Browser | Image Ref | Fleet Tier / Purpose | Primary Account | Secondary & Logged-In Accounts |
| :--- | :---: | :--- | :--- | :--- |
| **Mozilla Firefox** | Image 1 | **Fleet Tier 1** (Claude Core) | **`tier1-primary@account.internal`**<br>(Aaradhya Dev Tamrakar) | • `claude.worker.0@account.internal` (Claude User 0)<br>• `claude.worker.1@account.internal` (Claude User 1)<br>• `account-tier1-alt1@account.internal`<br>• `account-tier1-alt2@account.internal`<br>• `tier1-sync@account.internal` |
| **Vivaldi** | Image 2 | **Fleet Tier 2** (Claude Secondary) | **`tier2-primary@account.internal`**<br>(Aaradhya Dev Tamrakar — Pro) | • `claude.worker.2@account.internal` (Claude User 2)<br>• `claude.worker.3@account.internal` (Claude User 3)<br>• `claude.worker.4@account.internal` (Claude User 4)<br>• `claude.worker.5@account.internal` (Claude User 5)<br>• `claude.worker.6@account.internal` (Claude User 6)<br>• `tier2-alt1@account.internal`<br>• `tier2-alt2@account.internal` |
| **Microsoft Edge** | Image 3 | **Personal & Automation** | **`edge-automation@account.internal`**<br>(Aaradhya Dev Tamrakar) | • `edge-secondary@account.internal` |
| **Google Chrome** | Image 4 | **Multi-Profile Container**<br>*(12 distinct profiles)* | *(Profile Manager Grid)* | • **Profile 1**: `chrome.worker.01@account.internal`<br>• **Profile 2**: `chrome.worker.02@account.internal`<br>• **Profile 3**: `chrome.worker.03@account.internal`<br>• **Work**: `work.academic@account.internal`<br>• **Profile 5**: `chrome.worker.05@account.internal`<br>• **Affiliate 1**: `affiliate.01@account.internal`<br>• **Affiliate 2**: `affiliate.02@account.internal`<br>• **Cohort 1**: `cohort.worker.01@account.internal`<br>• **Cohort 2**: `cohort.worker.02@account.internal`<br>• **Cohort 3**: `cohort.worker.03@account.internal`<br>• **Profile 11**: `chrome.worker.11@account.internal`<br>• **Your Chrome**: Unsynced / Local |
| **Brave** | Image 5 | **Engineering / BEIE Container** | **`brave-engineering@account.internal`**<br>(BEIE) | • `brave-secondary@account.internal` *(Signed out)* |

---

## 3. Scope for the New Chat Session

1. **Secondary Google AI Studio API Key (`edge-automation@account.internal`)**:
   - Access Google AI Studio in **Microsoft Edge** where `edge-automation@account.internal` is active.
   - Harvest/create key, validate REST endpoint (`generativelanguage.googleapis.com`), and store in Bitwarden vault as `Google AI Studio API Key` (`bw create item` + `bw sync`).

2. **Secondary GitHub Copilot CLI Authorization (`Aaradhya-claudeuser0`)**:
   - Access **Mozilla Firefox** where `Claude User 0` (`claude.worker.0@account.internal`) is active.
   - Complete GitHub Device Code flow (`https://github.com/login/device`) via WinPilot.
   - Execute verification gate: `copilot -p "echo Copilot active (claudeuser0)" --allow-all`.

---

## 4. Environment & Execution Context

- **Bitwarden Session Key**:
  ```powershell
  $env:BW_SESSION = [Environment]::GetEnvironmentVariable("BW_SESSION", "User")
  ```
- **WinPilot Python Runtime**:
  `F:\Aaradhya-Dev-Tamrakar\Utility\windows-pilot\.venv\Scripts\python.exe`
- **WinPilot Repository Root**:
  `F:\Aaradhya-Dev-Tamrakar\Utility\windows-pilot`
- **Edge Binary**:
  `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`
- **Firefox Binary**:
  `C:\Program Files\Mozilla Firefox\firefox.exe`
