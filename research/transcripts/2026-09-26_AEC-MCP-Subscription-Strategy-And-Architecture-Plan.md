# Epistemic Record: AEC/A-E Tool Fleet Commercial Strategy, Offline Licensing & Architecture Plan
**Document ID:** `TRN-2026-09-26-AEC-MCP-SUBSCRIPTION-PLAN`  
**Timestamp:** 2026-09-26T08:00:00+05:45  
**Topic:** Subscription Business Model, Offline-First Cryptographic Licensing, Cracked CAD/BIM Compatibility, eSewa Payment Integration, and Architecture/Civil Undergrad GTM  
**Participants:** Aaradhya Dev Tamrakar & Antigravity (Gemini)  
**Status:** Canonical Strategic Blueprint  

---

## 1. Executive Summary & Core Pivot

This document captures the end-to-end strategic, commercial, and architectural decisions for commercializing Aaradhya's fleet of 13+ specialized CAD/BIM/Analysis Model Context Protocol (MCP) servers located in `F:\Aaradhya-Dev-Tamrakar\AEC-MCP Suite`.

### Core Strategic Shifts:
1. **Demographic Focus:** Primary initial cohort is **Architecture (B.Arch)** students, followed by **Civil Engineering (B.E. Civil)** students in Nepal (TU-IOE Pulchowk, Thapathali, WRC, ERC, KU Dhulikhel, and affiliated colleges), expanding regionally and globally.
2. **Naming & Taxonomy:** Deprecate the internal working title *"AEC MCP"*. Adopt outcome-oriented public brands: **StudioPilot** (for Architecture: SketchUp, Rhino, Revit) and **StructPilot** (for Civil/Structural: ETABS, SAP2000, STAAD, EPANET).
3. **Execution Model:** Fully **offline-first local execution** (zero server compute cost, total data privacy, sub-millisecond local COM/IPC interop) with an **opportunistic online time validation anchor** and **monotonic clock ratchet**.
4. **Monetization & Settlement:** Anchor perceived value to international standards using **USD reference rates ($5, $8, $15)** while collecting domestic payments via **eSewa in clean round-peg NPR (Rs. 650, Rs. 1,000, Rs. 2,000)** for non-recurring **Semester Passes**.

---

## 2. Customer Segmentation & Academic Dynamics

| Attribute | Architecture Cohort (B.Arch) | Civil Engineering Cohort (B.E. Civil) |
| :--- | :--- | :--- |
| **Primary Software** | SketchUp, Rhino/Grasshopper, Revit, AutoCAD, 3ds Max | CSI ETABS, SAP2000, STAAD.Pro, EPANET, QGIS |
| **Piracy / Host State** | Universally cracked / student editions on Windows laptops. | Universally cracked editions across multiple versions (v18–v22). |
| **Reverse-Eng. Risk** | **Near Zero.** Non-programmers; study design, form, materials. | **Moderate.** Some learn C++/Python; share hostels with CS students. |
| **Buying Trigger** | **Studio Jury Deadlines** (Concept, Mid-term, Final Jury panic). | **Lab Deadlines** (EPANET) & **7th/8th Sem Capstones** (ETABS). |
| **Output Nature** | Visual, spatial, massing, daylight studies, FAR/coverage tables. | Numerical, stiffness matrices, shear/moment checks, rebar ratios. |
| **Price Sensitivity** | Low resistance to Rs. 1,000 (already spend Rs. 10k+ on printing). | High utility focus (must directly save 40+ hours of report calculations). |

---

## 3. Product Branding & Multi-Repo Fleet Architecture

Do not modify individual tool repositories with licensing or billing code. Keep them decoupled as pure execution bridges. Centralize all licensing, validation, and tool routing inside the **Master Gateway**.

```
[AI Assistants: Claude Desktop, Antigravity, Cursor]
                        │  STDIO (JSON-RPC 2.0)
                        ▼
       ┌─────────────────────────────────┐
       │   AEC Master STDIO Gateway      │
       │   - Offline License & Ratchet   │
       │   - 2-Device Machine Lock       │
       │   - Dynamic Module Filtering    │
       └────────────────┬────────────────┘
                        │ Reads: %LOCALAPPDATA%\AutodeskMCP\registry.json
         ┌──────────────┼──────────────┬──────────────┐
         ▼              ▼              ▼              ▼
   [StudioPilot]  [StudioPilot]  [StructPilot]  [StructPilot]
     SketchUp        Revit          ETABS          SAP2000
    (Ruby API)     (C# .NET)      (CSI COM)      (CSI COM)
     Port :51280    Port :51281    Port :51282    Port :51283
```

### Module Inventory (`F:\Aaradhya-Dev-Tamrakar\AEC-MCP Suite`):
1. **Architecture & Visual Suite (StudioPilot):**
   - `sketchup-mcp`: Rapid 3D massing, solar shadows, base64 viewport capture.
   - `rhino-mcp`: Grasshopper parametric scripts and complex geometry.
   - `revit-mcp`: BIM parameter auditing, sheet extraction, and family management.
   - `autocad-mcp`: 2D layer management, polyline extraction, and DXF generation.
   - `3dsmax-mcp` / `maya-mcp`: Visualization staging and asset prep.
2. **Structural & Civil Suite (StructPilot):**
   - `etabs-mcp`: Building frame modeling, finite-element analysis, NBC 105 seismic audits.
   - `sap2000-mcp`: General 3D FEA frames, trusses, shells, and dynamic modal extraction.
   - `staad-mcp`: Bentley steel and concrete structural design verification.
   - `epanet-mcp`: Water distribution network hydraulics and water quality simulation.
   - `qgis-mcp`: Geospatial terrain, contour analysis, and catchment mapping.

---

## 4. Offline-First Licensing & Anti-Tamper Engine

### The Security Challenge:
Offline software is vulnerable to **System Clock Rollback** (students setting Windows date back from 2027 to 2026) and **Hostel Room Sharing** (one student sharing `license.key` with 60 classmates).

### The Engineering Solution:
1. **Opportunistic Online Time Anchor:**
   - When internet is detected, fetch trusted UTC time from auth server via HTTPS in <200ms.
   - Save `last_trusted_utc` and reset offline duration counters.
2. **Local Monotonic Ratchet (Offline Protection):**
   - Measure elapsed time using hardware CPU ticks (`time.monotonic()` / Win32 `QueryPerformanceCounter`). This clock *cannot* move backwards, even if the user changes the Windows system date.
   - Implement a High-Water Mark: Record `current_timestamp = max(last_recorded, current_system_time)`. If system time moves backwards by more than 5 minutes, flag tampering.
   - Enforce a **14-day maximum offline lease**. If offline continuously for >14 days, demand a 1-second online check-in.
3. **2-Device Machine Fingerprint Lock:**
   - Hash CPU ID + Motherboard UUID + MAC address.
   - License keys are cryptographically signed (Ed25519) and contain the authorized machine hashes.
   - Allows each student to activate on **2 personal machines** (e.g., laptop + desktop/lab PC).

---

## 5. Payment & Settlement Mechanics (USD Rates via eSewa)

### The Legal & User Experience Reality:
By Nepal Rastra Bank regulations, domestic payments must settle in NPR. Undergrads do not have international credit cards.

### The Clean Round-Peg Pricing:
* **Structural or Architecture Single Pack:** \$8 USD $\rightarrow$ **Rs. 1,000 NPR** (Clean single note).
* **Single Tool Micro-Pass (e.g., just EPANET):** \$5 USD $\rightarrow$ **Rs. 650 NPR**.
* **All-Access Capstone Pass (Full Suite):** \$15 USD $\rightarrow$ **Rs. 2,000 NPR**.
* **Jury Sprint Pass (7-Day Emergency Pass):** \$2.50 USD $\rightarrow$ **Rs. 350 NPR**.

### Automated Fulfillment Flow (eSewa ePay v2):
1. Student selects tier on landing page and inputs Email + Machine ID.
2. Web portal redirects to eSewa ePay with HMAC-SHA256 signature.
3. Student confirms payment on eSewa app/web.
4. eSewa webhooks backend $\rightarrow$ Backend verifies transaction code.
5. Server mints Ed25519-signed `license.key` and presents download link + email copy immediately.

---

## 6. Critical Domain-Specific Defenses & Features

### A. The Units Normalization Gate
- **Failure Mode:** A student prompts "Add 350x500 column." In ETABS set to `[KN, m, C]`, this creates a 350-meter column, freezing the software.
- **Defense:** Strict input schemas (`width_mm`, `height_mm`) + automated inspection of `SapModel.GetPresentUnits()` to normalize all coordinate and sectional math before issuing COM calls.

### B. Pre-Flight Snapshots (No `Ctrl+Z` in ETABS OAPI)
- **Failure Mode:** ETABS OAPI has no programmatic Undo. A failed agent call corrupts the model.
- **Defense:** The MCP must automatically snapshot the file (`_pre_ai_timestamp.edb`) before executing any geometry mutation.

### C. ETABS State Machine Awareness (Locked vs. Unlocked)
- **Failure Mode:** Modifying members while a model is analyzed throws unhandled COM exceptions or wipes out finite-element results without warning.
- **Defense:** Explicit `is_locked` guard that prevents write actions on locked models without explicit user consent.

### D. B.Arch Killer Feature: Multimodal Viewport Critique
- Use `sketchup_capture_viewport` to capture shaded base64 imagery after manipulating solar parameters (`sketchup_set_shadows`), allowing Claude 3.5 Sonnet or Gemini 1.5 Pro to visually review daylighting and courtyard shading.

### E. Municipal Bylaws & Area Programming Engine
- Auto-calculate Total Built-Up Area, Ground Coverage %, and Floor Area Ratio (FAR) from SketchUp tags/layers against municipal guidelines (e.g., Kathmandu/Lalitpur building norms).

### F. Civil Killer Feature: Nepal Building Code (NBC 105:2020) Audit
- Automated calculation of seismic base shear, modal mass participation (>90%), and inter-story drift limits (<0.015 / 0.025), formatting calculation tables directly for assignment and capstone reports.

### G. Cross-Discipline Translation Bridge
- `archi_to_etabs_grid`: Ingests AutoCAD/SketchUp architectural grid lines and automatically instantiates the structural grid and column frames inside ETABS, solving the primary friction point between architecture and civil partners.

---

## 7. Packaging, Deployment & Friction Removal

1. **Zero-CLI Guarantee:** Architecture students will not run terminal commands or PowerShell scripts.
   - Package the Gateway and dependencies using **Inno Setup** into a single `.exe` installer.
   - For SketchUp, provide a native `.rbz` extension installable via SketchUp Extension Manager.
2. **Multi-Year Path Auto-Detection:**
   - The installer must scan `%APPDATA%\SketchUp\SketchUp <Year>\` and `%APPDATA%\Autodesk\Revit\Addins\<Year>\` across all versions (2021–2025) and place plugins in all detected versions automatically.
3. **Runtime Bundling:**
   - Bundle `vcredist_x64.exe` (Microsoft Visual C++ Redistributable 2015–2022) to avoid silent `VCRUNTIME140.dll` crashes on budget student laptops.
4. **AI Client Quota Workaround:**
   - Since students run on free-tier Claude Desktop (hitting 2-prompt limits), provide support for **Google Antigravity** or a lightweight desktop chat GUI using a free **Google Gemini API Key** (up to 1M tokens/day free).
5. **The 72-Hour Free Trial:**
   - Deliver an automatic 3-day unrestricted trial on first install to prove functionality on the student's cracked software before asking for payment.

---

## 8. Go-To-Market & Revenue Roadmap

```
[Year 1 & 2: Form & Massing] ────────> StudioPilot for SketchUp ($8/sem)
[Year 3: Water Hydraulics]   ────────> StructPilot for EPANET ($5/sem)
[Year 3 & 4: Working Plans]  ────────> StudioPilot for Revit & Bylaws ($8/sem)
[Year 4: Major Capstone]     ────────> StructPilot for ETABS & NBC 105 ($8/sem)
[Year 5: Thesis All-Access]  ────────> Complete Capstone Master Bundle ($15/sem)
```

* **Organic Campus Acquisition:** Short 15-second split-screen workflow reels on Instagram and TikTok (*#architecturestudent #archihacks #civilengineering*).
* **Launch Timing:** Announce 5–7 days prior to major Studio Jury deadlines and 7th-semester Capstone project assignments.
* **Customer Lifetime Value (LTV):** Up to **Rs. 8,000–Rs. 10,000 per student** across their 5-year academic career.

---

## 9. Verification & Execution Checklist

- [ ] **Gateway Ratchet Engine:** Implement `time.monotonic()` and high-water mark timestamping inside `autodesk-mcp` router.
- [ ] **Ed25519 Verification:** Embed public key verification inside the compiled gateway binary.
- [ ] **SketchUp .rbz Packaging:** Package `sketchup_mcp.rb` as a standalone `.rbz` with auto-port allocation.
- [ ] **ETABS NBC 105 Checker:** Verify OAPI COM queries for story drift and base shear scaling factor.
- [ ] **Inno Setup Script:** Write an installer script scanning multi-year paths and bundling `vcredist_x64.exe`.
- [ ] **eSewa ePay Endpoint:** Stand up a minimal FastAPI webhook handler verifying eSewa HMAC-SHA256 signatures and minting signed license files.
