# Experiment Protocol: Empirical Reconnaissance of Nepal's Public Information Substrate

**ID:** `EXP-NISR-001`  
**Date:** 2026-09-28  
**Status:** Approved / Ready for Execution  
**Principal Investigator:** Aaradhya Dev Tamrakar  
**Parent Plan:** [`PLAN-NISR-001`](../plans/PLAN-NISR-001_PROGRAM_CHARTER.md) (Track `NISR-001`)  
**Epistemic Tier:** `E4` (Empirical Verification Protocol)  
**Associated Hypothesis:** [`HYP-007`](../hypotheses/HYP-007-ADAPTIVE-INGESTION-LANDSCAPE.yaml)  

---

## 1. Experimental Rationale & Objective

Before deploying or scaling web crawlers across `.gov.np` infrastructure, the NISR program requires empirical measurement of the target surface. Building crawlers on the assumption that Nepal's public websites are uniform static HTML pages containing clean digital PDFs leads to brittle failure modes.

### Primary Objective
Execute a lightweight, non-invasive reconnaissance probe across **10 structurally diverse Nepal public institutions** to empirically characterize:
1. **Infrastructure Health:** TLS certificate validity, TLS cipher support, and DNS resolution latency.
2. **Web Architecture & CMS:** Web server stack (Apache, Nginx, IIS), CMS framework (WordPress, Drupal, custom PHP, .NET), and client-side rendering requirements (Static HTML vs. React/Vue SPAs).
3. **Crawl Politeness Surface:** `robots.txt` presence, `crawl-delay` declarations, and rate-limiting behaviors.
4. **Document Modality Split:** Density and ratio of `.pdf`, `.docx`, `.xlsx`, and scanned image artifacts linked from top-level navigation hubs.

---

## 2. Falsifiable Hypotheses

- **`HYP-007.1` (Modality Heterogeneity):** At least $30\%$ of surveyed government portals employ dynamic client-side rendering (React/Vue/Angular) or non-standard query-based document archives that fail under simple static HTML link discovery.
- **`HYP-007.2` (TLS & Network Friction):** At least $20\%$ of surveyed institutional domains present TLS certificate chain discrepancies, expired certificates, or aggressive perimeter rate-limiting under standard non-browser User-Agents.
- **`HYP-007.3` (Robots.txt Paucity):** Less than $50\%$ of target `.gov.np` portals publish a standard `robots.txt` file, necessitating a conservative default crawl policy ($1.0\text{ req/sec}$ with exponential jitter).

---

## 3. Stratified 10-Target Reconnaissance Matrix

The 10 targets are intentionally selected across constitutional, ministerial, judicial, regulatory, and municipal tiers to ensure representative coverage:

| # | Institution Name | Domain | Tier / Rationale | Expected Modality |
|---|---|---|---|---|
| **1** | **Nepal Law Commission** | `lawcommission.gov.np` | Statutory Ground Truth | Structured Act PDFs, Gazettes |
| **2** | **Supreme Court of Nepal** | `supremecourt.gov.np` | Judicial Precedents | Cause lists, NKP judgment PDFs |
| **3** | **Ministry of Finance** | `mof.gov.np` | Economic & Fiscal Policy | Budget speeches, tax circulars, tables |
| **4** | **Ministry of Law, Justice & PA** | `moljpa.gov.np` | Legislative Drafting | Draft bills, notifications |
| **5** | **Ministry of Home Affairs** | `moha.gov.np` | Executive Administration | Directives, disaster circulars |
| **6** | **Department of Printing** | `dop.gov.np` | Official Gazette (*राजपत्र*) | Scanned historical gazettes (1950–present) |
| **7** | **PPMO (e-GP System)** | `bolpatra.gov.np` | Public Procurement | Dynamic tender portal, complex forms |
| **8** | **Financial Comptroller General** | `fcgo.gov.np` | Treasury & Accounting | Financial rules, fiscal reports, tables |
| **9** | **Nepal Rastra Bank** | `nrb.org.np` | Central Bank / Monetary | Monetary policy, statistical bulletins |
| **10** | **Kathmandu Metropolitan City** | `kathmandu.gov.np` | Local Government (Tier 3) | Municipal acts, tax notices, ward info |

---

## 4. Measurement Methodology & Safety Bounds

To ensure absolute politeness and zero disruption to public servers:
1. **Request Budget:** Exactly 1 HTTP `HEAD` request (for headers and TLS inspection) followed by at most 1 shallow HTTP `GET` request (to evaluate HTML body structure and extract document link anchors) per target.
2. **Rate Limiting:** Minimum 2.0-second delay between sequential probes across distinct domains.
3. **Identifiable User-Agent:**
   ```text
   NISR-ReconProbe/1.0 (+https://github.com/Aaradhya-Dev-Tamrakar/brainstorm; Research Inquiry; Aaradhya Dev Tamrakar)
   ```
4. **Strict TLS Assertion (`INV-SEC-TLS-001`):** Native Python `ssl.create_default_context()` with standard system trust anchors. Any certificate verification failure is captured as an empirical data point (`status="TLS_CERT_INVALID"`), never bypassed.

---

## 5. Recorded Metric Schema

Results must be recorded deterministically to `research/results/EXP-NISR-001_recon_matrix.json`:

```json
{
  "target_id": "TARGET-001",
  "domain": "lawcommission.gov.np",
  "resolved_ip": "string",
  "dns_latency_ms": 0.0,
  "tls_verified": true,
  "tls_version": "TLSv1.3",
  "tls_cert_expiry": "YYYY-MM-DD",
  "http_status": 200,
  "server_header": "Apache/2.4.52 (Ubuntu)",
  "cms_detected": "WordPress 6.4",
  "is_spa_rendered": false,
  "has_robots_txt": true,
  "crawl_delay_declared": null,
  "linked_documents": {
    "pdf_count": 42,
    "docx_count": 0,
    "xlsx_count": 0,
    "zip_count": 0
  },
  "modality_observation": "Static HTML archive with direct vector PDF links",
  "timestamp": "ISO-8601"
}
```

---

## 6. Success & Completion Criteria

1. All 10 target domains probed and recorded in the result ledger.
2. Zero server errors induced; zero IP connection drops or rate-limit blocks experienced.
3. Live empirical evidence synthesized into a structured analysis report informing Phase 3 (`DocumentRouter` design).
