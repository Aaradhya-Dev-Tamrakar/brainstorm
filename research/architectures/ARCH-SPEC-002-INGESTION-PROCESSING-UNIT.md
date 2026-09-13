> **Artifact ID:** `ARCH-SPEC-002`  
> **Title:** The Ingestion Processing Unit (IPU) & The Evolutionary Boundary-Reduction Strategy  
> **Version:** `1.1.0`  
> **Status:** `PROPOSED_ARCHITECTURE`  
> **Principal Architect:** Aaradhya Dev Tamrakar  
> **Discipline:** Electronics, Communication & Information Engineering (ECIE Capstone / Independent R&D)  
> **Domain:** Ingress-Aware Near-Memory Processing for High-Velocity Irregular Data Streams  
> **Created Date:** 2026-09-13  
> **Evidence Tier:** `HEURISTIC_HYPOTHESIS`  
> **Repository:** `F:\Aaradhya-Dev-Tamrakar\brainstorm`  
> **Execution Context:** Antigravity / Gemini Engine  
> **Upstream Trace:** [`ARCH-SPEC-001`](ARCH-SPEC-001-ECIE-COMPUTE-MEMORY.md), [`2026-09-13_STRANGLER-IPU_CONVERSATION.md`](../transcripts/2026-09-13_STRANGLER-IPU_CONVERSATION.md)  
> **Downstream Trace:** [`warehouse_mem_sim.py`](../../sim/warehouse_mem_sim.py), [`INV-MEM-001.md`](../invariants/INV-MEM-001.md)  

---

## 1. Executive Philosophy: The "Strangler Fig" Evolutionary Transition

### 1.1 The Revolutionary Fallacy vs. The Evolutionary Invariant
Clean-slate architectures almost always fail commercially if they demand a "rip-and-replace" of the existing global computing and telecommunications infrastructure. 

Just as **2G and 3G cellular standards could not be dismantled overnight** when 4G and 5G arrived (requiring multi-mode software-defined radios, backward compatibility, and gradual spectrum refarming over 20+ years), computing cannot simply abolish PCIe/CXL interconnects, standard DDR5/HBM DRAM, or the CUDA/PyTorch software ecosystem overnight.

### 1.2 The Core Thesis: Ingress Boundary Reduction
The fundamental question is not *"Can we invent a faster GPU from scratch?"*
The thesis is:
> **"Even when interconnect bandwidth scales (PCIe 6.0/7.0, CXL 3.0/4.0 at 128 GT/s), moving semantically reducible data through the conventional memory hierarchy remains unnecessarily expensive in energy, queue contention, and latency. By moving programmable reduction logic directly to the ingress boundary—where data first becomes expensive to transport—we can absorb high-velocity, low-semantic-density streams before they choke host memory."**

* **The 3 Workload Classes:**
  1. **High-Rate Communications:** Massive MIMO channel estimation, FFT pipelines, beamforming, and Sub-THz symbol detection.
  2. **AI Inference & KV-Cache:** Selective attention reductions, KV-cache filtering, token routing, and sparse embedding transformations.
  3. **High-Rate Sensing:** Radar point clouds, ISAC telemetry, and high-frequency vision streams.

* **The Strategic Evolutionary Path (The STRANGLER Model):**
  1. **Phase 1 (Transparent Compatibility):** The IPU acts as an enhanced, backward-compatible CXL/PCIe memory controller or smart NIC bridge (delivering burst packing and smart coalescing without host driver changes).
  2. **Phase 2 (Opportunistic Stream Processing):** Compilers and runtimes offload streaming reductions, baseband transforms, and attention pre-filters in-flight.
  3. **Phase 3 (Eventual Architectural Dominance):** As boundary processing absorbs 80–90% of raw data movement, monolithic host GPUs shrink into lightweight executive coordinators.

---

## 2. IPU System Topology & Channel Decomposition

```
[ 6G Sub-THz Ingress / High-Speed Sensor Array ] (1 Tbps Burst Stream)
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                 THE INGESTION PROCESSING UNIT (IPU)                         │
│                    (The Architectural Shock Absorber)                        │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ 1. Line-Rate Ingestion Buffer & Traffic Shaper                      │   │
│   │    • Absorbs multi-gigabit bursts without host CPU/GPU interrupts   │   │
│   │    • Dynamic Bank-Conflict & Jitter Predictor                       │   │
│   └──────────────────────────────────┬──────────────────────────────────┘   │
│                                      │ Filtered Stream                      │
│   ┌──────────────────────────────────▼──────────────────────────────────┐   │
│   │ 2. Inline Stream Transform & Reduction Engine (v+2 PIM Logic)        │   │
│   │    • Baseband Channel Estimation & Massive MIMO Matrix Inversion    │   │
│   │    • Semantic Tokenization & Attention Softmax Local Accumulation   │   │
│   │    • Zero-Copy Discard: 99%+ raw entropy reduced at boundary        │   │
│   └──────────────────────────────────┬──────────────────────────────────┘   │
│                                      │ Clustered Bursts                     │
│   ┌──────────────────────────────────▼──────────────────────────────────┐   │
│   │ 3. Smart Coalescing & Interconnect Adapter (v+1 Logic)              │   │
│   │    • Translates scattered payloads into optimal 64B cacheline bursts│   │
│   │    • Presents a standard, legacy-compliant CXL / PCIe / AXI-4 face  │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Pristine, Low-Bandwidth Semantic Payloads
                                       ▼ (PCIe 5.0/6.0, CXL 3.0, or AXI-4)
┌─────────────────────────────────────────────────────────────────────────────┐
│                      LEGACY HOST SUBSYSTEM                                  │
│   [ Host GPU / Vortex RISC-V Cores ] ── [ Commodity DDR5 / HBM Memory ]     │
│   (Zero hardware changes required; operates unthrottled on digested data)   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. High-Velocity Ingress Stress Scenarios: Telecom & AI Workloads

To stress-test host interconnect boundaries, consider high-velocity ingress scenarios across emerging telecommunications and distributed accelerator topologies:
* **Constructed Ingress Stress Test:** In extreme Sub-THz massive MIMO front-ends or multi-channel sensor arrays, aggregate raw digitized sample streams can peak in the $R_{\text{in}} \sim 50\text{ to } 200+\text{ Gbps}$ range (with research targets exploring higher aggregate burst rates).
* **The Modern Interconnect Context:** While modern interconnects continue scaling aggressively (PCIe 6.0/CXL 3.0 delivering $\sim 128\text{ GB/s}$ and CXL 4.0 reaching $128\text{ GT/s}$), brute-force bus bandwidth scaling does not eliminate the **thermodynamic energy cost of data transport**, queue latency, or memory bank contention.
* **The Ingress Boundary Advantage:** By intercepting streams directly at the ADC/PHY boundary:
  1. The IPU executes channel estimation, matched filtering, or KV-cache indexing **in-flight** in its stream accumulator.
  2. It emits only decoded symbols, high-value tokens, or semantic embeddings to the host bus.
  3. **Break-Even Condition:** Downstream memory pressure is reduced whenever the semantic compression ratio exceeds the IPU pipeline processing latency.

---

## 4. Hardware Realization & Open Predecessors

The IPU can be implemented entirely using proven, open-source building blocks:
* **Ingress PHY Interface:** Open LitePCIe / LiteEth / LiteX SerDes cores.
* **Control & Dispatch:** Lightweight open-source RV32IMC RISC-V control core (e.g., PicoRV32 or VexRiscv).
* **Streaming Compute Engine:** Custom synthesizable pipeline in Amaranth/Migen or SystemVerilog executing streaming matrix-vector arithmetic.
* **Memory Bridge:** LiteDRAM controller front-end interfacing standard LPDDR5 or DDR4 commodity chips.

---

## 5. Architectural Invariants for the IPU

1. **The Transparency Invariant:** In fallback mode, the IPU must pass transactions through to legacy memory with latency overhead bounded by $\Delta t \le 2\text{ clock cycles}$.
2. **The Absorption Invariant:** Any reduction or filtering operation with compression factor $\ge 2\times$ must be completed at line rate inside the IPU before touching the host system bus.
3. **The Coexistence Invariant:** The host operating system and GPU software stack must see the IPU as a standard, compliant memory-mapped I/O or CXL device, requiring zero proprietary kernel patches.
