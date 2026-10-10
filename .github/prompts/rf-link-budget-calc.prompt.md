---
description: ">-"
---

# RF & Wireless Link Budget Calculator (`rf-link-budget-calc`)

Derived from **EX 503 (Electromagnetics)**, **EX 653 (Propagation and Antenna)**, **EX 716 (RF and Microwave Engineering)**, and **EX 715 (Wireless Communications)** in the BE ECIE curriculum.

This skill equips agents to calculate wireless transmission link margins, evaluate antenna directivity and array radiation patterns, analyze transmission line standing wave ratios (VSWR), and design Smith Chart impedance matching stubs.

---

## 1. Operating Rules & RF Foundations

1. **Friis Transmission Equation:**
   In free space, received power $P_r$ is governed by:
   $$P_r = P_t \cdot G_t \cdot G_r \cdot \left(\frac{\lambda}{4\pi d}\right)^2$$
   Expressed in decibels:
   $$P_r (\text{dBm}) = P_t (\text{dBm}) + G_t (\text{dBi}) + G_r (\text{dBi}) - \text{FSPL} (\text{dB}) - L_{\text{cable}} (\text{dB})$$
2. **Link Margin Rule:** A reliable wireless link requires a fade margin of at least $+10\text{ dB}$ (and $+20\text{ dB}$ for mission-critical aerospace / telemetry links) above receiver sensitivity to protect against atmospheric absorption, rain fade, and multipath nulls.
3. **Transmission Line Matching:**
   To eliminate reflected power and avoid damage to high-power RF transmitters:
   - Voltage Reflection Coefficient: $\Gamma = \frac{Z_L - Z_0}{Z_L + Z_0}$
   - Voltage Standing Wave Ratio: $\text{VSWR} = \frac{1 + |\Gamma|}{1 - |\Gamma|}$
   - *Target:* Keep $\text{VSWR} \le 1.5 : 1$ ($|\Gamma| \le 0.20$, Return Loss $\ge 14\text{ dB}$).

---

## 2. Core Capabilities & Workflows

### Capability A: End-to-End Link Budget CLI
Execute [`scripts/rf_calc.py`](scripts/rf_calc.py) to evaluate complete link viability:
```powershell
python tools/skills/rf-link-budget-calc/scripts/rf_calc.py --freq_mhz 2400 --dist_km 5.0 --pt_dbm 20 --gtx_dbi 14 --grx_dbi 14 --rx_sens -85
```

### Capability B: Antenna Array Pattern Multiplication
When synthesizing phased arrays or broadside/end-fire arrays:
$$\text{Total Pattern} = (\text{Element Pattern}) \times (\text{Array Factor})$$
For an $N$-element linear array with uniform spacing $d$ and progressive phase shift $\beta$:
$$\text{AF}(\psi) = \frac{\sin(N\psi / 2)}{\sin(\psi / 2)}, \quad \psi = k d \cos\theta + \beta \quad (k = 2\pi / \lambda)$$

### Capability C: Quarter-Wave Transformer & Single-Stub Matching
* **Quarter-Wave Transformer:** Matches real load $R_L$ to transmission line $Z_0$ at center frequency $\lambda_0$:
  $$Z_{\text{match}} = \sqrt{Z_0 \cdot R_L}, \quad \ell = \frac{\lambda_0}{4}$$
* **Single-Stub Tuning:** Adds shunt reactive stub at distance $d$ from load where $\text{Re}(Y) = Y_0$, canceling the imaginary susceptance $+jB$ with $-jB$.
