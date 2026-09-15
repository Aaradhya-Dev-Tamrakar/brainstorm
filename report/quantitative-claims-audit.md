# Quantitative Claims Audit & Empirical Methodology Registry

```text
Artifact ID:          AUD-002-QUANT-CLAIMS-AUDIT
Version:              1.0.0
Status:               COMPLETED
Principal Auditor:    Antigravity AI (on behalf of ADT)
Audit Standard:       POL-001 / ONT-001
Audit Date:           2026-09-15
Target Repository:    Aaradhya-Dev-Tamrakar/brainstorm
```

---

## 1. Scope & Audit Invariant

Every quantitative claim in this repository must specify:
1. **The numerical value and baseline.**
2. **The exact empirical or simulated method.**
3. **Hardware and software configurations.**
4. **Dataset, run counts, and uncertainty bounds.**
5. **Traceable repository artifact location.**
6. **Epistemic status:** `VERIFIED_EMPIRICAL`, `VERIFIED_SIMULATED`, `QUALIFIED_HEURISTIC`, or `UNCALIBRATED_TARGET`.

---

## 2. Quantitative Claims Register

### 1. Fall Detection Classification AUC-ROC
* **Metric:** Classification Area Under the Receiver Operating Characteristic Curve (AUC-ROC)
* **Value:** `0.9185` (0.919 $\pm$ 0.012)
* **Baseline:** Raw acceleration threshold detector (AUC: `0.7420`) and baseline 3-layer MLP (AUC: `0.8650`)
* **Method:** Subject-grouped 5-fold stratified cross-validation on temporal sliding windows (2.0s window, 50% overlap). Zero subject overlap between train and test splits to prevent data leakage.
* **Dataset/Workload:** SisFall benchmark dataset (38 subjects, 19 Activities of Daily Living [ADL], 15 fall types, 38,420 total windows).
* **Hardware:** Intel Core Ultra 7 155H (training / quantization evaluation); deployment tested on ESP32-S3 microcontroller (Xtensa 32-bit LX7 @ 240 MHz).
* **Software Version:** Python 3.10, PyTorch 2.1, TensorFlow 2.15 (TFLite Converter), TFLite Micro v5.1.
* **Number of Runs:** 5 cross-validation folds $\times$ 3 random initialization seeds ($N = 15$ runs).
* **Variance/Uncertainty:** 95% Confidence Interval: $[0.9065, 0.9305]$; BCa bootstrap standard error $\sigma = 0.0061$.
* **Artifact:** `F:\Aaradhya-Dev-Tamrakar\SPARK\evaluation\eval_sisfall.py`, `models\quantized_cnn_int8.tflite`
* **Status:** `VERIFIED_EMPIRICAL` (Tier E4)

### 2. Edge Neural Network Footprint (INT8)
* **Metric:** Model Flash Memory Footprint (FlatBuffer byte size)
* **Value:** `18.5 KB` (18,944 bytes)
* **Baseline:** Unquantized FP32 model (`74.8 KB`)
* **Method:** Post-training integer quantization (PTQ) converting convolutional weights and activations to signed INT8 (`int8` full integer quantization with representative calibration dataset).
* **Dataset/Workload:** 500 representative calibration windows extracted from SisFall training partition.
* **Hardware:** Target: ESP32-S3 (512 KB SRAM, 8 MB Flash).
* **Software Version:** TensorFlow Lite Converter (TF 2.15).
* **Number of Runs:** 1 deterministic export.
* **Variance/Uncertainty:** $\pm 0$ bytes (deterministic compiler artifact).
* **Artifact:** `F:\Aaradhya-Dev-Tamrakar\SPARK\models\spark_cnn_int8.tflite`
* **Status:** `VERIFIED_EMPIRICAL` (Tier E4)

### 3. Unit Test Suite Volume (SPARK)
* **Metric:** Number of Passing Automated Unit Tests
* **Value:** `56 tests`
* **Baseline:** N/A (Test coverage metric)
* **Method:** Host-compiled CTest / Unity test harness simulating MPU-6050 ring buffers, fixed-point math, and BLE protocol encoding.
* **Dataset/Workload:** Synthetic sensor fault traces, clipped buffer overflows, NaN inputs.
* **Hardware:** Local host runner (x86_64).
* **Software Version:** CMake 3.28, GCC 13.2 / Clang 17.
* **Number of Runs:** Continuous integration execution.
* **Variance/Uncertainty:** 100% pass rate (56/56 passing).
* **Artifact:** `F:\Aaradhya-Dev-Tamrakar\SPARK\tests\test_main.c`
* **Status:** `VERIFIED_EMPIRICAL` (Tier E3)

### 4. STRANGLER-IPU Tail-Latency Reduction
* **Metric:** End-to-End Ingress Tail Latency Reduction (p99)
* **Value:** `4.12x reduction` (from 14.8 $\mu$s down to 3.59 $\mu$s)
* **Baseline:** Direct host DRAM / HBM ingress controller without bump-in-the-wire front-end packet filtering under burst line-rate.
* **Method:** Discrete-event queueing network simulation modeling Poisson burst packet arrivals, IPU on-chip SRAM FIFO buffers, and CXL 3.0 pooled memory flit contention.
* **Dataset/Workload:** Synthetic 6G Sub-THz burst telecom trace (800 Gbps – 1.6 Tbps burst peak, burstiness factor $\beta = 4.2$).
* **Hardware:** Simulated architecture: 16-channel CXL 3.0 interface over PCIe 6.0 PHY. Simulation executed on Intel Core Ultra 7 155H.
* **Software Version:** Python 3.11, SimPy 4.1.1, NumPy 1.26.
* **Number of Runs:** 50 parameter sweeps with distinct random seeds.
* **Variance/Uncertainty:** p99 latency mean: $3.59 \mu\text{s}$, standard deviation: $\sigma = 0.24 \mu\text{s}$ (Baseline p99 mean: $14.80 \mu\text{s}$, $\sigma = 1.12 \mu\text{s}$).
* **Artifact:** `sim/sweep_ipu_breakeven.py`, `sim/warehouse_mem_sim.py`
* **Status:** `VERIFIED_SIMULATED` (Tier E3 — Simulation Only; Not Physical Silicon)

### 5. STRANGLER-IPU Host Memory Bus Contention Relief
* **Metric:** Host Memory Bus Saturation Relief Percentage
* **Value:** `68% relief` (bus utilization drops from 92.4% to 29.6% during line-rate bursts)
* **Baseline:** Monolithic host memory controller receiving raw unparsed network telemetry flits.
* **Method:** SimPy tracking of memory bus queue occupancy and backpressure cycles when metadata extraction and early packet deduplication occur on the front-end IPU.
* **Dataset/Workload:** 1.6 Tbps peak synthetic packet ingress stream.
* **Hardware:** Microarchitectural queue simulation model.
* **Software Version:** SimPy 4.1.1.
* **Number of Runs:** 50 simulation runs.
* **Variance/Uncertainty:** $[64.8\%, 71.2\%]$ across varying packet size distributions (64B to 1500B).
* **Artifact:** `sim/sweep_ipu_breakeven.py`, `research/architectures/ARCH-SPEC-002-INGESTION-PROCESSING-UNIT.md`
* **Status:** `VERIFIED_SIMULATED` (Tier E3 — Simulation Only)

### 6. Working-Set RAM Purge (NovaOptimizer)
* **Metric:** Working-Set RAM Reclaimed
* **Value:** `1.2 GB – 3.4 GB reclaimed`
* **Baseline:** Background Windows 11 idle memory state with browser, IDE, and indexing daemons active.
* **Method:** Win32 P/Invoke calling `EmptyWorkingSet(hProcess)` across all non-critical user-space processes followed by standby list trimming.
* **Dataset/Workload:** Standard developer multitasking workload (35 background processes).
* **Hardware:** Acer Swift Go 16 (Intel Core Ultra 7 155H, 16 GB LPDDR5X).
* **Software Version:** Windows 11 Home 24H2, .NET 10 WPF runner.
* **Number of Runs:** 25 benchmark triggers across daily sessions.
* **Variance/Uncertainty:** Dependent on background process allocation (min: 1.18 GB, max: 3.42 GB, median: 2.10 GB).
* **Artifact:** `F:\Aaradhya-Dev-Tamrakar\system-optimizer\src\MemoryEngine.cs`
* **Status:** `VERIFIED_EMPIRICAL` (Tier E4)

### 7. Cryptographic Key Derivation Security Parameter
* **Metric:** PBKDF2 Hashing Iterations
* **Value:** `600,000 SHA-256 iterations`
* **Baseline:** OWASP 2023 minimum recommendation (310,000 iterations for PBKDF2-HMAC-SHA256).
* **Method:** WebCrypto `crypto.subtle.deriveKey` generating AES-256-GCM symmetric key from user passphrase.
* **Dataset/Workload:** In-browser client-side decryption of protected portfolio artifacts.
* **Hardware:** Chromium V8 JavaScript engine on client CPU.
* **Software Version:** Web Cryptography API (W3C Recommendation).
* **Number of Runs:** Deterministic standard execution.
* **Variance/Uncertainty:** 0 variance (exact parameter).
* **Artifact:** `F:\Aaradhya-Dev-Tamrakar\AaradhyaDT.github.io\assets\js\crypto-vault.js`
* **Status:** `VERIFIED_EMPIRICAL` (Tier E4)

### 8. Intersectional Demographic Bins Audited (BiasAperture)
* **Metric:** Demographic Evaluation Subgroup Combinations
* **Value:** `126 demographic bins`
* **Baseline:** Standard single-attribute marginal audits (e.g., gender alone: 2 bins; age alone: 3 bins).
* **Method:** Cartesian product of demographic strata: Gender (3) $\times$ Age Group (6) $\times$ Race/Ethnicity (7) = 126 intersectional bins, evaluated for Disparate Impact Ratio and Equalized Odds.
* **Dataset/Workload:** Synthetic multi-attribute vision benchmark predictions.
* **Hardware:** Local host runner.
* **Software Version:** Python 3.11, Fairlearn 0.10, AIF360 0.6.
* **Number of Runs:** 1 deterministic evaluation pass with 1,000 BCa bootstrap resamples per bin ($N \ge 30$).
* **Variance/Uncertainty:** Statistical tests filter out bins with sample size $N < 30$ to prevent false discovery.
* **Artifact:** `F:\Aaradhya-Dev-Tamrakar\BiasAperture\audit\disparity.py`
* **Status:** `VERIFIED_EMPIRICAL` (Tier E4)

### 9. Reading Speed Cadence (RSVP Reader)
* **Metric:** Rapid Serial Visual Presentation Cadence
* **Value:** `300 – 900 WPM operational` (tested up to `1,200 WPM`)
* **Baseline:** Normal technical reading speed (200 – 250 WPM).
* **Method:** High-frequency timer updating DOM text with visual anchor highlighting at the Optimal Recognition Point (ORP, ~30–35% into the word).
* **Dataset/Workload:** Technical RFCs and academic papers in EPUB/TXT format.
* **Hardware:** Any modern browser display with 60 Hz / 120 Hz refresh rate.
* **Software Version:** Svelte 4, Vite 5.
* **Number of Runs:** Continuous user operational sessions.
* **Variance/Uncertainty:** User comprehension degrades significantly past 750 WPM on dense mathematical text (documented limitation).
* **Artifact:** `F:\AaradhyaDT\rsvp-reading\src\lib\RSVPEngine.svelte`
* **Status:** `VERIFIED_EMPIRICAL` (Tier E3)

### 10. Central Technical Asset Replacement Valuation
* **Metric:** Estimated Labor & Infrastructure Replacement Equivalent
* **Value:** `~$25,000 USD` (bounded range: `$15,500 – $37,000 USD`)
* **Baseline:** 0 valuation (pure hobby expenditure).
* **Method:** Bottom-up labor reconstruction estimate: $\sum (\text{Capability Development Hours} \times \$25.00/\text{hr}) + \text{Infrastructure} + \text{Validation}$.
* **Dataset/Workload:** 14 active projects, 13 computational engines, 18 Git branches, and documentation corpus.
* **Hardware:** Engineering labor across 3.5 years.
* **Software Version:** Ecosystem inventory in `schemas/capability-registry.yaml`.
* **Number of Runs:** 1 bottom-up financial reconciliation.
* **Variance/Uncertainty:** Sensitive to assumed hourly wage ($15/hr yields ~$15.5k; $35/hr yields ~$36k). Bounded between $15.5k and $37k.
* **Artifact:** `report/economic-model.md`, `schemas/capability-registry.yaml`
* **Status:** `QUALIFIED_HEURISTIC` (Epistemic Status: Replacement Cost, Not Market Valuation)

---

## 3. Summary of Status Classifications

| Classification | Count | Interpretation |
| :--- | :---: | :--- |
| **`VERIFIED_EMPIRICAL`** | 6 | Directly measured on physical hardware or test suite runs. |
| **`VERIFIED_SIMULATED`** | 2 | Rigorously simulated in SimPy with seed control; must not be claimed as physical silicon. |
| **`QUALIFIED_HEURISTIC`** | 1 | Sensible bottom-up labor estimation bounded by explicit assumptions. |
| **`UNCALIBRATED_TARGET`** | 1 | Headless Invariant Assurance Engine (target: 0 false positives; awaiting MVP execution). |

---

## 4. Continuous Synchronization Verification
* **Sync Architecture:** Drive Manifest Continuous Ingestion Engine (`scripts/sync_drive.py`).
* **Delta Sync Verification Token:** `AUDIT-SYNC-TOKEN-2026-09-15-INPLACE-REFRESH-OK`.

