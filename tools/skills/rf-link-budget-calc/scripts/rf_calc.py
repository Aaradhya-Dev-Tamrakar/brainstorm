#!/usr/bin/env python3
"""
RF Transmission Line & Wireless Link Budget Calculator
File: tools/skills/rf-link-budget-calc/scripts/rf_calc.py
Purpose: Computes Friis free-space path loss, transmission line reflection coefficients,
         VSWR, and receiver link margins.
Standard: Pure Python standard library (no external numpy/scipy required).
"""

import argparse
import cmath
import math
import sys
from typing import Dict


def calculate_free_space_path_loss(freq_mhz: float, dist_km: float) -> float:
    """
    Computes Free Space Path Loss (FSPL) in dB.
    FSPL (dB) = 20*log10(d) + 20*log10(f) + 32.44
    (d in km, f in MHz)
    """
    return 20.0 * math.log10(max(dist_km, 1e-4)) + 20.0 * math.log10(max(freq_mhz, 1e-3)) + 32.44


def calculate_link_budget(pt_dbm: float, tx_gain_dbi: float, rx_gain_dbi: float, freq_mhz: float, dist_km: float, rx_sens_dbm: float, cable_loss_db: float = 2.0) -> Dict[str, float]:
    """
    Computes complete end-to-end RF link budget and link margin (dB).
    """
    fspl_db = calculate_free_space_path_loss(freq_mhz, dist_km)
    eirp_dbm = pt_dbm + tx_gain_dbi - cable_loss_db
    pr_dbm = eirp_dbm - fspl_db + rx_gain_dbi - cable_loss_db
    margin_db = pr_dbm - rx_sens_dbm

    return {
        "transmit_power_dbm": pt_dbm,
        "eirp_dbm": eirp_dbm,
        "path_loss_db": fspl_db,
        "received_power_dbm": pr_dbm,
        "receiver_sensitivity_dbm": rx_sens_dbm,
        "link_margin_db": margin_db,
        "link_viable": margin_db >= 0.0
    }


def calculate_vswr_and_reflection(z_load_real: float, z_load_imag: float, z0: float = 50.0) -> Dict[str, float]:
    """
    Computes transmission line reflection coefficient Gamma, return loss (dB), and VSWR.
    """
    zl = complex(z_load_real, z_load_imag)
    gamma = (zl - z0) / (zl + z0)
    gamma_mag = abs(gamma)
    
    if gamma_mag >= 1.0:
        vswr = float('inf')
        return_loss_db = 0.0
    else:
        vswr = (1.0 + gamma_mag) / (1.0 - gamma_mag)
        return_loss_db = -20.0 * math.log10(max(gamma_mag, 1e-6))

    return {
        "gamma_magnitude": gamma_mag,
        "gamma_angle_deg": math.degrees(cmath.phase(gamma)),
        "vswr": vswr,
        "return_loss_db": return_loss_db
    }


def main():
    parser = argparse.ArgumentParser(description="RF & Wireless Link Budget Calculator")
    parser.add_argument("--freq_mhz", type=float, default=2400.0, help="Carrier frequency in MHz (e.g. 2400 for 2.4 GHz)")
    parser.add_argument("--dist_km", type=float, default=5.0, help="Line-of-sight distance in km")
    parser.add_argument("--pt_dbm", type=float, default=20.0, help="Transmitter power in dBm (100mW)")
    parser.add_argument("--gtx_dbi", type=float, default=14.0, help="Transmit antenna gain in dBi")
    parser.add_argument("--grx_dbi", type=float, default=14.0, help="Receive antenna gain in dBi")
    parser.add_argument("--rx_sens", type=float, default=-85.0, help="Receiver sensitivity in dBm")
    args = parser.parse_args()

    lb = calculate_link_budget(args.pt_dbm, args.gtx_dbi, args.grx_dbi, args.freq_mhz, args.dist_km, args.rx_sens)
    print("=== RF Wireless Link Budget Summary ===")
    print(f"Frequency: {args.freq_mhz:.1f} MHz | Distance: {args.dist_km:.2f} km")
    print(f"EIRP: {lb['eirp_dbm']:.2f} dBm")
    print(f"Free Space Path Loss: {lb['path_loss_db']:.2f} dB")
    print(f"Received Power (Pr): {lb['received_power_dbm']:.2f} dBm")
    print(f"Receiver Sensitivity: {lb['receiver_sensitivity_dbm']:.2f} dBm")
    print(f"Link Margin: {lb['link_margin_db']:+.2f} dB [{'VIABLE / HEALTHY' if lb['link_margin_db'] >= 10.0 else 'MARGINAL' if lb['link_margin_db'] >= 0.0 else 'FAILED'}]")

    print("\n=== Sample Transmission Line Reflection Check (Z_load = 75 + j25 ohm against 50 ohm line) ===")
    vswr_res = calculate_vswr_and_reflection(75.0, 25.0, 50.0)
    print(f"Reflection Coefficient |Gamma|: {vswr_res['gamma_magnitude']:.4f} at {vswr_res['gamma_angle_deg']:.1f} deg")
    print(f"VSWR: {vswr_res['vswr']:.2f} : 1")
    print(f"Return Loss: {vswr_res['return_loss_db']:.2f} dB")


if __name__ == '__main__':
    main()
