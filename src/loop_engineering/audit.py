from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class AuditCheck:
    name: str
    passed: bool
    detail: str
    path: str | None = None


@dataclass(frozen=True)
class AuditResult:
    root: str
    checks: tuple[AuditCheck, ...]

    @property
    def passed(self) -> int:
        return sum(1 for check in self.checks if check.passed)

    @property
    def failed(self) -> int:
        return len(self.checks) - self.passed

    @property
    def score(self) -> int:
        if not self.checks:
            return 0
        return round((self.passed / len(self.checks)) * 100)

    def to_dict(self) -> dict[str, object]:
        return {
            "root": self.root,
            "score": self.score,
            "passed": self.passed,
            "failed": self.failed,
            "checks": [asdict(check) for check in self.checks],
        }


REQUIRED_DOCUMENTS = {
    "LOOP.md": ("purpose", "trigger", "agent", "guardrail"),
    "STATE.md": ("status", "owner", "next"),
    "loop-budget.md": ("budget", "token", "limit"),
    "loop-run-log.md": ("run", "outcome", "cost"),
}

RECOMMENDED_PATHS = (
    "patterns",
    "starters",
    "templates",
    "docs",
    ".github",
)


def audit_repository(root: str | Path) -> AuditResult:
    root_path = Path(root).expanduser().resolve()
    checks: list[AuditCheck] = []

    for relative_path, required_terms in REQUIRED_DOCUMENTS.items():
        document = root_path / relative_path
        checks.append(_check_exists(document, root_path))
        if document.exists():
            checks.extend(_check_terms(document, required_terms, root_path))

    for relative_path in RECOMMENDED_PATHS:
        checks.append(_check_recommended_path(root_path / relative_path, root_path))

    checks.append(_check_pattern_registry(root_path))
    checks.append(_check_cli_metadata(root_path))
    return AuditResult(root=str(root_path), checks=tuple(checks))


def render_markdown(result: AuditResult) -> str:
    lines = [
        "# Loop Audit",
        "",
        f"Root: `{result.root}`",
        f"Score: **{result.score}%** ({result.passed} passed, {result.failed} failed)",
        "",
        "| Check | Result | Detail |",
        "| --- | --- | --- |",
    ]
    for check in result.checks:
        status = "PASS" if check.passed else "FAIL"
        detail = check.detail.replace("|", "\\|")
        lines.append(f"| {check.name} | {status} | {detail} |")
    lines.append("")
    return "\n".join(lines)


def _check_exists(path: Path, root: Path) -> AuditCheck:
    relative = _relative(path, root)
    return AuditCheck(
        name=f"required:{relative}",
        passed=path.is_file(),
        detail="present" if path.is_file() else "missing required loop document",
        path=relative,
    )


def _check_terms(path: Path, required_terms: Iterable[str], root: Path) -> list[AuditCheck]:
    text = path.read_text(encoding="utf-8", errors="ignore").lower()
    relative = _relative(path, root)
    checks = []
    for term in required_terms:
        checks.append(
            AuditCheck(
                name=f"content:{relative}:{term}",
                passed=term in text,
                detail=f"mentions `{term}`" if term in text else f"missing `{term}`",
                path=relative,
            )
        )
    return checks


def _check_recommended_path(path: Path, root: Path) -> AuditCheck:
    relative = _relative(path, root)
    return AuditCheck(
        name=f"recommended:{relative}",
        passed=path.exists(),
        detail="present" if path.exists() else "recommended for repeatable loop operations",
        path=relative,
    )


def _check_pattern_registry(root: Path) -> AuditCheck:
    candidates = (root / "patterns" / "registry.json", root / "patterns" / "registry.yaml")
    present = [path for path in candidates if path.is_file()]
    return AuditCheck(
        name="patterns:registry",
        passed=bool(present),
        detail=f"found {_relative(present[0], root)}" if present else "add patterns/registry.json or patterns/registry.yaml",
        path=_relative(present[0], root) if present else "patterns",
    )


def _check_cli_metadata(root: Path) -> AuditCheck:
    present = (root / "pyproject.toml").is_file() or (root / "package.json").is_file()
    return AuditCheck(
        name="tooling:metadata",
        passed=present,
        detail="project metadata found" if present else "add pyproject.toml or package.json",
        path="pyproject.toml" if (root / "pyproject.toml").is_file() else None,
    )


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()
