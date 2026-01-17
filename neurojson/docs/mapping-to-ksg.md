# Mapping NeuroJSON to KnowShowGo (KSG)

This document describes a lightweight mapping between NeuroJSON v0.1 programs
and KSG entities. It is meant as guidance for integration, not a hard
requirement.

## Program storage
Store the NeuroJSON program as a first-class artifact:
- Entity type: `NeuroProgram` (or similar)
- Fields: `version`, `source`, `program_json`, `created_at`, `created_by`
- Reference by stable `program_id`

## Variables
Map NeuroJSON variables to KSG Concepts:
- Concept label: variable name
- Properties:
  - `neuro.type = "boolean"`
  - `neuro.prior = <prior>`
  - `neuro.program_id = <program_id>`

## Factors
Map factors to KSG Assertions or Associations:
- Assertion label: `Factor:<id>` (or a generated UUID)
- Properties:
  - `inputs`, `output`, `op`, `weight`, `mode`
  - `neuro.program_id`
- For `support` vs `inhibit`, store `mode` explicitly.

## Inference runs
Each inference run is an entity:
- Entity type: `NeuroInferenceRun`
- Fields:
  - `program_id`
  - `evidence`
  - `queries`
  - `posteriors`
  - `samples_used`, `effective_sample_size`
  - `created_at`

## Writing back posteriors
Optionally write posteriors into KSG Assertions:
- For each variable: update `Assertion.truth`
- Store provenance:
  - `source = "neurosym"`
  - `run_id = <NeuroInferenceRun.id>`

## Notes
- Keep program storage immutable; update by new version and program_id.
- Avoid mixing transient activation with persistent truth in v0.1.
