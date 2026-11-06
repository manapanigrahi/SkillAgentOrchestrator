# RetailHub Test Plan

## Scope

This plan covers 62 SRS requirements extracted from the supplied SRS and aligned to the SDS API-first design.

## Risk based coverage

- **High:** FR-AUTH-01, FR-AUTH-02, FR-AUTH-03, FR-AUTH-06, FR-CAT-01, FR-CAT-02, FR-CRT-01, FR-CRT-04, FR-ORD-03, FR-PAY-04, FR-CUS-01, FR-RPT-01
- **Medium:** FR-AUTH-04, FR-CAT-03, FR-CAT-04, FR-CRT-03, FR-ORD-05, FR-CUS-02, FR-POS-01, FR-POS-02, FR-POS-03, FR-NTF-02, FR-RPT-03, NFR-01, NFR-02, NFR-03, NFR-04, NFR-05, NFR-07, NFR-08, NFR-09, NFR-10, NFR-12, BR-02, BR-05, BR-06, BR-07, BR-10
- **Critical:** FR-AUTH-05, FR-INV-01, FR-INV-02, FR-INV-03, FR-INV-04, FR-INV-05, FR-CRT-02, FR-ORD-01, FR-ORD-02, FR-ORD-04, FR-PAY-01, FR-PAY-02, FR-PAY-03, FR-PAY-05, FR-CUS-03, FR-NTF-01, FR-RPT-02, NFR-06, NFR-11, BR-01, BR-03, BR-04, BR-08, BR-09

## Levels and approach

- Unit: business rules, calculators, validators.
- API/integration: endpoint contracts, authorization, idempotency and integrations.
- End-to-end: online order, payment, fulfilment, return and POS journeys.
- Non-functional: performance, security, accessibility, resilience and recovery.

## Entry and exit

Entry: stable QA build, seeded data, payment sandbox and API base URL. Exit: all Critical cases pass, no open Critical defects, and traced Must requirements have evidence.
