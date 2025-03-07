.PHONY: setup venv clean install dev test run lint format

# Variables
VENV_NAME := venv
PYTHON := python3
PIP := $(VENV_NAME)/bin/pip
PYTHON_VENV := $(VENV_NAME)/bin/python

# Default target
all: setup

# Create virtual environment
venv:
	$(PYTHON) -m venv $(VENV_NAME)

# Set up the development environment
setup: venv
	$(PIP) install --upgrade pip
	$(PIP) install -e .

# Install dependencies for development
dev: venv
	$(PIP) install -e ".[dev]"

# Install dependencies for production
install: venv
	$(PIP) install .

# Run tests
test: venv
	$(PYTHON_VENV) -m pytest

# Run the Tetris game
run: venv
	$(PYTHON_VENV) -m tetris

# Record a demo of the Tetris game
record-demo: venv
	$(PYTHON_VENV) -m tetris --record-demo

# Lint the code
lint: venv
	$(PYTHON_VENV) -m flake8 src tests
	$(PYTHON_VENV) -m mypy src tests

# Format the code
format: venv
	$(PYTHON_VENV) -m black src tests

# Clean up generated files
clean:
	rm -rf $(VENV_NAME)
	rm -rf *.egg-info
	rm -rf build/
	rm -rf dist/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

# Show help
help:
	@echo "Available targets:"
	@echo "  make setup       - Create virtualenv and install dependencies"
	@echo "  make dev         - Install development dependencies"
	@echo "  make install     - Install package"
	@echo "  make test        - Run tests"
	@echo "  make run         - Run the Tetris game"
	@echo "  make record-demo - Record a demo of the Tetris game"
	@echo "  make lint        - Run linters (flake8, mypy)"
	@echo "  make format      - Format code with black"
	@echo "  make clean       - Remove virtualenv and build artifacts"
