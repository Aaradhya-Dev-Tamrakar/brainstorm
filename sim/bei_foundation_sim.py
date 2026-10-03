#!/usr/bin/env python3
"""
BEI Curriculum Deterministic Foundation Verification Harness
File: sim/bei_foundation_sim.py
Purpose: Deterministic verification of foundational mathematics, algorithms,
         control loops, DSP, scheduling, avionics, and economics derived from
         the 4-year BE ECIE / BEIE curriculum.
Standard: ARCH-RFC-001 Compliant (EMPIRICALLY_VERIFIED). Pure Python standard library.
"""

import cmath
import math
import queue
import sys
import threading
import time
from typing import Dict, List, Set, Tuple


# ==============================================================================
# Engine 1: Data Structures, Algorithms & Graph Traversal (CT 552)
# ==============================================================================
def verify_dsa_engine() -> bool:
    """Verifies Dijkstra shortest path and Topological Sort on a DAG."""
    # 1. Dijkstra Shortest Path
    graph = {
        'A': {'B': 4, 'C': 2},
        'B': {'A': 4, 'C': 1, 'D': 5},
        'C': {'A': 2, 'B': 1, 'D': 8, 'E': 10},
        'D': {'B': 5, 'C': 8, 'E': 2, 'Z': 6},
        'E': {'C': 10, 'D': 2, 'Z': 3},
        'Z': {'D': 6, 'E': 3}
    }
    
    distances = {node: float('inf') for node in graph}
    distances['A'] = 0
    unvisited = set(graph.keys())
    
    while unvisited:
        curr = min(unvisited, key=lambda n: distances[n])
        unvisited.remove(curr)
        for neighbor, weight in graph[curr].items():
            if distances[curr] + weight < distances[neighbor]:
                distances[neighbor] = distances[curr] + weight
                
    # Shortest path A -> Z: A(0) -> C(2) -> B(3) -> D(8) -> E(10) -> Z(13)
    # or A(0) -> C(2) -> B(3) -> D(8) -> Z(14) or A(0) -> C(2) -> E(12) -> Z(15)
    # Optimal: A(0)->C(2)->B(3)->D(8)->E(10)->Z(13)
    assert distances['Z'] == 13, f"Dijkstra failed: expected 13, got {distances['Z']}"

    # 2. Topological Sort (Kahn's Algorithm) on DAG
    dag = {
        'SH401': [],
        'SH451': ['SH401'],
        'SH501': ['SH451'],
        'EX509': ['SH501', 'EE401'],
        'EE401': [],
        'EX710': ['SH501'],
    }
    in_degree = {u: 0 for u in dag}
    for u in dag:
        for v in dag[u]:
            in_degree[u] += 1  # u depends on v
            
    # Standard dependency resolution: items with 0 dependencies first
    # Let graph: u -> v means u must precede v
    dep_graph = {'SH401': ['SH451'], 'EE401': ['EX509'], 'SH451': ['SH501'], 'SH501': ['EX509', 'EX710'], 'EX509': [], 'EX710': []}
    indeg = {n: 0 for n in dep_graph}
    for u in dep_graph:
        for v in dep_graph[u]:
            indeg[v] += 1
            
    q = [n for n in indeg if indeg[n] == 0]
    topo_order = []
    while q:
        curr = q.pop(0)
        topo_order.append(curr)
        for nxt in dep_graph[curr]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)
                
    assert len(topo_order) == len(dep_graph), "Topological sort failed: cycle detected"
    assert topo_order.index('SH401') < topo_order.index('SH501')
    assert topo_order.index('SH501') < topo_order.index('EX710')
    return True


# ==============================================================================
# Engine 2: Systems Concurrency & Thread Synchronization (CT 612)
# ==============================================================================
class BoundedBlockingRingBuffer:
    """Thread-safe bounded FIFO queue using Mutex & Condition Variables."""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.buffer = [None] * capacity
        self.head = 0
        self.tail = 0
        self.count = 0
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)

    def put(self, item):
        with self.not_full:
            while self.count == self.capacity:
                self.not_full.wait()
            self.buffer[self.tail] = item
            self.tail = (self.tail + 1) % self.capacity
            self.count += 1
            self.not_empty.notify()

    def get(self):
        with self.not_empty:
            while self.count == 0:
                self.not_empty.wait()
            item = self.buffer[self.head]
            self.head = (self.head + 1) % self.capacity
            self.count -= 1
            self.not_full.notify()
            return item


def verify_concurrency_engine() -> bool:
    """Verifies Producer-Consumer thread synchronization with zero loss or deadlock."""
    buf = BoundedBlockingRingBuffer(capacity=5)
    items_to_produce = 100
    produced = []
    consumed = []

    def producer():
        for i in range(items_to_produce):
            buf.put(i)
            produced.append(i)

    def consumer():
        for _ in range(items_to_produce):
            val = buf.get()
            consumed.append(val)

    t_prod = threading.Thread(target=producer)
    t_cons = threading.Thread(target=consumer)
    t_prod.start()
    t_cons.start()
    t_prod.join(timeout=2.0)
    t_cons.join(timeout=2.0)

    assert len(consumed) == items_to_produce, f"Lost items in queue: consumed {len(consumed)}"
    assert consumed == list(range(items_to_produce)), "Queue ordering violation"
    return True


# ==============================================================================
# Engine 3: Discrete Mathematics & Finite Automata (CT 551)
# ==============================================================================
class DeterministicFiniteAutomaton:
    """DFA validating binary strings ending with '01'."""
    def __init__(self):
        self.states = {'q0', 'q1', 'q2'}
        self.start_state = 'q0'
        self.accept_states = {'q2'}
        self.transitions = {
            ('q0', '0'): 'q1', ('q0', '1'): 'q0',
            ('q1', '0'): 'q1', ('q1', '1'): 'q2',
            ('q2', '0'): 'q1', ('q2', '1'): 'q0'
        }

    def accepts(self, s: str) -> bool:
        curr = self.start_state
        for char in s:
            if (curr, char) not in self.transitions:
                return False
            curr = self.transitions[(curr, char)]
        return curr in self.accept_states


def verify_discrete_math_engine() -> bool:
    """Verifies Boolean logic truth-tables and DFA state transitions."""
    # 1. Boolean Logic Invariant: De Morgan's Law: not(A and B) == (not A or not B)
    for a in [False, True]:
        for b in [False, True]:
            assert (not (a and b)) == ((not a) or (not b)), "De Morgan's failure"

    # 2. DFA Validation
    dfa = DeterministicFiniteAutomaton()
    assert dfa.accepts("01") is True
    assert dfa.accepts("1101") is True
    assert dfa.accepts("0001") is True
    assert dfa.accepts("1010") is False
    assert dfa.accepts("111") is False
    return True


# ==============================================================================
# Engine 4: Signal Processing & Numerical Mathematics (EX 710, SH 553)
# ==============================================================================
def dft(x: List[complex]) -> List[complex]:
    """Direct Discrete Fourier Transform O(N^2)."""
    N = len(x)
    X = []
    for k in range(N):
        s = 0.0 + 0.0j
        for n in range(N):
            angle = -2.0 * math.pi * k * n / N
            s += x[n] * cmath.exp(complex(0, angle))
        X.append(s)
    return X


def fft(x: List[complex]) -> List[complex]:
    """Radix-2 Decimation-in-Time Fast Fourier Transform O(N log N)."""
    N = len(x)
    if N <= 1:
        return x
    even = fft(x[0::2])
    odd = fft(x[1::2])
    T = [cmath.exp(complex(0, -2.0 * math.pi * k / N)) * odd[k] for k in range(N // 2)]
    return [even[k] + T[k] for k in range(N // 2)] + [even[k] - T[k] for k in range(N // 2)]


def rk4_step(f, t: float, y: float, dt: float) -> float:
    """4th-Order Runge-Kutta numerical integrator."""
    k1 = f(t, y)
    k2 = f(t + 0.5 * dt, y + 0.5 * dt * k1)
    k3 = f(t + 0.5 * dt, y + 0.5 * dt * k2)
    k4 = f(t + dt, y + dt * k3)
    return y + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def verify_dsp_and_numerical_engine() -> bool:
    """Verifies FFT vs DFT mathematical equivalence and RK4 ODE convergence."""
    # 1. FFT vs DFT equivalence test
    signal = [complex(math.sin(2.0 * math.pi * 0.125 * i) + 0.5 * math.cos(2.0 * math.pi * 0.25 * i), 0.0) for i in range(16)]
    dft_res = dft(signal)
    fft_res = fft(signal)
    
    max_err = 0.0
    for a, b in zip(dft_res, fft_res):
        err = abs(a - b)
        if err > max_err:
            max_err = err
    assert max_err < 1e-12, f"FFT/DFT discrepancy: {max_err}"

    # 2. RK4 ODE Solver test: dy/dt = -y, analytic solution: y(t) = y(0)*exp(-t)
    dt = 0.05
    t = 0.0
    y = 1.0
    for _ in range(20):  # simulate up to t = 1.0
        y = rk4_step(lambda t, val: -val, t, y, dt)
        t += dt
    expected = math.exp(-1.0)
    assert abs(y - expected) < 1e-6, f"RK4 error too large: expected {expected}, got {y}"
    return True


# ==============================================================================
# Engine 5: Dynamic Feedback Control & PID Tuning (EX 509)
# ==============================================================================
class ClosedLoopPIDSystem:
    """Discrete-time closed loop simulation of a 2nd-order plant with PID control."""
    def __init__(self, kp: float, ki: float, kd: float, dt: float):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.integral = 0.0
        self.prev_error = 0.0
        # Plant state: mass-spring-damper (y = position, v = velocity)
        self.pos = 0.0
        self.vel = 0.0
        self.m = 1.0
        self.b = 2.0  # damping
        self.k = 5.0  # spring constant

    def step(self, setpoint: float) -> float:
        error = setpoint - self.pos
        self.integral += error * self.dt
        derivative = (error - self.prev_error) / self.dt
        u = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.prev_error = error

        # Plant physics: m*a + b*v + k*x = u -> a = (u - b*v - k*x) / m
        acc = (u - self.b * self.vel - self.k * self.pos) / self.m
        self.vel += acc * self.dt
        self.pos += self.vel * self.dt
        return self.pos


def verify_control_engine() -> bool:
    """Verifies that closed-loop PID control converges to setpoint within 0.01 error."""
    sys_ctrl = ClosedLoopPIDSystem(kp=45.0, ki=25.0, kd=8.0, dt=0.01)
    setpoint = 1.0
    for _ in range(800):  # 8.0 seconds for complete integral settling
        final_pos = sys_ctrl.step(setpoint)
    assert abs(final_pos - setpoint) < 0.01, f"PID did not settle at setpoint: pos={final_pos}"
    return True


# ==============================================================================
# Engine 6: Project Management & CPM/PERT Scheduling (CT 658)
# ==============================================================================
def verify_project_management_cpm() -> bool:
    """Verifies Forward/Backward pass critical path calculation on activity network."""
    # Tasks: name -> (duration, predecessors)
    tasks = {
        'A': (3, []),
        'B': (4, ['A']),
        'C': (2, ['A']),
        'D': (5, ['B']),
        'E': (1, ['C']),
        'F': (2, ['D', 'E'])
    }
    
    # Forward Pass: Early Start (ES) & Early Finish (EF)
    es = {}
    ef = {}
    for task in ['A', 'B', 'C', 'D', 'E', 'F']:
        dur, preds = tasks[task]
        if not preds:
            es[task] = 0
        else:
            es[task] = max(ef[p] for p in preds)
        ef[task] = es[task] + dur
        
    total_project_duration = max(ef.values())
    assert total_project_duration == 14, f"Expected project duration 14, got {total_project_duration}"

    # Backward Pass: Late Finish (LF) & Late Start (LS)
    lf = {}
    ls = {}
    for task in reversed(['A', 'B', 'C', 'D', 'E', 'F']):
        dur, _ = tasks[task]
        successors = [t for t in tasks if task in tasks[t][1]]
        if not successors:
            lf[task] = total_project_duration
        else:
            lf[task] = min(ls[s] for s in successors)
        ls[task] = lf[task] - dur

    # Critical path tasks have Total Slack (LF - EF) == 0
    critical_path = [t for t in tasks if lf[t] - ef[t] == 0]
    expected_critical_path = ['A', 'B', 'D', 'F']
    assert critical_path == expected_critical_path, f"Critical path mismatch: got {critical_path}"
    return True


# ==============================================================================
# Engine 7: Aeronautical Telecommunications & Radar (EX 725 04)
# ==============================================================================
def radar_max_range(pt_watts: float, g_linear: float, wavelength_m: float, sigma_sqm: float, pmin_watts: float) -> float:
    """Calculates maximum radar detection range via standard Radar Range Equation."""
    # R_max = [ (Pt * G^2 * lambda^2 * sigma) / ((4*pi)^3 * Pmin) ]^(1/4)
    numerator = pt_watts * (g_linear ** 2) * (wavelength_m ** 2) * sigma_sqm
    denominator = ((4.0 * math.pi) ** 3) * pmin_watts
    return (numerator / denominator) ** 0.25


def multilateration_tdoa_2d(receivers: List[Tuple[float, float]], time_delays_sec: List[float], speed_of_light: float = 3e8) -> Tuple[float, float]:
    """Solves 2D target position (x, y) from 3 TDOA hyperbolic receiver stations."""
    # Target at known test coordinates (x=1000, y=2000)
    # R0 = (0, 0), R1 = (10000, 0), R2 = (0, 10000)
    # Gauss-Newton iterative solver
    x, y = 500.0, 500.0  # Initial guess
    r0_x, r0_y = receivers[0]
    
    for _ in range(25):
        # Calculate theoretical range differences relative to receiver 0: di = dist(P, Ri) - dist(P, R0)
        d0 = math.hypot(x - r0_x, y - r0_y)
        residuals = []
        J = []
        for i in range(1, len(receivers)):
            ri_x, ri_y = receivers[i]
            di = math.hypot(x - ri_x, y - ri_y)
            pred_diff = di - d0
            actual_diff = time_delays_sec[i] * speed_of_light
            residuals.append(actual_diff - pred_diff)
            
            # Partial derivatives
            j_x = (x - ri_x) / (di if di != 0 else 1.0) - (x - r0_x) / (d0 if d0 != 0 else 1.0)
            j_y = (y - ri_y) / (di if di != 0 else 1.0) - (y - r0_y) / (d0 if d0 != 0 else 1.0)
            J.append((j_x, j_y))
            
        # Normal equations: (J^T * J) * delta = J^T * r
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


def verify_aeronautical_telecom_engine() -> bool:
    """Verifies Radar Range calculations and Multilateration TDOA positioning."""
    # 1. Radar Equation Test: Pt=250kW, G=30dB (1000), freq=3GHz (lambda=0.1m), sigma=1m^2, Pmin=1e-12 W
    r_max = radar_max_range(pt_watts=250000.0, g_linear=1000.0, wavelength_m=0.1, sigma_sqm=1.0, pmin_watts=1e-12)
    assert 25000 < r_max < 100000, f"Radar range out of expected physical bounds: {r_max} meters"

    # 2. Multilateration TDOA Test
    c = 3e8
    receivers = [(0.0, 0.0), (10000.0, 0.0), (0.0, 10000.0)]
    target_true = (3000.0, 4000.0)
    d0 = math.hypot(target_true[0] - receivers[0][0], target_true[1] - receivers[0][1])
    time_delays = [0.0]
    for i in range(1, len(receivers)):
        di = math.hypot(target_true[0] - receivers[i][0], target_true[1] - receivers[i][1])
        time_delays.append((di - d0) / c)

    est_x, est_y = multilateration_tdoa_2d(receivers, time_delays, c)
    assert abs(est_x - target_true[0]) < 1.0, f"TDOA x-position error: est={est_x}, true={target_true[0]}"
    assert abs(est_y - target_true[1]) < 1.0, f"TDOA y-position error: est={est_y}, true={target_true[1]}"
    return True


# ==============================================================================
# Engine 8: Engineering Economics & Earned Value Management (CE 615)
# ==============================================================================
def net_present_value(discount_rate: float, initial_investment: float, cash_flows: List[float]) -> float:
    """Computes Net Present Value (NPV) for a series of future cash flows."""
    npv = -initial_investment
    for t, cf in enumerate(cash_flows, 1):
        npv += cf / ((1.0 + discount_rate) ** t)
    return npv


def earned_value_metrics(pv: float, ev: float, ac: float) -> Dict[str, float]:
    """Computes Earned Value Management (EVM) variance and performance indices."""
    cv = ev - ac  # Cost Variance
    sv = ev - pv  # Schedule Variance
    cpi = ev / ac if ac != 0 else 1.0
    spi = ev / pv if pv != 0 else 1.0
    return {'CV': cv, 'SV': sv, 'CPI': cpi, 'SPI': spi}


def verify_economics_engine() -> bool:
    """Verifies NPV discounted cash flow and EVM project health metrics."""
    # 1. NPV: Invest 100k, return 35k each year for 4 years at 10% discount rate
    npv_val = net_present_value(discount_rate=0.10, initial_investment=100000.0, cash_flows=[35000.0, 35000.0, 35000.0, 35000.0])
    # Analytical: 35000 * [ (1 - (1.1)^-4) / 0.10 ] = 35000 * 3.169865 = 110,945.3 -> NPV = +10,945.30
    assert 10900 < npv_val < 11000, f"NPV calculation error: got {npv_val}"

    # 2. EVM metrics: Planned=50k, Earned=45k, Actual=40k -> Under budget (good), Behind schedule
    evm = earned_value_metrics(pv=50000.0, ev=45000.0, ac=40000.0)
    assert evm['CV'] == 5000.0, "Cost variance mismatch"
    assert evm['SV'] == -5000.0, "Schedule variance mismatch"
    assert evm['CPI'] == 1.125, "Cost performance index mismatch"
    assert evm['SPI'] == 0.90, "Schedule performance index mismatch"
    return True


# ==============================================================================
# Master Test Runner
# ==============================================================================
def run_all_foundation_verifications():
    print("=" * 70)
    print("BE ECIE / BEIE Deterministic Foundation Verification Harness")
    print("=" * 70)
    
    engines = [
        ("Engine 1: DSA & Graph Traversal (CT 552)", verify_dsa_engine),
        ("Engine 2: Systems Concurrency & Ring Buffer (CT 612)", verify_concurrency_engine),
        ("Engine 3: Discrete Mathematics & Automata (CT 551)", verify_discrete_math_engine),
        ("Engine 4: DSP & Numerical Mathematics (EX 710, SH 553)", verify_dsp_and_numerical_engine),
        ("Engine 5: Dynamic Feedback Control & PID (EX 509)", verify_control_engine),
        ("Engine 6: Project Management & CPM/PERT (CT 658)", verify_project_management_cpm),
        ("Engine 7: Aeronautical Telecommunications & Radar (EX 725 04)", verify_aeronautical_telecom_engine),
        ("Engine 8: Engineering Economics & EVM (CE 615)", verify_economics_engine),
    ]

    all_passed = True
    start_time = time.perf_counter()
    for name, test_fn in engines:
        try:
            res = test_fn()
            print(f" [PASS] {name}")
        except Exception as e:
            print(f" [FAIL] {name}: {str(e)}")
            all_passed = False

    elapsed = time.perf_counter() - start_time
    print("-" * 70)
    if all_passed:
        print(f"STATUS: ZERO DISCREPANCIES - All 8 BEI Foundation Engines Passed in {elapsed*1000:.2f}ms")
        print("=" * 70)
        sys.exit(0)
    else:
        print("STATUS: VERIFICATION FAILED - Discrepancies detected")
        print("=" * 70)
        sys.exit(1)


if __name__ == '__main__':
    run_all_foundation_verifications()
