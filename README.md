# loop-engineering

Python CLI tools and starter assets for loop engineering with AI coding agents.

Loop engineering is the practice of designing repeatable, observable, reviewable feedback loops around AI coding agents. This repository provides a Python package inspired by the practical pattern library and CLI shape of the original JavaScript loop-engineering project, while keeping the implementation idiomatic Python.

## What Is Included

- `loop init` creates loop operating documents for a repository.
- `loop audit` checks whether a repository has the minimum loop documents, guardrails, budget, run log, and pattern registry.
- `loop cost` estimates token, tool, and human-review costs for recurring agent runs.
- `loop patterns` lists built-in loop patterns such as daily triage, PR follow-up, dependency sweeping, and post-merge cleanup.
- `patterns/`, `starters/`, `templates/`, and `docs/` provide starter content for teams adopting agent loops.

## Install For Development

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## CLI Usage

Create loop starter documents in the current repository:

```bash
loop init --pattern daily-triage
```

Inspect available patterns:

```bash
loop patterns
loop patterns pr-babysitter
```

Audit loop readiness:

```bash
loop audit .
loop audit . --format json
loop audit . --fail-under 80
```

Estimate recurring loop cost:

```bash
loop cost \
	--agent-runs 20 \
	--input-tokens 1000000 \
	--output-tokens 200000 \
	--input-per-million 3 \
	--output-per-million 15 \
	--review-minutes 200 \
	--review-hourly-rate 120
```

The standalone entry points are also available:

```bash
loop-init
loop-audit
loop-cost
```

## Repository Documents

`loop init` creates these files:

- `LOOP.md`: operating contract, inputs, outputs, and safety checks.
- `STATE.md`: current loop status, autonomy level, cadence, and next review.
- `loop-budget.md`: rough recurring cost and review budget.
- `loop-run-log.md`: evidence trail for each run.
- `.github/copilot-instructions.md`: basic agent operating rules for the repository.

## Built-In Patterns

The initial pattern catalog is intentionally small:

- `daily-triage`: report-only issue clustering and routing.
- `pr-babysitter`: reviewed pull request follow-up.
- `dependency-sweeper`: weekly dependency update batches.
- `post-merge-cleanup`: supervised documentation and release hygiene after merge.

Each pattern is defined in Python in the package and summarized in `patterns/registry.json` for tooling and documentation.

## Development

Run tests with:

```bash
pytest
```

Run a quick local smoke test without installing:

```bash
PYTHONPATH=src python -m loop_engineering patterns
PYTHONPATH=src python -m loop_engineering cost --input-tokens 1000 --output-tokens 1000
```
