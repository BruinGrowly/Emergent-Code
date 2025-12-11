# Makefile for Emergent Code
# Provides convenient shortcuts for common development tasks

.PHONY: help install install-dev test lint format check clean validate run-experiments

help:
	@echo "Emergent Code - Development Commands"
	@echo "====================================="
	@echo ""
	@echo "Setup:"
	@echo "  make install      Install production dependencies"
	@echo "  make install-dev  Install development dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test         Run all tests and experiments"
	@echo "  make validate     Validate fractal proof"
	@echo "  make test-harmonizer  Test harmonizer integration"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint         Run linting checks"
	@echo "  make format       Auto-format code with black"
	@echo "  make check        Run all checks (lint + format check + type check)"
	@echo ""
	@echo "Experiments:"
	@echo "  make run-experiments  Run all fractal experiments"
	@echo "  make level1       Run Level 1 experiment"
	@echo "  make level2       Run Level 2 experiment"
	@echo "  make level3       Run Level 3 experiment"
	@echo "  make level4       Run Level 4 experiment"
	@echo "  make level5       Run Level 5 experiment"
	@echo "  make level6       Run Level 6 experiment"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        Remove generated files and caches"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

# Testing
test:
	python3 run_all_tests.py

validate:
	python3 validate_fractal_proof.py

test-harmonizer:
	python3 test_harmonizer.py

# Code Quality
lint:
	@echo "Running ruff..."
	ruff check .
	@echo "✅ Linting passed!"

format:
	@echo "Formatting code with black..."
	black .
	@echo "✅ Code formatted!"

check: format lint
	@echo "Running type check..."
	mypy master_grower.py calculator_components.py harmonizer_integration.py || true
	@echo "✅ All checks complete!"

# Experiments
run-experiments:
	@echo "Running all fractal experiments..."
	python3 run_all_tests.py

level1:
	python3 experiments/composition_discovery.py

level2:
	python3 experiments/fractal_composition_level2.py

level3:
	python3 experiments/fractal_level3_modules.py

level4:
	python3 experiments/fractal_level4_packages.py

level5:
	python3 experiments/fractal_level5_applications.py

level6:
	python3 experiments/fractal_level6_platforms.py

# Cleanup
clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ 2>/dev/null || true
	@echo "✅ Cleanup complete!"

# Build and distribute
build:
	python3 -m build

dist-check: build
	twine check dist/*

dist-test: dist-check
	twine upload --repository testpypi dist/* --skip-existing

# Git shortcuts
git-status:
	git status

git-diff:
	git diff

# Pre-commit
pre-commit-install:
	pre-commit install

pre-commit-run:
	pre-commit run --all-files
