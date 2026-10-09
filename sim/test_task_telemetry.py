"""
test_task_telemetry.py
-----------------------
Unit tests for sim/task_telemetry.py.
"""

import unittest
from sim.task_telemetry import (
    get_utc_now,
    ensure_telemetry_dir,
    load_tasks,
    run_self_test
)


class TestTaskTelemetry(unittest.TestCase):

    def test_utc_now_format(self):
        now = get_utc_now()
        self.assertIsInstance(now, str)
        self.assertIn("T", now)
        self.assertTrue(now.endswith("Z") or "+00:00" in now)

    def test_ensure_telemetry_dir(self):
        # ensure_telemetry_dir creates directory and returns None without error
        res = ensure_telemetry_dir()
        self.assertIsNone(res)

    def test_load_tasks(self):
        tasks = load_tasks()
        self.assertIsInstance(tasks, dict)

    def test_run_self_test(self):
        # run_self_test returns 0 on success
        res = run_self_test()
        self.assertEqual(res, 0, "Task telemetry self-test returned non-zero exit code")


if __name__ == "__main__":
    unittest.main()
