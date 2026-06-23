from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from .models import LoopPattern


def render_state(pattern: LoopPattern) -> str:
    return f"""# STATE

Loop: {pattern.name}
Pattern: {pattern.slug}
Autonomy: {pattern.autonomy.value}
Cadence: {pattern.cadence}
Owner: {pattern.owner}
Created: {datetime.now(UTC).date().isoformat()}

## Purpose
{pattern.summary}

## Agent
AI coding agent operating under human review until promoted.

## Triggers
{bullet_list(pattern.triggers)}

## Guardrails
{bullet_list(pattern.guardrails)}

## Outputs
{bullet_list(pattern.outputs)}

## Current Status
- Phase: design
- Last run: never
- Next review: before first automated action
"""


def render_loop_doc(pattern: LoopPattern) -> str:
    return f"""# LOOP

## {pattern.name}

{pattern.summary}

## Purpose
Create a repeatable engineering loop that an agent can execute with clear inputs, review gates, and stop conditions.

## Agent
Use an AI coding agent for bounded analysis, patches, and handoff notes. Keep a human owner accountable for promotion, rollback, and final review.

## Operating Contract
- Start in report-only mode until maintainers trust the output.
- Keep every run small enough for a human reviewer to audit quickly.
- Record assumptions, commands, costs, and handoff notes in the run log.
- Promote autonomy only after repeated successful runs with clear rollback paths.

## Triggers And Inputs
{bullet_list(pattern.triggers)}

## Outputs
{bullet_list(pattern.outputs)}

## Guardrails And Safety Checks
{bullet_list(pattern.guardrails)}
"""


def render_budget() -> str:
    return """# loop-budget

Use this budget before scheduling a recurring agent loop.

| Item | Estimate |
| --- | ---: |
| Runs per month | 20 |
| Input tokens per run | 50,000 |
| Output tokens per run | 10,000 |
| Human review minutes per run | 10 |
| Monthly budget limit | TBD |
| Rollback owner | TBD |

## Cost Notes
- Prefer smaller context windows over broad repository scans.
- Cache stable documentation and architecture notes where possible.
- Stop the loop when repeated runs produce no meaningful changes.
"""


def render_run_log() -> str:
    return """# loop-run-log

| Date | Run | Pattern | Mode | Outcome | Cost | Reviewer | Notes |
| --- | --- | --- | --- | --- | ---: | --- | --- |
"""


def write_text(path: Path, content: str, force: bool = False) -> bool:
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def bullet_list(items: tuple[str, ...]) -> str:
    return "\n".join(f"- {item}" for item in items)
