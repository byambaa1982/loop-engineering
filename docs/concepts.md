# Loop Engineering Concepts

Loop engineering is the practice of designing repeatable feedback loops around AI coding agents. The goal is not to make an agent do everything; the goal is to make useful automation observable, bounded, reviewable, and cheap enough to run repeatedly.

## Core Primitive

A loop combines:

- Trigger: the event that starts the loop.
- Context: the files, issues, docs, and state the agent may use.
- Agent task: the bounded operation the agent performs.
- Guardrails: hard limits, review gates, and stop conditions.
- Output: a report, patch, pull request, or handoff note.
- Log: evidence of cost, result, reviewer, and follow-up.

## Autonomy Levels

- L1 assisted: report-only, no repository changes.
- L2 reviewed: changes are allowed, but a human reviews every action.
- L3 supervised: recurring loop with explicit gates and rollback notes.
- L4 automated: narrow, low-risk loop with strong observability and owner accountability.

Prefer L1 or L2 until the loop has enough evidence to earn more autonomy.
