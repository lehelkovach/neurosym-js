# NeuroJSON v0.1 Specification

NeuroJSON is a small, versioned JSON format for probabilistic neurosymbolic
programs. v0.1 is intentionally minimal and focused on boolean variables,
weighted factors, and simple inference.

## Top-level fields
Required:
- `version`: string, must be `"0.1"`
- `variables`: object mapping variable names to variable definitions
- `factors`: array of factor definitions

Optional:
- `evidence`: object mapping variable names to observed values (0 or 1)
- `queries`: array of variable names to return in output
- `metadata`: free-form object for provenance, labels, etc.

## Variables
Variables are boolean in v0.1.

Variable definition:
- `type`: `"boolean"` (required)
- `prior`: number in [0, 1] (optional, default 0.5)
- `description`: string (optional)

## Factors
Factors connect input variables to a single output.

Factor definition:
- `inputs`: array of variable names (required)
- `output`: variable name (required)
- `op`: `IF_THEN` | `AND` | `OR` | `NOT` (required)
- `weight`: number in [0, 1] (required)
- `mode`: `support` | `inhibit` (optional, default `support`)
- `id`: string (optional, for explanations)
- `description`: string (optional)

### Arity rules
- `IF_THEN` requires exactly 1 input
- `NOT` requires exactly 1 input
- `AND` requires 1 or more inputs
- `OR` requires 1 or more inputs

## Ops semantics (v0.1)
Factor activation is boolean based on the current inputs:
- `IF_THEN`: active if the input is true
- `AND`: active if all inputs are true
- `OR`: active if any input is true
- `NOT`: active if the input is false

## Mode and aggregation
The output probability starts from its prior. Each active factor updates the
probability.

Recommended aggregation:
- Support (noisy-OR):
  - `p = 1 - (1 - p) * (1 - w)`
- Inhibit (attenuation):
  - `p = p * (1 - w)`

This provides a simple and stable way to combine multiple supports and
inhibitions.

## Evidence semantics
Evidence clamps a variable to 0 or 1. Inference should use likelihood-weighted
sampling rather than rejection, so evidence updates the sample weight instead
of discarding samples.

## Queries
If `queries` is provided, only those variables are returned in the output.
If omitted, all variable posteriors should be returned.

## Versioning policy
- Programs must declare a `version`.
- Validation is strict and versioned.
- Breaking changes require a new version and schema.
