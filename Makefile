# Makefile for cursor-analytics project

.PHONY: all setup_env lint test clean

VENV_NAME = venv
PYTHON = python3

# Load environment variables
ifneq (,$(wildcard .env))
	include .env
	export
endif

# Default target
all: setup_env

# Setup the Python virtual environment and install dependencies
setup_env:
	@echo "--- Setting up virtual environment ($(VENV_NAME)) ---"
	$(PYTHON) -m venv $(VENV_NAME)
	$(CURDIR)/$(VENV_NAME)/bin/pip install --upgrade pip
	$(CURDIR)/$(VENV_NAME)/bin/pip install -r requirements.txt
	@echo ""
	@echo ">>> Virtual environment '$(VENV_NAME)' created and dependencies installed."
	@echo ">>> Activate it by running: source $(VENV_NAME)/bin/activate"

# Lint the codebase
lint:
	@echo "--- Running linters ---"
	$(VENV_NAME)/bin/black . --line-length 100
	$(VENV_NAME)/bin/isort . --profile black --line-length 100 --skip $(VENV_NAME)
	$(VENV_NAME)/bin/flake8 . --max-line-length 100 --extend-ignore E203,D100,D104,D101,D102,D103,D105,D106,D107 --exclude .git,__pycache__,$(VENV_NAME),build,dist,data-dev-env,output
	$(VENV_NAME)/bin/mypy . --ignore-missing-imports --disallow-untyped-defs --disallow-incomplete-defs --exclude '^(venv/|tests/|examples/|output/|docs/|config/)$$'
	@echo "--- Linting complete ---"

# Run tests
test:
	@echo "--- Running tests ---"
	$(VENV_NAME)/bin/pytest tests/
	@echo "--- Testing complete ---"

# Clean up the environment
clean:
	@echo "--- Cleaning up ---"
	rm -rf $(VENV_NAME)
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -f .coverage
	@echo "--- Cleanup complete ---"

# Help target
help:
	@echo "Available targets:"
	@echo "  setup_env   - Sets up the Python virtual environment and installs dependencies."
	@echo "  lint        - Runs linters (black, isort, flake8, mypy)."
	@echo "  test        - Runs pytest on the 'tests/' directory."
	@echo "  clean       - Removes the virtual environment and cache files."
	@echo "  all         - (Default) Alias for setup_env." 