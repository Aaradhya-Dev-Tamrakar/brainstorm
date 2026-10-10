---
description: ">-"
---

# Aeronautical Telecommunication & Navigation Analyzer (`avionic-telecom-analyzer`)

Derived from **EX 725 04 (Aeronautical Telecommunication - Elective I)** and **EX 725 01 (Radar Technology)** in the BE ECIE curriculum.

This skill equips agents to calculate aviation ground-based electronics performance, model Communication, Navigation, Surveillance / Air Traffic Management (CNS/ATM) systems, solve hyperbolic Multilateration (MLAT) TDOA equations, and evaluate radar detection ranges under ICAO standards.

---

## 1. Operating Rules & Avionics Principles

1. **ICAO Annex 10 Regulatory Conformance:** All radio navigation frequencies, channel spacings (8.33 kHz / 25 kHz VHF air-band), and signal tolerances must align with International Civil Aviation Organization (ICAO) standards.
2. **Standard Aviation Units Conversion:**
   - Altitude: Feet (ft) $\times 0.3048 \rightarrow$ meters (m).
   - Horizontal Distance: Nautical Miles (NM) $\times 1852 \rightarrow$ meters (m).
   - Speed: Knots (kt) $\times 0.514444 \rightarrow \text{m/s}$.
3. **Radar Detection Fourth-Power Law:**
   Radar echo power decreases with the fourth power of target distance ($R^4$). To double detection range, transmitter power must increase by a factor of 16 ($+12\text{ dB}$).
4. **ILS Critical Geometry:**
   - Standard Localizer carrier: 108.10 MHz to 111.95 MHz, Difference in Depth of Modulation (DDM) = 0 at runway centerline (90 Hz left, 150 Hz right).
   - Standard Glide Slope carrier: 329.15 MHz to 335.00 MHz, standard descent angle $\theta = 3.0^\circ$.

---

## 2. Core Capabilities & Workflows

### Capability A: Radar Range Equation CLI
Execute [`scripts/aero_calc.py`](scripts/aero_calc.py) to calculate maximum detection range for primary radar targets:
```powershell
python tools/skills/avionic-telecom-analyzer/scripts/aero_calc.py --mode radar --pt_kw 250 --freq_ghz 3.0 --gain_db 32 --rcs 1.0 --pmin_dbm -90
```

### Capability B: Multilateration (MLAT) TDOA Hyperbolic Positioning
When localizing an aircraft transmitting ADS-B or Mode-S squitter pulses using multiple ground receiver stations:
- Each pair of receivers $(R_0, R_i)$ defines a hyperboloid of position given by:
  $$d_i - d_0 = c \cdot (t_i - t_0)$$
- Solve for target coordinates $(x, y, z)$ via nonlinear Gauss-Newton least-squares optimization:
```powershell
python tools/skills/avionic-telecom-analyzer/scripts/aero_calc.py --mode tdoa
```

### Capability C: VOR & DME Radio Navigation Geometry
* **VHF Omni-directional Range (VOR):**
  Phase difference between 30 Hz FM reference signal and 30 Hz AM variable phase signal directly yields the magnetic bearing (Radial) from the VOR ground beacon ($0^\circ \text{ to } 360^\circ$):
  $$\text{Bearing} = \phi_{\text{variable}} - \phi_{\text{reference}}$$
* **Distance Measuring Equipment (DME):**
  Airborne interrogator transmits pulse pairs separated by $12\,\mu\text{s}$ at carrier $f_1$; ground transponder replies with $50\,\mu\text{s}$ delay at carrier $f_2$. Slant range $R$:
  $$R = \frac{c \cdot (t_{\text{roundtrip}} - 50\,\mu\text{s})}{2}$$
