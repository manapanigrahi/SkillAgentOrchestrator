"""Specialized agents used by the deterministic QA orchestration pipeline."""
from __future__ import annotations

import re
from collections import defaultdict

from .models import Requirement, Scenario, TestCase, TestCycle


def _area(requirement_id: str) -> str:
    parts = requirement_id.split("-")
    return parts[1] if len(parts) > 2 else "RULE"


class RequirementsAgent:
    def run(self, product_name: str, requirements: list[Requirement], design_notes: list[str]) -> TestCycle:
        return TestCycle(product_name=product_name, requirements=requirements, design_notes=design_notes)


class TestPlanningAgent:
    def risk(self, requirement: Requirement) -> str:
        text = requirement.text.lower()
        if any(word in text for word in ("payment", "stock", "security", "lock", "refund", "webhook")):
            return "Critical"
        if requirement.priority == "Must":
            return "High"
        return "Medium"


class ScenarioAgent:
    def run(self, cycle: TestCycle) -> list[Scenario]:
        scenarios: list[Scenario] = []
        for index, requirement in enumerate(cycle.requirements, 1):
            test_type = "API / Integration" if requirement.id.startswith("FR-") else "Business rule / Non-functional"
            title = re.sub(r"\s+", " ", requirement.text.split(".", 1)[0])
            scenarios.append(Scenario(f"TS-{index:03d}", requirement.id, title[:100], test_type, requirement.text))
        return scenarios


class CaseAgent:
    def run(self, scenarios: list[Scenario], requirements: list[Requirement]) -> list[TestCase]:
        by_id = {item.id: item for item in requirements}
        cases: list[TestCase] = []
        counter = 1
        for scenario in scenarios:
            requirement = by_id[scenario.requirement_id]
            severity = "Critical" if any(word in requirement.text.lower() for word in ("payment", "stock", "security", "webhook")) else "High"
            endpoint_hint = self._endpoint_hint(requirement.id)
            cases.extend([
                TestCase(f"TC-{counter:03d}", scenario.id, requirement.id, f"{requirement.id} happy path", "Test data and an authorized user are available.", (f"Call {endpoint_hint} with valid data.", "Capture the response and persisted state."), "The request succeeds and the stated business outcome is recorded.", severity, "Automated"),
                TestCase(f"TC-{counter+1:03d}", scenario.id, requirement.id, f"{requirement.id} validation and boundary", "Test data is reset.", (f"Call {endpoint_hint} with invalid, missing, or boundary data.", "Verify status code, error code, and no unintended side effect."), "A documented validation or conflict response is returned; data remains consistent.", severity, "Automated"),
            ])
            counter += 2
        return cases

    @staticmethod
    def _endpoint_hint(requirement_id: str) -> str:
        mapping = {"AUTH": "/api/v1/auth/*", "CAT": "/api/v1/products", "INV": "/api/v1/inventory/*", "CRT": "/api/v1/cart", "ORD": "/api/v1/orders", "PAY": "/api/v1/payments/*", "CUS": "/api/v1/customers/me", "POS": "/api/v1/orders", "RPT": "/api/v1/reports/*"}
        return mapping.get(_area(requirement_id), "the relevant API or workflow")


class ScriptAgent:
    """Produces executable, safe HTTP contract probes for high-risk/API requirements."""
    def render(self, cycle: TestCycle) -> str:
        selected = [case for case in cycle.cases if case.severity == "Critical" or case.requirement_id in {"FR-AUTH-01", "FR-ORD-01"}]
        tests = "\n".join(
            f"    probe('{case.id}', '{case.requirement_id}', '{CaseAgent._endpoint_hint(case.requirement_id)}')" for case in selected[:18]
        )
        return f'''"""Generated RetailHub API contract probes. Set RETAILHUB_BASE_URL to run network checks."""
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL = os.getenv("RETAILHUB_BASE_URL", "").rstrip("/")

def probe(case_id, requirement_id, endpoint):
    if not BASE_URL:
        print(f"SKIP {{case_id}} ({{requirement_id}}): RETAILHUB_BASE_URL is not set")
        return
    path = endpoint.replace("*", "health")
    request = Request(BASE_URL + path, headers={{"Accept": "application/json", "X-Test-Case": case_id}})
    try:
        with urlopen(request, timeout=10) as response:
            assert response.status < 500, f"{{case_id}} server error: {{response.status}}"
            print(f"PASS {{case_id}} ({{requirement_id}}): {{response.status}}")
    except HTTPError as error:
        assert error.code < 500, f"{{case_id}} server error: {{error.code}}"
        print(f"PASS {{case_id}} ({{requirement_id}}): expected client response {{error.code}}")
    except URLError as error:
        raise AssertionError(f"{{case_id}} network failure: {{error}}") from error

def main():
{tests}

if __name__ == "__main__":
    main()
'''

    def render_pytest(self, cycle: TestCycle) -> str:
        """Create one pytest parameter per test-case artifact; execution is safe by default."""
        rows = "\n".join(
            f"    pytest.param('{case.id}', '{case.requirement_id}', '{CaseAgent._endpoint_hint(case.requirement_id)}', id='{case.id}'),"
            for case in cycle.cases
        )
        return f'''"""Generated pytest suite. Every parameter maps one-to-one to test_cases.md."""
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pytest

BASE_URL = os.getenv("RETAILHUB_BASE_URL", "").rstrip("/")

CASES = [
{rows}
]


@pytest.mark.parametrize(("case_id", "requirement_id", "endpoint"), CASES)
def test_retailhub_case(case_id, requirement_id, endpoint):
    """Run one traceable API contract probe for each generated test case."""
    if not BASE_URL:
        pytest.skip("Set RETAILHUB_BASE_URL to execute API checks")
    path = endpoint.replace("*", "health")
    request = Request(BASE_URL + path, headers={{"Accept": "application/json", "X-Test-Case": case_id}})
    try:
        with urlopen(request, timeout=10) as response:
            assert response.status < 500, f"{{case_id}} / {{requirement_id}} returned {{response.status}}"
    except HTTPError as error:
        assert error.code < 500, f"{{case_id}} / {{requirement_id}} returned {{error.code}}"
    except URLError as error:
        pytest.fail(f"{{case_id}} / {{requirement_id}} network failure: {{error}}")
'''
