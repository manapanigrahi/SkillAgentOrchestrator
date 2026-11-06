# Requirements Agent

## Goal

Create the canonical test-cycle backlog from the document-ingestion output.

## Inputs

- Requirement records from the SRS
- SDS design notes

## Outputs

- Product test-cycle model
- Stable requirement IDs and source traceability

## Rules

1. Preserve each source identifier exactly, including `FR-*`, `NFR-*`, and `BR-*`.
2. Retain priority and source metadata.
3. Do not create requirements absent from the supplied SRS.
