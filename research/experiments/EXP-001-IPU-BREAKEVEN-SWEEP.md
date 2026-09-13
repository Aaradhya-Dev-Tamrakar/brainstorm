# 🏛️ RESEARCH PROTOCOL: EXP-001 (Ingress-Boundary Reduction Break-Even Parameter Sweep)

> **Artifact ID:** `EXP-001`  
> **Title:** Break-Even Interconnect Sweep: Conventional Host vs. Ingestion Processing Unit (IPU)  
> **Version:** `1.0.0`  
> **Status:** `PROPOSED_PROTOCOL`  
> **Principal Architect:** Aaradhya Dev Tamrakar  
> **Discipline:** Electronics, Communication & Information Engineering  
> **Domain:** Ingress-Aware Stream Processing & Interconnect Modeling  
> **Created Date:** 2026-09-13  
> **Evidence Tier:** `HEURISTIC_HYPOTHESIS` (Simulation Protocol)  
> **Upstream Trace:** [`ARCH-SPEC-002`](../architectures/ARCH-SPEC-002-INGESTION-PROCESSING-UNIT.md)  
> **Downstream Trace:** [`sim/sweep_ipu_breakeven.py`](../../sim/sweep_ipu_breakeven.py)  

---

## 1. Research Questions Addressed

* **RQ1 (Traffic Reducibility):** What fraction of ingress traffic must be semantically reducible ($\rho$) for an ingress processor to outperform scaling bus bandwidth?
* **RQ2 (Break-Even Frontier):** At what combinations of ingress data rate ($R_{\text{in}} \in [10, 1000]\text{ GB/s}$) and semantic compression ratio ($\rho \in [0.001, 1.0]$) does boundary processing yield net end-to-end latency and energy benefits?
* **RQ3 (Interconnect Neutrality):** Does the IPU retain its structural advantage across interconnect generations (PCIe 5.0 @ 64 GB/s, PCIe 6.0/CXL 3.0 @ 128 GB/s, and CXL 4.0 @ 128 GT/s)?

---

## 2. Parameter Sweep Matrix

### Independent Variables
1. **Ingress Data Rate ($R_{\text{in}}$):**
   $$R_{\text{in}} \in \{10, 25, 50, 100, 200, 500, 1000\}\text{ GB/s}$$
2. **Semantic Density / Output-to-Input Ratio ($\rho$):**
   $$\rho = \frac{\text{Useful Output Bytes}}{\text{Raw Input Bytes}} \in \{0.001, 0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 1.0\}$$
3. **Host Interconnect Bandwidth ($B_{\text{bus}}$):**
   - Baseline PCIe 5.0 x16: $64\text{ GB/s}$
   - Advanced CXL 3.0 / PCIe 6.0 x16: $128\text{ GB/s}$
   - Next-Gen CXL 4.0: $256\text{ GB/s}$ aggregate

### Evaluated Architectural Topologies
1. **Architecture A (Conventional Host Pipeline):**
   $$\text{Ingress} \xrightarrow{R_{\text{in}}} \text{Interconnect} \xrightarrow{B_{\text{bus}}} \text{Host Memory (DRAM)} \xrightarrow{\text{Memory Bus}} \text{GPU/ALU} \xrightarrow{\text{Compute}} \text{Result}$$
2. **Architecture B (CXL-Attached Pooled Memory):**
   $$\text{Ingress} \xrightarrow{R_{\text{in}}} \text{CXL Memory Pool} \xrightarrow{\text{Coherent Switch}} \text{Host Accelerator} \xrightarrow{\text{Compute}} \text{Result}$$
3. **Architecture C (STRANGLER-IPU Boundary Processing):**
   $$\text{Ingress} \xrightarrow{R_{\text{in}}} \text{IPU Pipeline} \xrightarrow{\text{Line-Rate Reduction } \rho} \text{Interconnect } (\rho \cdot R_{\text{in}}) \xrightarrow{B_{\text{bus}}} \text{Host Memory/GPU}$$

---

## 3. Measured Metrics
* **End-to-End Ingress Latency ($T_{\text{e2e}}$):** Ingress queueing delay + transport time + compute time.
* **Host Interconnect Traffic ($B_{\text{host}}$):** Total bytes traversing the physical motherboard/interposer traces.
* **Energy Proxy ($E_{\text{movement}}$):** Joules dissipated moving raw bytes vs. reduced semantic tokens.
* **Break-Even Boundary ($\rho^*$):** The critical value of $\rho$ where $T_{\text{IPU}} = T_{\text{Conventional}}$. Below $\rho^*$, IPU strictly dominates.
