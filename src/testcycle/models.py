from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Requirement:
    id: str
    text: str
    priority: str = ""
    source: str = "SRS"


@dataclass(frozen=True)
class Scenario:
    id: str
    requirement_id: str
    title: str
    test_type: str
    objective: str


@dataclass(frozen=True)
class TestCase:
    id: str
    scenario_id: str
    requirement_id: str
    title: str
    preconditions: str
    steps: tuple[str, ...]
    expected: str
    severity: str
    automation: str


@dataclass
class TestCycle:
    product_name: str
    requirements: list[Requirement] = field(default_factory=list)
    design_notes: list[str] = field(default_factory=list)
    scenarios: list[Scenario] = field(default_factory=list)
    cases: list[TestCase] = field(default_factory=list)
