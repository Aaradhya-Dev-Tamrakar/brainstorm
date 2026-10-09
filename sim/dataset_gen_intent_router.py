"""Synthetic & Historical Dataset Generator for Ecosystem Intent & Skill Router.

Generates high-fidelity (instruction, input, output) JSONL records specifically
tuned for Qwen2.5-0.5B-Instruct / Qwen3.5-0.8B LoRA fine-tuning in Google Colab.
Grounds training targets directly in:
1. 7 Adaptive Archetypes (Stage 1 Scope)
2. 2D Orthogonal Matrix Coordinates (V0-V2, R0-R2)
3. 30+ Installed Ecosystem Skills (Stage 2 Route)
4. Velocity Profiles (TURBO, BALANCED, ECONOMY)
"""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any, Dict, List

BRAINSTORM_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BRAINSTORM_ROOT / "research" / "datasets" / "intent_routing"
TRAIN_FILE = OUTPUT_DIR / "intent_routing_train.jsonl"
EVAL_FILE = OUTPUT_DIR / "intent_routing_eval.jsonl"

SYSTEM_PROMPT = (
    "You are the high-speed Intent and Skill Router for the Aaradhya development ecosystem. "
    "Classify the incoming user intent into the exact lifecycle archetype, tier, 2D matrix cell, "
    "primary skill, supporting skills, and velocity profile in strict JSON format."
)

ARCHETYPES = [
    "ENGINEERING_DEV",
    "DOMAIN_HARDWARE",
    "DOMAIN_AEC_CAD",
    "RESEARCH_ACADEMIC",
    "FRONTEND_PRODUCT",
    "SWARM_ORCHESTRATION",
    "SYSADMIN_SECURITY",
]

# Curated seed templates reflecting real ecosystem tasks
DATASET_SEEDS: List[Dict[str, Any]] = [
    # 1. ENGINEERING_DEV
    {
        "input": "Fix the regression in test_warehouse_mem_sim.py where queue latency was calculating as zero.",
        "output": {
            "archetype": "ENGINEERING_DEV",
            "tier": "Tier 1",
            "matrix_cell": "(V0, R1)",
            "policy": "BRANCH_GUARD",
            "primary_skill": "github-workflow",
            "supporting_skills": ["systems-concurrency-harness"],
            "velocity": "BALANCED",
        },
    },
    {
        "input": "Refactor reconciliation_engine.py to verify SMT Z3 invariants and commit via sync.bat.",
        "output": {
            "archetype": "ENGINEERING_DEV",
            "tier": "Tier 2",
            "matrix_cell": "(V1, R2)",
            "policy": "DECOUPLED_SLICES",
            "primary_skill": "github-workflow",
            "supporting_skills": ["adaptive-workflow"],
            "velocity": "BALANCED",
        },
    },
    {
        "input": "Check git status, audit schemas, and run sync.bat with maintainer bypass.",
        "output": {
            "archetype": "ENGINEERING_DEV",
            "tier": "Tier 1",
            "matrix_cell": "(V0, R0)",
            "policy": "DIRECT_FAST",
            "primary_skill": "github-workflow",
            "supporting_skills": [],
            "velocity": "BALANCED",
        },
    },
    # 2. DOMAIN_HARDWARE
    {
        "input": "Synthesize a 4th-order Chebyshev low-pass IIR filter for 10kHz audio sampling via Bilinear Transform.",
        "output": {
            "archetype": "DOMAIN_HARDWARE",
            "tier": "Tier 2",
            "matrix_cell": "(V0, R1)",
            "policy": "BRANCH_GUARD",
            "primary_skill": "dsp-signal-engine",
            "supporting_skills": ["dsa-complexity-optimizer"],
            "velocity": "BALANCED",
        },
    },
    {
        "input": "Calculate the Radar Range Equation and link margin for an SSR Mode-S transponder interrogation at 150km.",
        "output": {
            "archetype": "DOMAIN_HARDWARE",
            "tier": "Tier 2",
            "matrix_cell": "(V0, R1)",
            "policy": "BRANCH_GUARD",
            "primary_skill": "avionic-telecom-analyzer",
            "supporting_skills": ["rf-link-budget-calc"],
            "velocity": "BALANCED",
        },
    },
    {
        "input": "Design a FreeRTOS circular ring buffer and ISR handler for STM32 UART DMA reception.",
        "output": {
            "archetype": "DOMAIN_HARDWARE",
            "tier": "Tier 2",
            "matrix_cell": "(V1, R1)",
            "policy": "STAR_SUBAGENTS",
            "primary_skill": "embedded-firmware-scaffold",
            "supporting_skills": ["systems-concurrency-harness"],
            "velocity": "BALANCED",
        },
    },
    # 3. RESEARCH_ACADEMIC
    {
        "input": "Scaffold IOE BE semester IV-II notes for CE 752 and EX 756 with syllabus markdown hubs.",
        "output": {
            "archetype": "RESEARCH_ACADEMIC",
            "tier": "Tier 2",
            "matrix_cell": "(V1, R1)",
            "policy": "STAR_SUBAGENTS",
            "primary_skill": "academic-notebook-architect",
            "supporting_skills": ["super-nlm", "fleet-orchestrator"],
            "velocity": "TURBO",
        },
    },
    {
        "input": "Query NotebookLM notebook 2c00f5a4 for recent SPARK findings and extract podcast audio overview.",
        "output": {
            "archetype": "RESEARCH_ACADEMIC",
            "tier": "Tier 1",
            "matrix_cell": "(V0, R0)",
            "policy": "DIRECT_FAST",
            "primary_skill": "super-nlm",
            "supporting_skills": ["super-nlm-downloads"],
            "velocity": "BALANCED",
        },
    },
    {
        "input": "Download all mind maps and quizzes from NotebookLM link and share the folder over LocalSend.",
        "output": {
            "archetype": "RESEARCH_ACADEMIC",
            "tier": "Tier 1",
            "matrix_cell": "(V0, R0)",
            "policy": "DIRECT_FAST",
            "primary_skill": "super-nlm-downloads",
            "supporting_skills": ["super-nlm"],
            "velocity": "BALANCED",
        },
    },
    # 4. FRONTEND_PRODUCT
    {
        "input": "Add a new project card into AaradhyaDT.github.io, generate encrypted access token, and verify zero tokens.",
        "output": {
            "archetype": "FRONTEND_PRODUCT",
            "tier": "Tier 1",
            "matrix_cell": "(V0, R2)",
            "policy": "SURGICAL_LOCK",
            "primary_skill": "portfolio-project-manager",
            "supporting_skills": ["modern-web-guidance", "github-workflow"],
            "velocity": "BALANCED",
        },
    },
    {
        "input": "Fix the jumping navbar on scroll by implementing fluid wordmark collapse to ADT monogram.",
        "output": {
            "archetype": "FRONTEND_PRODUCT",
            "tier": "Tier 1",
            "matrix_cell": "(V0, R1)",
            "policy": "BRANCH_GUARD",
            "primary_skill": "fluid-wordmark-collapse",
            "supporting_skills": ["design-taste-frontend", "modern-web-guidance"],
            "velocity": "BALANCED",
        },
    },
    {
        "input": "Audit compliance report HTML and style PDF export matching regulatory Blink standards.",
        "output": {
            "archetype": "FRONTEND_PRODUCT",
            "tier": "Tier 2",
            "matrix_cell": "(V0, R1)",
            "policy": "BRANCH_GUARD",
            "primary_skill": "compliance-report-harmonizer",
            "supporting_skills": ["modern-web-guidance"],
            "velocity": "BALANCED",
        },
    },
    # 5. SWARM_ORCHESTRATION
    {
        "input": "Dispatch 12 batch copilot tasks across all 27 accounts in Fleet-Orchestrator with full turbo velocity.",
        "output": {
            "archetype": "SWARM_ORCHESTRATION",
            "tier": "Tier 2",
            "matrix_cell": "(V2, R0)",
            "policy": "FLEET_SWARM",
            "primary_skill": "fleet-orchestrator",
            "supporting_skills": ["adaptive-workflow"],
            "velocity": "TURBO",
        },
    },
    {
        "input": "Preview an overnight autonomous swarm team with Scout, Reviewer, and Writer roles.",
        "output": {
            "archetype": "SWARM_ORCHESTRATION",
            "tier": "Tier 2",
            "matrix_cell": "(V1, R1)",
            "policy": "STAR_SUBAGENTS",
            "primary_skill": "agent-teams-orchestration",
            "supporting_skills": ["adaptive-workflow"],
            "velocity": "BALANCED",
        },
    },
    # 6. SYSADMIN_SECURITY
    {
        "input": "Scan D:/Downloads for hidden Alternate Data Streams and check PE headers for stealth masquerading.",
        "output": {
            "archetype": "SYSADMIN_SECURITY",
            "tier": "Tier 1",
            "matrix_cell": "(V0, R1)",
            "policy": "BRANCH_GUARD",
            "primary_skill": "cyber-forensics",
            "supporting_skills": [],
            "velocity": "BALANCED",
        },
    },
    {
        "input": "Lock the private research directory using kernel NTFS ACL security in Win-Vault.",
        "output": {
            "archetype": "SYSADMIN_SECURITY",
            "tier": "Tier 1",
            "matrix_cell": "(V0, R1)",
            "policy": "BRANCH_GUARD",
            "primary_skill": "win-vault",
            "supporting_skills": [],
            "velocity": "BALANCED",
        },
    },
    {
        "input": "Capture silent window screenshot of active Edge browser tab and inspect UI automation tree.",
        "output": {
            "archetype": "SYSADMIN_SECURITY",
            "tier": "Tier 1",
            "matrix_cell": "(V0, R0)",
            "policy": "DIRECT_FAST",
            "primary_skill": "winpilot",
            "supporting_skills": [],
            "velocity": "BALANCED",
        },
    },
]

# Variations to augment the seed dataset
PROMPT_PREFIXES = [
    "",
    "Please ",
    "Can you ",
    "Task: ",
    "Agent, ",
    "Hey, ",
    "Quickly ",
    "Run workflow to ",
    "I need to ",
]


def expand_dataset(seeds: List[Dict[str, Any]], target_count: int = 800) -> List[Dict[str, Any]]:
    """Synthesizes rich variations while preserving structural ground truth."""
    expanded = []
    random.seed(42)

    while len(expanded) < target_count:
        for seed in seeds:
            prefix = random.choice(PROMPT_PREFIXES)
            base_input = seed["input"]
            if prefix and base_input[0].isupper():
                aug_input = prefix + base_input[0].lower() + base_input[1:]
            else:
                aug_input = prefix + base_input

            sample = {
                "instruction": SYSTEM_PROMPT,
                "input": aug_input,
                "output": json.dumps(seed["output"], ensure_ascii=False),
            }
            expanded.append(sample)
            if len(expanded) >= target_count:
                break

    random.shuffle(expanded)
    return expanded


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    total_samples = expand_dataset(DATASET_SEEDS, target_count=900)

    # 80/20 train/eval split
    split_idx = int(len(total_samples) * 0.8)
    train_data = total_samples[:split_idx]
    eval_data = total_samples[split_idx:]

    with open(TRAIN_FILE, "w", encoding="utf-8") as f:
        for item in train_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    with open(EVAL_FILE, "w", encoding="utf-8") as f:
        for item in eval_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"Generated {len(train_data)} train samples -> {TRAIN_FILE}")
    print(f"Generated {len(eval_data)} eval samples -> {EVAL_FILE}")


if __name__ == "__main__":
    main()
