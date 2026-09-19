import json
import tempfile
import unittest
from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO

from sim.run_experiments import ExperimentConfig, build_result, main, run_case


class RunExperimentsTests(unittest.TestCase):
    def test_deterministic_canonical_result(self):
        a = build_result(seed=7, quick=True)
        b = build_result(seed=7, quick=True)
        self.assertEqual(a["canonical_result_sha256"], b["canonical_result_sha256"])
        self.assertEqual(a["canonical_result"], b["canonical_result"])

    def test_overload_creates_queue(self):
        cfg = ExperimentConfig(ingress_gb_s=1000, interconnect_gb_s=10, chunks=12)
        rows = run_case(cfg)["records"]
        conventional = next(r for r in rows if r["variant"] == "conventional")
        self.assertTrue(conventional["transport_stall"])
        self.assertGreater(conventional["queue_delay_us"], 0)
        self.assertGreater(conventional["queue_depth_indicator"], 1)

    def test_output_shape_and_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            with redirect_stdout(StringIO()):
                self.assertEqual(main(["--reproduce-all", "--quick", "--seed", "9",
                                       "--output-dir", directory]), 0)
            result = json.loads((Path(directory) / "results-quick.json").read_text())
            self.assertTrue((Path(directory) / "REPORT-quick.md").exists())
        for key in ("schema_version", "run_timestamp_utc", "provenance",
                    "raw_records", "summary", "limitations", "canonical_result",
                    "inspectability"):
            self.assertIn(key, result)
        self.assertEqual(set(r["variant"] for r in result["raw_records"]),
                         {"conventional", "naive_partitioned", "prefetch_only", "strangler_adaptive"})

    def test_falsification_probes_are_present(self):
        report = build_result(seed=42, quick=True)["inspectability"]
        self.assertEqual(set(report["falsification_probes"]),
                         {"high_interconnect", "low_ingress_pressure",
                          "tiny_working_set", "no_reduction"})

    def test_qualitative_reduction_relationship(self):
        rows = run_case(ExperimentConfig(rho=0.01))["records"]
        conventional = next(r for r in rows if r["variant"] == "conventional")
        strangler = next(r for r in rows if r["variant"] == "strangler_adaptive")
        self.assertEqual(conventional["traffic_reduction_percent"], 0)
        self.assertGreater(strangler["traffic_reduction_percent"], 98)
        self.assertLess(strangler["boundary_bytes"], conventional["boundary_bytes"])


if __name__ == "__main__":
    unittest.main()
