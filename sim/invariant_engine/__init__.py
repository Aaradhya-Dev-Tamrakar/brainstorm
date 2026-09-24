"""
Invariant Assurance Engine Package.
ARCH-RFC-006 / INV-BMK-001 Implementation.
Translates protocol contracts into SMT-LIB2/Z3 assertions, generates counterexamples,
and confirms runtime divergence via deterministic sandbox replay.
"""

from .contract_types import (
    InvariantClassification,
    InvariantProperty,
    VerificationResult,
    ReplayResult,
    BenchmarkEvaluationRecord
)
from .state_machine import (
    BaseStateMachine,
    CXLMemoryAllocatorMachine,
    TokenBucketRateLimiterMachine,
    WorkerSessionRuntimeMachine,
    SequenceNonceTrackerMachine
)
from .smt_encoder import SMTInvariantProver
from .sandbox_replay import SandboxReplayEngine

__all__ = [
    "InvariantClassification",
    "InvariantProperty",
    "VerificationResult",
    "ReplayResult",
    "BenchmarkEvaluationRecord",
    "BaseStateMachine",
    "CXLMemoryAllocatorMachine",
    "TokenBucketRateLimiterMachine",
    "WorkerSessionRuntimeMachine",
    "SequenceNonceTrackerMachine",
    "SMTInvariantProver",
    "SandboxReplayEngine"
]
