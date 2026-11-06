# Test Cycle Orchestrator

Test Cycle Orchestrator converts SRS and SDS Word documents into a traceable QA pack:

- test plan
- test scenarios
- test cases
- runnable Python API test script stubs
- requirements-to-test traceability matrix

It models a skills-and-agents workflow without requiring an LLM at runtime. Each agent has one responsibility and the orchestrator passes a structured `TestCycle` between them. This makes the result repeatable, reviewable, and easy to replace with an LLM-backed agent later.

## Quick start

```powershell
python -m src.testcycle.cli `
  --srs "D:\Project-Practice\AI\PromptEngineering\Data\RetailHub_SRS.docx" `
  --sds "D:\Project-Practice\AI\PromptEngineering\Data\RetailHub_SDS.docx" `
  --out Output
```

Review the generated Markdown files in `Output/`. To execute the generated API checks against a deployed environment:

```powershell
$env:RETAILHUB_BASE_URL = "https://qa.retailhub.example.com"
python Output/scripts/test_retailhub_api.py
```

The generated checks intentionally skip network calls until `RETAILHUB_BASE_URL` is supplied.

## Flow

```text
SRS + SDS (.docx)
      |
 DocumentIngestionSkill
      |
 RequirementsAgent -> TestPlanningAgent -> ScenarioAgent -> CaseAgent -> ScriptAgent
      |                                                                  |
      +--------------------- TestCycleOrchestrator ---------------------+
                                                                         |
                                plan.md, scenarios.md, cases.md, traceability.md, scripts/
```

## Project layout

- `src/testcycle/skills.py` - DOCX requirements/design extraction skill
- `src/testcycle/agents.py` - specialized QA agents
- `src/testcycle/orchestrator.py` - pipeline coordinator and artifact writer
- `src/testcycle/cli.py` - command-line entry point
- `blueprints/skills/` - editable Markdown definitions for document-ingestion skills
- `blueprints/Agents/` - one editable Markdown definition per QA agent
- `blueprints/orchestrator.md` - workflow and deliverable contract
- `Output/` - generated QA pack: plan, scenarios, cases, traceability, and pytest scripts

## Extension points

Replace individual agent methods with an LLM, a test-management connector, or an OpenAPI parser while keeping the `TestCycle` contract. The deterministic baseline remains useful for CI, document revisions, and auditable traceability.
