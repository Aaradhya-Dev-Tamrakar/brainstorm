"""Dependency-free validation for the canonical ecosystem verification manifest."""

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "schemas" / "ecosystem.verification.json"
SCHEMA = ROOT / "schemas" / "ecosystem.verification.schema.json"
PROJECT_IDS = {"super-nlm", "claude-desktop", "aaradhyadt-github-io", "brainstorm"}
TOP_LEVEL_KEYS = {"$schema", "schema_version", "manifest_kind", "generated_by", "projects"}
PROJECT_KEYS = {"id", "repository", "claimed_result", "claims", "provenance", "verification"}
CLAIM_KEYS = {"metric", "value", "scope", "evidence_tier", "limitations"}
PROVENANCE_KEYS = {"source_path", "source_commit", "recorded_at"}
VERIFICATION_KEYS = {"method", "status", "deterministic", "command"}


def fail(message):
    raise ValueError(message)


def validate():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    if set(manifest) != TOP_LEVEL_KEYS:
        fail("manifest contains keys outside the v1 schema")
    if manifest.get("$schema") != schema["$id"]:
        fail("manifest $schema does not match the canonical schema id")
    if manifest.get("schema_version") != "1.0.0" or manifest.get("manifest_kind") != "ecosystem_verification":
        fail("unexpected manifest version or kind")
    projects = manifest.get("projects")
    if not isinstance(projects, list) or {p.get("id") for p in projects} != PROJECT_IDS:
        fail("manifest must contain exactly the four in-scope project ids")
    for project in projects:
        if set(project) != PROJECT_KEYS:
            fail(f"project {project.get('id', '<unknown>')} contains schema-invalid keys")
        if not re.fullmatch(r"^[^/]+/[^/]+$", project["repository"]):
            fail(f"invalid repository: {project['repository']}")
        provenance = project["provenance"]
        if set(provenance) != PROVENANCE_KEYS:
            fail(f"invalid provenance keys for {project['id']}")
        date.fromisoformat(provenance["recorded_at"])
        if not provenance["source_path"] or not provenance["source_commit"]:
            fail(f"incomplete provenance for {project['id']}")
        verification = project["verification"]
        if set(verification) - VERIFICATION_KEYS:
            fail(f"invalid verification keys for {project['id']}")
        if not isinstance(verification["deterministic"], bool):
            fail(f"deterministic must be boolean for {project['id']}")
        for claim in project["claims"]:
            if set(claim) != CLAIM_KEYS:
                fail(f"invalid claim keys in {project['id']}")
            if claim["evidence_tier"] not in {"E0", "E1", "E2", "E3", "E4", "E5"}:
                fail(f"invalid evidence tier in {project['id']}")
            if not claim["scope"] or not claim["limitations"]:
                fail(f"claim scope/limitations missing in {project['id']}")
    return len(projects), sum(len(p["claims"]) for p in projects)


if __name__ == "__main__":
    try:
        projects, claims = validate()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ECOSYSTEM MANIFEST: FAIL: {exc}")
        sys.exit(1)
    print(f"ECOSYSTEM MANIFEST: PASS ({projects} projects, {claims} claims)")
