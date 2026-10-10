---
description: ">-"
---

# Dynamic Control Systems & Stability Simulator (`control-systems-sim`)

Derived from **EX 509 (Control System)** in the BE ECIE curriculum.

This skill equips agents to evaluate linear time-invariant (LTI) dynamic systems, calculate stability margins (Gain Margin, Phase Margin via Routh-Hurwitz, Bode, and Nyquist criteria), and tune closed-loop Proportional-Integral-Derivative (PID) controllers.

---

## 1. Operating Rules & Control Principles

1. **BIBO Stability Requirement:** A linear continuous system is Bounded-Input Bounded-Output (BIBO) stable if and only if all poles of the closed-loop transfer function lie strictly in the open Left Half of the s-plane ($\text{Re}(p_i) < 0$).
2. **Frequency Domain Stability Margins:**
   - **Phase Margin ($PM$):** $180^\circ + \angle G(j\omega_{gc})$, where $|G(j\omega_{gc})| = 1$ ($0\text{ dB}$).
   - **Gain Margin ($GM$):** $-20 \log_{10} |G(j\omega_{pc})|$, where $\angle G(j\omega_{pc}) = -180^\circ$.
   - *Target Stability:* Robust control systems require $PM \ge 45^\circ$ to $60^\circ$ and $GM \ge 6\text{ dB}$ to ensure stability under parameter drift.
3. **PID Parameter Roles:**
   - $K_p$ (Proportional): Increases loop bandwidth, decreases rise time, but increases overshoot.
   - $K_i$ (Integral): Eliminates steady-state offset error, but degrades phase margin and increases oscillation.
   - $K_d$ (Derivative): Adds phase lead, dampens oscillations, improves transient stability, but amplifies high-frequency measurement noise.

---

## 2. Core Capabilities & Workflows

### Capability A: Second-Order Plant Transient Analysis CLI
Execute [`scripts/control_analyzer.py`](scripts/control_analyzer.py) to calculate exact damping characteristics:
```powershell
python tools/skills/control-systems-sim/scripts/control_analyzer.py --wn 5.0 --zeta 0.6 --kp 2.0 --ki 1.0 --kd 0.2
```

### Capability B: State-Space Representation & Conversion
Convert high-order transfer functions into first-order differential state-space matrices:
$$\dot{x}(t) = A x(t) + B u(t)$$
$$y(t) = C x(t) + D u(t)$$

For a standard 2nd-order system $\ddot{y} + 2\zeta\omega_n \dot{y} + \omega_n^2 y = \omega_n^2 u$:
$$A = \begin{bmatrix} 0 & 1 \\ -\omega_n^2 & -2\zeta\omega_n \end{bmatrix}, \quad B = \begin{bmatrix} 0 \\ \omega_n^2 \end{bmatrix}, \quad C = \begin{bmatrix} 1 & 0 \end{bmatrix}, \quad D = [0]$$

### Capability C: Ziegler-Nichols Closed-Loop Tuning Rules
When tuning an unfamiliar physical plant using sustained oscillation method (finding critical gain $K_{cr}$ and period $P_{cr}$):

| Controller Type | Proportional Gain ($K_p$) | Integral Time ($T_i$) | Derivative Time ($T_d$) |
| :--- | :--- | :--- | :--- |
| **P** | $0.50 \cdot K_{cr}$ | $\infty$ | $0$ |
| **PI** | $0.45 \cdot K_{cr}$ | $P_{cr} / 1.2$ | $0$ |
| **PID** | $0.60 \cdot K_{cr}$ | $0.50 \cdot P_{cr}$ | $0.125 \cdot P_{cr}$ |
