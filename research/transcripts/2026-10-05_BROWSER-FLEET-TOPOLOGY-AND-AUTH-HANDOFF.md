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
| **Antigravity CLI** (`agy`) | `aaradhyadevtmr@gmail.com` | `agy -p "PONG" --dangerously-skip-permissions` | **Exit 0**, returned `PING! Ready when you are. What would you like to work on?` | Active token cache in `~/.gemini/antigravity-cli` |
| **Google AI Studio API Key** | `aaradhyadevtmr@gmail.com` | `Invoke-RestMethod -Uri "https://generativelanguage.googleapis.com/v1beta/models?key=$env:GEMINI_API_KEY"` | **HTTP 200 OK**, retrieved models `gemini-2.5-flash`, `gemini-2.5-pro`, `gemini-2.5-flash-preview-tts` | Saved in Bitwarden: `Google AI Studio API Key` (`eab48399-6626-4c91-9e45-b4da00fb824f`), cloud synced |
| **WinPilot Engine** | N/A | `winpilot.core.screen.Screen.capture_window()` | Verified silent Win32 GDI BitBlt capture (2584x1624) and UIA tree discovery | Operational in `F:\Aaradhya-Dev-Tamrakar\Utility\windows-pilot` |

---

## 2. Authoritative 5-Browser Fleet Architecture

Transcribed and cross-verified directly from user desktop screen captures (`media_1791214286317.png` through `media_1791214355691.png`):

| Browser | Image Ref | Fleet Tier / Purpose | Primary Account | Secondary & Logged-In Accounts |
| :--- | :---: | :--- | :--- | :--- |
| **Mozilla Firefox** | Image 1 | **Fleet Tier 1** (Claude Core) | **`aaradhyadevtm@gmail.com`**<br>(Aaradhya Dev Tamrakar) | • `aaradhya.claude.user0@gmail.com` (Claude User 0)<br>• `aaradhya.claude.user1@gmail.com` (Claude User 1)<br>• `kaaliz.official@gmail.com` (Kaaliz)<br>• `nabintmr@gmail.com` (Nabin TAMRAKAR)<br>• `aaradhyadevtmr@gmail.com` (Aaradhya Dev Tamrakar) |
| **Vivaldi** | Image 2 | **Fleet Tier 2** (Claude Secondary) | **`aaradhyadevtmr@gmail.com`**<br>(Aaradhya Dev Tamrakar — Pro) | • `aaradhya.claude.user2@gmail.com` (Claude User 2)<br>• `aaradhya.claude.user3@gmail.com` (Claude User 3)<br>• `aaradhya.claude.user4@gmail.com` (Claude User 4)<br>• `aaradhya.claude.user5@gmail.com` (Claude User 5)<br>• `aaradhya.claude.user6@gmail.com` (Claude User 6)<br>• `xavier.valois007@gmail.com` (Xavier Valois)<br>• `adtgames2061@gmail.com` (Aaradhya Dev Tamrakar) |
| **Microsoft Edge** | Image 3 | **Personal & Automation** | **`devtamrakaraaradhya83@gmail.com`**<br>(Aaradhya Dev Tamrakar) | • `aaradhyadevtmr@gmail.com` (Aaradhya Dev Tamrakar) |
| **Google Chrome** | Image 4 | **Multi-Profile Container**<br>*(12 distinct profiles)* | *(Profile Manager Grid)* | • **Aaradhya Dev**: `aaradhyadtmr@gmail.com`<br>• **Aaradhya Dev**: `majorprj79001@gmail.com`<br>• **Aaradhya Dev**: `aaradhya.bei79001@gmail.com`<br>• **Work**: `aaradhya.devtamrakar@ieee.org`<br>• **Amulya Dev**: `amulyadevtamrakar@gmail.com`<br>• **IEEE**: `ieee.stb.kecktm@gmail.com`<br>• **KEC**: `kec.makerspace@gmail.com`<br>• **Rupesh**: `majorprj79034@gmail.com`<br>• **Sankalpa**: `majorprj79039@gmail.com`<br>• **Sonia**: `majorprj79043@gmail.com`<br>• **The Way To**: `offonthewaytoheart@gmail.com`<br>• **Your Chrome**: Unsynced / Local |
| **Brave** | Image 5 | **Engineering / BEIE Container** | **`beie7923@gmail.com`**<br>(BEIE) | • `aaradhyadevtmr@gmail.com` *(Signed out)* |

---

## 3. Scope for the New Chat Session

1. **Secondary Google AI Studio API Key (`devtamrakaraaradhya83@gmail.com`)**:
   - Access Google AI Studio in **Microsoft Edge** where `devtamrakaraaradhya83@gmail.com` is active.
   - Harvest/create key, validate REST endpoint (`generativelanguage.googleapis.com`), and store in Bitwarden vault as `Google AI Studio API Key (devtamrakaraaradhya83)` (`bw create item` + `bw sync`).

2. **Secondary GitHub Copilot CLI Authorization (`Aaradhya-claudeuser0`)**:
   - Access **Mozilla Firefox** where `Claude User 0` (`aaradhya.claude.user0@gmail.com`) is active.
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
