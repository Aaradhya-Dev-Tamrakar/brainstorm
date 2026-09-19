"""Deterministic regression checks for the warehouse memory simulator."""

import random
import json
import unittest
from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO

from sim.warehouse_mem_sim import (
    main,
    run_baseline_uncoalesced,
    run_upgrade_v1_smart_coalescer,
    run_upgrade_v2_near_memory_reduction,
)


class WarehouseMemorySimulatorTests(unittest.TestCase):
    def test_documented_v1_boundary_result(self):
        random.seed(42)
        base_ptr = 0x100000
        addresses = [
            base_ptr + (random.randint(0, 100) * 128) + (i % 4) * 4
            for i in range(32)
        ]

        baseline = run_baseline_uncoalesced(addresses)
        v1 = run_upgrade_v1_smart_coalescer(addresses)

        self.assertEqual((baseline.total_latency_cycles, v1.total_latency_cycles), (980, 434))
        self.assertAlmostEqual(
            baseline.total_latency_cycles / v1.total_latency_cycles, 2.26, places=2
        )
        self.assertAlmostEqual(baseline.row_buffer_hit_rate * 100, 40.625, places=3)
        self.assertAlmostEqual(v1.row_buffer_hit_rate * 100, 88.0, places=3)

    def test_v2_hit_rate_uses_internal_row_accesses(self):
        v2 = run_upgrade_v2_near_memory_reduction(4096)

        self.assertEqual(v2.total_bursts, 1)
        self.assertEqual(v2.row_buffer_accesses, 256)
        self.assertEqual((v2.row_hits, v2.row_misses), (255, 1))
        self.assertAlmostEqual(v2.row_buffer_hit_rate * 100, 99.609375, places=6)
        self.assertAlmostEqual((1 - 4 / (4096 * 4)) * 100, 99.976, places=3)

    def test_json_output_contains_deterministic_metrics(self):
        output_path = Path(__file__).with_name(".warehouse_mem_sim_test.json")
        try:
            stdout = StringIO()
            with redirect_stdout(stdout):
                main(["--json-output", str(output_path)])

            result = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(result["baseline"]["total_latency_cycles"], 980)
            self.assertEqual(result["v1"]["total_latency_cycles"], 434)
            self.assertEqual(result["v2"]["row_buffer_accesses"], 256)
            self.assertAlmostEqual(result["derived"]["v1_speedup"], 980 / 434)
            self.assertAlmostEqual(
                result["derived"]["v2_boundary_traffic_reduction_percent"], 99.976, places=3
            )
            self.assertIn("WAREHOUSE LOGISTICS", stdout.getvalue())
        finally:
            output_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
