"""Interactive CLI & Query Tool for 2026 Dynamic MoE & Cascade Router.

Provides command-line task triage, complexity scoring, multi-constraint model selection,
and FrugalGPT 4-tier cascade planning for developer workflows.

Usage:
  python tools/route_task.py "extract regex from 200 json files"
  python tools/route_task.py "refactor AST architecture in compiler" --cascade
  python tools/route_task.py "offline code generation" --local --vram 24.0
  python tools/route_task.py "verify distributed consensus proofs" --budget 10.0 --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Add repository root to path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sim.routing_engine import (
    ModelRouter,
    TaskRequirements,
    get_router,
)


def format_currency(amount: float) -> str:
    if amount < 0.0001:
        return f"${amount * 1000:.3f}m"  # in millidollars
    elif amount < 0.01:
        return f"${amount:.5f}"
    return f"${amount:.4f}"


def run_cli() -> None:
    parser = argparse.ArgumentParser(
        description="2026 Dynamic MoE & Cascade Model Router (Brainstorm Ecosystem)"
    )
    parser.add_argument("task", nargs="?", default="", help="Task prompt or description to route")
    parser.add_argument("-t", "--task-text", dest="task_alt", default=None, help="Explicit task description")
    parser.add_argument("--tokens-in", type=int, default=1000, help="Estimated input tokens (default: 1000)")
    parser.add_argument("--tokens-out", type=int, default=500, help="Estimated output tokens (default: 500)")
    parser.add_argument("--tokens-cached", type=int, default=0, help="Estimated cached input tokens (default: 0)")
    parser.add_argument("--budget", type=float, default=None, help="Max input price per 1M tokens ($)")
    parser.add_argument("--latency", choices=["ultra_fast", "fast", "standard", "slow_cot"], default=None, help="Preferred latency tier")
    parser.add_argument("--domain", type=str, default=None, help="Domain affinity hint (e.g. ast_code_refactoring, math_reasoning)")
    parser.add_argument("--local", action="store_true", help="Constrain to locally runnable open-weight models")
    parser.add_argument("--vram", type=float, default=24.0, help="Max local GPU VRAM in GB (default: 24.0)")
    parser.add_argument("--cascade", action="store_true", help="Generate full 4-tier FrugalGPT cascade execution plan")
    parser.add_argument("--council", type=str, default=None, help="Filter by ARCH-RFC-002 Cognitive Council role")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    args = parser.parse_args()
    description = args.task_alt or args.task

    if not description:
        parser.print_help()
        sys.exit(1)

    req = TaskRequirements(
        description=description,
        estimated_input_tokens=args.tokens_in,
        estimated_output_tokens=args.tokens_out,
        cached_tokens=args.tokens_cached,
        max_cost_per_m=args.budget,
        preferred_latency=args.latency,
        domain=args.domain,
        local_only=args.local,
        max_vram_gb=args.vram if args.local else None,
        council_role=args.council,
    )

    router = get_router()

    if args.cascade:
        plan = router.build_cascade(req)
        if args.json:
            out = {
                "task": plan.task_description,
                "complexity": plan.complexity_score,
                "recommended_entry_tier": plan.recommended_entry_tier,
                "guidance": plan.execution_guidance,
                "savings_pct": plan.savings_pct,
                "composite_expected_cost_usd": plan.composite_expected_cost_usd,
                "worst_case_cost_usd": plan.worst_case_cost_usd,
                "unrouted_sota_cost_usd": plan.unrouted_sota_cost_usd,
                "stages": [
                    {
                        "stage_name": s.stage_name,
                        "tier": s.tier_level,
                        "model_id": s.model.id,
                        "model_name": s.model.name,
                        "exit_probability": s.exit_probability,
                        "stage_cost_usd": s.estimated_stage_cost_usd,
                    }
                    for s in plan.stages
                ],
            }
            print(json.dumps(out, indent=2))
            return

        print("\n" + "=" * 78)
        print("  2026 DYNAMIC MOE CASCADE EXECUTION PLAN (FrugalGPT Architecture)")
        print("=" * 78)
        print(f"Task Description  : {plan.task_description}")
        print(f"Assigned Score    : {plan.complexity_score} / 10.0")
        print(f"Recommended Entry : Tier {plan.recommended_entry_tier}")
        print(f"Execution Guidance: {plan.execution_guidance}")
        print("-" * 78)
        print(f"{'Stage':<18} | {'Model':<22} | {'Exit Prob':<10} | {'Stage Cost':<12}")
        print("-" * 78)
        for s in plan.stages:
            star = " (Entry)" if s.tier_level == plan.recommended_entry_tier else ""
            print(f"{s.stage_name:<18} | {s.model.name + star:<22} | {s.exit_probability * 100:5.1f}%    | {format_currency(s.estimated_stage_cost_usd):<12}")
        print("-" * 78)
        print(f"Composite Expected Cost : {format_currency(plan.composite_expected_cost_usd)}")
        print(f"Worst-Case Cascade Cost : {format_currency(plan.worst_case_cost_usd)}")
        print(f"Unrouted SOTA Baseline  : {format_currency(plan.unrouted_sota_cost_usd)} (Claude Opus 5.5)")
        print(f"Expected Cost Savings   : {plan.savings_pct:.1f}%")
        print("=" * 78 + "\n")
        return

    # Direct single-model routing
    res = router.route(req)

    if args.json:
        out = {
            "task": description,
            "assigned_complexity": res.assigned_complexity,
            "primary_model": {
                "id": res.primary_model.id,
                "name": res.primary_model.name,
                "provider": res.primary_model.provider,
                "tier": res.primary_model.tier,
                "context_window": res.primary_model.context_window,
                "latency_tier": res.primary_model.latency_tier,
                "cascade_role": res.primary_model.cascade_role,
                "council_role": res.primary_model.cognitive_council_role,
            },
            "alternative_model": {
                "id": res.alternative_model.id,
                "name": res.alternative_model.name,
            } if res.alternative_model else None,
            "estimated_cost_usd": res.estimated_cost_usd,
            "candidate_pool_size": res.candidate_pool_size,
            "rejected_count": res.rejected_count,
            "rationale": res.rationale,
        }
        print(json.dumps(out, indent=2))
        return

    print("\n" + "=" * 78)
    print("  2026 DYNAMIC MOE ROUTING DECISION")
    print("=" * 78)
    print(f"Task Description  : {description}")
    print(f"Tokens (In/Out)   : {args.tokens_in:,} / {args.tokens_out:,}")
    print(f"Assigned Score    : {res.assigned_complexity} / 10.0")
    print("-" * 78)
    print(f"Recommended Model : {res.primary_model.name} ({res.primary_model.id})")
    print(f"Provider & Tier   : {res.primary_model.provider} | {res.primary_model.tier}")
    print(f"Latency & Role    : {res.primary_model.latency_tier} | {res.primary_model.cascade_role}")
    if res.primary_model.cognitive_council_role:
        print(f"Cognitive Council : {res.primary_model.cognitive_council_role}")
    print(f"Estimated Cost    : {format_currency(res.estimated_cost_usd)} (Input: ${res.primary_model.input_cost_per_m}/M)")
    if res.alternative_model:
        print(f"Fallback Model    : {res.alternative_model.name} ({res.alternative_model.id})")
    print("-" * 78)
    print("Decision Rationale:")
    for r in res.rationale:
        print(f"  * {r}")
    print(f"Candidates Audited: {res.candidate_pool_size} evaluated ({res.rejected_count} filtered by constraints)")
    print("=" * 78 + "\n")


if __name__ == "__main__":
    run_cli()
