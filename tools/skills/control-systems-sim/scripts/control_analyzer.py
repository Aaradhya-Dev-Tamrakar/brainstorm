#!/usr/bin/env python3
"""
Dynamic Feedback Control Loop & Stability Analyzer
File: tools/skills/control-systems-sim/scripts/control_analyzer.py
Purpose: Evaluates 2nd-order transfer functions, computes time-domain metrics
         (rise time, overshoot, settling time), and simulates closed-loop PID control.
Standard: Pure Python standard library (no external numpy/scipy required).
"""

import argparse
import math
import sys
from typing import Dict, List, Tuple


def analyze_second_order_system(wn: float, zeta: float) -> Dict[str, float]:
    """
    Computes analytical characteristics of standard 2nd-order transfer function:
    T(s) = wn^2 / (s^2 + 2*zeta*wn*s + wn^2)
    """
    metrics = {
        "natural_frequency_rad_s": wn,
        "damping_ratio": zeta,
        "damped_frequency_rad_s": wn * math.sqrt(max(0.0, 1.0 - zeta**2)) if zeta < 1.0 else 0.0,
    }
    
    if zeta < 1.0:  # Underdamped
        # Peak Overshoot Mp = exp(-pi * zeta / sqrt(1 - zeta^2)) * 100%
        mp = math.exp(-math.pi * zeta / math.sqrt(1.0 - zeta**2)) * 100.0
        # Peak Time tp = pi / wd
        wd = metrics["damped_frequency_rad_s"]
        tp = math.pi / wd if wd > 0 else 0.0
        # Settling Time (2% criterion) ts ~ 4 / (zeta * wn)
        ts = 4.0 / (zeta * wn) if (zeta * wn) > 0 else 0.0
        # Rise Time tr ~ (pi - beta) / wd where beta = atan(sqrt(1-zeta^2)/zeta)
        beta = math.atan(math.sqrt(1.0 - zeta**2) / max(zeta, 1e-6))
        tr = (math.pi - beta) / wd if wd > 0 else 0.0

        metrics["type"] = "Underdamped (zeta < 1.0)"
        metrics["max_overshoot_pct"] = mp
        metrics["peak_time_s"] = tp
        metrics["settling_time_2pct_s"] = ts
        metrics["rise_time_s"] = tr
    elif abs(zeta - 1.0) < 1e-4:
        metrics["type"] = "Critically Damped (zeta == 1.0)"
        metrics["max_overshoot_pct"] = 0.0
        metrics["settling_time_2pct_s"] = 5.83 / wn
    else:
        metrics["type"] = "Overdamped (zeta > 1.0)"
        metrics["max_overshoot_pct"] = 0.0
        s1 = -zeta * wn + wn * math.sqrt(zeta**2 - 1.0)
        metrics["settling_time_2pct_s"] = 4.0 / abs(s1)

    return metrics


def simulate_pid_step_response(kp: float, ki: float, kd: float, wn: float, zeta: float, dt: float = 0.005, duration: float = 4.0) -> Tuple[List[float], List[float]]:
    """
    Simulates closed-loop PID control of the plant:
    d^2y/dt^2 + 2*zeta*wn*(dy/dt) + wn^2*y = wn^2 * u(t)
    """
    num_steps = int(duration / dt)
    time_series = []
    output_series = []

    pos = 0.0
    vel = 0.0
    integral = 0.0
    prev_error = 0.0
    setpoint = 1.0

    for step in range(num_steps):
        t = step * dt
        error = setpoint - pos
        integral += error * dt
        derivative = (error - prev_error) / dt if step > 0 else 0.0
        
        # PID control effort
        u = kp * error + ki * integral + kd * derivative
        prev_error = error

        # Plant dynamics: acc = wn^2 * u - 2*zeta*wn*vel - wn^2*pos
        acc = (wn**2) * u - 2.0 * zeta * wn * vel - (wn**2) * pos
        vel += acc * dt
        pos += vel * dt

        time_series.append(t)
        output_series.append(pos)

    return time_series, output_series


def main():
    parser = argparse.ArgumentParser(description="Control Systems Second-Order & PID Analyzer")
    parser.add_argument("--wn", type=float, default=5.0, help="Natural frequency omega_n (rad/s)")
    parser.add_argument("--zeta", type=float, default=0.6, help="Damping ratio zeta")
    parser.add_argument("--kp", type=float, default=2.0, help="PID Proportional gain")
    parser.add_argument("--ki", type=float, default=1.0, help="PID Integral gain")
    parser.add_argument("--kd", type=float, default=0.2, help="PID Derivative gain")
    args = parser.parse_args()

    print(f"=== Open-Loop Plant Analysis (wn = {args.wn} rad/s, zeta = {args.zeta}) ===")
    m = analyze_second_order_system(args.wn, args.zeta)
    for k, v in m.items():
        if isinstance(v, float):
            print(f"  {k:28s}: {v:8.4f}")
        else:
            print(f"  {k:28s}: {v}")

    print(f"\n=== Closed-Loop PID Step Response Simulation (Kp={args.kp}, Ki={args.ki}, Kd={args.kd}) ===")
    t_series, y_series = simulate_pid_step_response(args.kp, args.ki, args.kd, args.wn, args.zeta)
    
    # Sample prints at t=0.5, 1.0, 2.0, 4.0
    sample_indices = [int(len(t_series) * frac) - 1 for frac in [0.125, 0.25, 0.5, 1.0]]
    for idx in sample_indices:
        print(f"  t = {t_series[idx]:.2f}s -> Output y(t) = {y_series[idx]:.4f} (Error = {1.0 - y_series[idx]:+.4f})")


if __name__ == '__main__':
    main()
