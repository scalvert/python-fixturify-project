#* Variables
SHELL := /usr/bin/env bash
PYTHON := python3
PYTHONPATH := `pwd`

#* Docker variables
IMAGE := python_fixturify_project
VERSION := latest

#* Poetry
.PHONY: poetry-download
poetry-download:
	curl -sSL https://install.python-poetry.org | $(PYTHON) -

.PHONY: poetry-remove
poetry-remove:
	curl -sSL https://install.python-poetry.org | $(PYTHON) - --uninstall

#* Installation
.PHONY: install
install:
	poetry lock -n && poetry export --without-hashes > requirements.txt
	poetry install -n
	-poetry run mypy --install-types --non-interactive ./

.PHONY: pre-commit-install
pre-commit-install:
	poetry run pre-commit install

#* Formatters
.PHONY: format
format:
	poetry run pyupgrade --exit-zero-even-if-changed --py37-plus **/*.py
	poetry run isort --settings-path pyproject.toml ./
	poetry run black --config pyproject.toml ./

.PHONY: test
test:
	PYTHONPATH=$(PYTHONPATH) poetry run pytest -vv -c pyproject.toml --cov-report=html --cov=python_fixturify_project tests/
	poetry run coverage-badge -o assets/images/coverage.svg -f

.PHONY: update-snapshot
update-snapshot:
		PYTHONPATH=$(PYTHONPATH) poetry run pytest --snapshot-update -c pyproject.toml tests/

.PHONY: check-codestyle
check-codestyle:
	poetry run isort --diff --check-only --settings-path pyproject.toml ./
	poetry run black --diff --check --config pyproject.toml ./
	poetry run darglint --verbosity 2 python_fixturify_project tests

.PHONY: mypy
mypy:
	poetry run mypy --config-file pyproject.toml ./

.PHONY: check
check:
	poetry check
	poetry run bandit -ll --recursive python_fixturify_project tests

.PHONY: lint
lint: check-codestyle mypy check

.PHONY: update-dev-deps
update-dev-deps:
	poetry add -D bandit@latest darglint@latest "isort[colors]@latest" mypy@latest pre-commit@latest pydocstyle@latest pylint@latest pytest@latest pyupgrade@latest safety@latest coverage@latest coverage-badge@latest pytest-html@latest pytest-cov@latest
	poetry add -D --allow-prereleases black@latest

#* Cleaning
.PHONY: pycache-remove
pycache-remove:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

.PHONY: dsstore-remove
dsstore-remove:
	find . | grep -E ".DS_Store" | xargs rm -rf

.PHONY: mypycache-remove
mypycache-remove:
	find . | grep -E ".mypy_cache" | xargs rm -rf

.PHONY: ipynbcheckpoints-remove
ipynbcheckpoints-remove:
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf

.PHONY: pytestcache-remove
pytestcache-remove:
	find . | grep -E ".pytest_cache" | xargs rm -rf

.PHONY: build-remove
build-remove:
	rm -rf build/

.PHONY: clean
clean: pycache-remove dsstore-remove mypycache-remove ipynbcheckpoints-remove pytestcache-remove
