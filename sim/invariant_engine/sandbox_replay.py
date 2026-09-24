"""
sandbox_replay.py
-----------------
Deterministic Python sandbox replay engine for INV-BMK-001.
Replays SMT-generated counterexamples in concrete state machines to empirically
confirm that mathematical counterexamples produce true runtime contract violations.
"""

import time
from typing import Dict, Any, Callable
try:
    from .contract_types import ReplayResult, VerificationResult
    from .state_machine import BaseStateMachine
except (ImportError, ValueError):
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from sim.invariant_engine.contract_types import ReplayResult, VerificationResult
    from sim.invariant_engine.state_machine import BaseStateMachine


class SandboxReplayEngine:
    def __init__(self):
        pass

    def replay_counterexample(
        self,
        machine: BaseStateMachine,
        verif_result: VerificationResult,
        runtime_predicate: Callable[[Dict[str, Any]], bool]
    ) -> ReplayResult:
        """
        Executes counterexample trace inside isolated runtime environment.
        Verifies whether runtime state diverges and violates invariant.
        """
        t0 = time.perf_counter()

        if verif_result.status != "COUNTEREXAMPLE_FOUND" or not verif_result.counterexample:
            lat = (time.perf_counter() - t0) * 1000.0
            return ReplayResult(
                property_id=verif_result.property_id,
                state_machine_id=machine.machine_id,
                status="SKIPPED_HOLDS",
                replay_latency_ms=round(lat, 3),
                details="No counterexample to replay; property holds or was rejected as negative control."
            )

        ce = verif_result.counterexample
        action = ce.get("action", "")
        init_state = ce.get("initial_state", {})
        
        # 1. Reset machine and inject initial counterexample state
        machine.reset()
        for k, v in init_state.items():
            if k in machine.state:
                machine.state[k] = v

        initial_snapshot = dict(machine.state)

        # 2. Extract action parameters from initial state
        kwargs = {}
        if "req" in init_state:
            kwargs["amount"] = init_state["req"]
        if "amount" in init_state:
            kwargs["amount"] = init_state["amount"]
        if "dt" in init_state:
            kwargs["dt"] = init_state["dt"]
        if "incoming_nonce" in init_state:
            kwargs["nonce"] = init_state["incoming_nonce"]

        # 3. Step state machine in runtime
        final_state, success = machine.step(action, **kwargs)
        final_snapshot = dict(machine.state)

        # 4. Check whether candidate invariant is violated at runtime
        holds_at_runtime = runtime_predicate(final_snapshot)
        violation_confirmed = not holds_at_runtime

        lat = (time.perf_counter() - t0) * 1000.0

        if violation_confirmed:
            return ReplayResult(
                property_id=verif_result.property_id,
                state_machine_id=machine.machine_id,
                status="REPLAY_CONFIRMED",
                replay_latency_ms=round(lat, 3),
                initial_state=initial_snapshot,
                action_taken=f"{action}({kwargs})",
                final_state=final_snapshot,
                violation_observed=True,
                details="Counterexample executed in sandbox: runtime invariant violation confirmed."
            )
        else:
            return ReplayResult(
                property_id=verif_result.property_id,
                state_machine_id=machine.machine_id,
                status="REPLAY_DIVERGENCE",
                replay_latency_ms=round(lat, 3),
                initial_state=initial_snapshot,
                action_taken=f"{action}({kwargs})",
                final_state=final_snapshot,
                violation_observed=False,
                details="Replay divergence: runtime state did not violate invariant despite solver SAT trace."
            )
