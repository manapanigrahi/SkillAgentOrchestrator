# Document Ingestion Skill

## Purpose

Read the supplied SRS and SDS Word documents and expose requirements, business rules, non-functional requirements, endpoints, and design constraints in structured form.

## Inputs

- Approved SRS DOCX
- Current SDS DOCX

## Outputs

- Requirement ID, text, priority, and source
- Design notes that affect test scope, including API conventions, security controls, workflows, and deployment assumptions

## Rules

1. Preserve source identifiers such as `FR-PAY-02`, `NFR-04`, and `BR-01`.
2. Treat every functional and non-functional requirement as traceable test scope.
3. Extract business rules even where they appear in prose rather than a table.
4. Do not invent requirements not present in the source documents.
