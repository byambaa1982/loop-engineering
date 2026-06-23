from __future__ import annotations

from .models import AutonomyLevel, LoopPattern

PATTERNS: tuple[LoopPattern, ...] = (
    LoopPattern(
        slug="daily-triage",
        name="Daily Triage",
        summary="Cluster new issues, identify likely owners, and prepare a reviewable triage report.",
        autonomy=AutonomyLevel.ASSISTED,
        cadence="daily",
        triggers=("new issues", "stale unlabelled issues", "support handoff"),
        guardrails=("report-only", "human assigns labels", "link every recommendation to evidence"),
        outputs=("triage report", "suggested labels", "owner candidates"),
    ),
    LoopPattern(
        slug="pr-babysitter",
        name="PR Babysitter",
        summary="Watch pull requests for failing checks, reviewer comments, and merge readiness.",
        autonomy=AutonomyLevel.REVIEWED,
        cadence="on pull request activity",
        triggers=("failing checks", "review requested", "merge conflicts"),
        guardrails=("never merge", "small patch size", "tests required before handoff"),
        outputs=("fix branch", "review summary", "risk notes"),
    ),
    LoopPattern(
        slug="dependency-sweeper",
        name="Dependency Sweeper",
        summary="Batch dependency updates into small, testable changes with rollback notes.",
        autonomy=AutonomyLevel.REVIEWED,
        cadence="weekly",
        triggers=("dependabot alerts", "package updates", "security advisories"),
        guardrails=("one ecosystem per run", "lockfile diff required", "security updates first"),
        outputs=("update PR", "changelog summary", "test evidence"),
    ),
    LoopPattern(
        slug="post-merge-cleanup",
        name="Post-Merge Cleanup",
        summary="After merge, remove temporary scaffolding, update docs, and check release notes.",
        autonomy=AutonomyLevel.SUPERVISED,
        cadence="after merge",
        triggers=("merged feature PR", "release branch cut", "docs drift"),
        guardrails=("no product behavior changes", "docs owner review", "audit trail retained"),
        outputs=("cleanup PR", "docs patch", "release note draft"),
    ),
)


def list_patterns() -> tuple[LoopPattern, ...]:
    return PATTERNS


def get_pattern(slug: str) -> LoopPattern:
    normalized = slug.strip().lower()
    for pattern in PATTERNS:
        if pattern.slug == normalized:
            return pattern
    available = ", ".join(pattern.slug for pattern in PATTERNS)
    raise KeyError(f"Unknown pattern '{slug}'. Available patterns: {available}")
