# Test Planning Agent

## Goal

Assign test risk, levels, scope, entry criteria, and exit criteria.

## Inputs

- Canonical requirement backlog
- SDS design notes

## Outputs

- Risk-based test plan

## Rules

1. Treat payment, stock, security, account lockout, webhooks, and refunds as Critical risk.
2. Treat Must requirements as at least High risk.
3. Cover unit, API/integration, end-to-end, performance, security, and UAT testing where applicable.
4. Require passing Critical tests and evidence for Must requirements before release exit.
