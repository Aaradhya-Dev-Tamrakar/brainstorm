# Router CDP Management Controller

Production-grade browser automation controller for Broadcom-based CPE / GPON ONT gateways (e.g. SCTY TEWA-500G, Broadcom `micro_httpd`). Uses the Chrome DevTools Protocol (CDP) and Playwright to automate management, spectrum tuning, and telemetry extraction with zero credential leaks.

---

## Capabilities

* **Automated Frameset Navigation:** Programmatically traverses Broadcom legacy `<frameset>` interfaces (`basefrm`, `menufrm`).
* **Masked Stdin Input:** Prompts for administrator credentials locally in the terminal with asterisks (`****`) to eliminate shoulder surfing and logging leakage.
* **1-Click Optimization (`--auto`):** Automatically retunes congested 2.4 GHz spectrum (e.g., Channel 8 $\rightarrow$ Channel 6) and configures resilient upstream DNS (Cloudflare `1.1.1.1` + ISP secondary).
* **Automated Page Crawling (`--crawl`):** Crawls all 12 primary management endpoints, captures full-page high-resolution screenshots, and compiles an offline visual index.
* **Multi-Browser Resilience:** Automatically launches Playwright Chromium with dynamic fallback to system Google Chrome or Microsoft Edge.

---

## Installation

```bash
cd tools/router_cdp
npm install
```

---

## Usage

### 1. Interactive Automation Console
```bash
.\router.bat
# or
node cdp_router_manager.js
```

Presents an interactive terminal menu:
```text
=================================================================
 AUTOMATED TASK MENU
=================================================================
 [1] Run Full Automated Page Crawl & Capture Screenshots
 [2] Optimize Wi-Fi Channel (Set to 1, 6, or 11)
 [3] Configure Fast Resilient DNS (Cloudflare + ISP)
 [4] View Connected Wi-Fi Stations Live (wlstationlist)
 [5] Keep Browser Open for Manual Exploration
 [6] Exit
=================================================================
```

### 2. 1-Click Fast Optimization
```bash
.\router.bat --auto
```

### 3. Automated Screenshot Audit
```bash
.\router.bat --crawl
```

### 4. Custom RF Channel Tuning
```bash
.\router.bat --set-channel 11
```

---

## Security Invariants

* **No Hardcoded Passwords:** Credentials are read strictly from local interactive prompt or ephemeral environment variables (`ROUTER_USER`, `ROUTER_PASS`).
* **Git Cleanliness:** `.gitignore` strictly prevents `.conf`, `screenshots/`, `*.log`, and `*.png` files from entering version control.
