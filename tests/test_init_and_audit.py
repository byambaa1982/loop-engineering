from pathlib import Path

from loop_engineering.audit import audit_repository
from loop_engineering.initializer import initialize_loop


def test_initialize_loop_creates_expected_files(tmp_path: Path) -> None:
    result = initialize_loop(tmp_path, pattern_slug="pr-babysitter")
    paths = {item.path for item in result if item.action == "created"}

    assert "LOOP.md" in paths
    assert "STATE.md" in paths
    assert "loop-budget.md" in paths
    assert "loop-run-log.md" in paths
    assert ".github/copilot-instructions.md" in paths
    assert "PR Babysitter" in (tmp_path / "LOOP.md").read_text(encoding="utf-8")


def test_initialize_loop_skips_existing_files(tmp_path: Path) -> None:
    initialize_loop(tmp_path)
    result = initialize_loop(tmp_path)

    skipped = {item.path for item in result if item.action == "skipped"}
    assert "LOOP.md" in skipped
    assert "STATE.md" in skipped


def test_audit_repository_scores_initialized_project(tmp_path: Path) -> None:
    result = audit_repository(Path.cwd())

    assert result.score >= 80
    assert result.failed <= 3
