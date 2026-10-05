"""Unit and Invariant Test Suite for Dynamic MoE & Cascade Routing Engine.

Grounded in ARCH-RFC-001 (Epistemic Records) and ARCH-RFC-002 (Cognitive Council).
Executed automatically by sim/reconciliation_engine.py as Layer 2 Behavioral Verification.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

# Ensure brainstorm root is in sys.path for direct execution
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from sim.routing_engine import (
        ComplexityAnalyzer,
        ModelRouter,
        TaskRequirements,
        cascade_task,
        get_router,
        route_task,
    )
except ImportError:
    from routing_engine import (
        ComplexityAnalyzer,
        ModelRouter,
        TaskRequirements,
        cascade_task,
        get_router,
        route_task,
    )


class TestRoutingEngine(unittest.TestCase):
    """Behavioral and Invariant test cases for 2026 Model Router."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.router = get_router()

    def test_01_catalog_loading_and_counts(self) -> None:
        """Verify that the model registry loads all 25 models with valid schemas."""
        self.assertEqual(len(self.router.models), 25, "Registry must contain exactly 25 models.")
        
        # Verify critical 2026 frontier IDs are present
        critical_ids = [
            "claude-opus-5-5",
            "claude-sonnet-5-5",
            "gpt-6-astra",
            "gpt-6-1-sol",
            "gemini-4-argon",
            "gemini-3-8-flash",
            "gemini-3-5-flash-lite",
            "deepseek-v4-pro",
            "deepseek-v4-1-flash",
            "grok-4-7",
            "qwen3-6-35b-a3b",
        ]
        for cid in critical_ids:
            model = self.router.get_model(cid)
            self.assertIsNotNone(model, f"Critical 2026 frontier model '{cid}' missing from registry.")
            self.assertGreater(model.context_window, 0)
            self.assertIsNotNone(model.latency_tier)
            self.assertIsNotNone(model.cascade_role)

    def test_02_complexity_analyzer_calibration(self) -> None:
        """Verify heuristic complexity calibration across task archetypes."""
        # Simple micro-tasks (Expected 1.0 - 4.0)
        triage_score = ComplexityAnalyzer.evaluate("extract json from api response and parse regex table", input_tokens=500)
        self.assertLessEqual(triage_score, 4.0, f"Simple triage scored too high: {triage_score}")

        # Mid-tier refactoring tasks (Expected 4.0 - 7.5)
        refactor_score = ComplexityAnalyzer.evaluate("refactor python class with unit tests and clean imports", input_tokens=2500)
        self.assertTrue(4.0 <= refactor_score <= 7.5, f"Refactor scored out of bounds: {refactor_score}")

        # High-tier formal reasoning (Expected 8.0 - 10.0)
        formal_score = ComplexityAnalyzer.evaluate("formal proof of z3 smt solver invariants for kernel memory allocator deadlock", input_tokens=15000)
        self.assertGreaterEqual(formal_score, 8.0, f"Formal verification scored too low: {formal_score}")

    def test_03_micro_triage_routing(self) -> None:
        """Verify simple tasks route to ultra-fast low-cost triage models."""
        task = TaskRequirements(
            description="extract json keys and format regex pattern",
            estimated_input_tokens=800,
            estimated_output_tokens=200,
            preferred_latency="ultra_fast",
        )
        res = self.router.route(task)
        self.assertIn(
            res.primary_model.id,
            ["gemini-3-5-flash-lite", "gpt-6-luna", "gemini-3-8-flash", "smollm2-1-7b"],
            f"Expected ultra-fast triage model, got {res.primary_model.id}"
        )
        self.assertLessEqual(res.estimated_cost_usd, 0.001, "Triage cost should be sub-mil ($0.001).")

    def test_04_systems_code_refactoring_routing(self) -> None:
        """Verify code engineering tasks route to Tier 1 worker specialists."""
        task = TaskRequirements(
            description="refactor AST architecture in multi-file python repository",
            domain="ast_code_refactoring",
            estimated_input_tokens=8000,
            estimated_output_tokens=3000,
        )
        res = self.router.route(task)
        self.assertIn(
            res.primary_model.id,
            ["claude-sonnet-5-5", "gpt-6-1-sol", "qwen3-8-max", "deepseek-v4-1-flash"],
            f"Expected elite code worker, got {res.primary_model.id}"
        )
        self.assertEqual(res.primary_model.cascade_role, "tier_1_worker")

    def test_05_frontier_formal_reasoning_routing(self) -> None:
        """Verify extreme complexity tasks route to Tier 3 Escalation models."""
        task = TaskRequirements(
            description="formal proof of z3 smt solver invariants for distributed concurrency deadlock",
            estimated_input_tokens=15000,
            estimated_output_tokens=5000,
            explicit_complexity=9.5,
        )
        res = self.router.route(task)
        self.assertIn(
            res.primary_model.id,
            ["claude-opus-5-5", "gpt-6-astra", "deepseek-v4-pro", "deepseek-r1"],
            f"Expected frontier escalation model, got {res.primary_model.id}"
        )
        self.assertEqual(res.primary_model.cascade_role, "tier_3_escalation")

    def test_06_massive_context_ingestion_routing(self) -> None:
        """Verify tasks requiring >1M tokens strictly resolve to Gemini 4 Argon."""
        task = TaskRequirements(
            description="ingest and synthesize 1.4 million token research library and 4-hour audio lectures",
            min_context=1_400_000,
            estimated_input_tokens=1_400_000,
            estimated_output_tokens=16000,
        )
        res = self.router.route(task)
        self.assertEqual(res.primary_model.id, "gemini-4-argon", "Only Gemini 4 Argon supports 2M tokens context.")
        self.assertEqual(res.primary_model.context_window, 2_000_000)

    def test_07_local_workstation_constraint_enforcement(self) -> None:
        """Verify local_only tasks with 24GB VRAM ceiling reject cloud models."""
        task = TaskRequirements(
            description="run offline code refactoring on local developer desktop",
            local_only=True,
            max_vram_gb=24.0,
            estimated_input_tokens=4000,
            estimated_output_tokens=1000,
        )
        res = self.router.route(task)
        self.assertTrue(res.primary_model.local_runnable, "Chosen model must be locally runnable.")
        self.assertIn(
            res.primary_model.id,
            ["qwen-3-6-35b-a3b", "qwen-2-5-coder-32b", "phi-4", "smollm2-1-7b"],
            f"Expected 24GB-compatible local model, got {res.primary_model.id}"
        )
        vram = res.primary_model.vram_q4_gb or res.primary_model.vram_fp16_gb or 0.0
        self.assertLessEqual(vram, 24.0, f"Model VRAM {vram}GB exceeds 24GB ceiling.")

    def test_08_budget_ceiling_enforcement(self) -> None:
        """Verify strict price ceilings reject expensive frontier models."""
        task = TaskRequirements(
            description="analyze large log files with tight budget constraints",
            max_cost_per_m=0.30,
            estimated_input_tokens=5000,
            estimated_output_tokens=1000,
        )
        res = self.router.route(task)
        self.assertLessEqual(
            res.primary_model.input_cost_per_m,
            0.30,
            f"Input cost ${res.primary_model.input_cost_per_m}/M exceeds $0.30 ceiling."
        )

    def test_09_frugal_cascade_savings(self) -> None:
        """Verify FrugalGPT cascade achieves >60% cost reduction vs unconditional Opus 5.5."""
        plan = cascade_task("extract json keys and classify sentiment from user feedback stream")
        self.assertGreaterEqual(
            plan.savings_pct,
            60.0,
            f"Expected at least 60% savings on simple tasks, got {plan.savings_pct}%"
        )
        self.assertEqual(len(plan.stages), 4, "Cascade must contain 4 tiers.")
        self.assertEqual(plan.recommended_entry_tier, 0, "Simple task must enter at Tier 0 triage.")

    def test_10_cognitive_council_role_allocation(self) -> None:
        """Verify resolution of ARCH-RFC-002 Cognitive Council roles."""
        craftsmen = self.router.get_by_council_role("Craftsman")
        self.assertTrue(any("claude" in m.id for m in craftsmen), "Claude must fulfill Code Craftsman role.")

        skeptics = self.router.get_by_council_role("Skeptic")
        self.assertTrue(any("gpt-6" in m.id or "deepseek-r1" in m.id for m in skeptics), "GPT-6/DeepSeek must fulfill Skeptic role.")

        synthesizers = self.router.get_by_council_role("Synthesizer")
        self.assertTrue(any("gemini" in m.id for m in synthesizers), "Gemini must fulfill Synthesizer role.")

        provocateurs = self.router.get_by_council_role("Provocateur")
        self.assertTrue(any("grok" in m.id for m in provocateurs), "Grok must fulfill First-Principles Provocateur role.")


if __name__ == "__main__":
    unittest.main()
