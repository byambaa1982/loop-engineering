from loop_engineering.cli import main


def test_patterns_command_lists_known_pattern(capsys) -> None:
    exit_code = main(["patterns"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "daily-triage" in output


def test_cost_command_outputs_json(capsys) -> None:
    exit_code = main([
        "cost",
        "--agent-runs",
        "1",
        "--input-tokens",
        "1000",
        "--output-tokens",
        "1000",
        "--format",
        "json",
    ])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert '"total_cost"' in output
