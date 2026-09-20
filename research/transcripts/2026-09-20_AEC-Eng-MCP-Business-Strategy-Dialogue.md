# Epistemic Record: AEC & Engineering MCP Suite Business Strategy & Roadmap
**Document ID:** `TRN-2026-09-20-AEC-ENG-MCP`  
**Timestamp:** 2026-09-20T11:32:00+05:45  
**Topic:** Monetization Model, Inbound Gateway Strategy (NPR + USD), Local STDIO Execution, and Nepal Engineering Market Alignment  
**Participants:** Aaradhya Dev Tamrakar & Antigravity (Gemini)

---

## 1. Initial Proposition & Constraints
* **Core Proposal:** Leasing annuity-based subscription for Civil/Architecture Model Context Protocol (MCP) servers. Quoting in USD ($) while accepting both NPR and USD.
* **Tiers:** Free to discounted rates for beta testers and inner circle; standard rate for international users.
* **Constraints Identified:**
  * Distribution method initially undefined.
  * Payment gateway undefined; user holds an NRB prepaid dollar card.
  * System operates as an online AI agent - MCP integration.

---

## 2. Key Epistemic Deductions & Strategic Pivots

### A. Dollar Card & Inbound Payment Realities
* **Fact:** In Nepal, commercial bank prepaid dollar cards are outbound spending cards only ($500/year NRB limit) and cannot receive inbound merchant payouts.
* **Resolution (Dual-Rail Model):**
  * *Domestic (NPR):* Direct Fonepay Dynamic QR / eSewa / Khalti API for automated or invoice-based settlement.
  * *Global (USD):* Merchant of Record (MoR) platforms (Polar.sh / Lemon Squeezy) handling global VAT and credit cards, disbursing funds via Payoneer or SWIFT wire directly to Nepali bank accounts.

### B. The Zero-Cloud-Cost Bootstrap Realization
* **Founder Principle:** *"I mean if an archi or civil person spends that much time reverse engineering it, then they might as well have it for free... I hope it can be set to local run to amass cloud budget from start."*
* **Architecture Impact:**
  * The suite connects to desktop software (AutoCAD, Revit, SAP2000, STAAD.Pro, ETABS, SolidWorks) running on local Windows workstations via COM/OAPI/.NET.
  * Running the MCP locally via STDIO (with user-provided LLM keys) reduces operational cloud burn to **$0.00/month**.
  * 100% of upfront subscription cash flow is retained as profit to fund future cloud features.

### C. Rebranding from `autodesk-mcp` to `aec-mcp`
* **Trademark & Scope Defense:** Out of 13 built tools, only 5 are Autodesk products; the rest are CSI (SAP2000/ETABS), Bentley (STAAD.Pro), Trimble (SketchUp), McNeel (Rhino), and US EPA (EPANET).
* **Decision:** Master STDIO gateway rebranded to **`aec-mcp`**, establishing an industry-standard, vendor-neutral identity with zero trademark risk.

### D. Nepal Academic & Industry Moat (IOE & KU)
* **Market Fit:**
  * Over 12,000 engineering students in Nepal (TU-IOE Pulchowk/Thapathali/WRC/ERC, KU Dhulikhel, and 30+ private colleges) require software aligned with syllabus modules: EPANET (Water Supply), SAP2000/ETABS (Structural), QGIS (Geomatics), and AutoCAD.
  * Hundreds of engineering consultancies require automated structural checking complying with **NBC 105:2020** and **IS 456:2000**.
