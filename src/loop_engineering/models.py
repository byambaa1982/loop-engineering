from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AutonomyLevel(str, Enum):
    """Practical autonomy levels for agentic engineering loops."""

    ASSISTED = "L1"
    REVIEWED = "L2"
    SUPERVISED = "L3"
    AUTOMATED = "L4"


@dataclass(frozen=True)
class LoopPattern:
    slug: str
    name: str
    summary: str
    autonomy: AutonomyLevel
    cadence: str
    triggers: tuple[str, ...]
    guardrails: tuple[str, ...]
    outputs: tuple[str, ...]
    owner: str = "engineering"


@dataclass(frozen=True)
class AuditResult:
    name: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class CostEstimate:
    runs: int
    input_tokens: int
    output_tokens: int
    input_price_per_million: float
    output_price_per_million: float

    @property
    def input_cost(self) -> float:
        return (self.input_tokens / 1_000_000) * self.input_price_per_million

    @property
    def output_cost(self) -> float:
        return (self.output_tokens / 1_000_000) * self.output_price_per_million

    @property
    def total_cost(self) -> float:
        return self.runs * (self.input_cost + self.output_cost)
