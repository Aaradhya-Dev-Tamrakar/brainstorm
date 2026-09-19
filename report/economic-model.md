# Defensible Economic Accounting & R&D Resource Allocation Model

```text
Artifact ID:          ECON-001-ACCOUNTING-MODEL
Version:              1.0.0
Status:               CANONICAL
Principal Architect:  Aaradhya Dev Tamrakar (ADT)
Evidence Tier:        E1 — DESIGN SPECIFICATION
Audit Reference:      report/repository-audit.md (Items 07, 08, 09, 10)
```

---

## 1. Executive Summary & Epistemic Correction

Earlier revisions of `ECOSYSTEM_ARCHITECTURAL_BRAINSTORM.md` conflated basic human survival costs (hostel accommodation, subsistence food) and undergraduate university tuition with productive engineering capital expenditure. Furthermore, internal estimates of replacement labor were labeled as "market valuation" and divided by historical outlays to claim "8.4x ROI" or "5,000x AI leverage."

This document establishes a **methodologically defensible accounting model**. It separates productive assets from living baselines, reframes internal valuation as *replacement labor equivalents*, replaces mixed-unit scalar ratios with *vectorized resource tracking*, and formalizes the economic efficiency of autonomous invariant discovery.

---

## 2. Five-Pillar Financial & Capital Decomposition

```
┌────────────────────────────────────────────────────────────────────────┐
│                     THE FIVE ACCOUNTING PILLARS                        │
├─────────────────────────┬──────────────────────────────────────────────┤
│ Pillar                  │ Scope & Character                            │
├─────────────────────────┼──────────────────────────────────────────────┤
│ 1. Productive CAPEX     │ Durable physical assets (laptop, hardware).  │
│ 2. Productive OPEX      │ Recurring operational cash (APIs, internet). │
│ 3. Living & Tuition     │ Biological/academic overhead (EXCLUDED from  │
│    (Separated Base)     │ R&D productive asset ratios).                │
│ 4. Human Capital        │ Cumulative engineering, research, doc hours. │
│ 5. Replacement Cost     │ Hypothetical labor reconstruction expense.   │
└─────────────────────────┴──────────────────────────────────────────────┘
```

### 2.1 Pillar 1: Productive Capital Expenditure (CAPEX)
Durable, productive hardware assets purchased specifically for engineering and computation:

| Asset Description | Purchase Period | Cost (NPR) | Cost (USD Equiv.) | Asset Category |
| :--- | :---: | :---: | :---: | :--- |
| **Acer Swift Go 16** (Intel Core Ultra 7 155H, 16GB LPDDR5X) | Early 2024 | NRs 155,000 | ~$1,160.00 | Primary Compute Workstation |
| **Hardware Peripherals & Tools** (ESP32-S3, MPU-6050, logic analyzer, wiring, soldering) | 2023–2026 | NRs 10,000 | ~$75.00 | Embedded Edge AI Lab |
| **Cumulative Productive CAPEX** | — | **NRs 165,000** | **~$1,235.00** | **Durable Asset Base** |

### 2.2 Pillar 2: Productive Operating Expenditure (OPEX)
Recurring marginal cash expenditures required to keep services and toolchains operational:

| Service / Utility | Duration / Term | Cost (NPR) | Cost (USD Equiv.) | Operating Nature |
| :--- | :---: | :---: | :---: | :--- |
| **Shared 300 Mbps Fiber Internet** (Shared student flat rate: NRs 1,250/yr) | 3.5 years | NRs 4,375 | ~$32.55 | Connectivity / Telemetry |
| **Paid AI Subscriptions (Late 2023 – Aug 2026)** | 35 months | **NRs 0.00** | **$0.00** | 100% Free Quotas & Open Source |
| **Paid AI Subscriptions (Sep 2026 – Present)** (Google AI Pro Student Tier via Dollar Card) | 1 month | NRs 670 | $5.00 | Cognitive Worker 01 |
| **Cumulative Productive OPEX** | — | **NRs 5,045** | **~$37.55** | **Direct Recurring Cash** |

$$\text{Total Direct Productive Cash Outlay} = \text{CAPEX} + \text{OPEX} = \$1,235.00 + \$37.55 = \mathbf{\$1,272.55 \text{ USD}} \quad (\sim\text{NRs } 170,045)$$

### 2.3 Pillar 3: Academic Tuition & Cost of Living (Separated Baseline)
Under strict GAAP and management accounting standards, personal living overhead and university degrees are general life expenses, not capital invested into a software repository. They are documented here for complete personal transparency but are **strictly excluded** from engineering leverage calculations:

| Category | Description | Term | Local Cost (NPR) | USD Equiv. |
| :--- | :--- | :---: | :---: | :---: |
| **College Engineering Fees** | IOE Tribhuvan University / KEC 4-Year Tuition | 4 years | NRs 62,984 | ~$471.79 |
| **Hostel Accommodation** | Modest student hostel (NRs 3,500/mo, includes electricity/water) | 48 months | NRs 168,000 | ~$1,258.43 |
| **Baseline Food Living** | Basic subsistence dining (NRs 9,000–11,000/mo average) | 42 months | ~NRs 420,000 | ~$3,146.00 |
| **Discretionary Personal** | Incidental local transit, personal supplies (<= NRs 1,500/mo) | 42 months | ~NRs 36,000 | ~$269.66 |
| **Total Academic & Living Baseline** | — | — | **~NRs 686,984** | **~$5,145.88** |

### 2.4 Pillar 4: Human Capital (Engineering Labor Invested)
The primary driver of technical asset accumulation in this ecosystem is not financial capital, but disciplined human engineering time:

| Effort Domain | Cumulative Hours | Nature of Work |
| :--- | :---: | :--- |
| **Active Capability Development** | 560 hrs | Writing, debugging, and testing 17 computational modules and firmware across 18 projects. |
| **Architectural RFCs & Schemas** | 160 hrs | Formalizing memory specifications, invariants, capability contracts, and ontology manifests. |
| **Discrete-Event Simulation** | 95 hrs | Developing, running, and tuning SimPy models (`warehouse_mem_sim.py`, `sweep_ipu_breakeven.py`). |
| **Toolchain & Pre-commit Automation** | 110 hrs | Developing `sync.ps1`, `reconciliation_engine.py`, and multi-category verification suites. |
| **Repository Maintenance & Git Hygiene** | 80 hrs | 18-branch coordination, documentation syncing, and transcript archiving. |
| **Total Human Capital Invested** | **~1,005 hrs** | **High-leverage engineering labor over 3.5 years** |

### 2.5 Pillar 5: Estimated Replacement-Equivalent Labor Cost
Replacement cost estimates what it would cost an organization or independent engineering client to reproduce the ecosystem's working code, verified architectures, test suites, and documentation from scratch.

$$\text{Replacement Cost} = \sum_{i=1}^{M} \left( H_i \times W_{\text{defensible}} \right) + C_{\text{infra}} + C_{\text{validation}}$$

Where:
- $H_i$ = Defensible engineering hours required to rebuild capability $i$ (~850 hours net rebuilding time excluding learning curve).
- $W_{\text{defensible}}$ = Defensible junior-to-mid systems engineering contracting rate ($25.00 – $35.00 / hour).
- $C_{\text{infra}}$ = Minimal cloud/hardware infrastructure reproduction setup ($500 – $1,000).
- $C_{\text{validation}}$ = Test suite and dataset calibration overhead ($1,500 – $2,500).

```
┌────────────────────────────────────────────────────────────────────────┐
│                   REPLACEMENT-EQUIVALENT RECONSTRUCTION                │
├───────────────────────────────┬───────────────────┬────────────────────┤
│ Rebuilt Component             │ Estimated Hours   │ Replacement Cost   │
│                               │                   │ (@ $25.00 / hour)  │
├───────────────────────────────┼───────────────────┼────────────────────┤
│ 17 Computational Capabilities │ 450 hrs           │ $11,250 USD        │
│ 4 Presentation & Web Hubs     │ 80 hrs            │ $2,000 USD         │
│ Architecture RFCs & Invariants│ 140 hrs           │ $3,500 USD         │
│ Discrete Simulation Suites    │ 90 hrs            │ $2,250 USD         │
│ Multi-Branch Automation/Sync  │ 90 hrs            │ $2,250 USD         │
│ Test Fixtures & Datasets      │ —                 │ $2,000 USD         │
│ Cloud / Tooling Overhead      │ —                 │ $1,750 USD         │
├───────────────────────────────┼───────────────────┼────────────────────┤
│ Total Central Replacement Base│ **~850 net hrs**  │ **~$25,000 USD**   │
└───────────────────────────────┴───────────────────┴────────────────────┘
```

> [!IMPORTANT]
> **Defensible Valuation Bounds:**  
> - **Lower Bound (Pessimistic: $15/hr labor rate):** ~$15,500 USD  
> - **Central Estimate (Realistic: $25/hr labor rate):** ~$25,000 USD  
> - **Upper Bound (Optimistic: $35/hr labor rate):** ~$37,000 USD  
>
> *Epistemic Warning:* This figure is strictly an **accounting replacement-labor proxy**. It does NOT represent enterprise market value, liquidated asset worth, or commercial enterprise value.

---

## 3. Defensible Financial & Operational Metrics

We formally retire and replace the following ungrounded metrics:

```
❌ RETIRED:  "$25,000 / $2,965 = 8.4x ROI"              (Conflated living expenses with CAPEX; called replacement cost "ROI")
❌ RETIRED:  "$25,000 / $5.00 = 5,000x AI Leverage"     (Attributed 3.5 years of manual code to a 1-week AI subscription)
❌ RETIRED:  "+2,298.8% Net Rebate ROI"                 (Treated consumer retail discount as financial income)
```

We establish the following **calibrated, transparent metrics**:

### 3.1 Replacement-Cost to Direct-Cash-Spend Ratio ($\rho_{\text{cash}}$)
Measures how much reproducible technical infrastructure was accumulated relative to actual cash out-of-pocket on productive assets:

$$\rho_{\text{cash}} = \frac{\text{Central Replacement Cost (\$25,000)}}{\text{Direct Productive Cash Outlay (\$1,272.55)}} \approx \mathbf{19.65\times}$$

### 3.2 Direct AI Spend as a Fraction of Replacement Base ($\phi_{\text{AI}}$)
Measures the direct paid AI cash contribution toward the accumulated technical asset base:

$$\phi_{\text{AI}} = \frac{\text{Cumulative Paid AI Spend (\$5.00)}}{\text{Central Replacement Cost (\$25,000)}} = \mathbf{0.020\%} \quad (0.0002)$$

*Interpretation:* The ecosystem's software infrastructure was 99.98% self-bootstrapped through open-source tooling, free-tier quotas, and human engineering before any international card was utilized.

### 3.3 Google Family Theoretical Retail Cost-Avoidance Multiplier ($M_{\text{retail}}$)
Measures the nominal consumer price discount achieved by consolidating 6 developer accounts under one $5.00/mo Google One AI Pro Family plan:

$$M_{\text{retail}} = \frac{6 \times \$19.99\text{/month}}{\$5.00\text{/month}} = \frac{\$119.94}{\$5.00} = \mathbf{23.99\times \text{ Retail Cost Avoidance}}$$

*Operational Value:* Unlocks **6x independent rate-limit quotas** and parallel NotebookLM slots for `Super-NLM`, but generates **$0.00 in monetary cash dividends**.

---

## 4. Vectorized R&D Resource Consumption

Combining disparate dimensional units (dollars, human minutes, inference tokens, CPU seconds) into an arbitrary scalar formula creates false precision. All R&D tasks in this repository must represent resource consumption as a **4-dimensional telemetry vector**:

$$\vec{R}_{\text{task}} = \begin{bmatrix} C_{\text{usd}} \\ T_{\text{human}} \\ N_{\text{tokens}} \\ S_{\text{compute}} \end{bmatrix} = \begin{bmatrix} \text{Financial Cash Outlay (USD)} \\ \text{Human Active Intervention (minutes)} \\ \text{LLM Inference Tokens Consumed} \\ \text{Deterministic CPU/GPU Execution (seconds)} \end{bmatrix}$$

### Task Comparison Example
| Task Profile | $C_{\text{usd}}$ | $T_{\text{human}}$ | $N_{\text{tokens}}$ | $S_{\text{compute}}$ | Vector Evaluation |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Manual Coding** | $0.00 | 180 min | 0 | 5 s | Labor-intensive, Zero Token |
| **Agent-Assisted** | $0.00 | 25 min | 45,000 | 12 s | Token-intensive, Low Human |
| **SMT Verification** | $0.00 | 5 min | 2,000 | 180 s | Compute-heavy, High Determinism |

No composite score may be derived from $\vec{R}_{\text{task}}$ without an explicit, empirically justified weighting model.

---

## 5. Economic Research Direction: Discovery Efficiency & Funnel Pruning

The true economic value of the **Headless Invariant Assurance Engine** lies in **discovery cost efficiency**: filtering massive hypothesis spaces down to verified truths at minimum financial and human cost.

### 5.1 Discovery Cost Efficiency ($E_{\text{discovery}}$)
$$\text{Discovery Cost Efficiency} = \frac{C_{\text{financial}} + C_{\text{compute}}}{\text{Verified Discoveries}}$$

### 5.2 Human Intervention Ratio ($I_{\text{human}}$)
$$I_{\text{human}} = \frac{\text{Human Active Minutes}}{\text{Verified Discoveries}}$$

### 5.3 The Funnel Pruning Pipeline & Invariant Tracking

```text
Raw Natural Language Claims (N = 1,000)
    ↓ (Stage 1: AST / Static Type Filter — Zero Token Cost)
AST Survivors (N = 250)
    ↓ (Stage 2: SMT Symbolic Verification — Zero Token Compute Cost)
SMT / Z3 Survivors (N = 40)
    ↓ (Stage 3: Deterministic Sandbox Execution — Anvil / Docker)
Sandbox Candidates (N = 12)
    ↓ (Stage 4: Human / Verifier Dossier Review)
VERIFIED DISCOVERIES (N = 8)
```

> [!CAUTION]
> **The False-Negative Pruning Hazard:**  
> A pruning filter that eliminates 99% of candidates is worthless if it discards real invariant violations. The pipeline must be evaluated not merely by pruning throughput, but by:
> 
> $$\text{Precision} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Positives}}, \quad \text{Recall} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Negatives}}$$
>
> **Core Architecture Requirement:** Every version of the Invariant Assurance Engine must maintain **100% recall on a benchmark suite of planted synthetic violations** before being deployed against real systems.

---

## 6. Integration-Cost & Synergy Measurement Models

### 6.1 Integration-Cost & Net Capability Value
To prevent "platform sprawl" and architectural debt, adding a new capability must satisfy:

$$\text{Net Capability Value} = V_{\text{cap}} - C_{\text{dev}} - C_{\text{maint}} - C_{\text{integration}} > 0$$

Where:
- $V_{\text{cap}}$: Quantified utility (hours saved per month $\times$ rate).
- $C_{\text{dev}}$: Amortized initial development cost.
- $C_{\text{maint}}$: Monthly upkeep, API updates, and dependency maintenance.
- $C_{\text{integration}}$: Protocol adapter and schema translation overhead.

### 6.2 Measuring Emergent Synergy
Synergy between two capabilities $A$ and $B$ must be experimentally demonstrated, not assumed:

$$\text{Synergy}(A, B) = \text{Metric}(A + B) - \left( \text{Metric}(A) + \text{Metric}(B) \right)$$

Measured strictly along operational axes:
1. **Task completion elapsed time.**
2. **Human intervention minutes.**
3. **Reproducibility pass rate (%).**
4. **Token and compute expenditure.**
