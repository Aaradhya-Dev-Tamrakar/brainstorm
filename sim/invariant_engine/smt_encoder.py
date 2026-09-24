"""
smt_encoder.py
--------------
SMT-LIB2 / Z3 inductive invariant prover and counterexample extractor for INV-BMK-001.
Performs base-case verification, inductive transition checks, vacuity detection,
and extracts concrete counterexample assignments for downstream sandbox replay.
"""

import time
from typing import Dict, Any, List, Tuple, Optional, Callable
import z3

try:
    from .contract_types import InvariantProperty, VerificationResult, InvariantClassification
    from .state_machine import BaseStateMachine
except (ImportError, ValueError):
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from sim.invariant_engine.contract_types import InvariantProperty, VerificationResult, InvariantClassification
    from sim.invariant_engine.state_machine import BaseStateMachine


class SMTInvariantProver:
    def __init__(self, timeout_ms: int = 2000):
        self.timeout_ms = timeout_ms

    def verify_property(
        self,
        machine: BaseStateMachine,
        prop: InvariantProperty,
        actions: List[str],
        predicate_fn: Callable[[Dict[str, z3.ExprRef]], z3.BoolRef]
    ) -> VerificationResult:
        """
        Verify candidate invariant property against machine transitions.
        Returns VerificationResult with status, latency, and counterexample if SAT.
        """
        t0 = time.perf_counter()

        # Step 1: Vacuity / Contradiction Negative Control Checks
        s_unconstrained = machine.get_symbolic_vars("unconstrained")
        p_unconstrained = predicate_fn(s_unconstrained)

        # Check if P is contradictory (P is always FALSE)
        solver_contra = z3.Solver()
        solver_contra.set("timeout", self.timeout_ms)
        solver_contra.add(p_unconstrained)
        if solver_contra.check() == z3.unsat:
            lat = (time.perf_counter() - t0) * 1000.0
            return VerificationResult(
                property_id=prop.property_id,
                state_machine_id=machine.machine_id,
                classification=prop.classification,
                status="CONTRADICTION_REJECTED",
                solver_latency_ms=round(lat, 3),
                details="Property is contradictory (unsatisfiable in all states)."
            )

        # Check if P is vacuous tautology (not(P) is always FALSE)
        solver_taut = z3.Solver()
        solver_taut.set("timeout", self.timeout_ms)
        solver_taut.add(z3.Not(p_unconstrained))
        if solver_taut.check() == z3.unsat:
            lat = (time.perf_counter() - t0) * 1000.0
            return VerificationResult(
                property_id=prop.property_id,
                state_machine_id=machine.machine_id,
                classification=prop.classification,
                status="VACUOUS_REJECTED",
                solver_latency_ms=round(lat, 3),
                details="Property is a vacuous tautology (true across all unconstrained states)."
            )

        # Step 2: Base Case Check: I(s) => P(s)
        s0 = machine.get_symbolic_vars("s0")
        solver_base = z3.Solver()
        solver_base.set("timeout", self.timeout_ms)
        solver_base.add(machine.get_initial_constraint(s0))
        solver_base.add(z3.Not(predicate_fn(s0)))

        if solver_base.check() == z3.sat:
            lat = (time.perf_counter() - t0) * 1000.0
            model = solver_base.model()
            ce = {k: self._model_val(model, v) for k, v in s0.items() if not k.startswith("unconstrained")}
            return VerificationResult(
                property_id=prop.property_id,
                state_machine_id=machine.machine_id,
                classification=prop.classification,
                status="COUNTEREXAMPLE_FOUND",
                solver_latency_ms=round(lat, 3),
                counterexample={
                    "stage": "BASE_CASE",
                    "action": "INIT",
                    "initial_state": ce,
                    "final_state": ce
                },
                z3_model_str=str(model),
                details="Base case violated: initial state does not satisfy candidate invariant."
            )

        # Step 3: Inductive Step: for each action a, P(s) and T(s, a, s') => P(s')
        for action in actions:
            s = machine.get_symbolic_vars("s")
            s_prime = machine.get_symbolic_vars("sp")

            solver_step = z3.Solver()
            solver_step.set("timeout", self.timeout_ms)
            
            # Hypothesis: P holds in s
            solver_step.add(predicate_fn(s))
            # Transition occurs
            solver_step.add(machine.get_transition_relation(s, s_prime, action))
            # Check violation in s_prime: not P(s_prime)
            solver_step.add(z3.Not(predicate_fn(s_prime)))

            if solver_step.check() == z3.sat:
                lat = (time.perf_counter() - t0) * 1000.0
                model = solver_step.model()
                
                initial_vals = {k: self._model_val(model, v) for k, v in s.items()}
                final_vals = {k: self._model_val(model, v) for k, v in s_prime.items()}

                return VerificationResult(
                    property_id=prop.property_id,
                    state_machine_id=machine.machine_id,
                    classification=prop.classification,
                    status="COUNTEREXAMPLE_FOUND",
                    solver_latency_ms=round(lat, 3),
                    counterexample={
                        "stage": "INDUCTIVE_STEP",
                        "action": action,
                        "initial_state": initial_vals,
                        "final_state": final_vals
                    },
                    z3_model_str=str(model),
                    details=f"Inductive violation detected on transition '{action}'."
                )

        lat = (time.perf_counter() - t0) * 1000.0
        return VerificationResult(
            property_id=prop.property_id,
            state_machine_id=machine.machine_id,
            classification=prop.classification,
            status="PROVED_INVARIANT",
            solver_latency_ms=round(lat, 3),
            details="Formally proved: invariant holds inductively across all reachable transitions."
        )

    def _model_val(self, model: z3.ModelRef, var: z3.ExprRef) -> Any:
        try:
            val = model.eval(var, model_completion=True)
            if z3.is_int(val):
                return val.as_long()
            elif z3.is_bool(val):
                return z3.is_true(val)
            return str(val)
        except Exception:
            return 0
