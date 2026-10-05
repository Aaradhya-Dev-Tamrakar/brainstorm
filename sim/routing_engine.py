"""Dynamic Mixture-of-Experts (MoE) & Cascade Routing Engine.

Grounded in ARCH-RFC-001 (Epistemic Records) and ARCH-RFC-002 (Cognitive Council).
Consumes authoritative October 2026 telemetry from research/datasets/llm_models.yaml
to provide deterministic, multi-constraint task routing and FrugalGPT-style cascades.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import yaml

# Path resolution for repository root and dataset
BRAINSTORM_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATASET_PATH = BRAINSTORM_ROOT / "research" / "datasets" / "llm_models.yaml"


@dataclass
class ModelEntry:
    """Strongly typed representation of a 2026 LLM catalog record."""
    id: str
    name: str
    provider: str
    family: str
    tier: str
    release_date: str
    context_window: int
    output_limit: int
    open_weights: bool
    api_available: bool
    local_runnable: bool
    vram_q4_gb: Optional[float]
    vram_fp16_gb: Optional[float]
    input_cost_per_m: float
    output_cost_per_m: float
    cached_input_per_m: float
    free_tier: bool
    swe_bench_verified: Optional[float]
    math_500: Optional[float]
    arena_elo: Optional[int]
    capabilities: Dict[str, bool]
    complexity_range: Tuple[int, int]
    best_domains: List[str]
    avoid_domains: List[str]
    cascade_role: str
    latency_tier: str
    tool_calling_reliability: float
    instruction_drift_threshold_k: int
    cache_discount_pct: int
    cognitive_council_role: Optional[str]
    raw_data: Dict[str, Any] = field(repr=False, default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ModelEntry:
        arch = data.get("architecture", {})
        access = data.get("access", {})
        pricing = data.get("pricing", {})
        bench = data.get("benchmarks", {})
        caps = data.get("capabilities", {})
        rp = data.get("routing_profile", {})

        cr = rp.get("complexity_range", [1, 10])
        complexity_range = (int(cr[0]), int(cr[1])) if len(cr) >= 2 else (1, 10)

        return cls(
            id=data["id"],
            name=data.get("name", data["id"]),
            provider=data.get("provider", "Unknown"),
            family=data.get("family", "Unknown"),
            tier=data.get("tier", "unknown"),
            release_date=data.get("release_date", ""),
            context_window=int(arch.get("context_window") or 32000),
            output_limit=int(arch.get("output_limit") or 4096),
            open_weights=bool(access.get("open_weights", False)),
            api_available=bool(access.get("api_available", True)),
            local_runnable=bool(access.get("local_runnable", False)),
            vram_q4_gb=float(access["vram_q4_gb"]) if access.get("vram_q4_gb") is not None else None,
            vram_fp16_gb=float(access["vram_fp16_gb"]) if access.get("vram_fp16_gb") is not None else None,
            input_cost_per_m=float(pricing.get("input_per_m") or 0.0),
            output_cost_per_m=float(pricing.get("output_per_m") or 0.0),
            cached_input_per_m=float(pricing.get("cached_input_per_m") or 0.0),
            free_tier=bool(pricing.get("free_tier", False)),
            swe_bench_verified=float(bench["swe_bench_verified"]) if bench.get("swe_bench_verified") is not None else None,
            math_500=float(bench["math_500"]) if bench.get("math_500") is not None else None,
            arena_elo=int(bench["arena_elo"]) if bench.get("arena_elo") is not None else None,
            capabilities=caps,
            complexity_range=complexity_range,
            best_domains=rp.get("best_domains", []),
            avoid_domains=rp.get("avoid_domains", []),
            cascade_role=rp.get("cascade_role", "tier_1_worker"),
            latency_tier=rp.get("latency_tier", "standard"),
            tool_calling_reliability=float(rp.get("tool_calling_reliability", 0.90)),
            instruction_drift_threshold_k=int(rp.get("instruction_drift_threshold_k", 32)),
            cache_discount_pct=int(rp.get("cache_discount_pct", 0)),
            cognitive_council_role=rp.get("cognitive_council_role"),
            raw_data=data,
        )

    def calculate_cost(self, input_tokens: int, output_tokens: int, cached_tokens: int = 0) -> float:
        """Calculate total dollar cost for given token volumes."""
        uncached_input = max(0, input_tokens - cached_tokens)
        cost = (uncached_input / 1_000_000.0) * self.input_cost_per_m
        cost += (cached_tokens / 1_000_000.0) * self.cached_input_per_m
        cost += (output_tokens / 1_000_000.0) * self.output_cost_per_m
        return cost


@dataclass
class TaskRequirements:
    """Requirements and constraints for an agentic or user task."""
    description: str
    estimated_input_tokens: int = 1000
    estimated_output_tokens: int = 500
    cached_tokens: int = 0
    min_context: Optional[int] = None
    max_cost_per_m: Optional[float] = None
    max_total_cost: Optional[float] = None
    preferred_latency: Optional[str] = None  # 'ultra_fast', 'fast', 'standard', 'slow_cot'
    required_capabilities: List[str] = field(default_factory=list)
    domain: Optional[str] = None
    local_only: bool = False
    prefer_api: bool = True
    max_vram_gb: Optional[float] = None
    council_role: Optional[str] = None
    explicit_complexity: Optional[float] = None


@dataclass
class RoutingResult:
    """Outcome of model routing evaluation."""
    primary_model: ModelEntry
    alternative_model: Optional[ModelEntry]
    assigned_complexity: float
    estimated_cost_usd: float
    latency_tier: str
    rationale: List[str]
    candidate_pool_size: int
    rejected_count: int


@dataclass
class CascadeStage:
    """Single stage in a multi-model cascade pipeline."""
    stage_name: str
    tier_level: int
    model: ModelEntry
    description: str
    exit_probability: float
    estimated_stage_cost_usd: float


@dataclass
class CascadePlan:
    """Full 4-tier FrugalGPT execution cascade."""
    task_description: str
    complexity_score: float
    stages: List[CascadeStage]
    composite_expected_cost_usd: float
    worst_case_cost_usd: float
    unrouted_sota_cost_usd: float
    savings_pct: float
    recommended_entry_tier: int
    execution_guidance: str


class ComplexityAnalyzer:
    """Heuristic task complexity classifier calibrating tasks on a 1.0 to 10.0 scale."""

    LOW_COMPLEXITY_TRIGGERS = [
        r"\bregex\b", r"\bextract\b", r"\bjson\b", r"\btriage\b", r"\bformat\b",
        r"\bspell check\b", r"\bsummarize briefly\b", r"\bclassify\b", r"\btag\b",
        r"\bsort\b", r"\bparse table\b", r"\bgrammar\b", r"\bsimple\b"
    ]

    MODERATE_COMPLEXITY_TRIGGERS = [
        r"\brefactor\b", r"\bunit test\b", r"\bdebug\b", r"\bexplain\b",
        r"\boptimize\b", r"\bdraft\b", r"\bscript\b", r"\bapi\b",
        r"\bconvert\b", r"\bclean\b", r"\banalyze\b"
    ]

    HIGH_COMPLEXITY_TRIGGERS = [
        r"\bformal proof\b", r"\bsmt solver\b", r"\bz3\b", r"\bkernel\b",
        r"\bdeadlock\b", r"\bconcurrency\b", r"\bdistributed\b", r"\bcompiler\b",
        r"\barchitect\b", r"\bsecurity audit\b", r"\bzero-day\b", r"\bswe-bench\b",
        r"\bhumanity's last exam\b", r"\bmemory leak\b", r"\bntfs acl\b", r"\basynchronous\b"
    ]

    @classmethod
    def evaluate(cls, description: str, input_tokens: int = 1000) -> float:
        text = description.lower()
        score = 5.0  # Default neutral midpoint

        # 1. Token volume heuristic
        if input_tokens < 1000:
            score -= 1.0
        elif input_tokens > 200_000:
            score += 2.5
        elif input_tokens > 50_000:
            score += 1.5
        elif input_tokens > 10_000:
            score += 0.5

        # 2. Keyword trigger evaluation
        low_hits = sum(1 for p in cls.LOW_COMPLEXITY_TRIGGERS if re.search(p, text))
        mod_hits = sum(1 for p in cls.MODERATE_COMPLEXITY_TRIGGERS if re.search(p, text))
        high_hits = sum(1 for p in cls.HIGH_COMPLEXITY_TRIGGERS if re.search(p, text))

        score -= min(3.0, low_hits * 1.2)
        score += min(2.0, mod_hits * 0.5)
        score += min(4.5, high_hits * 1.8)

        # 3. Code density heuristic
        code_markers = ["def ", "class ", "fn ", "impl ", "SELECT ", "import ", "template<", "void ", "#include"]
        if any(marker in description for marker in code_markers):
            score += 0.8

        return max(1.0, min(10.0, round(score, 1)))


class ModelRouter:
    """Authoritative Dynamic MoE & Cascade Router for the Brainstorm Ecosystem."""

    def __init__(self, dataset_path: Optional[Union[str, Path]] = None) -> None:
        self.dataset_path = Path(dataset_path or DEFAULT_DATASET_PATH)
        if not self.dataset_path.exists():
            raise FileNotFoundError(f"LLM dataset not found at: {self.dataset_path}")

        self.models: List[ModelEntry] = []
        self._load_dataset()

    def _load_dataset(self) -> None:
        with open(self.dataset_path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)

        raw_models = raw.get("models", [])
        self.models = [ModelEntry.from_dict(m) for m in raw_models]
        if not self.models:
            raise ValueError(f"No models found in dataset {self.dataset_path}")

    def get_model(self, model_id: str) -> Optional[ModelEntry]:
        """Lookup model entry by exact ID."""
        for m in self.models:
            if m.id == model_id:
                return m
        return None

    def get_by_council_role(self, role_keyword: str) -> List[ModelEntry]:
        """Find models fulfilling a specific ARCH-RFC-002 Cognitive Council role."""
        kw = role_keyword.lower()
        matches = []
        for m in self.models:
            if m.cognitive_council_role and kw in m.cognitive_council_role.lower():
                matches.append(m)
        return matches

    def filter_candidates(self, req: TaskRequirements) -> Tuple[List[ModelEntry], List[str]]:
        """Filter out models that violate hard operational constraints."""
        candidates = []
        reasons = []
        needed_context = max(
            req.min_context or 0,
            req.estimated_input_tokens + req.estimated_output_tokens
        )

        for m in self.models:
            # 1. Context window check
            if m.context_window < needed_context:
                continue

            # 2. Output limit check
            if m.output_limit < req.estimated_output_tokens:
                continue

            # 3. Local-only constraint
            if req.local_only and not m.local_runnable:
                continue

            # 4. VRAM ceiling check (for local workstations)
            if req.local_only and req.max_vram_gb is not None:
                model_vram = m.vram_q4_gb or m.vram_fp16_gb
                if model_vram is not None and model_vram > req.max_vram_gb:
                    continue

            # 5. Cost ceiling constraints
            if req.max_cost_per_m is not None and m.input_cost_per_m > req.max_cost_per_m:
                continue

            if req.max_total_cost is not None:
                est_cost = m.calculate_cost(req.estimated_input_tokens, req.estimated_output_tokens, req.cached_tokens)
                if est_cost > req.max_total_cost:
                    continue

            # 6. Required capabilities check
            missing_cap = False
            for cap in req.required_capabilities:
                if not m.capabilities.get(cap, False):
                    missing_cap = True
                    break
            if missing_cap:
                continue

            candidates.append(m)

        return candidates, reasons

    def score_model(self, model: ModelEntry, req: TaskRequirements, complexity: float) -> Tuple[float, List[str]]:
        """Calculate alignment score for a model given task complexity and preferences."""
        score = 100.0
        rationale = []

        # 1. Complexity fit (Gaussian-like penalty for mismatch)
        min_c, max_c = model.complexity_range
        if min_c <= complexity <= max_c:
            score += 35.0
            rationale.append(f"Complexity {complexity} is within optimal range [{min_c}, {max_c}].")
        elif complexity < min_c:
            penalty = (min_c - complexity) * 15.0
            score -= penalty
            rationale.append(f"Model overpowered for complexity {complexity} (min: {min_c}, penalty: -{penalty:.1f}).")
        else:
            penalty = (complexity - max_c) * 25.0  # Underpowered penalty is heavier
            score -= penalty
            rationale.append(f"Model underpowered for complexity {complexity} (max: {max_c}, penalty: -{penalty:.1f}).")

        # 2. Domain alignment
        if req.domain:
            norm_domain = req.domain.lower()
            if any(norm_domain in d.lower() or d.lower() in norm_domain for d in model.best_domains):
                score += 30.0
                rationale.append(f"Specialized domain match for '{req.domain}'.")
            if any(norm_domain in d.lower() or d.lower() in norm_domain for d in model.avoid_domains):
                score -= 50.0
                rationale.append(f"Domain '{req.domain}' is flagged in avoid_domains.")

        # 3. Latency tier alignment
        if req.preferred_latency:
            if model.latency_tier == req.preferred_latency:
                score += 25.0
                rationale.append(f"Exact latency tier match: '{model.latency_tier}'.")
            elif req.preferred_latency == "ultra_fast" and model.latency_tier != "ultra_fast":
                score -= 30.0

        # 4. Cognitive Council alignment
        if req.council_role and model.cognitive_council_role:
            if req.council_role.lower() in model.cognitive_council_role.lower():
                score += 35.0
                rationale.append(f"Direct match for Cognitive Council role: '{model.cognitive_council_role}'.")

        # 5. Cloud API vs Local Workstation preference
        if not req.local_only and req.prefer_api and model.api_available:
            score += 15.0
        elif req.local_only and model.local_runnable:
            score += 20.0

        # 6. Cost efficiency incentive (reward cheaper models when complexity is low)
        if complexity <= 5.0 and model.input_cost_per_m > 0:
            cost_factor = min(20.0, 1.0 / (model.input_cost_per_m + 0.05))
            score += cost_factor

        # 7. Benchmark strength bonus for high complexity
        if complexity >= 7.0 and model.swe_bench_verified:
            score += (model.swe_bench_verified - 70.0) * 0.5

        return score, rationale

    def route(self, task: Union[str, TaskRequirements]) -> RoutingResult:
        """Deterministically route a task to the optimal primary model and fallback."""
        if isinstance(task, str):
            req = TaskRequirements(description=task)
        else:
            req = task

        complexity = req.explicit_complexity or ComplexityAnalyzer.evaluate(
            req.description,
            req.estimated_input_tokens
        )

        candidates, filter_notes = self.filter_candidates(req)
        if not candidates:
            # Fallback relaxation: try without budget/latency caps
            relaxed_req = TaskRequirements(
                description=req.description,
                estimated_input_tokens=req.estimated_input_tokens,
                estimated_output_tokens=req.estimated_output_tokens,
                min_context=req.min_context,
                local_only=req.local_only,
                max_vram_gb=req.max_vram_gb,
            )
            candidates, _ = self.filter_candidates(relaxed_req)

        if not candidates:
            # Ultimate safety fallback: pick highest capacity models in catalog
            candidates = sorted(self.models, key=lambda m: m.context_window, reverse=True)[:3]

        scored_candidates: List[Tuple[float, ModelEntry, List[str]]] = []
        for model in candidates:
            sc, rat = self.score_model(model, req, complexity)
            scored_candidates.append((sc, model, rat))

        scored_candidates.sort(key=lambda x: x[0], reverse=True)

        primary_score, primary_model, primary_rationale = scored_candidates[0]
        alt_model = scored_candidates[1][1] if len(scored_candidates) > 1 else None

        cost = primary_model.calculate_cost(req.estimated_input_tokens, req.estimated_output_tokens, req.cached_tokens)

        return RoutingResult(
            primary_model=primary_model,
            alternative_model=alt_model,
            assigned_complexity=complexity,
            estimated_cost_usd=cost,
            latency_tier=primary_model.latency_tier,
            rationale=primary_rationale,
            candidate_pool_size=len(scored_candidates),
            rejected_count=len(self.models) - len(candidates),
        )

    def build_cascade(self, task: Union[str, TaskRequirements]) -> CascadePlan:
        """Construct a 4-tier FrugalGPT cascade for progressive triage and escalation."""
        if isinstance(task, str):
            req = TaskRequirements(description=task)
        else:
            req = task

        complexity = req.explicit_complexity or ComplexityAnalyzer.evaluate(
            req.description,
            req.estimated_input_tokens
        )

        # Standard SOTA baseline for comparison (unconditional Claude Opus 5.5)
        sota_model = self.get_model("claude-opus-5-5") or self.models[0]
        sota_cost = sota_model.calculate_cost(req.estimated_input_tokens, req.estimated_output_tokens, req.cached_tokens)

        # Select stage models based on local_only preference
        if req.local_only:
            local_models = [m for m in self.models if m.local_runnable]
            if req.max_vram_gb is not None:
                local_models = [
                    m for m in local_models
                    if (m.vram_q4_gb or m.vram_fp16_gb or 999.0) <= req.max_vram_gb
                ]
            t0_model = self.get_model("smollm2-1-7b") or (local_models[0] if local_models else self.models[0])
            t1_model = self.get_model("qwen-3-6-35b-a3b") or self.get_model("qwen-2-5-coder-32b") or self.get_model("phi-4") or t0_model
            t2_model = t1_model
            t3_model = self.get_model("qwen-2-5-coder-32b") or t1_model
        else:
            # Tier 0: Triage (ultra-fast, sub-$0.15/M hosted API model)
            t0_candidates = [m for m in self.models if m.cascade_role == "tier_0_triage" and m.tier != "small_edge"]
            t0_model = min(t0_candidates, key=lambda m: m.input_cost_per_m) if t0_candidates else self.models[-1]

            # Tier 1: Worker (high efficiency specialist, Claude Sonnet 5.5 / GPT-6.1 Sol)
            t1_candidates = [m for m in self.models if m.cascade_role == "tier_1_worker" and m.tier != "small_edge"]
            t1_model = self.get_model("claude-sonnet-5-5") or (t1_candidates[0] if t1_candidates else self.models[1])

            # Tier 2: Verifier / Living Repository (Gemini 4 Argon or Grok 4.7)
            t2_candidates = [m for m in self.models if m.cascade_role == "tier_2_verifier"]
            t2_model = self.get_model("gemini-4-argon") or (t2_candidates[0] if t2_candidates else t1_model)

            # Tier 3: Escalation (Claude Opus 5.5 or GPT-6 Astra)
            t3_candidates = [m for m in self.models if m.cascade_role == "tier_3_escalation"]
            t3_model = self.get_model("claude-opus-5-5") or (t3_candidates[0] if t3_candidates else sota_model)

        # Exit probabilities calibrated against task complexity
        if complexity <= 3.0:
            p0, p1, p2, p3 = 0.75, 0.20, 0.04, 0.01
            entry_tier = 0
            guidance = "Low complexity task: High-probability instant exit at Tier 0 triage."
        elif complexity <= 6.5:
            p0, p1, p2, p3 = 0.15, 0.65, 0.15, 0.05
            entry_tier = 1
            guidance = "Moderate complexity: Direct execution at Tier 1 Worker, minimal escalation."
        elif complexity <= 8.5:
            p0, p1, p2, p3 = 0.00, 0.30, 0.40, 0.30
            entry_tier = 1
            guidance = "High complexity: Multi-stage execution with guaranteed verification pass."
        else:
            p0, p1, p2, p3 = 0.00, 0.00, 0.10, 0.90
            entry_tier = 3
            guidance = "Extreme frontier complexity: Immediate dispatch to Tier 3 Escalation."

        c0 = t0_model.calculate_cost(req.estimated_input_tokens, req.estimated_output_tokens, req.cached_tokens)
        c1 = t1_model.calculate_cost(req.estimated_input_tokens, req.estimated_output_tokens, req.cached_tokens)
        c2 = t2_model.calculate_cost(req.estimated_input_tokens, req.estimated_output_tokens, req.cached_tokens)
        c3 = t3_model.calculate_cost(req.estimated_input_tokens, req.estimated_output_tokens, req.cached_tokens)

        # Cascade cumulative execution: Stage 0 runs with prob 1.0 (if entry 0); Stage 1 runs if not resolved, etc.
        if entry_tier == 0:
            prob_run = [1.0, 1.0 - p0, max(0.0, 1.0 - p0 - p1), p3]
        elif entry_tier == 1:
            prob_run = [0.0, 1.0, max(0.0, 1.0 - p1), p3]
        elif entry_tier == 2:
            prob_run = [0.0, 0.0, 1.0, p3]
        else:
            prob_run = [0.0, 0.0, 0.0, 1.0]

        stage_costs = [c0, c1, c2, c3]
        composite_cost = sum(p * c for p, c in zip(prob_run, stage_costs))
        worst_case_cost = sum(stage_costs)

        savings_pct = max(0.0, ((sota_cost - composite_cost) / (sota_cost or 1e-6)) * 100.0)

        stages = [
            CascadeStage("Tier 0: Triage", 0, t0_model, "Ultra-low-latency classification & micro-extraction", p0, c0),
            CascadeStage("Tier 1: Worker", 1, t1_model, "Primary functional code generation & editing", p1, c1),
            CascadeStage("Tier 2: Verifier", 2, t2_model, "Cross-context verification & invariant audit", p2, c2),
            CascadeStage("Tier 3: Escalation", 3, t3_model, "Frontier reasoning & SOTA fallback", p3, c3),
        ]

        return CascadePlan(
            task_description=req.description,
            complexity_score=complexity,
            stages=stages,
            composite_expected_cost_usd=composite_cost,
            worst_case_cost_usd=worst_case_cost,
            unrouted_sota_cost_usd=sota_cost,
            savings_pct=round(savings_pct, 1),
            recommended_entry_tier=entry_tier,
            execution_guidance=guidance,
        )


# Global singleton convenience
_ROUTER_INSTANCE: Optional[ModelRouter] = None


def get_router() -> ModelRouter:
    """Obtain or initialize the global ModelRouter singleton."""
    global _ROUTER_INSTANCE
    if _ROUTER_INSTANCE is None:
        _ROUTER_INSTANCE = ModelRouter()
    return _ROUTER_INSTANCE


def route_task(task_or_description: Union[str, TaskRequirements]) -> RoutingResult:
    """Convenience function to route a task prompt directly."""
    return get_router().route(task_or_description)


def cascade_task(task_or_description: Union[str, TaskRequirements]) -> CascadePlan:
    """Convenience function to generate a 4-tier cascade plan for a task."""
    return get_router().build_cascade(task_or_description)
