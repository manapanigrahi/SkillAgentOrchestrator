# Test Cycle Orchestrator Blueprint

## Workflow

```text
Document Ingestion Skill (`skills/document_ingestion.md`)
  -> Requirements Agent (`Agents/requirements_agent.md`)
  -> Test Planning Agent (`Agents/test_planning_agent.md`)
  -> Scenario Agent (`Agents/scenario_agent.md`)
  -> Case Agent (`Agents/case_agent.md`)
  -> Script Agent (`Agents/script_agent.md`)
  -> QA Pack Publisher
```

## Required deliverables

1. Test plan
2. Test scenarios
3. Test cases
4. Requirements traceability matrix
5. Pytest suite containing every automated test case

## Quality gates

- Every requirement has at least one scenario.
- Every scenario has positive and negative/boundary coverage.
- Every pytest parameter has a matching test case ID.
- No test makes a network request until a QA base URL is explicitly configured.
