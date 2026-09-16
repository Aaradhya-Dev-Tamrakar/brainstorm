"""
Warehouse Logistics Memory Simulator (Lightweight GPU-to-DRAM Discrete Event Model)
-----------------------------------------------------------------------------------
Demonstrates the exact penalty of uncoalesced memory access and the benefit of
Smart Dynamic Coalescing (v+1) and Near-Memory Reduction (v+2).

The row-buffer hit rate is calculated over row-buffer accesses
(`row_hits + row_misses`).  For v+2, those accesses are the internal DRAM
stream, while `total_bursts` remains the single scalar transaction sent over
the external bus.

Zero dependencies. Zero analog headache. Pure algorithmic systems logic.
"""

from dataclasses import dataclass
import argparse
import json
from pathlib import Path
from typing import List
import random

# JEDEC DDR4/DDR5 standard representative timing cycles (at memory controller clock)
BURST_SIZE_BYTES = 64     # 1 DRAM burst = 64 bytes (cache line)
BYTES_PER_ELEMENT = 4     # 32-bit float = 4 bytes
t_CAS = 14                # Column Access Strobe (Row Hit latency: ~14 cycles)
t_RCD = 14                # Row Address to Column Address Delay
t_RP = 14                 # Row Precharge delay (Closing old row: ~14 cycles)
ROW_MISS_LATENCY = t_RP + t_RCD + t_CAS  # ~42 cycles
ROW_HIT_LATENCY = t_CAS                  # ~14 cycles
ROW_SIZE_BYTES = 4096                    # 4KB DRAM Page/Row buffer


@dataclass
class SimulationStats:
    mode: str
    total_bursts: int
    row_hits: int
    row_misses: int
    total_latency_cycles: int
    bytes_transferred: int

    @property
    def row_buffer_accesses(self) -> int:
        return self.row_hits + self.row_misses

    @property
    def row_buffer_hit_rate(self) -> float:
        return self.row_hits / max(1, self.row_buffer_accesses)

    def as_dict(self) -> dict:
        return {
            "mode": self.mode,
            "total_bursts": self.total_bursts,
            "row_hits": self.row_hits,
            "row_misses": self.row_misses,
            "row_buffer_accesses": self.row_buffer_accesses,
            "row_buffer_hit_rate": self.row_buffer_hit_rate,
            "total_latency_cycles": self.total_latency_cycles,
            "bytes_transferred": self.bytes_transferred,
        }

    def print_summary(self):
        hit_rate = self.row_buffer_hit_rate * 100
        print(f"\n[{self.mode.upper()}]")
        print(f"  |-- Bus Bursts Dispatched : {self.total_bursts} transactions")
        print(f"  |-- Data Moved Over Bus   : {self.bytes_transferred} bytes")
        print(f"  |-- Row-Buffer Hit Rate   : {hit_rate:.1f}% ({self.row_hits} hits, {self.row_misses} misses)")
        print(f"  +-- Total Memory Latency  : {self.total_latency_cycles} cycles")


def run_baseline_uncoalesced(thread_addresses: List[int]) -> SimulationStats:
    """
    Baseline (Naive): Every thread's request is dispatched independently
    without grouping or reordering.
    """
    current_open_row = -1
    total_cycles = 0
    row_hits = 0
    row_misses = 0
    total_bursts = len(thread_addresses)
    
    for addr in thread_addresses:
        row_id = addr // ROW_SIZE_BYTES
        if row_id == current_open_row:
            row_hits += 1
            total_cycles += ROW_HIT_LATENCY
        else:
            row_misses += 1
            total_cycles += ROW_MISS_LATENCY
            current_open_row = row_id
            
    return SimulationStats(
        mode="Baseline (Naive / Uncoalesced)",
        total_bursts=total_bursts,
        row_hits=row_hits,
        row_misses=row_misses,
        total_latency_cycles=total_cycles,
        bytes_transferred=total_bursts * BURST_SIZE_BYTES
    )


def run_upgrade_v1_smart_coalescer(thread_addresses: List[int]) -> SimulationStats:
    """
    Upgrade v+1: Smart Coalescer & Bank-Aware Schedular
    1. Deduplicates memory requests within the same 64-byte burst.
    2. Clusters bursts by DRAM Row buffer before dispatching to the bus.
    """
    burst_line_indices = sorted(list(set(addr // BURST_SIZE_BYTES for addr in thread_addresses)))
    
    current_open_row = -1
    total_cycles = 0
    row_hits = 0
    row_misses = 0
    total_bursts = len(burst_line_indices)
    
    for line_idx in burst_line_indices:
        byte_addr = line_idx * BURST_SIZE_BYTES
        row_id = byte_addr // ROW_SIZE_BYTES
        if row_id == current_open_row:
            row_hits += 1
            total_cycles += ROW_HIT_LATENCY
        else:
            row_misses += 1
            total_cycles += ROW_MISS_LATENCY
            current_open_row = row_id
            
    return SimulationStats(
        mode="Upgrade v+1 (Smart Coalescer & Reordering)",
        total_bursts=total_bursts,
        row_hits=row_hits,
        row_misses=row_misses,
        total_latency_cycles=total_cycles,
        bytes_transferred=total_bursts * BURST_SIZE_BYTES
    )


def run_upgrade_v2_near_memory_reduction(vector_size_elements: int) -> SimulationStats:
    """
    Upgrade v+2: Near-Memory Streaming Accumulator
    Instead of hauling 4096 elements across the bus for Softmax/LayerNorm sum,
    the memory controller streams the row locally and transmits only the final scalar.
    """
    total_bytes = vector_size_elements * BYTES_PER_ELEMENT
    dram_bursts_internal = (total_bytes + BURST_SIZE_BYTES - 1) // BURST_SIZE_BYTES
    
    # Internal DRAM read cycles (row hit streaming)
    internal_cycles = (dram_bursts_internal - 1) * ROW_HIT_LATENCY + ROW_MISS_LATENCY
    
    # Only ONE 4-byte scalar result travels back across the physical bus!
    bus_bursts = 1
    bytes_on_bus = 4
    
    return SimulationStats(
        mode="Upgrade v+2 (Near-Memory Reduction)",
        total_bursts=bus_bursts,
        row_hits=dram_bursts_internal - 1,
        row_misses=1,
        total_latency_cycles=internal_cycles,
        bytes_transferred=bytes_on_bus
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run the warehouse memory simulator.")
    parser.add_argument(
        "--json-output",
        type=Path,
        metavar="PATH",
        help="also write deterministic baseline/v1/v2 metrics as JSON",
    )
    args = parser.parse_args(argv)

    print("=" * 70)
    print("WAREHOUSE LOGISTICS GPU-TO-DRAM SIMULATOR (Brainstorm Spec)")
    print("=" * 70)

    # Scenario: 32 GPU threads in a warp accessing scattered KV-cache entries
    # e.g., Attention lookup across irregular attention pointers
    random.seed(42)
    base_ptr = 0x100000
    
    # 32 threads picking elements from scattered memory regions
    scattered_addresses = [
        base_ptr + (random.randint(0, 100) * 128) + (i % 4) * 4
        for i in range(32)
    ]

    print("\nSimulating Warp Memory Request (32 threads, scattered KV-cache pointers)...")
    baseline = run_baseline_uncoalesced(scattered_addresses)
    v1 = run_upgrade_v1_smart_coalescer(scattered_addresses)

    baseline.print_summary()
    v1.print_summary()

    speedup = baseline.total_latency_cycles / v1.total_latency_cycles
    bus_saving = ((baseline.bytes_transferred - v1.bytes_transferred) / baseline.bytes_transferred) * 100
    print(f"\n>> v+1 Performance Gain: {speedup:.2f}x Speedup | {bus_saving:.1f}% Less Bus Data Moved")

    print("\n" + "-" * 70)
    print("Simulating Attention Softmax Reduction (Vector Dimension N = 4096 elements)...")
    v2 = run_upgrade_v2_near_memory_reduction(4096)
    v2.print_summary()

    traffic_reduction = ((4096 * 4 - v2.bytes_transferred) / (4096 * 4)) * 100
    print(f">> v+2 Bus Traffic Reclaimed: {traffic_reduction:.3f}% reduction on physical interconnect!")
    print("=" * 70)

    if args.json_output:
        results = {
            "baseline": baseline.as_dict(),
            "v1": v1.as_dict(),
            "v2": v2.as_dict(),
            "derived": {
                "v1_speedup": speedup,
                "v1_bus_traffic_reduction_percent": bus_saving,
                "v2_boundary_traffic_reduction_percent": traffic_reduction,
            },
        }
        args.json_output.write_text(
            json.dumps(results, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
