from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class CostEstimate:
    agent_runs: int
    input_tokens: int
    output_tokens: int
    tool_calls: int
    input_cost: float
    output_cost: float
    tool_cost: float
    review_cost: float
    total_cost: float

    def to_dict(self) -> dict[str, int | float]:
        return asdict(self)


def estimate_cost(
    *,
    agent_runs: int,
    input_tokens: int,
    output_tokens: int,
    input_per_million: float,
    output_per_million: float,
    tool_calls: int = 0,
    tool_call_cost: float = 0.0,
    review_minutes: float = 0.0,
    review_hourly_rate: float = 0.0,
) -> CostEstimate:
    input_cost = (input_tokens / 1_000_000) * input_per_million
    output_cost = (output_tokens / 1_000_000) * output_per_million
    tool_cost = tool_calls * tool_call_cost
    review_cost = (review_minutes / 60) * review_hourly_rate
    total_cost = input_cost + output_cost + tool_cost + review_cost
    return CostEstimate(
        agent_runs=agent_runs,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        tool_calls=tool_calls,
        input_cost=round(input_cost, 4),
        output_cost=round(output_cost, 4),
        tool_cost=round(tool_cost, 4),
        review_cost=round(review_cost, 4),
        total_cost=round(total_cost, 4),
    )


def load_cost_inputs(path: str | Path) -> dict[str, int | float]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("cost input file must contain a JSON object")
    return data


def render_cost_table(estimate: CostEstimate) -> str:
    rows = [
        ("Agent runs", estimate.agent_runs),
        ("Input tokens", estimate.input_tokens),
        ("Output tokens", estimate.output_tokens),
        ("Tool calls", estimate.tool_calls),
        ("Input cost", f"${estimate.input_cost:.4f}"),
        ("Output cost", f"${estimate.output_cost:.4f}"),
        ("Tool cost", f"${estimate.tool_cost:.4f}"),
        ("Review cost", f"${estimate.review_cost:.4f}"),
        ("Total", f"${estimate.total_cost:.4f}"),
    ]
    width = max(len(label) for label, _ in rows)
    return "\n".join(f"{label:<{width}}  {value}" for label, value in rows)
