# ⚡ Brainstorm & Campus Swarm Marketplace

A responsive, zero-install, single-page P2P dataset and magnet marketplace designed for **IOE Pulchowk Campus** and the **Brainstorm Lab R&D** mesh.

---

## 🌟 Overview

The Brainstorm Swarm Marketplace replaces ad-monetized commercial torrent bloatware with a clean, high-performance web dashboard that runs directly in the browser. It enables students, researchers, and project cohorts to share and download heavy datasets, AI models, Linux VM images, and courseware at saturating network speeds.

### Key Features
- **Dual-Audience Catalog**: Brainstorm Lab R&D datasets (SPARK kinematics, DeepSeek coding model, Fusion 360 MCP CAD models) and IOE Pulchowk coursework (CT 552 DSA, EX 509 Control Systems, Cyber-Forensics VM).
- **Instant Search & Filtering**: Fast client-side filtering across categories, departments, tags, and SHA-1 infohashes.
- **1-Click Actions**:
  - `🧲 Copy Magnet`: Copies the full `magnet:?xt=urn:btih:...` URI to clipboard.
  - `💻 CLI Command`: Copies a ready-to-run `aria2c "<magnet>"` terminal command.
  - `📱 QR Code Modal`: Renders a pure-JavaScript SVG QR code on-screen so students can scan and download directly on their phones (via Flud / tTorrent).
- **Dual-Tier Role Gating**:
  - **Student View**: Open access; includes a non-intrusive campus announcement card (club workshops, hackathons).
  - **Cohort Pro View**: Gated by secret token (`cohort-pro-2026`); completely disables all announcement banners, unlocks an in-browser **Dataset Publishing Panel**, and provides catalog JSON export capabilities.

---

## 🚀 Quick Start

### 1. Launch the Server
From the repository root:
```powershell
.\scripts\start_marketplace.ps1
```

The script displays:
- **Local URL:** `http://localhost:8080`
- **Campus / Wi-Fi URL:** `http://<your-lan-ip>:8080` *(shareable with anyone on the same campus Wi-Fi)*
- **Cohort Pro Link:** `http://<your-lan-ip>:8080/?token=cohort-pro-2026`

### 2. Package a Dataset into a Torrent
```powershell
python scripts\make_dataset_torrent.py "F:\Path\To\Dataset"
```

### 3. Start Seeding
```powershell
.\scripts\seed_dataset.ps1 -Torrent "F:\Path\To\Dataset.torrent"
```

---

## 📁 File Structure

- `index.html` — Single-page responsive web dashboard.
- `app.js` — Client-side search, category filter, QR generator, and Cohort Pro authentication.
- `style.css` — High-agency dark mode UI adhering to `design-taste-frontend` (slate/zinc palette, glass cards, cobalt/emerald accents, M3 spring physics).
- `marketplace_data.json` — Authoritative dataset and magnet catalog registry.
