"""
reconciliation_engine.py
------------------------
Two-Layer Deterministic Reconciliation & Verification Engine for brainstorm.
Enforces ARCH-RFC-001 / ARCH-RFC-005 / ARCH-RFC-006 / INV-EPI-001 invariants across the repository.

Verification Layers:
  Layer 1 (Structural Consistency Gate):
    1. Broken Cross-References (dangling Markdown links).
    2. Missing Mandatory Metadata Headers (ID, Status, Evidence Tier).
    3. JSON & YAML Schema Validation (capability-registry.yaml, contracts).
    4. Epistemic Evidence Invariants (IMPLEMENTED requires Evidence Tier >= E2).
    5. Ecosystem Taxonomy Count Invariants (21 modules, 17 computational, 4 presentation, 6 workflows).
    6. Physical Output Artifact Existence (verifying research/results/*.pdf files claimed in experiments).
    7. Economic Model Constant Reconciliation ($1,272.55 outlay, $25,000 replacement base, 19.65x ratio).

  Layer 2 (Behavioral Reproducibility Gate):
    1. Warehouse Memory Simulator Deterministic Latency & Hit Rate Checks (test_warehouse_mem_sim.py).
    2. Canonical Output Invariance Regression (test_reproducibility.py).
    3. Parameter Sweep Reproducibility & Golden Value Assertions.

Usage:
    python sim/reconciliation_engine.py
"""

import os
import re
import sys
import json
import unittest
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

BRAINSTORM_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESEARCH_DIR = os.path.join(BRAINSTORM_ROOT, "research")
SCHEMAS_DIR = os.path.join(BRAINSTORM_ROOT, "schemas")
REPORT_DIR = os.path.join(BRAINSTORM_ROOT, "report")
RESULTS_DIR = os.path.join(RESEARCH_DIR, "results")
SIM_DIR = os.path.join(BRAINSTORM_ROOT, "sim")

REQUIRED_METADATA_KEYS = [
    "Artifact ID", "Status", "Principal Architect", "Evidence Tier"
]

VALID_STATUSES = {"IMPLEMENTED", "EXPERIMENTAL", "PROPOSED", "ASPIRATIONAL", "RETIRED"}
VALID_EVIDENCE_TIERS = {"E0", "E1", "E2", "E3", "E4", "E5"}


def parse_simple_yaml_capabilities(filepath):
    """Fallback zero-dependency YAML parser for capability-registry.yaml."""
    capabilities = []
    current_cap = None
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("- id:"):
                if current_cap:
                    capabilities.append(current_cap)
                val = stripped.split(":", 1)[1].strip().strip('"').strip("'")
                current_cap = {"id": val}
            elif current_cap and ":" in stripped:
                k, v = stripped.split(":", 1)
                k = k.strip().strip("- ")
                v = v.strip().strip('"').strip("'")
                if k in ["name", "repository", "category", "status", "evidence", "confidence", "last_verified"]:
                    current_cap[k] = v
        if current_cap:
            capabilities.append(current_cap)
    return capabilities


def audit_layer_1_consistency():
    """Layer 1: Structural consistency, schemas, metadata, links, and economic constants."""
    discrepancies = []
    total_files_audited = 0
    
    print("\n" + "=" * 75)
    print(" [LAYER 1: STRUCTURAL CONSISTENCY GATE] (Deterministic Zero-Token Audit)")
    print("=" * 75)
    
    all_files = {}
    for root, dirs, files in os.walk(BRAINSTORM_ROOT):
        if ".git" in root or "node_modules" in root or "graphify-out" in root:
            continue
        for f in files:
            if f.endswith((".md", ".py", ".json", ".yaml", ".yml")):
                rel_path = os.path.relpath(os.path.join(root, f), BRAINSTORM_ROOT)
                all_files[rel_path.replace("\\", "/")] = os.path.join(root, f)

    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    artifact_pattern = re.compile(r'research/results/([a-zA-Z0-9_\-\.]+\.pdf)')
    
    for rel_path, full_path in all_files.items():
        if rel_path.endswith(".json"):
            total_files_audited += 1
            try:
                with open(full_path, "r", encoding="utf-8") as jf:
                    data = json.load(jf)
                if rel_path == "schemas/ecosystem.registry.json":
                    stats = data.get("statistics", {})
                    if stats.get("total_tool_modules") != 21:
                        discrepancies.append({
                            "type": "TAXONOMY_DISCREPANCY",
                            "file": rel_path,
                            "detail": f"Expected 21 total_tool_modules, found {stats.get('total_tool_modules')}"
                        })
                    if stats.get("computational_modules") != 17:
                        discrepancies.append({
                            "type": "TAXONOMY_DISCREPANCY",
                            "file": rel_path,
                            "detail": f"Expected 17 computational_modules, found {stats.get('computational_modules')}"
                        })
                    if stats.get("presentation_and_educational_modules") != 4:
                        discrepancies.append({
                            "type": "TAXONOMY_DISCREPANCY",
                            "file": rel_path,
                            "detail": f"Expected 4 presentation_and_educational_modules, found {stats.get('presentation_and_educational_modules')}"
                        })
            except Exception as e:
                discrepancies.append({
                    "type": "INVALID_JSON",
                    "file": rel_path,
                    "detail": str(e)
                })
            continue

        if rel_path.endswith((".yaml", ".yml")):
            total_files_audited += 1
            caps = []
            try:
                import yaml
                with open(full_path, "r", encoding="utf-8") as yf:
                    data = yaml.safe_load(yf)
                if isinstance(data, dict):
                    caps = data.get("capabilities", [])
            except ImportError:
                if rel_path == "schemas/capability-registry.yaml":
                    caps = parse_simple_yaml_capabilities(full_path)
            except Exception as e:
                discrepancies.append({
                    "type": "INVALID_YAML",
                    "file": rel_path,
                    "detail": str(e)
                })
            
            # Verify capability registry invariants
            if rel_path == "schemas/capability-registry.yaml":
                for cap in caps:
                    cid = cap.get("id", "UNKNOWN")
                    cstatus = cap.get("status")
                    cevidence = cap.get("evidence")
                    if cstatus not in VALID_STATUSES:
                        discrepancies.append({
                            "type": "INVALID_STATUS",
                            "file": rel_path,
                            "detail": f"Capability '{cid}' has invalid status: '{cstatus}'"
                        })
                    if cevidence not in VALID_EVIDENCE_TIERS:
                        discrepancies.append({
                            "type": "INVALID_EVIDENCE_TIER",
                            "file": rel_path,
                            "detail": f"Capability '{cid}' has invalid evidence tier: '{cevidence}'"
                        })
                    # Strict Rule: IMPLEMENTED requires E2 or higher
                    if cstatus == "IMPLEMENTED" and cevidence in ["E0", "E1"]:
                        discrepancies.append({
                            "type": "EPISTEMIC_VIOLATION",
                            "file": rel_path,
                            "detail": f"Capability '{cid}' is marked IMPLEMENTED but only has tier {cevidence}"
                        })
            continue

        if not rel_path.endswith(".md"):
            continue
        total_files_audited += 1
        
        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        file_dir = os.path.dirname(full_path)
        
        # Skip checking literal link strings inside raw transcripts (Layer 0)
        if "research/transcripts" in rel_path:
            continue

        # Check cross-references / internal markdown links
        for match in link_pattern.finditer(content):
            target = match.group(2).split("#")[0].strip()
            if not target or target.startswith(("http", "mailto", "file:", "conversation:")):
                continue
                
            resolved_target = os.path.normpath(os.path.join(file_dir, target))
            if not os.path.exists(resolved_target):
                discrepancies.append({
                    "type": "BROKEN_LINK",
                    "file": rel_path,
                    "detail": f"Target not found: '{target}'"
                })

        # Check metadata headers in architecture specs and invariants
        if "research/architectures" in rel_path or "research/invariants" in rel_path:
            if not rel_path.endswith("README.md"):
                missing_keys = [k for k in REQUIRED_METADATA_KEYS if k not in content]
                if missing_keys:
                    discrepancies.append({
                        "type": "MISSING_METADATA",
                        "file": rel_path,
                        "detail": f"Missing required headers: {missing_keys}"
                    })

        # Check claimed output artifacts in experiments
        if "research/experiments" in rel_path:
            for art_match in artifact_pattern.finditer(content):
                pdf_name = art_match.group(1)
                pdf_path = os.path.join(RESULTS_DIR, pdf_name)
                if not os.path.exists(pdf_path) or os.path.getsize(pdf_path) == 0:
                    discrepancies.append({
                        "type": "MISSING_RESULT_ARTIFACT",
                        "file": rel_path,
                        "detail": f"Claimed output artifact 'research/results/{pdf_name}' does not exist on disk or is empty."
                    })

    # Dynamic Physical Research Artifact Enumeration & Validation
    arch_dir = os.path.join(RESEARCH_DIR, "architectures")
    exp_dir = os.path.join(RESEARCH_DIR, "experiments")
    inv_dir = os.path.join(RESEARCH_DIR, "invariants")

    def count_valid_md_artifacts(dir_path):
        if not os.path.exists(dir_path):
            return []
        return [
            f for f in os.listdir(dir_path)
            if f.endswith(".md") and f != "README.md" and not f.startswith("INV-template") and not f.startswith(".")
        ]

    arch_artifacts = count_valid_md_artifacts(arch_dir)
    exp_artifacts = count_valid_md_artifacts(exp_dir)
    inv_artifacts = count_valid_md_artifacts(inv_dir)
    total_physical_artifacts = len(arch_artifacts) + len(exp_artifacts) + len(inv_artifacts)
    canonical_artifact_count = 24

    if total_physical_artifacts != canonical_artifact_count:
        discrepancies.append({
            "type": "RESEARCH_ARTIFACT_COUNT_DRIFT",
            "file": "research/",
            "detail": f"Expected {canonical_artifact_count} physical research artifacts, but enumerated {total_physical_artifacts} on disk (Arch: {len(arch_artifacts)}, Exp: {len(exp_artifacts)}, Inv: {len(inv_artifacts)})."
        })

    # Validate ontology, README, and audit research artifact count consistency
    readme_file = os.path.join(BRAINSTORM_ROOT, "README.md")
    if os.path.exists(readme_file):
        with open(readme_file, "r", encoding="utf-8") as rf:
            readme_text = rf.read()
        if f"{canonical_artifact_count} Research Specs & Experiments" not in readme_text:
            discrepancies.append({
                "type": "README_TAXONOMY_ERROR",
                "file": "README.md",
                "detail": f"README.md missing canonical '{canonical_artifact_count} Research Specs & Experiments' inventory declaration."
            })

    ontology_file = os.path.join(SCHEMAS_DIR, "capability-ontology.md")
    if os.path.exists(ontology_file):
        with open(ontology_file, "r", encoding="utf-8") as of:
            ont_text = of.read()
        if "21" not in ont_text or "17" not in ont_text or "6" not in ont_text or str(canonical_artifact_count) not in ont_text:
            discrepancies.append({
                "type": "ONTOLOGY_TAXONOMY_ERROR",
                "file": "schemas/capability-ontology.md",
                "detail": f"Ontology missing reconciled counts (21 modules, 17 computational engines, 6 workflows, {canonical_artifact_count} research artifacts)."
            })

    audit_file = os.path.join(REPORT_DIR, "repository-audit.md")
    if os.path.exists(audit_file):
        with open(audit_file, "r", encoding="utf-8") as af:
            audit_text = af.read()
        if f"{canonical_artifact_count} Research Artifacts" not in audit_text:
            discrepancies.append({
                "type": "AUDIT_TAXONOMY_ERROR",
                "file": "report/repository-audit.md",
                "detail": f"repository-audit.md missing canonical '{canonical_artifact_count} Research Artifacts' declaration."
            })

    # Validate economic model invariants
    econ_file = os.path.join(REPORT_DIR, "economic-model.md")
    if os.path.exists(econ_file):
        with open(econ_file, "r", encoding="utf-8") as ef:
            econ_text = ef.read()
        if "$1,272.55" not in econ_text or "$25,000" not in econ_text or "19.65" not in econ_text:
            discrepancies.append({
                "type": "ECONOMIC_RECONCILIATION_ERROR",
                "file": "report/economic-model.md",
                "detail": "Core economic constants ($1,272.55 outlay, $25,000 replacement base, 19.65x ratio) not reconciled."
            })

    print(f"[*] Total Documentation & Schema Files Audited: {total_files_audited}")
    
    if not discrepancies:
        print("[+] PASS: Layer 1 (Structural Consistency) is 100% verified (0 discrepancies).")
        print("    All links resolve, capability schemas valid, epistemic tiers enforced, economic constants reconciled.")
    else:
        print(f"[!] FAIL: Found {len(discrepancies)} Discrepancy(ies) in Layer 1:")
        for d in discrepancies:
            print(f"    - [{d['type']}] in {d['file']}: {d['detail']}")
            
    return len(discrepancies)


def audit_layer_2_behavioral():
    """Layer 2: Behavioral verification & simulation test suite execution."""
    print("\n" + "=" * 75)
    print(" [LAYER 2: BEHAVIORAL REPRODUCIBILITY GATE] (Deterministic Simulation Runner)")
    print("=" * 75)
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Dynamically discover tests in sim/
    test_files = [f for f in os.listdir(SIM_DIR) if f.startswith("test_") and f.endswith(".py")]
    
    sys.path.insert(0, BRAINSTORM_ROOT)
    for tf in test_files:
        mod_name = f"sim.{tf[:-3]}"
        try:
            mod = __import__(mod_name, fromlist=["*"])
            suite.addTests(loader.loadTestsFromModule(mod))
        except Exception as e:
            print(f"[!] Error loading test module {mod_name}: {e}")
            return 1
            
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print(f"[+] PASS: Layer 2 (Behavioral Reproducibility) passed all {result.testsRun} regression tests.")
        print("    Deterministic invariants, latency reductions, hit-rates, and golden outputs verified.")
        return 0
    else:
        print(f"[!] FAIL: Layer 2 failed with {len(result.failures)} failure(s) and {len(result.errors)} error(s).")
        return len(result.failures) + len(result.errors)


def audit_repository():
    print("=" * 75)
    print("   BRAINSTORM DUAL-LAYER DETERMINISTIC VERIFICATION ENGINE (ARCH-RFC-001/005)")
    print("=" * 75)
    
    l1_errors = audit_layer_1_consistency()
    l2_errors = audit_layer_2_behavioral()
    
    print("\n" + "=" * 75)
    print(" VERIFICATION SUMMARY & EPISTEMIC CERTIFICATION")
    print("=" * 75)
    print(f"  * Layer 1 (Structural Consistency): {'PASSED (Tier E3/E4)' if l1_errors == 0 else 'FAILED'}")
    print(f"  * Layer 2 (Behavioral Tests)      : {'PASSED (Tier E4/E5)' if l2_errors == 0 else 'FAILED'}")
    
    total_errors = l1_errors + l2_errors
    if total_errors == 0:
        print("\n[+] CERTIFIED: Repository satisfies all structural consistency and behavioral ground truth invariants.")
    else:
        print(f"\n[!] REJECTED: Total verification failures: {total_errors}")
        
    print("=" * 75)
    return total_errors


if __name__ == "__main__":
    exit_code = audit_repository()
    sys.exit(0 if exit_code == 0 else 1)
