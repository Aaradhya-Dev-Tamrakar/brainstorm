# Quest C0-AIDA: The Assistive AI Challenge Sprint (AIDA 2026)

**ID:** `QUEST-C0-AIDA`  
**Rank Requirement:** Open to all Cohort 0 Fellows  
**Target Competition:** AIDA Impact Challenge 2026 — “AI Without Barriers”  
**Squad Size:** 3–4 Fellows (Innovation Challenge Team) / Solo or Duo (Research Challenge)  
**Application Deadline:** **16 October 2026**  
**Official Portal:** [https://aida.prateekinnovations.com/](https://aida.prateekinnovations.com/) *(Referral Code: `CA_6051`)*  
**Primary Repository Reference:** [`research/plans/PLAN-A11Y-001_ONE_SHOT_CIVIC_ACCESS_ENGINE_FOR_DISABILITIES.md`](PLAN-A11Y-001_ONE_SHOT_CIVIC_ACCESS_ENGINE_FOR_DISABILITIES.md)  

---

## 1. Challenge Overview & Lab Strategy

The **AIDA Impact Challenge 2026** invites students and researchers to build AI-powered solutions that improve **accessibility, independence, and quality of life for people with disabilities (PwDs)**.

### Our Competitive Advantage
Most hackathon entrants will pitch surface-level chatbots. BRL enters with an already grounded, deterministic architecture:
1. **The Core Problem:** Persons with disabilities in Nepal face an 80%+ bureaucratic rejection rate and grueling repeat visits to physically inaccessible Ward and Palika counters just to get their **Disability Identity Card (*अपाङ्गता परिचयपत्र*)** or social security allowances.
2. **The Solution (Sahaj-Sewa / Nagarik-Access):** A multimodal **Pre-Flight Dossier Verification Engine** and **Devanagari Voice Guide** that validates hospital stamps, photo specs, and ward recommendations from home, guaranteeing **100% completion in exactly one physical visit**.
3. **Existing Substrate:** Schema [`schemas/examples/disability-id-card.civic.json`](../../schemas/examples/disability-id-card.civic.json) and hypothesis [`HYP-010`](../hypotheses/HYP-010-ONE-SHOT-A11Y-CIVIC-DETERMINISM.yaml) are already merged into BRL `main`.

---

## 2. Squad Role Distribution (Team of 3–4)

| Role | Focus Area | Core Deliverable for Sprint |
| :--- | :--- | :--- |
| **Squad Lead & Integrator** | Architecture & Pitch Dossier | System pipeline integration, 2-minute pitch video, and AIDA portal submission. |
| **Multimodal Vision Engineer** | Pre-Flight Document Triage | Python/FastAPI module checking document image clarity, medical stamp presence, and photo counts. |
| **Accessible Frontend Engineer** | Voice-First Web/PWA Client | WCAG 2.2 AAA high-contrast UI with Devanagari audio-in / audio-out guidance. |
| **Civic Domain & Ontology Researcher** | Statutory Legal Contracts | Mapping the 4 disability tiers (Red/Blue/Yellow/White) and local Palika procedures into JSON schemas. |

---

## 3. Sprint Timeline (Oct 8 – Oct 16)

* **Oct 8–10 (Phase 1):** Team formation, registration on AIDA portal using referral code `CA_6051`, and problem statement draft.
* **Oct 11–13 (Phase 2):** Connect Frontend UI with Vision triage API; run synthetic dossier test (`EXP-A11Y-001`).
* **Oct 14–15 (Phase 3):** Record end-to-end demo video and finalize technical slide deck.
* **Oct 16 (Phase 4):** Final submission to AIDA Impact Challenge 2026.
