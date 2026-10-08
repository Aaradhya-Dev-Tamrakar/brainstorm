# ==============================================================================
# Makefile - Canonical Evaluator & Cross-Platform Task Dispatcher
# Conforms to github-workflow v1.3.0 Evaluator & Decluttering Standard
# ==============================================================================

.PHONY: all help audit test verify sim reconcile clean

PYTHON ?= python3
ifeq ($(OS),Windows_NT)
    PYTHON := python
endif

all: verify

help: ## Show this help message
	@echo "Brainstorm Ecosystem Task Dispatcher"
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'

audit: ## Run deterministic structural audit (0 discrepancies gate)
	$(PYTHON) sim/reconciliation_engine.py

reconcile: ## Auto-reconcile cross-document counts and invariant ledgers
	$(PYTHON) sim/reconciliation_engine.py --fix

test: ## Execute dynamic behavioral simulation unit test suite
	$(PYTHON) -m unittest discover -s sim -p "test_*.py"

sim: ## Run warehouse memory discrete-event simulation
	$(PYTHON) sim/warehouse_mem_sim.py

verify: ## Run full dual-layer verification gate and ledger certification
	$(PYTHON) tools/validate_ecosystem.py
	$(PYTHON) sim/reconciliation_engine.py --ledger
	$(PYTHON) -m unittest discover -s sim -p "test_*.py"
	$(PYTHON) sim/task_telemetry.py --test

clean: ## Clean cache and temporary artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
