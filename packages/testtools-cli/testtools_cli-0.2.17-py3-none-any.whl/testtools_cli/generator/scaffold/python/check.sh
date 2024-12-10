#!/usr/bin/env bash

set -exu -o pipefail

uv sync --all-extras --dev
uv run ruff format src
uv run ruff format tests
uv run ruff check src
uv run ruff check tests
uv run mypy src --strict
uv run pytest tests --durations=5 --cov=. --cov-fail-under=90 --cov-report term
uv export --no-dev --locked >requirements.txt