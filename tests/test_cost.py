from loop_engineering.cost import estimate_cost


def test_estimate_cost_includes_tokens_tools_and_review() -> None:
    estimate = estimate_cost(
        agent_runs=2,
        input_tokens=100_000,
        output_tokens=20_000,
        input_per_million=3.0,
        output_per_million=15.0,
        tool_calls=4,
        tool_call_cost=0.05,
        review_minutes=30,
        review_hourly_rate=120,
    )

    assert estimate.input_cost == 0.3
    assert estimate.output_cost == 0.3
    assert estimate.tool_cost == 0.2
    assert estimate.review_cost == 60.0
    assert estimate.total_cost == 60.8
