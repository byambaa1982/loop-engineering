# STATE

Loop: Daily Triage
Pattern: daily-triage
Autonomy: L1
Cadence: daily
Owner: engineering
Created: 2026-06-23

## Purpose
Cluster new issues, identify likely owners, and prepare a reviewable triage report.

## Agent
AI coding agent operating under human review until promoted.

## Triggers
- new issues
- stale unlabelled issues
- support handoff

## Guardrails
- report-only
- human assigns labels
- link every recommendation to evidence

## Outputs
- triage report
- suggested labels
- owner candidates

## Current Status
- Phase: design
- Last run: never
- Next review: before first automated action
