# Convenience commands. Windows users without `make` should run the
# equivalent Python commands documented in docs/setup.md.

PYTHON ?= python

.PHONY: help setup test test-cov lint format format-check typecheck validate \
        notebooks review report clean-notebooks clean

help:
	@echo "Available targets:"
	@echo "  setup            Install dev dependencies into the active environment"
	@echo "  test             Run pytest"
	@echo "  test-cov         Run pytest with coverage"
	@echo "  lint             Run ruff check"
	@echo "  format           Run ruff format"
	@echo "  format-check     Verify formatting without writing"
	@echo "  typecheck        Run mypy on scripts and src"
	@echo "  validate         Run repository validation"
	@echo "  notebooks        Validate notebook format"
	@echo "  review           Generate the review queue"
	@echo "  report           Generate the progress report"
	@echo "  clean-notebooks  Strip outputs from tracked notebooks (opt-in)"
	@echo "  clean            Remove cache directories"

setup:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest

test-cov:
	$(PYTHON) -m pytest --cov --cov-report=term-missing

lint:
	$(PYTHON) -m ruff check .

format:
	$(PYTHON) -m ruff format .

format-check:
	$(PYTHON) -m ruff format --check .

typecheck:
	$(PYTHON) -m mypy scripts src

validate:
	$(PYTHON) scripts/validate_repository.py

notebooks:
	$(PYTHON) scripts/validate_repository.py --notebooks-only

review:
	$(PYTHON) scripts/generate_review_queue.py

report:
	$(PYTHON) scripts/generate_progress_report.py

clean-notebooks:
	$(PYTHON) scripts/clean_notebook_outputs.py --apply

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache .coverage htmlcov build dist
	find . -type d -name '__pycache__' -not -path './.git/*' -exec rm -rf {} +
