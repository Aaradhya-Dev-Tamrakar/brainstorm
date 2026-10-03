#!/usr/bin/env python3
"""
Analog Electronics & Sensor Signal Conditioning Calculator
File: tools/skills/electronics-circuit-synth/scripts/circuit_calc.py
Purpose: Designs Sallen-Key active filters, calculates 555 timer component values,
         and computes Wheatstone bridge transducer sensitivity.
Standard: Pure Python standard library (no external numpy/scipy required).
"""

import argparse
import math
import sys
from typing import Dict


def calculate_sallen_key_lowpass(fc_hz: float, c1_farad: float = 10e-9, c2_farad: float = 10e-9) -> Dict[str, float]:
    """
    Computes resistor values R1, R2 for a unity-gain 2nd-order Sallen-Key lowpass filter
    with Butterworth response (Q = 0.7071).
    fc = 1 / (2*pi * sqrt(R1*R2*C1*C2))
    For Butterworth with C1=C2=C: R1 = 1 / (sqrt(2) * 2*pi * fc * C), R2 = 2 * R1
    """
    omega_c = 2.0 * math.pi * fc_hz
    # Choosing standard equal C: C1 = C2 = C
    # To get Q = 1/sqrt(2), R2 / R1 ratio is adjusted
    # Q = sqrt(R1*R2*C1*C2) / (C2*(R1+R2))
    # If C1 = C2: Q = sqrt(R1*R2) / (R1+R2) <= 0.5 (cannot get Butterworth with equal R and equal C!)
    # Standard choice: R1 = R2 = R, then C1 = 2*C2 for Q = 1/sqrt(2) = 0.707
    c2 = c2_farad
    c1 = 2.0 * c2
    r = 1.0 / (math.sqrt(2.0) * omega_c * c2)

    return {
        "cutoff_freq_hz": fc_hz,
        "resistor_r1_ohms": r,
        "resistor_r2_ohms": r,
        "capacitor_c1_farads": c1,
        "capacitor_c2_farads": c2,
        "q_factor": 0.7071
    }


def calculate_ne555_astable(freq_hz: float, duty_cycle_pct: float = 60.0, c_farad: float = 100e-9) -> Dict[str, float]:
    """
    Computes R1 and R2 for NE555 astable multivibrator.
    T_high = 0.693 * (R1 + R2) * C
    T_low  = 0.693 * R2 * C
    Frequency = 1.44 / ((R1 + 2*R2) * C)
    Duty Cycle = (R1 + R2) / (R1 + 2*R2) * 100% (must be > 50%)
    """
    assert duty_cycle_pct > 50.0, "Standard 555 astable duty cycle must be strictly greater than 50%"
    d = duty_cycle_pct / 100.0
    # Total resistance: R_total = (R1 + 2*R2) = 1.44 / (freq * C)
    r_total = 1.44 / (freq_hz * c_farad)
    # d = (R1 + R2) / R_total -> R1 + R2 = d * R_total
    # Since R_total = R1 + 2*R2: R2 = R_total - (R1 + R2) = R_total * (1 - d)
    r2 = r_total * (1.0 - d)
    r1 = r_total - 2.0 * r2

    return {
        "frequency_hz": freq_hz,
        "duty_cycle_pct": duty_cycle_pct,
        "resistor_r1_ohms": r1,
        "resistor_r2_ohms": r2,
        "capacitor_c_farads": c_farad,
        "t_high_ms": 0.693 * (r1 + r2) * c_farad * 1000.0,
        "t_low_ms": 0.693 * r2 * c_farad * 1000.0
    }


def calculate_wheatstone_bridge(v_supply: float, r_nominal: float, delta_r: float) -> Dict[str, float]:
    """
    Computes differential output voltage from a single-element active Wheatstone bridge:
    Delta V = V_supply * [ (R + delta_R)/(2*R + delta_R) - 0.5 ] ~ V_supply * (delta_R / (4*R))
    """
    r_active = r_nominal + delta_r
    v_out_exact = v_supply * ((r_active / (r_nominal + r_active)) - 0.5)
    v_out_linear_approx = v_supply * (delta_r / (4.0 * r_nominal))

    return {
        "v_supply_volts": v_supply,
        "r_nominal_ohms": r_nominal,
        "delta_r_ohms": delta_r,
        "v_out_exact_mv": v_out_exact * 1000.0,
        "v_out_approx_mv": v_out_linear_approx * 1000.0,
        "linearity_error_pct": abs(v_out_exact - v_out_linear_approx) / max(abs(v_out_exact), 1e-9) * 100.0
    }


def main():
    parser = argparse.ArgumentParser(description="Analog Circuit & Sensor Conditioning Calculator")
    parser.add_argument("--mode", type=str, default="sallen_key", choices=["sallen_key", "555", "bridge"])
    args = parser.parse_args()

    if args.mode == "sallen_key":
        res = calculate_sallen_key_lowpass(fc_hz=1000.0, c2_farad=10e-9)
        print("=== 2nd-Order Sallen-Key Butterworth Lowpass Filter (fc = 1 kHz) ===")
        print(f"R1 = R2 = {res['resistor_r1_ohms']:.1f} Ohms (Standard ~11.25 kOhm)")
        print(f"C1 = {res['capacitor_c1_farads']*1e9:.1f} nF | C2 = {res['capacitor_c2_farads']*1e9:.1f} nF")
    elif args.mode == "555":
        res = calculate_ne555_astable(freq_hz=1000.0, duty_cycle_pct=65.0, c_farad=100e-9)
        print("=== NE555 Astable Multivibrator (1 kHz, 65% Duty Cycle) ===")
        print(f"R1 = {res['resistor_r1_ohms']:.1f} Ohms | R2 = {res['resistor_r2_ohms']:.1f} Ohms")
        print(f"T_high = {res['t_high_ms']:.3f} ms | T_low = {res['t_low_ms']:.3f} ms")
    elif args.mode == "bridge":
        res = calculate_wheatstone_bridge(v_supply=5.0, r_nominal=350.0, delta_r=0.7)
        print("=== Wheatstone Bridge Strain Gauge Response (350 Ohm, delta_R = 0.7 Ohm) ===")
        print(f"Exact Differential Output: {res['v_out_exact_mv']:.4f} mV")
        print(f"Linear Approximation: {res['v_out_approx_mv']:.4f} mV (Linearity Error: {res['linearity_error_pct']:.4f}%)")


if __name__ == '__main__':
    main()
