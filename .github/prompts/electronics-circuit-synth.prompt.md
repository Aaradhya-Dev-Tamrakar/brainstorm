---
description: ">-"
---

# Analog Electronics & Circuit Synthesizer (`electronics-circuit-synth`)

Derived from **EX 501 (Electronic Devices & Circuits)**, **EX 553 (Advanced Electronics)**, **EX 510 (Instrumentation)**, and **EE 401 (Basic Electrical Engineering)** in the BE ECIE curriculum.

This skill equips agents to synthesize analog signal conditioning circuits, design active RC filters, calculate transistor small-signal bias stability, configure multivibrators (555 timers), and analyze Wheatstone bridge transducer interfaces.

---

## 1. Operating Rules & Analog Design Principles

1. **Virtual Ground Invariant:** For negative-feedback operational amplifier circuits operating in their linear region, the potential difference between inverting ($V^-$) and non-inverting ($V^+$) terminals is zero ($V^+ \approx V^-$), and input bias current is negligible ($I_{in} \approx 0$).
2. **Gain-Bandwidth Product (GBWP) Constraint:**
   $$\text{Closed-Loop Bandwidth} = \frac{\text{GBWP}}{A_{CL}}$$
   Always verify that chosen op-amp parts provide sufficient GBWP and slew rate ($SR \ge 2\pi f V_{pk}$) for the desired output amplitude and frequency.
3. **Sensor Bridge Amplification:**
   Small resistance changes ($\Delta R / R \ll 1$) produce millivolt-level differential signals that must be amplified using high-CMRR 3-op-amp instrumentation amplifiers (e.g., AD620 / INA128) before ADC digitizing.

---

## 2. Core Capabilities & Workflows

### Capability A: Analog Circuit Synthesis CLI
Execute [`scripts/circuit_calc.py`](scripts/circuit_calc.py) to calculate exact passive component values:
```powershell
python tools/skills/electronics-circuit-synth/scripts/circuit_calc.py --mode sallen_key
python tools/skills/electronics-circuit-synth/scripts/circuit_calc.py --mode 555
python tools/skills/electronics-circuit-synth/scripts/circuit_calc.py --mode bridge
```

### Capability B: 2nd-Order Sallen-Key Lowpass Active Filter
* Toplogy: Unity gain, 2 resistors ($R_1 = R_2 = R$), 2 capacitors ($C_1 = 2 C_2$).
* Transfer Function:
  $$H(s) = \frac{\omega_0^2}{s^2 + \frac{\omega_0}{Q} s + \omega_0^2}$$
* Natural Frequency: $\omega_0 = \frac{1}{\sqrt{R_1 R_2 C_1 C_2}} = \frac{1}{\sqrt{2} R C_2}$
* Quality Factor: $Q = \frac{1}{\sqrt{2}} \approx 0.7071$ (Maximally flat Butterworth passband).

### Capability C: Transistor DC Biasing & Small-Signal Voltage Gain
For a Common-Emitter BJT amplifier with emitter degeneration resistor $R_E$:
* Voltage Gain:
  $$A_v \approx -\frac{R_C \parallel R_L}{r_e + R_E}, \quad r_e = \frac{V_T}{I_C} \approx \frac{26\text{ mV}}{I_C}$$
* Input Impedance: $R_{in} = R_1 \parallel R_2 \parallel [\beta (r_e + R_E)]$
* Output Impedance: $R_{out} \approx R_C$
