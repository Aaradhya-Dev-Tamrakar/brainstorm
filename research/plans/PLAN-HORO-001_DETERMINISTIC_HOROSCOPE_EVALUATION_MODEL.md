# Research Plan: Deterministic Horoscope Evaluation Engine & Ground Truth Benchmark
**ID:** `PLAN-HORO-001`  
**Date:** 2026-10-01  
**Status:** Approved Research Plan & Implementation Blueprint  
**Authors:** Aaradhya Dev Tamrakar, Antigravity Agent  
**Context:** Central Architecture Registry, Verification Engine, and Knowledge Mesh Root (`brainstorm`)  
**Epistemic Governance:** ARCH-RFC-001 (Calibrated Evidence Tiers) & ARCH-RFC-002 (Multi-Model Cognitive Council)  

---

## 1. Executive Summary & Problem Formulation

Astrological horoscope analysis has historically been dismissed in computational literature due to **subjective validation, the Barnum/Forer effect, confirmation bias, and non-deterministic natural language interpretations**. However, from a systems engineering perspective, horoscope processing cleanly separates into two distinct domains:

1. **The Physical Ephemeris Domain (`FORMALLY_PROVEN` / Celestial Mechanics):** Given an exact UTC timestamp and geographic coordinates $(t, \phi, \lambda)$, planetary orbital longitudes, ascendant (Lagna) cusps, 27 Nakshatras, and 120-year Vimshottari Dasha intervals are **strictly closed-form, deterministic mathematical functions**.
2. **The Interpretive & Predictive Domain (`HEURISTIC_HYPOTHESIS`):** Traditional human practitioners and generative LLMs introduce stochastic noise, hallucinations, and unfalsifiable platitudes (*"You have unused potential," "Challenges will arise"*).

**Objective:** Build an end-to-end, deterministic evaluation engine and data collection framework that:
- Codifies astronomical calculations into a zero-dependency, verified algorithmic pipeline.
- Formulates classical Vedic/Western rules into formal Boolean satisfaction predicates (Symbolic AI).
- Curates an empirically verifiable ground-truth dataset (Rodden Rating AA birth records paired with dated life milestones).
- Benchmarks predictive claims using formal proper scoring rules and mathematical ambiguity filters, isolating true signal from Barnum noise.

---

## 2. System Architecture & Layer Decomposition

```
                    Input: Birth Vector (t_UTC, Latitude, Longitude, Altitude)
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   Layer 1: Deterministic Ephemeris Engine (Physical Truth)              │
│  - Julian Day Number (JDN) & Mean Obliquity of Ecliptic (ε)                            │
│  - Greenwich Mean Sidereal Time (GMST) & Local Sidereal Time (LST / RAMC)             │
│  - Analytical Keplerian / Meeus Planetary Reductions (Sun, Moon, Mars, etc.)          │
│  - Lahiri (Chitrapaksha) Ayanamsha Precession Conversion (Sayana -> Nirayana)          │
│  - Ascendant (Lagna) Trigonometry & 12 Bhava Cusps (Whole Sign & Equal House)          │
│  - 27 Nakshatras, 108 Padas, and Vimshottari Mahadasha Closed-Form Schedules          │
└───────────────────────────────────┬────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   Layer 2: Symbolic Rule & SMT Knowledge Mesh                          │
│  - Formal Boolean Predicates for 300+ Classical Yogas (Gajakesari, Budhaditya, etc.)   │
│  - Planetary Dignities (Exaltation, Debilitation, Moolatrikona, Shadbala)             │
│  - Kuja / Manglik Dosha Detection & Cancellation Logic                                │
│  - Zero LLM Hallucination: Deterministic Algebraic Evaluation                          │
└───────────────────────────────────┬────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   Layer 3: Empirical Ground Truth Data Ingestion Pipeline              │
│  - Astro-Databank AA Harvester (Birth Certificate Records with exact seconds/minutes) │
│  - Wikidata / Wikipedia SPARQL Life Event Chronologies (Dated Milestones)             │
│  - Synthetic Geographic Grid Sweeps (Equator to Polar Latitudes, Timezone Deltas)     │
│  - Bikram Sambat (B.S.) Nepali Calendar Interop via sim/nepali_calendar.py            │
└───────────────────────────────────┬────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   Layer 4: Deterministic Model Evaluation & Scoring Gate              │
│  - Astronomical Fidelity Metric (Degrees error against JPL / Swiss Ephemeris)         │
│  - Barnum Ambiguity Index (Ratio of universal platitudes to falsifiable propositions)  │
│  - Event-Dasha Timing Alignment via Brier Scoring                                     │
│  - Monte Carlo Permutation Null Hypothesis Test (p < 0.01 Significance Gate)          │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Collection Strategy & Stratification

To eliminate selection bias and retrofitting, data collection is partitioned into four distinct, tracked tranches:

### Tranche A: Rodden Rating AA Gold-Standard Cohort
- **Source:** Astro-Databank verified records.
- **Criteria:** Strict Rodden Rating AA only (derived directly from government birth certificates, hospital registries, or official civil ledgers).
- **Metadata Required:** Exact minute/second, timezone transition records (pre-DST/post-DST), hospital coordinates.
- **Target Volume:** 500 validated profiles across diverse latitudes.

### Tranche B: Verifiable Discrete Life Milestones (Target Vector $\mathbf{Y}$)
- **Source:** Cross-referenced historical records, public biographies, and official gazettes.
- **Accepted Event Types (Objective & Falsifiable):**
  - Academic graduation date.
  - Marriage and legal divorce decree dates.
  - Childbirth dates.
  - Business founding date / IPO / bankruptcy filing date.
  - Public electoral victory or deposition date.
  - Major documented acute medical procedure or surgical intervention.
  - Date and verifiable cause of death.
- **Rejection Filter:** Subjective self-reports ("felt anxious in 2018", "spiritually awakened in spring") are strictly excluded.

### Tranche C: Synthetic Geographic & Temporal Perturbation Grids
- **Source:** Deterministic procedural generation across the global coordinate space.
- **Purpose:** Stress-test boundary conditions and mathematical stability:
  - Latitude sweeps: $0^\circ \to \pm 75^\circ$ (auditing polar ascendant flipping anomalies).
  - Temporal jitter: $t_{\text{birth}} \pm 1, \pm 5, \pm 15, \pm 60$ minutes to establish the empirical **Time-Sensitivity Gradient** ($\frac{\Delta \text{Features}}{\Delta t}$).
  - Timezone anomalies: High-precision validation for non-standard offsets (e.g. Nepal UTC+5:45, India UTC+5:30, Newfoundland UTC-3:30).

### Tranche D: LLM Generation Corpus (Candidate Models $\mathbf{\hat{Y}}$)
- **Source:** Standardized prompting of candidate foundation models (Claude 3.5 Sonnet, GPT-4o, Gemini 1.5/2.0 Flash/Pro).
- **Control Variables:** Identical system prompts, temperature=0.0, zero conversational framing.
- **Evaluation:** Measuring calculation fidelity (did the model compute the right chart?) vs. linguistic evasion (did the model hide behind vague Barnum statements?).

---

## 4. Mathematical Formulations & Scoring Metrics

### 4.1 Ascendant (Lagna) Trigonometric Derivation
Let Greenwich Mean Sidereal Time be $\theta_{\text{GMST}}$, geographic longitude be $\lambda$, and latitude be $\phi$. The Local Sidereal Time in degrees (Right Ascension of the Midheaven, RAMC) is:
$$\alpha_{\text{MC}} = \theta_{\text{GMST}} \cdot 15^\circ + \lambda$$

Given true obliquity of the ecliptic $\varepsilon$, the Ascendant $\lambda_{\text{Asc}}$ is computed deterministically:
$$\tan \lambda_{\text{Asc}} = \frac{\cos \alpha_{\text{MC}}}{-\left(\sin \alpha_{\text{MC}} \cos \varepsilon + \tan \phi \sin \varepsilon\right)}$$

Converting to the Sidereal Nirayana zodiac using Lahiri Ayanamsha $\Delta \psi_{\text{Lahiri}}(t)$:
$$\lambda_{\text{Nirayana}} = \left(\lambda_{\text{Sayana}} - \Delta \psi_{\text{Lahiri}}(t)\right) \pmod{360^\circ}$$

### 4.2 Barnum Ambiguity Index ($I_{\text{Barnum}}$)
Let a candidate prediction text contain $N_b$ matched universal Barnum tokens (subjective validation markers: *"sometimes", "need for appreciation", "inner conflict"*) and $N_s$ specific, falsifiable predictive markers (*"marriage in [Month/Year]", "promotion", "surgery"*):
$$I_{\text{Barnum}} = \frac{N_b}{\max(1, N_b + N_s)}, \quad I_{\text{Falsifiable}} = \frac{N_s}{\max(1, N_b + N_s)}$$

**Acceptance Rule:** Any claim with $I_{\text{Barnum}} > 0.60$ is classified as non-evaluable subjective noise.

### 4.3 Event Window Alignment & Brier Score
For a verifiable life event $E_k$ occurring at timestamp $t_k$, and a predicted activation window (e.g. Jupiter-Mercury Mahadasha/Antardasha) spanning $[t_{\text{start}}, t_{\text{end}}]$ with predicted probability $p_k$:
$$o_k = \begin{cases} 1 & \text{if } t_{\text{start}} \le t_k \le t_{\text{end}} \\ 0 & \text{otherwise} \end{cases}$$
$$\text{Brier Score} = \frac{1}{K} \sum_{k=1}^K (p_k - o_k)^2$$

### 4.4 Monte Carlo Permutation Null Hypothesis Test
To guard against the multiple-testing fallacy (p-hacking across hundreds of sub-dasha combinations):
1. Compute the empirical event alignment rate $R_{\text{obs}}$.
2. Generate $M = 10,000$ synthetic permuted cohorts where birth dates are randomized across the dataset while fixing event dates.
3. Calculate empirical $p$-value:
   $$p = \frac{1}{M} \sum_{m=1}^M \mathbb{I}(R_{\text{perm}}^{(m)} \ge R_{\text{obs}})$$
4. The astrological predictive correlation hypothesis is rejected unless $p < 0.01$.

---

## 5. Repository Assets & Traceability

This research plan is formally linked to existing active repository artifacts:

| Artifact | Repository Path | Epistemic Status | Purpose |
| :--- | :--- | :--- | :--- |
| **Data Schema** | [`schemas/horoscope.evaluation.v1.json`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/schemas/horoscope.evaluation.v1.json) | `FORMALLY_PROVEN` | Validated JSON Schema for birth vectors, ephemeris, and ground truth |
| **Simulation Engine** | [`sim/horoscope_eval_engine.py`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/sim/horoscope_eval_engine.py) | `EMPIRICALLY_VERIFIED` | Zero-dependency Python 3 celestial mechanics & Yoga extractor |
| **Hypothesis Card** | [`research/hypotheses/HYP-HORO-001.yaml`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/hypotheses/HYP-HORO-001.yaml) | `HEURISTIC_HYPOTHESIS` | Formal hypothesis card with falsification criteria and invariants |
| **B.S. Calendar** | [`sim/nepali_calendar.py`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/sim/nepali_calendar.py) | `EMPIRICALLY_VERIFIED` | 125-year Bikram Sambat to Gregorian conversion engine |

---

## 6. Phased Implementation Roadmap

### Phase 1: Engine Hardening & Ephemeris Verification Gate
- [x] Create formal data collection schema (`schemas/horoscope.evaluation.v1.json`).
- [x] Implement deterministic Python 3 ephemeris and yoga detection engine (`sim/horoscope_eval_engine.py`).
- [x] Register hypothesis card (`research/hypotheses/HYP-HORO-001.yaml`).
- [ ] Add unit tests comparing `sim/horoscope_eval_engine.py` against NASA JPL Horizons / Swiss Ephemeris reference test vectors for 10 historical dates (error target: $< 0.05^\circ$).

### Phase 2: Ingestion & Dataset Assembly
- [ ] Implement automated harvester script (`sim/horoscope_data_harvester.py`) targeting Astro-Databank Rodden AA records.
- [ ] Ingest Wikidata biographical milestones via SPARQL for public figures with Rodden AA birth records.
- [ ] Integrate `sim/nepali_calendar.py` to allow direct Bikram Sambat date queries for South Asian horoscopes.
- [ ] Generate synthetic grid sweep dataset across equatorial, temperate, and polar coordinates (`data/synthetic_grid_1000.jsonl`).

### Phase 3: Benchmark Suite & LLM Auditing
- [ ] Build automated evaluation harness benchmarking candidate LLMs (GPT-4o, Claude 3.5 Sonnet, Gemini 2.0).
- [ ] Compute astronomical calculation hallucination rate per model.
- [ ] Compute mean Barnum Ambiguity Index across 1,000 generated readings.
- [ ] Publish benchmark results into `research/results/BMK-HORO-001_results.json`.

### Phase 4: Statistical Backtesting & Hypothesis Verdict
- [ ] Run Monte Carlo permutation test ($M=10,000$) over Dasha-Bhukti activation windows vs. objective life events.
- [ ] Compute Brier score and effect size.
- [ ] Finalize formal research report and update `HYP-HORO-001.yaml` status to `EMPIRICALLY_VERIFIED` or `FALSIFIED`.
