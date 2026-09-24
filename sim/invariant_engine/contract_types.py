"""
contract_types.py
-----------------
Typed contracts and schemas for the Invariant Assurance Engine (INV-BMK-001).
Distinguishes formalization, solver verification, and runtime replay tiers.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Callable


class InvariantClassification(str, Enum):
    VALID_INVARIANT = "VALID_INVARIANT"              # True safety/liveness invariant (must hold across all reachable states)
    PLANTED_VIOLATION = "PLANTED_VIOLATION"          # Deliberately planted boundary bug (must produce counterexample)
    VACUOUS_TAUTOLOGY = "VACUOUS_TAUTOLOGY"          # Tautological / unconstrained predicate (negative control)
    CONTRADICTORY_SPEC = "CONTRADICTORY_SPEC"        # Infeasible / mutually exclusive constraint (negative control)


@dataclass
class InvariantProperty:
    property_id: str
    name: str
    state_machine_id: str
    classification: InvariantClassification
    natural_language_spec: str
    predicate_symbolic: str
    expected_outcome: str                            # "UNSAT" (holds) or "SAT" (counterexample)


@dataclass
class VerificationResult:
    property_id: str
    state_machine_id: str
    classification: InvariantClassification
    status: str                                      # "PROVED_INVARIANT" | "COUNTEREXAMPLE_FOUND" | "VACUOUS_REJECTED" | "CONTRADICTION_REJECTED"
    solver_latency_ms: float
    counterexample: Optional[Dict[str, Any]] = None
    z3_model_str: Optional[str] = None
    details: str = ""


@dataclass
class ReplayResult:
    property_id: str
    state_machine_id: str
    status: str                                      # "REPLAY_CONFIRMED" | "REPLAY_DIVERGENCE" | "SKIPPED_HOLDS"
    replay_latency_ms: float
    initial_state: Optional[Dict[str, Any]] = None
    action_taken: Optional[str] = None
    final_state: Optional[Dict[str, Any]] = None
    violation_observed: bool = False
    details: str = ""


@dataclass
class BenchmarkEvaluationRecord:
    timestamp: str
    benchmark_id: str
    total_properties_evaluated: int
    planted_violations_tested: int
    planted_violations_discovered: int
    discovery_recall_pct: float
    counterexamples_generated: int
    counterexamples_replay_confirmed: int
    counterexample_validity_pct: float
    false_discovery_rate_pct: float
    vacuous_controls_tested: int
    vacuous_controls_flagged: int
    contradictory_specs_tested: int
    contradictory_specs_flagged: int
    mean_solver_latency_ms: float
    mean_replay_latency_ms: float
    results_ledger: List[Dict[str, Any]] = field(default_factory=list)
