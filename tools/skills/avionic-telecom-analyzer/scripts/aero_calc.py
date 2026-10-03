#!/usr/bin/env python3
"""
Aeronautical Telecommunication & Navigation System Calculator
File: tools/skills/avionic-telecom-analyzer/scripts/aero_calc.py
Purpose: Computes Radar Range Equations, solves Multilateration TDOA positioning,
         and calculates VOR/DME/ILS geometries.
Standard: Pure Python standard library (no external numpy/scipy required).
"""

import argparse
import math
import sys
from typing import List, Tuple


def calculate_radar_range(pt_kw: float, freq_ghz: float, gain_db: float, rcs_sqm: float, pmin_dbm: float) -> float:
    """
    Computes maximum radar detection range R_max (km).
    Pt: Peak transmit power (kW)
    freq: Carrier frequency (GHz)
    gain_db: Antenna gain (dB)
    rcs_sqm: Radar Cross Section sigma (m^2)
    pmin_dbm: Minimum detectable signal (dBm)
    """
    c = 3e8
    wavelength = c / (freq_ghz * 1e9)
    pt_watts = pt_kw * 1000.0
    g_linear = 10.0 ** (gain_db / 10.0)
    pmin_watts = (10.0 ** (pmin_dbm / 10.0)) / 1000.0

    numerator = pt_watts * (g_linear ** 2) * (wavelength ** 2) * rcs_sqm
    denominator = ((4.0 * math.pi) ** 3) * pmin_watts
    r_max_meters = (numerator / denominator) ** 0.25
    return r_max_meters / 1000.0  # Return in km


def solve_tdoa_2d(receivers: List[Tuple[float, float]], time_delays_microsec: List[float]) -> Tuple[float, float]:
    """
    Solves 2D target position (x, y) in meters from 3 TDOA receiver stations.
    time_delays_microsec: delays of Station 1 and 2 relative to Station 0.
    """
    c = 3e8  # m/s
    time_delays_sec = [t * 1e-6 for t in time_delays_microsec]
    r0_x, r0_y = receivers[0]
    
    # Gauss-Newton solver starting at centroid
    x = sum(r[0] for r in receivers) / len(receivers)
    y = sum(r[1] for r in receivers) / len(receivers)

    for _ in range(50):
        d0 = math.hypot(x - r0_x, y - r0_y)
        residuals = []
        J = []
        for i in range(1, len(receivers)):
            ri_x, ri_y = receivers[i]
            di = math.hypot(x - ri_x, y - ri_y)
            pred_diff = di - d0
            actual_diff = time_delays_sec[i] * c
            residuals.append(actual_diff - pred_diff)

            j_x = (x - ri_x) / max(di, 1e-6) - (x - r0_x) / max(d0, 1e-6)
            j_y = (y - ri_y) / max(di, 1e-6) - (y - r0_y) / max(d0, 1e-6)
            J.append((j_x, j_y))

        # (J^T * J) * delta = J^T * r
        j00 = sum(row[0] * row[0] for row in J)
        j01 = sum(row[0] * row[1] for row in J)
        j11 = sum(row[1] * row[1] for row in J)
        det = j00 * j11 - j01 * j01
        if abs(det) < 1e-12:
            break

        rhs0 = sum(J[i][0] * residuals[i] for i in range(len(residuals)))
        rhs1 = sum(J[i][1] * residuals[i] for i in range(len(residuals)))
        dx = (j11 * rhs0 - j01 * rhs1) / det
        dy = (j00 * rhs1 - j01 * rhs0) / det
        x += dx
        y += dy
        if math.hypot(dx, dy) < 1e-3:
            break

    return x, y


def calculate_ils_glide_slope(alt_ft: float, dist_nm: float) -> float:
    """Computes vertical glide slope angle in degrees from altitude (ft) and DME distance (nautical miles)."""
    dist_meters = dist_nm * 1852.0
    alt_meters = alt_ft * 0.3048
    angle_rad = math.atan2(alt_meters, dist_meters)
    return math.degrees(angle_rad)


def main():
    parser = argparse.ArgumentParser(description="Aeronautical Telecom & Radar Calculator")
    parser.add_argument("--mode", type=str, default="radar", choices=["radar", "ils", "tdoa"])
    parser.add_argument("--pt_kw", type=float, default=250.0, help="Peak radar power (kW)")
    parser.add_argument("--freq_ghz", type=float, default=3.0, help="Carrier frequency (GHz)")
    parser.add_argument("--gain_db", type=float, default=30.0, help="Antenna gain (dB)")
    parser.add_argument("--rcs", type=float, default=1.0, help="Target RCS (m^2)")
    parser.add_argument("--pmin_dbm", type=float, default=-90.0, help="Receiver sensitivity (dBm)")
    args = parser.parse_args()

    if args.mode == "radar":
        r_km = calculate_radar_range(args.pt_kw, args.freq_ghz, args.gain_db, args.rcs, args.pmin_dbm)
        print(f"=== Primary Radar Maximum Range ===")
        print(f"Transmit Power: {args.pt_kw} kW | Freq: {args.freq_ghz} GHz | Gain: {args.gain_db} dB")
        print(f"Target RCS: {args.rcs} m^2 | Sensitivity: {args.pmin_dbm} dBm")
        print(f"-> Maximum Detection Range: {r_km:.2f} km ({r_km * 0.539957:.2f} Nautical Miles)")
    elif args.mode == "ils":
        slope = calculate_ils_glide_slope(alt_ft=1500.0, dist_nm=4.7)
        print(f"=== ILS Glide Slope Angle ===")
        print(f"Altitude: 1500 ft | Distance: 4.7 NM -> Glide Slope: {slope:.2f} degrees (Standard: ~3.0 deg)")
    elif args.mode == "tdoa":
        stations = [(0.0, 0.0), (12000.0, 0.0), (0.0, 12000.0)]
        target_x, target_y = solve_tdoa_2d(stations, [0.0, 5.0, 8.0])
        print(f"=== Multilateration TDOA 2D Fix ===")
        print(f"Estimated Coordinates: X = {target_x:.2f} m, Y = {target_y:.2f} m")


if __name__ == '__main__':
    main()
