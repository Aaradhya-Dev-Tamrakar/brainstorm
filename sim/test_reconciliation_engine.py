"""
test_reconciliation_engine.py
------------------------------
Unit tests for sim/reconciliation_engine.py helper functions.
"""

import os
import unittest
from sim.reconciliation_engine import (
    get_ecosystem_module_counts,
    get_physical_research_artifacts,
    parse_simple_yaml_capabilities,
    SCHEMAS_DIR
)


class TestReconciliationEngine(unittest.TestCase):

    def test_get_ecosystem_module_counts(self):
        ereg_data, modules, total, comp, pres = get_ecosystem_module_counts()
        self.assertIsInstance(ereg_data, dict)
        self.assertIsInstance(modules, list)
        self.assertGreater(total, 0)
        self.assertEqual(comp + pres, total)

    def test_get_physical_research_artifacts(self):
        arch, exp, inv, total = get_physical_research_artifacts()
        self.assertIsInstance(arch, list)
        self.assertIsInstance(exp, list)
        self.assertIsInstance(inv, list)
        self.assertGreater(total, 0)
        self.assertEqual(len(arch) + len(exp) + len(inv), total)

    def test_parse_simple_yaml_capabilities(self):
        registry_path = os.path.join(SCHEMAS_DIR, "capability-registry.yaml")
        if os.path.exists(registry_path):
            caps = parse_simple_yaml_capabilities(registry_path)
            self.assertIsInstance(caps, list)
            self.assertGreater(len(caps), 0)


if __name__ == "__main__":
    unittest.main()
