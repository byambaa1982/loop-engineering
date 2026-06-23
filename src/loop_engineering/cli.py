from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .audit import audit_repository, render_markdown
from .cost import estimate_cost, load_cost_inputs, render_cost_table
from .initializer import available_patterns, initialize_loop
from .patterns import get_pattern, list_patterns


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="loop",
        description="Python tools for designing, auditing, and budgeting AI agent loops.",
    )
    parser.add_argument("--version", action="store_true", help="Show package version and exit.")
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="Create starter loop documents.")
    _add_init_args(init_parser)

    audit_parser = subparsers.add_parser("audit", help="Audit a repository for loop readiness.")
    _add_audit_args(audit_parser)

    cost_parser = subparsers.add_parser("cost", help="Estimate loop execution cost.")
    _add_cost_args(cost_parser)

    patterns_parser = subparsers.add_parser("patterns", help="List or show built-in loop patterns.")
    _add_patterns_args(patterns_parser)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.version:
        from . import __version__

        print(__version__)
        return 0
    if args.command == "init":
        return run_init(args)
    if args.command == "audit":
        return run_audit(args)
    if args.command == "cost":
        return run_cost(args)
    if args.command == "patterns":
        return run_patterns(args)
    parser.print_help()
    return 0


def loop_init_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="loop-init", description="Create starter loop documents.")
    _add_init_args(parser)
    return run_init(parser.parse_args(argv))


def loop_audit_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="loop-audit", description="Audit loop readiness.")
    _add_audit_args(parser)
    return run_audit(parser.parse_args(argv))


def loop_cost_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="loop-cost", description="Estimate loop execution cost.")
    _add_cost_args(parser)
    return run_cost(parser.parse_args(argv))


def run_init(args: argparse.Namespace) -> int:
    created = initialize_loop(args.path, pattern_slug=args.pattern, force=args.force)
    for item in created:
        print(f"{item.action:>7}  {item.path}")
    return 0


def run_patterns(args: argparse.Namespace) -> int:
    if args.slug:
        pattern = get_pattern(args.slug)
        print(f"{pattern.slug}: {pattern.name}")
        print(pattern.summary)
        print(f"Autonomy: {pattern.autonomy.value}")
        print(f"Cadence: {pattern.cadence}")
        print("Guardrails:")
        for guardrail in pattern.guardrails:
            print(f"- {guardrail}")
        return 0
    for pattern in list_patterns():
        print(f"{pattern.slug:<24} {pattern.name} ({pattern.autonomy.value})")
    return 0


def run_audit(args: argparse.Namespace) -> int:
    result = audit_repository(args.path)
    if args.format == "json":
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(render_markdown(result))
    if args.fail_under is not None and result.score < args.fail_under:
        print(f"score {result.score}% is below required {args.fail_under}%", file=sys.stderr)
        return 1
    return 0


def run_cost(args: argparse.Namespace) -> int:
    values = vars(args).copy()
    input_file = values.pop("input", None)
    values.pop("format", None)
    values.pop("version", None)
    values.pop("command", None)
    if input_file:
        values.update(load_cost_inputs(input_file))
    estimate = estimate_cost(**values)
    if args.format == "json":
        print(json.dumps(estimate.to_dict(), indent=2))
    else:
        print(render_cost_table(estimate))
    return 0


def _add_init_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("path", nargs="?", default=".", help="Repository path to initialize.")
    parser.add_argument("--pattern", choices=available_patterns(), default="daily-triage")
    parser.add_argument("--force", action="store_true", help="Overwrite existing starter files.")


def _add_audit_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("path", nargs="?", default=".", help="Repository path to audit.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--fail-under", type=int, default=None, help="Exit non-zero below this score.")


def _add_cost_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--input", type=Path, help="JSON file with cost inputs.")
    parser.add_argument("--agent-runs", type=int, default=1)
    parser.add_argument("--input-tokens", type=int, default=0)
    parser.add_argument("--output-tokens", type=int, default=0)
    parser.add_argument("--input-per-million", type=float, default=3.0)
    parser.add_argument("--output-per-million", type=float, default=15.0)
    parser.add_argument("--tool-calls", type=int, default=0)
    parser.add_argument("--tool-call-cost", type=float, default=0.0)
    parser.add_argument("--review-minutes", type=float, default=0.0)
    parser.add_argument("--review-hourly-rate", type=float, default=0.0)
    parser.add_argument("--format", choices=("table", "json"), default="table")


def _add_patterns_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("slug", nargs="?", help="Pattern slug to inspect.")
