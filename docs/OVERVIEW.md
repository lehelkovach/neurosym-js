# Repository overview (what, how, why)

This document is the single high-level explanation of what exists in this
repository, how the pieces fit together, and what is planned but not yet
implemented.

## 1) What this repo contains

Top-level components:
- `neurojson/`: NeuroJSON v0.1 spec + schema + examples + fixtures.
- `neurosym-js/`: main TypeScript library (legacy engine + v0.1 sampler).
- `neurosym.js-standalone/`: standalone package with docs and examples.
- `src/knowshowgo/`: Python integration and KnowShowGo reasoning bridge.
- `docs/`: plans, KnowShowGo modeling, procedures, and this overview.

## 2) Core concepts

Terminology used across the repo:
- **Variable / Node**: a boolean concept with a prior (baseline belief).
- **Factor / Rule**: weighted influence from inputs to an output.
- **Constraint**: attack/support/mutex relationships (argumentation).
- **Evidence**: hard clamped observations (0/1).
- **Query**: which variables to return posteriors for.
- **Belief**: a node value computed for a specific context, not an edge weight.

## 3) NeuroJSON v0.1 (the portable schema)

Location:
- Spec: `neurojson/spec/neurojson.v0.1.md`
- Schema: `neurojson/spec/neurojson.schema.json`
- Examples: `neurojson/examples/*.json`
- Fixtures: `neurojson/fixtures/v0.1/expectations.json`

NeuroJSON v0.1 is intentionally minimal:
- Boolean variables only.
- Factors with ops: `IF_THEN`, `AND`, `OR`, `NOT`.
- Modes: `support` or `inhibit`.
- Evidence and queries are optional.

## 4) NeuroSym.js APIs (two layers)

The TS library exports two parallel APIs:

### A) Legacy (v1.0) engine
This is the original engine with rule/constraint semantics:
- `NeuroEngine`, `NeuroGraph`, `InferenceEngine`
- Schema type: `NeuroJSON` with `version: "1.0"`, `rules`, `constraints`
- Deterministic fuzzy inference (not sampling)

### B) NeuroJSON v0.1 compiler + sampler
This is the new v0.1 pipeline:
- `validateProgram`, `compileProgram`, `infer`
- Schema type: `NeuroJSONProgram` with `version: "0.1"`, `factors`
- Likelihood-weighted sampling with evidence + explanations

Both are shipped from the same `neurosym` package. The v0.1 path is the
portable, JSON-first layer used for cross-runtime parity.

## 5) Inference (what happens at runtime)

NeuroJSON v0.1 inference uses likelihood-weighted sampling:
- Evidence multiplies sample weight.
- Posteriors are weighted averages over samples.
- `effectiveSampleSize` reports weight quality.
- `warnings` report unknown queries/evidence or cycles.
- `explanations` list supporting/inhibiting factor contributions.

## 6) KnowShowGo (KSG) integration

KSG stores a graph of nodes + associations. Reasoning is derived by compiling
a NeuroJSON view of a subgraph.

Key docs:
- `docs/KNOWSHOWGO_MODEL.md`: belief model + lazy evaluation.
- `docs/KNOWSHOWGO_PROCEDURES.md`: procedure/fork convention.
- `docs/KNOWSHOWGO_PLAN.md`: integration roadmap.
- `docs/KNOWSHOWGO_HANDOFF.md`: refactor priorities and handoff plan.

## 7) What exists vs what is planned

### Implemented now
- NeuroJSON v0.1 spec, schema, fixtures, examples.
- TypeScript v0.1 compiler + sampler + warnings + explanations.
- Legacy v1.0 engine with rules/constraints (support/attack/mutex).
- KSG belief resolver abstraction + graph-derived resolver.
- Procedure modeling primitives (FOLLOWS + gates + MUTEX).

### Planned or not yet implemented
- **VSA layer** (vector symbolic memory): planned, not implemented.
- **Neural predicates / DeepProbLog features**: not implemented.
- **Recursion / probabilistic logic programming**: not implemented.
- **Arbitrary factor potentials / rich factor graphs**: not implemented.
- **Loopy inference / exact inference**: not implemented.

## 8) Does it have all VSA / factor-graph / DeepProbLog needs for KSG?

Not yet. KSG has:
- A usable belief model and graph-to-NeuroJSON mapping.
- Weighted support/inhibit and MUTEX constraints.
- Lazy, context-aware priors/evidence via resolver policies.

But it does **not** yet include:
- VSA (bundling/binding) memory.
- Neural predicates or differentiable logic programming.
- Recursion or full Prolog/ProbLog semantics.

Those are explicitly tracked as future work in `docs/KNOWSHOWGO_PLAN.md`.

## 9) Testing and CI

- JS: `npm test`, `npm run test:coverage`, `npm run lint`, `npm run typecheck`.
- Python: `pytest` for KnowShowGo integration.
- CI: `.github/workflows/ci.yml` runs JS checks.

## 10) Where to start

- New to the project: read `README.md` then this file.
- Working on core library: `neurosym-js/README.md` and `docs/DEVELOPMENT_PLAN.md`.
- Working on KSG: `docs/KNOWSHOWGO_MODEL.md` + `docs/KNOWSHOWGO_HANDOFF.md`.
