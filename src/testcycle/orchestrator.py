from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from .agents import CaseAgent, RequirementsAgent, ScenarioAgent, ScriptAgent, TestPlanningAgent
from .models import TestCycle
from .skills import DocumentIngestionSkill


class TestCycleOrchestrator:
    def __init__(self) -> None:
        self.ingestion = DocumentIngestionSkill()
        self.requirements_agent = RequirementsAgent()
        self.planning_agent = TestPlanningAgent()
        self.scenario_agent = ScenarioAgent()
        self.case_agent = CaseAgent()
        self.script_agent = ScriptAgent()

    def run(self, srs: Path, sds: Path, output: Path) -> TestCycle:
        requirements = self.ingestion.extract_requirements(srs)
        design_notes = self.ingestion.extract_design_notes(sds)
        cycle = self.requirements_agent.run("RetailHub", requirements, design_notes)
        cycle.scenarios = self.scenario_agent.run(cycle)
        cycle.cases = self.case_agent.run(cycle.scenarios, cycle.requirements)
        self._write_artifacts(cycle, output)
        return cycle

    def _write_artifacts(self, cycle: TestCycle, output: Path) -> None:
        output.mkdir(parents=True, exist_ok=True)
        (output / "scripts").mkdir(exist_ok=True)
        risk_groups = defaultdict(list)
        for requirement in cycle.requirements:
            risk_groups[self.planning_agent.risk(requirement)].append(requirement.id)
        plan = [f"# {cycle.product_name} Test Plan", "", "## Scope", "", f"This plan covers {len(cycle.requirements)} SRS requirements extracted from the supplied SRS and aligned to the SDS API-first design.", "", "## Risk based coverage", ""]
        plan += [f"- **{risk}:** {', '.join(ids)}" for risk, ids in risk_groups.items()]
        plan += ["", "## Levels and approach", "", "- Unit: business rules, calculators, validators.", "- API/integration: endpoint contracts, authorization, idempotency and integrations.", "- End-to-end: online order, payment, fulfilment, return and POS journeys.", "- Non-functional: performance, security, accessibility, resilience and recovery.", "", "## Entry and exit", "", "Entry: stable QA build, seeded data, payment sandbox and API base URL. Exit: all Critical cases pass, no open Critical defects, and traced Must requirements have evidence."]
        (output / "test_plan.md").write_text("\n".join(plan) + "\n", encoding="utf-8")

        scenario_lines = [f"# {cycle.product_name} Test Scenarios", "", "| ID | Requirement | Type | Scenario |", "| --- | --- | --- | --- |"]
        scenario_lines += [f"| {s.id} | {s.requirement_id} | {s.test_type} | {s.title} |" for s in cycle.scenarios]
        (output / "test_scenarios.md").write_text("\n".join(scenario_lines) + "\n", encoding="utf-8")

        case_lines = [f"# {cycle.product_name} Test Cases", ""]
        for case in cycle.cases:
            case_lines += [f"## {case.id} {case.title}", f"- Traceability: {case.requirement_id} / {case.scenario_id}", f"- Severity: {case.severity}; Automation: {case.automation}", f"- Preconditions: {case.preconditions}", "- Steps:"]
            case_lines += [f"  {index}. {step}" for index, step in enumerate(case.steps, 1)]
            case_lines += [f"- Expected result: {case.expected}", ""]
        (output / "test_cases.md").write_text("\n".join(case_lines), encoding="utf-8")

        trace = [f"# {cycle.product_name} Requirements Traceability", "", "| Requirement | Priority | Scenario | Test cases |", "| --- | --- | --- | --- |"]
        cases_by_requirement = defaultdict(list)
        for case in cycle.cases:
            cases_by_requirement[case.requirement_id].append(case.id)
        scenario_by_requirement = {s.requirement_id: s.id for s in cycle.scenarios}
        trace += [f"| {r.id} | {r.priority} | {scenario_by_requirement.get(r.id, '')} | {', '.join(cases_by_requirement[r.id])} |" for r in cycle.requirements]
        (output / "traceability.md").write_text("\n".join(trace) + "\n", encoding="utf-8")
        (output / "scripts" / "test_retailhub_api.py").write_text(self.script_agent.render(cycle), encoding="utf-8")
        (output / "scripts" / "test_retailhub_cases.py").write_text(self.script_agent.render_pytest(cycle), encoding="utf-8")
