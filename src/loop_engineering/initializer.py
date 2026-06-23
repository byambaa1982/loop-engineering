from __future__ import annotations

from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path

from .patterns import get_pattern, list_patterns
from .rendering import render_budget, render_loop_doc, render_run_log, render_state


@dataclass(frozen=True)
class CreatedFile:
    path: str
    action: str


TEMPLATE_PACKAGE = "loop_engineering.data"
DEFAULT_TEMPLATE_FILES = {
    "copilot-instructions.md.template": ".github/copilot-instructions.md",
}


def initialize_loop(root: str | Path, *, pattern_slug: str = "daily-triage", force: bool = False) -> tuple[CreatedFile, ...]:
    root_path = Path(root).expanduser().resolve()
    created: list[CreatedFile] = []
    pattern = get_pattern(pattern_slug)
    generated_files = {
        "LOOP.md": render_loop_doc(pattern),
        "STATE.md": render_state(pattern),
        "loop-budget.md": render_budget(),
        "loop-run-log.md": render_run_log(),
    }
    for destination_name, content in generated_files.items():
        destination = root_path / destination_name
        if destination.exists() and not force:
            created.append(CreatedFile(path=_relative(destination, root_path), action="skipped"))
            continue
        existed = destination.exists()
        destination.write_text(content, encoding="utf-8")
        created.append(CreatedFile(path=_relative(destination, root_path), action="written" if existed else "created"))

    for template_name, destination_name in DEFAULT_TEMPLATE_FILES.items():
        destination = root_path / destination_name
        template = files(TEMPLATE_PACKAGE).joinpath("templates", template_name)
        if destination.exists() and not force:
            created.append(CreatedFile(path=_relative(destination, root_path), action="skipped"))
            continue
        existed = destination.exists()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
        created.append(CreatedFile(path=_relative(destination, root_path), action="written" if existed else "created"))

    for directory in ("patterns", "starters", "templates", "docs"):
        path = root_path / directory
        path.mkdir(parents=True, exist_ok=True)
        readme = path / "README.md"
        if not readme.exists() or force:
            readme.write_text(_starter_readme(directory), encoding="utf-8")
            created.append(CreatedFile(path=_relative(readme, root_path), action="created"))
    return tuple(created)


def _starter_readme(directory: str) -> str:
    titles = {
        "patterns": "Loop Patterns",
        "starters": "Loop Starters",
        "templates": "Loop Templates",
        "docs": "Loop Engineering Docs",
    }
    return f"# {titles[directory]}\n\nUse this directory to capture reusable {directory} for agent loops.\n"


def available_patterns() -> tuple[str, ...]:
    return tuple(pattern.slug for pattern in list_patterns())


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()
