# LOOP

## Daily Triage

Cluster new issues, identify likely owners, and prepare a reviewable triage report.

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
- new issues
- stale unlabelled issues
- support handoff

## Outputs
- triage report
- suggested labels
- owner candidates

## Guardrails And Safety Checks
- report-only
- human assigns labels
- link every recommendation to evidence
