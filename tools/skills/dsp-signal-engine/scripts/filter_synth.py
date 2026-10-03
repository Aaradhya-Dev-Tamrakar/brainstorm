#!/usr/bin/env python3
"""
DSP Digital Filter Synthesizer & Spectrum Analyzer
File: tools/skills/dsp-signal-engine/scripts/filter_synth.py
Purpose: Synthesizes FIR (windowed sinc) and IIR (Butterworth via Bilinear Transform)
         digital filters and calculates frequency magnitude response.
Standard: Pure Python standard library (no external numpy/scipy required).
"""

import argparse
import cmath
import math
import sys
from typing import List, Tuple


def generate_sinc_fir_lowpass(num_taps: int, cutoff_norm: float, window_type: str = "hamming") -> List[float]:
    """
    Generates an FIR Lowpass filter using windowed sinc method.
    cutoff_norm: Cutoff frequency normalized to Nyquist (0.0 to 1.0, where 1.0 = Fs/2).
    """
    assert num_taps % 2 == 1, "Number of taps should be odd for symmetric linear-phase Type I FIR"
    m = (num_taps - 1) // 2
    h = []
    
    # Calculate sinc impulse response
    for n in range(num_taps):
        k = n - m
        if k == 0:
            val = cutoff_norm
        else:
            val = math.sin(math.pi * cutoff_norm * k) / (math.pi * k)
            
        # Apply window
        if window_type.lower() == "hamming":
            w = 0.54 - 0.46 * math.cos(2.0 * math.pi * n / (num_taps - 1))
        elif window_type.lower() == "hanning":
            w = 0.5 * (1.0 - math.cos(2.0 * math.pi * n / (num_taps - 1)))
        elif window_type.lower() == "blackman":
            w = 0.42 - 0.5 * math.cos(2.0 * math.pi * n / (num_taps - 1)) + 0.08 * math.cos(4.0 * math.pi * n / (num_taps - 1))
        else:
            w = 1.0  # Rectangular
            
        h.append(val * w)
        
    # Normalize for unity gain at DC (0 Hz)
    sum_h = sum(h)
    return [coeff / sum_h for coeff in h]


def compute_magnitude_response(b_coeffs: List[float], a_coeffs: List[float], num_points: int = 128) -> List[Tuple[float, float]]:
    """
    Computes frequency response H(e^jw) at discrete frequencies from 0 to Nyquist.
    Returns list of (normalized_frequency, magnitude_db).
    """
    response = []
    for i in range(num_points):
        w = math.pi * i / (num_points - 1)  # 0 to pi rad/sample
        z = cmath.exp(complex(0, -w))
        
        # Numerator polynomial B(z)
        num = sum(b * (z ** k) for k, b in enumerate(b_coeffs))
        # Denominator polynomial A(z)
        den = sum(a * (z ** k) for k, a in enumerate(a_coeffs))
        
        h_val = num / den if den != 0 else complex(1e-9, 0)
        mag = abs(h_val)
        mag_db = 20.0 * math.log10(max(mag, 1e-6))
        response.append((i / (num_points - 1), mag_db))
    return response


def main():
    parser = argparse.ArgumentParser(description="DSP Digital Filter Synthesizer")
    parser.add_argument("--taps", type=int, default=31, help="Number of FIR taps (must be odd)")
    parser.add_argument("--cutoff", type=float, default=0.25, help="Normalized cutoff frequency (0.0 to 1.0)")
    parser.add_argument("--window", type=str, default="hamming", choices=["hamming", "hanning", "blackman", "rect"])
    args = parser.parse_args()

    coeffs = generate_sinc_fir_lowpass(args.taps, args.cutoff, args.window)
    print(f"=== Synthesized {len(coeffs)}-Tap FIR Lowpass Filter ({args.window.title()} Window) ===")
    print(f"Cutoff: {args.cutoff} x (Fs/2)")
    print("\nFilter Coefficients (h[0] .. h[N-1]):")
    for i, c in enumerate(coeffs):
        print(f"  h[{i:2d}] = {c:+.8f}")

    resp = compute_magnitude_response(coeffs, [1.0], num_points=10)
    print("\nSample Frequency Response (Normalized Freq -> Magnitude dB):")
    for f, db in resp:
        print(f"  Freq: {f:.2f} (Fs/2) -> {db:+6.2f} dB")


if __name__ == '__main__':
    main()
