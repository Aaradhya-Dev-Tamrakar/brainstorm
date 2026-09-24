"""
test_invariant_engine.py
------------------------
Deterministic behavioral regression tests for the Headless Invariant Assurance Engine (INV-BMK-001).
Discovered dynamically by sim/reconciliation_engine.py Layer 2 verification gate.
"""

import unittest
from sim.invariant_engine.benchmark_runner import run_benchmark, build_benchmark_testbed
from sim.invariant_engine.smt_encoder import SMTInvariantProver
from sim.invariant_engine.sandbox_replay import SandboxReplayEngine
from sim.invariant_engine.contract_types import InvariantClassification


class InvariantAssuranceEngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = build_benchmark_testbed()
        cls.prover = SMTInvariantProver(timeout_ms=1000)
        cls.replay = SandboxReplayEngine()

    def test_planted_bug_discovery_recall_is_100_percent(self):
        """Verifies that 100% of planted violations in synthetic state machines produce counterexamples."""
        planted_cases = [c for c in self.cases if c["prop"].classification == InvariantClassification.PLANTED_VIOLATION]
        self.assertGreaterEqual(len(planted_cases), 4)

        for case in planted_cases:
            res = self.prover.verify_property(case["machine"], case["prop"], case["actions"], case["sym_pred"])
            self.assertEqual(
                res.status,
                "COUNTEREXAMPLE_FOUND",
                f"Failed to discover planted violation for {case['prop'].property_id}"
            )
            self.assertIsNotNone(res.counterexample)

    def test_counterexample_replay_confirmed_in_sandbox(self):
        """Verifies that SMT counterexamples trigger actual runtime contract violations when executed in sandbox."""
        planted_cases = [c for c in self.cases if c["prop"].classification == InvariantClassification.PLANTED_VIOLATION]

        for case in planted_cases:
            v_res = self.prover.verify_property(case["machine"], case["prop"], case["actions"], case["sym_pred"])
            r_res = self.replay.replay_counterexample(case["machine"], v_res, case["runtime_pred"])
            self.assertEqual(
                r_res.status,
                "REPLAY_CONFIRMED",
                f"Counterexample for {case['prop'].property_id} failed sandbox confirmation"
            )
            self.assertTrue(r_res.violation_observed)

    def test_valid_invariants_proved_with_zero_false_discoveries(self):
        """Verifies that all true invariants hold inductively with 0% false discovery rate."""
        valid_cases = [c for c in self.cases if c["prop"].classification == InvariantClassification.VALID_INVARIANT]
        self.assertGreaterEqual(len(valid_cases), 6)

        for case in valid_cases:
            res = self.prover.verify_property(case["machine"], case["prop"], case["actions"], case["sym_pred"])
            self.assertEqual(
                res.status,
                "PROVED_INVARIANT",
                f"Valid invariant {case['prop'].property_id} was falsely flagged"
            )

    def test_vacuous_tautology_and_contradiction_negative_controls(self):
        """Verifies that vacuous tautologies and contradictory specifications are flagged and rejected."""
        vacuous_case = next(c for c in self.cases if c["prop"].classification == InvariantClassification.VACUOUS_TAUTOLOGY)
        v_res = self.prover.verify_property(vacuous_case["machine"], vacuous_case["prop"], vacuous_case["actions"], vacuous_case["sym_pred"])
        self.assertEqual(v_res.status, "VACUOUS_REJECTED")

        contra_case = next(c for c in self.cases if c["prop"].classification == InvariantClassification.CONTRADICTORY_SPEC)
        c_res = self.prover.verify_property(contra_case["machine"], contra_case["prop"], contra_case["actions"], contra_case["sym_pred"])
        self.assertEqual(c_res.status, "CONTRADICTION_REJECTED")

    def test_full_benchmark_execution_and_dossier_generation(self):
        """Executes full benchmark suite and asserts deterministic record metrics."""
        record = run_benchmark()
        self.assertEqual(record.discovery_recall_pct, 100.0)
        self.assertEqual(record.counterexample_validity_pct, 100.0)
        self.assertEqual(record.false_discovery_rate_pct, 0.0)
        self.assertEqual(record.total_properties_evaluated, 12)
        self.assertLess(record.mean_solver_latency_ms, 50.0)


if __name__ == "__main__":
    unittest.main()
