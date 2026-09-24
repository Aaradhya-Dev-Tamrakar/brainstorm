"""
state_machine.py
----------------
Formal state machine implementations and benchmark testbeds for INV-BMK-001.
Provides deterministic Python runtime execution alongside formal symbolic specifications.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Tuple
import z3


class BaseStateMachine(ABC):
    def __init__(self, machine_id: str, buggy_mode: bool = False):
        self.machine_id = machine_id
        self.buggy_mode = buggy_mode
        self.state: Dict[str, Any] = {}
        self.reset()

    @abstractmethod
    def reset(self) -> Dict[str, Any]:
        """Reset state to canonical initial state."""
        pass

    @abstractmethod
    def step(self, action: str, **kwargs) -> Tuple[Dict[str, Any], bool]:
        """Execute a state transition. Returns (new_state, transition_successful)."""
        pass

    @abstractmethod
    def get_symbolic_vars(self, prefix: str = "") -> Dict[str, z3.ExprRef]:
        """Generate Z3 symbolic variables for state."""
        pass

    @abstractmethod
    def get_initial_constraint(self, s: Dict[str, z3.ExprRef]) -> z3.BoolRef:
        """Z3 initial state predicate I(s)."""
        pass

    @abstractmethod
    def get_transition_relation(
        self, s: Dict[str, z3.ExprRef], s_prime: Dict[str, z3.ExprRef], action: str
    ) -> z3.BoolRef:
        """Z3 transition relation T(s, action, s_prime)."""
        pass


class CXLMemoryAllocatorMachine(BaseStateMachine):
    TOTAL_CREDITS = 64

    def __init__(self, buggy_mode: bool = False):
        super().__init__("CXL_ALLOCATOR", buggy_mode)

    def reset(self) -> Dict[str, Any]:
        self.state = {
            "credits_total": self.TOTAL_CREDITS,
            "credits_free": self.TOTAL_CREDITS,
            "credits_allocated": 0
        }
        return dict(self.state)

    def step(self, action: str, **kwargs) -> Tuple[Dict[str, Any], bool]:
        req = int(kwargs.get("amount", 1))
        if action == "allocate":
            if 0 < req <= self.state["credits_free"]:
                self.state["credits_free"] -= req
                self.state["credits_allocated"] += req
                return dict(self.state), True
            return dict(self.state), False
        elif action == "release":
            if self.buggy_mode:
                # Planted Violation: No boundary check on credits_allocated allows double-free inflation
                self.state["credits_free"] += req
                self.state["credits_allocated"] -= req
                return dict(self.state), True
            else:
                if 0 < req <= self.state["credits_allocated"]:
                    self.state["credits_free"] += req
                    self.state["credits_allocated"] -= req
                    return dict(self.state), True
                return dict(self.state), False
        return dict(self.state), False

    def get_symbolic_vars(self, prefix: str = "") -> Dict[str, z3.ExprRef]:
        p = f"{prefix}_" if prefix else ""
        return {
            "credits_total": z3.Int(f"{p}credits_total"),
            "credits_free": z3.Int(f"{p}credits_free"),
            "credits_allocated": z3.Int(f"{p}credits_allocated"),
            "req": z3.Int(f"{p}req")
        }

    def get_initial_constraint(self, s: Dict[str, z3.ExprRef]) -> z3.BoolRef:
        return z3.And(
            s["credits_total"] == self.TOTAL_CREDITS,
            s["credits_free"] == self.TOTAL_CREDITS,
            s["credits_allocated"] == 0
        )

    def get_transition_relation(
        self, s: Dict[str, z3.ExprRef], s_prime: Dict[str, z3.ExprRef], action: str
    ) -> z3.BoolRef:
        req = s["req"]
        req_valid = req > 0
        unchanged_total = (s_prime["credits_total"] == s["credits_total"])

        if action == "allocate":
            guard = z3.And(req_valid, req <= s["credits_free"])
            succ = z3.And(
                unchanged_total,
                s_prime["credits_free"] == s["credits_free"] - req,
                s_prime["credits_allocated"] == s["credits_allocated"] + req
            )
            fail = z3.And(
                unchanged_total,
                s_prime["credits_free"] == s["credits_free"],
                s_prime["credits_allocated"] == s["credits_allocated"]
            )
            return z3.If(guard, succ, fail)

        elif action == "release":
            if self.buggy_mode:
                # Planted bug in formal spec reflects buggy implementation:
                return z3.And(
                    unchanged_total,
                    req_valid,
                    s_prime["credits_free"] == s["credits_free"] + req,
                    s_prime["credits_allocated"] == s["credits_allocated"] - req
                )
            else:
                guard = z3.And(req_valid, req <= s["credits_allocated"])
                succ = z3.And(
                    unchanged_total,
                    s_prime["credits_free"] == s["credits_free"] + req,
                    s_prime["credits_allocated"] == s["credits_allocated"] - req
                )
                fail = z3.And(
                    unchanged_total,
                    s_prime["credits_free"] == s["credits_free"],
                    s_prime["credits_allocated"] == s["credits_allocated"]
                )
                return z3.If(guard, succ, fail)

        return z3.BoolVal(False)


class TokenBucketRateLimiterMachine(BaseStateMachine):
    CAPACITY = 100
    FILL_RATE = 10

    def __init__(self, buggy_mode: bool = False):
        super().__init__("TOKEN_BUCKET", buggy_mode)

    def reset(self) -> Dict[str, Any]:
        self.state = {
            "tokens": self.CAPACITY,
            "consumed": 0
        }
        return dict(self.state)

    def step(self, action: str, **kwargs) -> Tuple[Dict[str, Any], bool]:
        if action == "refill":
            dt = int(kwargs.get("dt", 1))
            added = dt * self.FILL_RATE
            if self.buggy_mode:
                # Planted Violation: No clamp to capacity allows unbounded token accumulation
                self.state["tokens"] += added
            else:
                self.state["tokens"] = min(self.CAPACITY, self.state["tokens"] + added)
            return dict(self.state), True
        elif action == "consume":
            amt = int(kwargs.get("amount", 1))
            if 0 < amt <= self.state["tokens"]:
                self.state["tokens"] -= amt
                self.state["consumed"] += amt
                return dict(self.state), True
            return dict(self.state), False
        return dict(self.state), False

    def get_symbolic_vars(self, prefix: str = "") -> Dict[str, z3.ExprRef]:
        p = f"{prefix}_" if prefix else ""
        return {
            "tokens": z3.Int(f"{p}tokens"),
            "consumed": z3.Int(f"{p}consumed"),
            "amount": z3.Int(f"{p}amount"),
            "dt": z3.Int(f"{p}dt")
        }

    def get_initial_constraint(self, s: Dict[str, z3.ExprRef]) -> z3.BoolRef:
        return z3.And(s["tokens"] == self.CAPACITY, s["consumed"] == 0)

    def get_transition_relation(
        self, s: Dict[str, z3.ExprRef], s_prime: Dict[str, z3.ExprRef], action: str
    ) -> z3.BoolRef:
        if action == "refill":
            dt = s["dt"]
            dt_valid = dt >= 0
            if self.buggy_mode:
                return z3.And(
                    dt_valid,
                    s_prime["tokens"] == s["tokens"] + dt * self.FILL_RATE,
                    s_prime["consumed"] == s["consumed"]
                )
            else:
                target = s["tokens"] + dt * self.FILL_RATE
                clamped = z3.If(target > self.CAPACITY, self.CAPACITY, target)
                return z3.And(
                    dt_valid,
                    s_prime["tokens"] == clamped,
                    s_prime["consumed"] == s["consumed"]
                )
        elif action == "consume":
            amt = s["amount"]
            guard = z3.And(amt > 0, amt <= s["tokens"])
            succ = z3.And(
                s_prime["tokens"] == s["tokens"] - amt,
                s_prime["consumed"] == s["consumed"] + amt
            )
            fail = z3.And(
                s_prime["tokens"] == s["tokens"],
                s_prime["consumed"] == s["consumed"]
            )
            return z3.If(guard, succ, fail)
        return z3.BoolVal(False)


class WorkerSessionRuntimeMachine(BaseStateMachine):
    TOTAL_TASKS = 20

    def __init__(self, buggy_mode: bool = False):
        super().__init__("WORKER_SESSION_RUNTIME", buggy_mode)

    def reset(self) -> Dict[str, Any]:
        self.state = {
            "pending": self.TOTAL_TASKS,
            "running": 0,
            "completed": 0,
            "failed": 0
        }
        return dict(self.state)

    def step(self, action: str, **kwargs) -> Tuple[Dict[str, Any], bool]:
        if action == "dispatch":
            if self.state["pending"] > 0:
                self.state["pending"] -= 1
                self.state["running"] += 1
                return dict(self.state), True
            return dict(self.state), False
        elif action == "complete":
            if self.state["running"] > 0:
                self.state["running"] -= 1
                self.state["completed"] += 1
                return dict(self.state), True
            return dict(self.state), False
        elif action == "fail":
            if self.state["running"] > 0:
                self.state["running"] -= 1
                if self.buggy_mode:
                    # Planted Violation: Increments failed count by 2 (phantom duplication)
                    self.state["failed"] += 2
                else:
                    self.state["failed"] += 1
                return dict(self.state), True
            return dict(self.state), False
        return dict(self.state), False

    def get_symbolic_vars(self, prefix: str = "") -> Dict[str, z3.ExprRef]:
        p = f"{prefix}_" if prefix else ""
        return {
            "pending": z3.Int(f"{p}pending"),
            "running": z3.Int(f"{p}running"),
            "completed": z3.Int(f"{p}completed"),
            "failed": z3.Int(f"{p}failed")
        }

    def get_initial_constraint(self, s: Dict[str, z3.ExprRef]) -> z3.BoolRef:
        return z3.And(
            s["pending"] == self.TOTAL_TASKS,
            s["running"] == 0,
            s["completed"] == 0,
            s["failed"] == 0
        )

    def get_transition_relation(
        self, s: Dict[str, z3.ExprRef], s_prime: Dict[str, z3.ExprRef], action: str
    ) -> z3.BoolRef:
        if action == "dispatch":
            guard = s["pending"] > 0
            succ = z3.And(
                s_prime["pending"] == s["pending"] - 1,
                s_prime["running"] == s["running"] + 1,
                s_prime["completed"] == s["completed"],
                s_prime["failed"] == s["failed"]
            )
            fail = z3.And(
                s_prime["pending"] == s["pending"],
                s_prime["running"] == s["running"],
                s_prime["completed"] == s["completed"],
                s_prime["failed"] == s["failed"]
            )
            return z3.If(guard, succ, fail)
        elif action == "complete":
            guard = s["running"] > 0
            succ = z3.And(
                s_prime["pending"] == s["pending"],
                s_prime["running"] == s["running"] - 1,
                s_prime["completed"] == s["completed"] + 1,
                s_prime["failed"] == s["failed"]
            )
            fail = z3.And(
                s_prime["pending"] == s["pending"],
                s_prime["running"] == s["running"],
                s_prime["completed"] == s["completed"],
                s_prime["failed"] == s["failed"]
            )
            return z3.If(guard, succ, fail)
        elif action == "fail":
            guard = s["running"] > 0
            fail_inc = 2 if self.buggy_mode else 1
            succ = z3.And(
                s_prime["pending"] == s["pending"],
                s_prime["running"] == s["running"] - 1,
                s_prime["completed"] == s["completed"],
                s_prime["failed"] == s["failed"] + fail_inc
            )
            fail = z3.And(
                s_prime["pending"] == s["pending"],
                s_prime["running"] == s["running"],
                s_prime["completed"] == s["completed"],
                s_prime["failed"] == s["failed"]
            )
            return z3.If(guard, succ, fail)
        return z3.BoolVal(False)


class SequenceNonceTrackerMachine(BaseStateMachine):
    def __init__(self, buggy_mode: bool = False):
        super().__init__("SEQUENCE_NONCE_TRACKER", buggy_mode)

    def reset(self) -> Dict[str, Any]:
        self.state = {
            "current_nonce": 0,
            "replays_detected": 0
        }
        return dict(self.state)

    def step(self, action: str, **kwargs) -> Tuple[Dict[str, Any], bool]:
        if action == "receive":
            incoming = int(kwargs.get("nonce", 0))
            if self.buggy_mode:
                # Planted Violation: Accepts stale/past nonces without replay detection
                self.state["current_nonce"] = incoming
                return dict(self.state), True
            else:
                if incoming > self.state["current_nonce"]:
                    self.state["current_nonce"] = incoming
                    return dict(self.state), True
                else:
                    self.state["replays_detected"] += 1
                    return dict(self.state), False
        return dict(self.state), False

    def get_symbolic_vars(self, prefix: str = "") -> Dict[str, z3.ExprRef]:
        p = f"{prefix}_" if prefix else ""
        return {
            "current_nonce": z3.Int(f"{p}current_nonce"),
            "replays_detected": z3.Int(f"{p}replays_detected"),
            "incoming_nonce": z3.Int(f"{p}incoming_nonce")
        }

    def get_initial_constraint(self, s: Dict[str, z3.ExprRef]) -> z3.BoolRef:
        return z3.And(s["current_nonce"] == 0, s["replays_detected"] == 0)

    def get_transition_relation(
        self, s: Dict[str, z3.ExprRef], s_prime: Dict[str, z3.ExprRef], action: str
    ) -> z3.BoolRef:
        if action == "receive":
            inc = s["incoming_nonce"]
            if self.buggy_mode:
                return z3.And(
                    s_prime["current_nonce"] == inc,
                    s_prime["replays_detected"] == s["replays_detected"]
                )
            else:
                guard = inc > s["current_nonce"]
                succ = z3.And(
                    s_prime["current_nonce"] == inc,
                    s_prime["replays_detected"] == s["replays_detected"]
                )
                fail = z3.And(
                    s_prime["current_nonce"] == s["current_nonce"],
                    s_prime["replays_detected"] == s["replays_detected"] + 1
                )
                return z3.If(guard, succ, fail)
        return z3.BoolVal(False)
