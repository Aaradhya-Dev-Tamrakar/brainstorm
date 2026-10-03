---
name: dsp-signal-engine
description: >-
  Digital Signal Processing (DSP) & Filter Design engine (EX 710, EX 605, SH 501).
  Synthesizes FIR (windowed sinc) and IIR (Butterworth/Chebyshev via Bilinear Transform)
  filters, calculates FFT frequency spectra, and models quantization noise.
---

# Digital Signal Processing & Filter Design Engine (`dsp-signal-engine`)

Derived from **EX 710 (Digital Signal Analysis and Processing)**, **EX 605 (Filter Design)**, and **SH 501 (Engineering Mathematics III)** in the BE ECIE curriculum.

This skill equips agents to design digital FIR/IIR filters, analyze discrete frequency spectra via FFT, model quantization noise for fixed-point integer architectures, and simulate audio and sensor pipelines (connecting directly to [`SPARK`](file:///F:/Aaradhya-Dev-Tamrakar/SPARK)).

---

## 1. Operating Rules & Mathematical Foundations

1. **Sampling Criterion (Nyquist-Shannon):** Always verify $f_s \ge 2 \cdot f_{max}$ to prevent spectral aliasing.
2. **Phase Linearity:**
   - For audio/telecom applications where phase distortion must be strictly zero (constant group delay), synthesize **Linear-Phase FIR filters** (symmetric impulse response $h[n] = h[N-1-n]$).
   - When steep cutoff roll-off is required with minimal computational cost, synthesize **IIR filters** (Butterworth for flat passband, Chebyshev for steep transition).
3. **Bilinear Transformation Pre-Warping:**
   When mapping analog poles to the digital Z-plane, pre-warp critical frequencies to compensate for tangent nonlinear frequency mapping:
   $$\omega_a = \frac{2}{T} \tan\left(\frac{\omega_d T}{2}\right)$$

---

## 2. Core Capabilities & Workflows

### Capability A: FIR Filter Synthesis CLI
Execute [`scripts/filter_synth.py`](scripts/filter_synth.py) to generate impulse response coefficients:
```powershell
python tools/skills/dsp-signal-engine/scripts/filter_synth.py --taps 31 --cutoff 0.25 --window hamming
```

### Capability B: Discrete Fourier Transform (FFT) Spectral Analysis
When evaluating frequency components of an acquired sensor stream:
- Compute Radix-2 FFT to obtain complex frequency bins $X[k]$.
- Compute Power Spectral Density (PSD):
  $$P[k] = \frac{1}{N} |X[k]|^2$$
- Convert to decibels relative to full scale (dBFS):
  $$\text{dBFS} = 20 \log_{10}\left(\frac{|X[k]|}{N / 2}\right)$$

### Capability C: Quantization & Fixed-Point Q-Format Modeling
When porting floating-point algorithms to microcontrollers without an FPU:
- Model Q15 format: Range $[-1.0, +0.9999]$, step size $\Delta = 2^{-15} \approx 3.05 \times 10^{-5}$.
- Signal-to-Quantization-Noise Ratio (SQNR):
  $$\text{SQNR} \approx 6.02 \cdot B + 1.76 \text{ dB} \quad (B = \text{bits})$$
  *(For a 16-bit ADC, $\text{SQNR} \approx 98.08 \text{ dB}$)*
