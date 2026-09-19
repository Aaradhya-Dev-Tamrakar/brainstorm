"""Regression test for the checked-in canonical STRANGLER-IPU output."""

import json
import unittest
from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO

from sim.warehouse_mem_sim import main


class ReproducibilityTests(unittest.TestCase):
    def test_canonical_output_matches_simulator(self):
        output = Path(__file__).with_name(".reproducibility.json")
        try:
            with redirect_stdout(StringIO()):
                main(["--json-output", str(output)])
            actual = json.loads(output.read_text(encoding="utf-8"))
            expected = json.loads(
                (Path(__file__).with_name("results") / "latest.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(actual, expected)
        finally:
            output.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
