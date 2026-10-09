"""
sim/test_adaptive_orchestrator.py
---------------------------------
Behavioral unit tests for the deterministic zero-AI adaptive orchestrator engine.
Automatically discovered and verified by audit.bat and sim/reconciliation_engine.py.
"""

from __future__ import annotations

import os
import sys
import stat
import tempfile
import unittest
from unittest import mock
from pathlib import Path

# Add brainstorm root to sys.path
BRAINSTORM_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BRAINSTORM_ROOT not in sys.path:
    sys.path.insert(0, BRAINSTORM_ROOT)

from sim.adaptive_orchestrator import (
    AntigravityMemoryGovernor,
    DeterministicTriageEngine,
    DeterministicCPMScheduler,
    DAGCycleError,
    FleetFirstBridge,
    DeterministicTransactionalRecovery,
    AdaptiveRateGovernor,
    PreExistingFileGuard,
    OrchestratorFencingManager,
    get_git_common_dir,
    resilient_unlink,
    resilient_rmtree,
)


class TestAdaptiveOrchestrator(unittest.TestCase):
    """Test suite certifying deterministic invariants for adaptive orchestration."""

    def setUp(self):
        # Isolate regression tests to deterministic heuristic ground truth
        os.environ["FORCE_HEURISTIC_ROUTING"] = "1"

    def tearDown(self):
        os.environ.pop("FORCE_HEURISTIC_ROUTING", None)

    def test_01_antigravity_memory_guard(self):
        """Validates 2.5 GB free headroom assertion and 500 MB model ceiling."""
        status = AntigravityMemoryGovernor.get_memory_status()
        self.assertIn("total_mb", status)
        self.assertIn("available_mb", status)
        self.assertIn("used_mb", status)
        self.assertIn("percent_used", status)
        self.assertIn("nova_state", status)
        self.assertGreater(status["total_mb"], 0)

        # Assert headroom behavior
        safe, msg = AntigravityMemoryGovernor.assert_headroom(required_mb=1000)
        self.assertTrue(safe)

        # Assert local model safety limit (<= 500 MB)
        model_safe, _ = AntigravityMemoryGovernor.assert_model_safety(397)  # Qwen 0.5B GGUF
        self.assertTrue(model_safe)

        model_violation, _ = AntigravityMemoryGovernor.assert_model_safety(4500)  # Heavy 7B model
        self.assertFalse(model_violation)

    def test_02_matrix_triage_boundaries(self):
        """Asserts V0, V1, V2 and R0, R1, R2 cell mapping against matrix definitions."""
        # Volume boundary tests
        v0, c0 = DeterministicTriageEngine.compute_volume(["file1.py", "file2.py"])
        self.assertEqual(v0, "V0")
        self.assertEqual(c0, 2)

        v1, c1 = DeterministicTriageEngine.compute_volume([f"file{i}.py" for i in range(5)])
        self.assertEqual(v1, "V1")
        self.assertEqual(c1, 5)

        v2, c2 = DeterministicTriageEngine.compute_volume([f"file{i}.py" for i in range(20)])
        self.assertEqual(v2, "V2")
        self.assertEqual(c2, 20)

        # Criticality tests
        r2, s2 = DeterministicTriageEngine.compute_criticality(["schemas/ecosystem.registry.json"])
        self.assertEqual(r2, "R2")
        self.assertGreaterEqual(s2, 0.40)

        r1, s1 = DeterministicTriageEngine.compute_criticality(["sim/warehouse_mem_sim.py"])
        self.assertEqual(r1, "R1")

        r0, s0 = DeterministicTriageEngine.compute_criticality(["notes/scratch.md"])
        self.assertEqual(r0, "R0")

        # Matrix lookup integrity
        triage_v0_r0 = DeterministicTriageEngine.triage("view status", ["README.md"])
        self.assertEqual(triage_v0_r0["matrix_cell"], "(V0, R0)")
        self.assertEqual(triage_v0_r0["policy"], "DIRECT_FAST")

        triage_v1_r1 = DeterministicTriageEngine.triage("update sim scripts", [f"sim/test_{i}.py" for i in range(4)])
        self.assertEqual(triage_v1_r1["matrix_cell"], "(V1, R1)")
        self.assertEqual(triage_v1_r1["policy"], "STAR_SUBAGENTS")

        triage_v2_r2 = DeterministicTriageEngine.triage("refactor core schemas", [f"schemas/schema_{i}.json" for i in range(18)])
        self.assertEqual(triage_v2_r2["matrix_cell"], "(V2, R2)")
        self.assertEqual(triage_v2_r2["policy"], "STRICT_INTERLOCK_BLOCKED")
        self.assertTrue(triage_v2_r2["requires_interlock"])

    def test_03_zero_ai_fast_path_detection(self):
        """Verifies detection of routine CLI tasks (audit, format, sync, test, status, sim)."""
        fast_audit = DeterministicTriageEngine.detect_fast_path("run repository audit now")
        self.assertIsNotNone(fast_audit)
        self.assertEqual(fast_audit["action_type"], "audit")
        self.assertEqual(fast_audit["execution_tier"], "Tier 0")
        self.assertEqual(fast_audit["ai_tokens"], 0)

        fast_sync = DeterministicTriageEngine.detect_fast_path("sync all changes with git")
        self.assertIsNotNone(fast_sync)
        self.assertEqual(fast_sync["action_type"], "sync")

        fast_test = DeterministicTriageEngine.detect_fast_path("run unit test suite")
        self.assertIsNotNone(fast_test)
        self.assertEqual(fast_test["action_type"], "test")

        fast_sim = DeterministicTriageEngine.detect_fast_path("run discrete event simulation")
        self.assertIsNotNone(fast_sim)
        self.assertEqual(fast_sim["action_type"], "sim")

        # Generative tasks must NOT trigger fast path
        non_fast = DeterministicTriageEngine.detect_fast_path("write new DSP filter architecture and scaffold code")
        self.assertIsNone(non_fast)

    def test_04_cpm_mathematical_solver(self):
        """Validates exact DAG early/late dates, critical path, and slack calculations."""
        # Canonical textbook DAG:
        # A (dur=3) -> B (dur=2), C (dur=4)
        # B -> D (dur=3)
        # C -> D (dur=3)
        # Project length: A(3) + C(4) + D(3) = 10
        tasks = [
            {"id": "A", "duration": 3, "predecessors": []},
            {"id": "B", "duration": 2, "predecessors": ["A"]},
            {"id": "C", "duration": 4, "predecessors": ["A"]},
            {"id": "D", "duration": 3, "predecessors": ["B", "C"]},
        ]
        res = DeterministicCPMScheduler.calculate_schedule(tasks)
        self.assertEqual(res["project_duration"], 10.0)
        self.assertEqual(res["critical_path"], ["A", "C", "D"])
        self.assertEqual(res["parallel_slack"], ["B"])

        # Check task B slack
        t_b = res["tasks"]["B"]
        self.assertEqual(t_b["ES"], 3.0)
        self.assertEqual(t_b["EF"], 5.0)
        self.assertEqual(t_b["LS"], 5.0)
        self.assertEqual(t_b["LF"], 7.0)
        self.assertEqual(t_b["TS"], 2.0)
        self.assertEqual(t_b["FS"], 2.0)
        self.assertFalse(t_b["is_critical"])

        # Check task C critical
        t_c = res["tasks"]["C"]
        self.assertEqual(t_c["TS"], 0.0)
        self.assertTrue(t_c["is_critical"])

    def test_05_local_router_integration(self):
        """Verifies local intent routing and deterministic heuristic fallback."""
        route = FleetFirstBridge.route_intent("Scaffold IOE semester IV-II notes for CE 752")
        self.assertIn("archetype", route)
        self.assertIn("latency_ms", route)
        self.assertIn("source", route)
        self.assertIn(route["source"], ["lm_studio_qwen0.5b", "deterministic_heuristic"])
        self.assertEqual(route["primary_skill"], "academic-notebook-architect")

    def test_06_context_firebreak_manifest(self):
        """Tests that subagent delivery manifests are strictly bounded to <300 words."""
        long_notes = "Detailed worker execution logs " * 50
        manifest = FleetFirstBridge.format_context_firebreak_manifest(
            task_id="TASK-123456-AST-PARSER",
            title="Refactor AST Parser",
            files_modified=["parser.py", "tokens.py", "ast.py"],
            verification_passed=True,
            commit_sha="a1b2c3d4",
            notes=long_notes,
        )
        word_count = len(manifest.split())
        self.assertLessEqual(word_count, 300)
        self.assertIn("INV-CTX-FIREBREAK", manifest)

    def test_07_transactional_integrity_and_hashing(self):
        """Tests SHA-256 pre/post hashing and collateral mutation detection."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_a = Path(tmpdir) / "file_a.txt"
            file_b = Path(tmpdir) / "file_b.txt"
            file_a.write_text("initial A", encoding="utf-8")
            file_b.write_text("initial B", encoding="utf-8")

            hashes_before = DeterministicTransactionalRecovery.compute_file_hashes([str(file_a), str(file_b)])

            # Mutate file_a intentionally, file_b stays same
            file_a.write_text("modified A", encoding="utf-8")
            hashes_after = DeterministicTransactionalRecovery.compute_file_hashes([str(file_a), str(file_b)])

            # Verify when file_a is expected modified
            check1 = DeterministicTransactionalRecovery.verify_integrity(
                hashes_before, hashes_after, expected_modified=[str(file_a)]
            )
            self.assertTrue(check1["is_clean"])
            self.assertEqual(len(check1["collateral_mutations"]), 0)

            # Mutate file_b unintentionally
            file_b.write_text("corrupted B", encoding="utf-8")
            hashes_after_corrupt = DeterministicTransactionalRecovery.compute_file_hashes([str(file_a), str(file_b)])
            check2 = DeterministicTransactionalRecovery.verify_integrity(
                hashes_before, hashes_after_corrupt, expected_modified=[str(file_a)]
            )
            self.assertFalse(check2["is_clean"])
            self.assertEqual(len(check2["collateral_mutations"]), 1)

    def test_08_cpm_cycle_deadlock_detection(self):
        """Tests that cyclic task graphs raise ValueError in CPM scheduler."""
        cyclic_tasks = [
            {"id": "A", "duration": 2, "predecessors": ["B"]},
            {"id": "B", "duration": 3, "predecessors": ["A"]},
        ]
        with self.assertRaises(ValueError):
            DeterministicCPMScheduler.calculate_schedule(cyclic_tasks)

    def test_09_cpm_cycle_detailed_diagnostics_and_remediation(self):
        """Asserts that cyclic task graphs raise DAGCycleError with cycle path and remediation."""
        cyclic_tasks = [
            {"id": "Alpha", "duration": 2, "predecessors": ["Gamma"]},
            {"id": "Beta", "duration": 3, "predecessors": ["Alpha"]},
            {"id": "Gamma", "duration": 1, "predecessors": ["Beta"]},
        ]
        with self.assertRaises(DAGCycleError) as ctx:
            DeterministicCPMScheduler.calculate_schedule(cyclic_tasks)

        err = ctx.exception
        self.assertIsInstance(err, ValueError)  # Backward-compatible subclass
        self.assertIn("Alpha", err.cycle)
        self.assertIn("Beta", err.cycle)
        self.assertIn("Gamma", err.cycle)
        self.assertEqual(len(err.unresolved_tasks), 3)
        self.assertIn("Remove dependency", err.remediation)

    def test_10_router_telemetry_tracking_and_state_transitions(self):
        """Validates that router telemetry records request counts, latency, and status."""
        initial_telem = FleetFirstBridge.get_router_telemetry()
        self.assertIn("port_1234_online", initial_telem)
        self.assertIn("current_state", initial_telem)
        self.assertIn("total_requests", initial_telem)
        self.assertIn("fallback_count", initial_telem)

        # Trigger routing call to record metrics
        res = FleetFirstBridge.route_intent("Build an embedded firmware driver for STM32 SPI")
        self.assertEqual(res["primary_skill"], "embedded-firmware-scaffold")

        post_telem = FleetFirstBridge.get_router_telemetry()
        self.assertGreater(post_telem["total_requests"], 0)
        self.assertIsNotNone(post_telem["last_latency_ms"])

    def test_11_fleet_task_manifest_contract_compatibility(self):
        """Asserts that generated Fleet task manifests satisfy both SCHEMA.md and legacy contracts."""
        manifest = FleetFirstBridge.create_fleet_task_manifest(
            title="Implement Kalman Filter for Radar Tracking",
            repo="brainstorm",
            prompt="Scaffold high-throughput Kalman filter in sim/kalman.py",
            priority="high",
            kind="code",
        )
        # Canonical Fleet-Orchestrator SCHEMA.md assertions
        self.assertIn("id", manifest)
        self.assertTrue(manifest["id"].startswith("task_"))
        self.assertEqual(manifest["kind"], "code")
        self.assertEqual(manifest["status"], "pending")
        self.assertIsNone(manifest["owner_account"])
        self.assertIn("spec", manifest)
        self.assertEqual(manifest["created_by"], "adaptive-workflow")
        self.assertIn("created_at", manifest)

        # Legacy & Ecosystem compatibility assertions
        self.assertIn("task_id", manifest)
        self.assertTrue(manifest["task_id"].startswith("TASK-"))
        self.assertIn("prompt", manifest)
        self.assertEqual(manifest["title"], "Implement Kalman Filter for Radar Tracking")
        self.assertEqual(manifest["priority"], "high")

    def test_12_windows_resilient_cleanup(self):
        """Verifies resilient unlinking and rmtree handle read-only attributes without crashing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / "locked_dir"
            test_dir.mkdir()
            test_file = test_dir / "readonly_file.txt"
            test_file.write_text("protected content", encoding="utf-8")

            # Set read-only attribute on file
            test_file.chmod(stat.S_IREAD)

            # Test resilient_unlink
            unlink_success = resilient_unlink(test_file)
            self.assertTrue(unlink_success)
            self.assertFalse(test_file.exists())

            # Create another read-only file inside test_dir and test resilient_rmtree
            sub_file = test_dir / "sub_readonly.txt"
            sub_file.write_text("sub content", encoding="utf-8")
            sub_file.chmod(stat.S_IREAD)

            rmtree_success = resilient_rmtree(test_dir)
            self.assertTrue(rmtree_success)
            self.assertFalse(test_dir.exists())

    def test_13_adaptive_rate_governor(self):
        """Validates rate governor alpha damping, hysteresis M halving, 120s recovery, and ramp."""
        AdaptiveRateGovernor.reset()

        # Latency damping
        self.assertEqual(AdaptiveRateGovernor.calculate_alpha(1000.0), 1.0)
        self.assertEqual(AdaptiveRateGovernor.calculate_alpha(1200.0), 1.0)
        self.assertEqual(AdaptiveRateGovernor.calculate_alpha(1800.0), 0.75)
        # Latency 2500 ms: e_L = 1300/1200 ~ 1.083 -> 1 - 0.5 * 1.083 ~ 0.458
        self.assertAlmostEqual(AdaptiveRateGovernor.calculate_alpha(2500.0), 0.458, places=2)
        # Latency 3360 ms: e_L = 2160/1200 = 1.8 -> clamped to 0.1
        self.assertEqual(AdaptiveRateGovernor.calculate_alpha(3360.0), 0.1)

        # Regulated concurrency u(t) = max(1, floor(base_workers * alpha * M))
        # At base=27, L=1800 (alpha=0.75), M=1.0: 27 * 0.75 * 1.0 = 20.25 -> 20
        self.assertEqual(AdaptiveRateGovernor.calculate_concurrency(27, 1800.0), 20)

        # 429 excursion handling
        m1, exc1 = AdaptiveRateGovernor.record_rate_limit(current_time=100.0)
        self.assertEqual(m1, 1.0)
        self.assertFalse(exc1)  # Single isolated 429 in nominal state does not trigger halving

        # Second 429 within 60s triggers halving
        m2, exc2 = AdaptiveRateGovernor.record_rate_limit(current_time=120.0)
        self.assertEqual(m2, 0.5)
        self.assertTrue(exc2)
        status = AdaptiveRateGovernor.get_status()
        self.assertEqual(status["multiplier"], 0.5)
        self.assertEqual(status["recovery_until"], 240.0)

        # While M < 1.0, any new 429 immediately cuts M
        m3, exc3 = AdaptiveRateGovernor.record_rate_limit(current_time=130.0)
        self.assertEqual(m3, 0.25)
        self.assertTrue(exc3)
        self.assertEqual(AdaptiveRateGovernor.get_status()["recovery_until"], 250.0)

        # Checkpoint recovery: before recovery_until, multiplier does not ramp
        AdaptiveRateGovernor.record_checkpoint(success=True, current_time=200.0)
        self.assertEqual(AdaptiveRateGovernor.get_status()["multiplier"], 0.25)

        # After recovery_until has elapsed, each checkpoint ramps by +0.1
        AdaptiveRateGovernor.record_checkpoint(success=True, current_time=255.0)
        self.assertEqual(AdaptiveRateGovernor.get_status()["multiplier"], 0.35)
        AdaptiveRateGovernor.record_checkpoint(success=True, current_time=260.0)
        self.assertEqual(AdaptiveRateGovernor.get_status()["multiplier"], 0.45)

    def test_14_temp_repo_snapshot_rollback(self):
        """Verifies transactional recovery snapshot creation and rollback in an isolated Git repository."""
        import subprocess
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            # Initialize temp git repo
            subprocess.run(["git", "init"], cwd=str(repo_path), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git", "config", "user.name", "TestRunner"], cwd=str(repo_path), check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=str(repo_path), check=True)

            # Create initial file and commit
            tracked_file = repo_path / "target.txt"
            tracked_file.write_text("v1.0.0 initial baseline", encoding="utf-8")
            subprocess.run(["git", "add", "target.txt"], cwd=str(repo_path), check=True)
            subprocess.run(["git", "commit", "-m", "initial commit"], cwd=str(repo_path), check=True, stdout=subprocess.DEVNULL)

            # Create snapshot
            ok, msg = DeterministicTransactionalRecovery.create_snapshot(tag="test-snap", repo_root=str(repo_path))
            self.assertTrue(ok)

            # Mutate and commit change
            tracked_file.write_text("v2.0.0 broken regression", encoding="utf-8")
            subprocess.run(["git", "commit", "-am", "bad commit"], cwd=str(repo_path), check=True, stdout=subprocess.DEVNULL)
            self.assertEqual(tracked_file.read_text(encoding="utf-8"), "v2.0.0 broken regression")

            # Rollback to snapshot
            ok_roll, msg_roll = DeterministicTransactionalRecovery.rollback(snapshot_ref="refs/backup/test-snap", repo_root=str(repo_path))
            self.assertTrue(ok_roll)
            self.assertEqual(tracked_file.read_text(encoding="utf-8"), "v1.0.0 initial baseline")

    def test_15_flight_check_and_worker_concurrency(self):
        """Verifies Antigravity memory headroom, reserve floor (2048 MB), and Banker's worker concurrency."""
        # Test worker concurrency Banker's formula:
        # raw_workers = floor((available - 2048) / 256)
        # <= 2048 MB -> 0
        self.assertEqual(AntigravityMemoryGovernor.calculate_worker_concurrency(2048), 0)
        self.assertEqual(AntigravityMemoryGovernor.calculate_worker_concurrency(2000), 0)
        # 2303 MB -> (2303 - 2048)//256 = 255//256 = 0 (strictly preserves 2048 MB floor!)
        self.assertEqual(AntigravityMemoryGovernor.calculate_worker_concurrency(2303), 0)
        # 2304 MB -> (2304 - 2048)//256 = 256//256 = 1
        self.assertEqual(AntigravityMemoryGovernor.calculate_worker_concurrency(2304), 1)
        # 4096 MB -> (4096 - 2048)//256 = 2048//256 = 8
        self.assertEqual(AntigravityMemoryGovernor.calculate_worker_concurrency(4096), 8)
        # Capped at velocity_cap (default 27)
        self.assertEqual(AntigravityMemoryGovernor.calculate_worker_concurrency(32768), 27)

    def test_16_worktree_gitlink_and_pre_existing_file_guard(self):
        """Verifies get_git_common_dir and PreExistingFileGuard backup/restore in a git worktree."""
        import subprocess
        with tempfile.TemporaryDirectory() as tmpdir:
            base_dir = Path(tmpdir)
            main_repo = base_dir / "main_repo"
            main_repo.mkdir()

            # Init main repo
            subprocess.run(["git", "init"], cwd=str(main_repo), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git", "config", "user.name", "TestRunner"], cwd=str(main_repo), check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=str(main_repo), check=True)

            dummy = main_repo / "dummy.txt"
            dummy.write_text("base", encoding="utf-8")
            subprocess.run(["git", "add", "dummy.txt"], cwd=str(main_repo), check=True)
            subprocess.run(["git", "commit", "-m", "init"], cwd=str(main_repo), check=True, stdout=subprocess.DEVNULL)

            # Create worktree
            wt_path = base_dir / "wt"
            subprocess.run(["git", "worktree", "add", str(wt_path)], cwd=str(main_repo), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Assert get_git_common_dir resolves to main repo's .git
            common_git = get_git_common_dir(wt_path)
            self.assertEqual(common_git.resolve(), (main_repo / ".git").resolve())

            # Test PreExistingFileGuard inside worktree
            pre_file = wt_path / "existing.json"
            pre_file.write_text('{"original": true}', encoding="utf-8")

            # Project existing.json and new_file.json
            untracked = PreExistingFileGuard.prepare_projection(
                task_id="task-wt-01",
                worktree_root=wt_path,
                projected_paths=["existing.json", "new_file.json"],
                repo_root=main_repo,
            )
            self.assertEqual(untracked, ["new_file.json"])

            # Simulate worker modifying existing.json and creating new_file.json
            pre_file.write_text('{"polluted": true}', encoding="utf-8")
            new_file = wt_path / "new_file.json"
            new_file.write_text('{"ephemeral": true}', encoding="utf-8")

            # Teardown projection
            PreExistingFileGuard.teardown_projection(
                task_id="task-wt-01",
                worktree_root=wt_path,
                untracked_created=untracked,
                repo_root=main_repo,
            )

            # Assert existing.json restored, new_file.json unlinked
            self.assertEqual(pre_file.read_text(encoding="utf-8"), '{"original": true}')
            self.assertFalse(new_file.exists())

    def test_17_orchestrator_fencing_manager(self):
        """Verifies monotonic fencing token generation and rejection of stale worker branch merges."""
        t1 = OrchestratorFencingManager.acquire_lease("task-fence-99")
        self.assertEqual(t1, 1)
        self.assertTrue(OrchestratorFencingManager.verify_branch_merge("task-fence-99", 1))

        # Stale worker with token 1 tries to merge after lease eviction
        t2 = OrchestratorFencingManager.evict_stale_lease("task-fence-99")
        self.assertEqual(t2, 2)

        # Worker 1 rejected!
        self.assertFalse(OrchestratorFencingManager.verify_branch_merge("task-fence-99", 1))
        # Worker 2 accepted
        self.assertTrue(OrchestratorFencingManager.verify_branch_merge("task-fence-99", 2))

    def test_18_calm_authority_zero_rpg_and_emojis(self):
        """Asserts zero RPG terms and zero emojis across all tools/skills/adaptive-workflow/ markdown files."""
        import re
        target_dir = Path(BRAINSTORM_ROOT) / "tools" / "skills" / "adaptive-workflow"
        if not target_dir.exists():
            self.skipTest("Target skill directory does not exist")

        rpg_pattern = re.compile(r"\b(High\s+Lord|Sovereign|Fleet\s+Army|Supreme\s+Architect)\b", re.IGNORECASE)
        emoji_pattern = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u26FF\u2700-\u27BF\uFE0F]")

        rpg_violations = []
        emoji_violations = []

        for p in target_dir.rglob("*.md"):
            rel = p.relative_to(target_dir).as_posix()
            content = p.read_text(encoding="utf-8")
            for idx, line in enumerate(content.splitlines(), 1):
                if rpg_pattern.search(line):
                    rpg_violations.append(f"{rel}:{idx}: {line.strip()}")
                if emoji_pattern.search(line):
                    emoji_violations.append(f"{rel}:{idx}: {line.strip()}")

        self.assertEqual(rpg_violations, [], f"RPG terms found in adaptive-workflow docs: {rpg_violations}")
        self.assertEqual(emoji_violations, [], f"Emojis found in adaptive-workflow docs: {emoji_violations}")

    @mock.patch.object(FleetFirstBridge, "is_lm_studio_online", return_value=False)
    def test_19_colab_intent_routing_and_aliases(self, _mock_online):
        """Verifies Colab Cloud Accelerator heuristic routing and skill aliases."""
        # Test alias resolution
        self.assertEqual(FleetFirstBridge.SKILL_ALIASES.get("colab"), "colab-cloud-accelerator")
        self.assertEqual(FleetFirstBridge.SKILL_ALIASES.get("colab-mcp"), "colab-cloud-accelerator")
        self.assertEqual(FleetFirstBridge.SKILL_ALIASES.get("colab-accelerator"), "colab-cloud-accelerator")

        # Test heuristic intent routing when LM Studio is offline
        res1 = FleetFirstBridge.route_intent("Fine-tune Qwen LoRA model on Colab L4 GPU")
        self.assertEqual(res1["primary_skill"], "colab-cloud-accelerator")
        self.assertEqual(res1["archetype"], "SWARM_ORCHESTRATION")

        res2 = FleetFirstBridge.route_intent("Run CUDA benchmark in cloud TPU accelerator")
        self.assertEqual(res2["primary_skill"], "colab-cloud-accelerator")


if __name__ == "__main__":
    unittest.main()

