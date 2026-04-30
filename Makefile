.PHONY: install install-dev test lint validate ci

install:
	python -m pip install -e ".[experiment,quantum]"

install-dev:
	python -m pip install -e ".[dev]"

test:
	python -m pytest

lint:
	python -m ruff check .

validate:
	python scripts/validate_notebooks.py

ci: lint test validate
