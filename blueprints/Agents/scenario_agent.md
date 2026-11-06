# Scenario Agent

## Goal

Produce one readable test scenario for every requirement.

## Inputs

- Requirement backlog
- Risk and test-level guidance

## Outputs

- Scenario ID
- Requirement ID
- Title
- Objective
- Test type

## Rules

1. Every scenario must link to exactly one source requirement.
2. Use API/integration scenarios for functional API requirements.
3. Use business-rule or non-functional scenarios for NFR and BR requirements.
