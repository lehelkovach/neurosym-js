# Unified Development Plan

This file is the single source of truth for development planning in this
repository. It merges and supersedes all other design and planning documents
except KnowShowGo-specific plans, which are intentionally separated.

## Source documents merged
- `docs/NEUROSYM_MASTER_PLAN.md`
- `docs/GPT-5.2.txt`
- `docs/claude-opus-4-analysis.txt`
- `docs/gemini-3-pro-preview.txt`
- `readme-agentic-memory-prototype.md`
- `neurosym-js/README.md`
- `neurosym.js-standalone/README.md`

## Related plan (separate)
- KnowShowGo-specific plans are maintained in `docs/KNOWSHOWGO_PLAN.md`.

## Scope and goals
1) Deliver a zero-dependency NeuroSym.js core for neurosymbolic reasoning.
2) Maintain a stable NeuroJSON schema shared across JS and Python.
3) Provide a standalone NeuroJSON spec repository with examples and schema.
4) Offer clean documentation, examples, and testing guidance.

## Current state (summary)
- TypeScript core library exists in `neurosym-js/`.
- Standalone package and deeper docs exist in `neurosym.js-standalone/`.
- Python neuro engine and KnowShowGo integration live in `src/knowshowgo/`.
- Integration guides and salvage analyses exist in `docs/`.

## Guiding principles
- Code as data: logic is defined in NeuroJSON, not hardcoded functions.
- Separation of concerns: logic core, graph state, and engine remain decoupled.
- Parity: JS and Python should produce equivalent results for the same schema.
- Zero-dependency runtime core; dev-only dependencies are acceptable.
- Keep KnowShowGo integration plans separate and optional.

## Design and positioning (v0.1)
NeuroJSON is a small, versioned, JSON-first language for neurosymbolic logic.
neurosym.js is the reference JavaScript/TypeScript implementation that can
validate, compile, and run NeuroJSON programs.

The core stance is "code as data":
- Logic is expressed as JSON and stored alongside data.
- Programs are portable, inspectable, and versioned.
- Reasoning can be embedded into web apps, services, and tools without
  heavyweight dependencies.

Design goals:
- A strict, minimal schema that is easy to validate.
- Boolean variables only, with weighted support and inhibition.
- A simple compiler to an explicit intermediate representation (IR).
- A deterministic and testable inference engine (likelihood-weighted sampling).
- Clear diagnostics for schema errors and invalid programs.

Non-goals (v0.1):
- Categorical or continuous variables.
- Complex factor graphs with arbitrary potentials.
- Large-scale optimization or GPU acceleration.
- Full logic programming (Datalog/Prolog) semantics.

Why NeuroJSON (and not Prolog/Datalog):
- NeuroJSON: weighted factors + probabilistic aggregation.
- Datalog/Prolog: discrete rules + strict logical entailment.

In short: NeuroJSON is pragmatic for uncertainty; Datalog/Prolog are ideal for
strict symbolic reasoning.

Core model (v0.1):
- Variables are boolean with optional priors in [0, 1].
- Factors connect inputs to a single output.
- Operations: IF_THEN, AND, OR, NOT.
- Mode: support or inhibit.

Recommended aggregation is noisy-OR for supports and multiplicative attenuation
for inhibition.

Versioning:
- Programs must declare a version string.
- Validation is strict and versioned.
- Breaking changes require a version bump.

Intended usage patterns:
- Store NeuroJSON alongside other knowledge artifacts.
- Compile to a lightweight IR for fast inference.
- Provide posteriors and minimal explanations.
- Add integration layers that map to external systems (e.g., KnowShowGo).

Roadmap pointers:
v0.1 establishes the minimal program shape and inference behavior. v0.2 and
beyond can add categorical variables, loopy inference, richer factors, and
compiler backends for symbolic systems.

## Architecture summary
- Logic core: t-norms and operators for fuzzy logic and argumentation.
- NeuroGraph: in-memory structure for variables, rules, and constraints.
- NeuroEngine: inference, training, and export surface.
- NeuroJSON: the shared schema that encodes variables, rules, constraints.
- Spec repo: versioned spec, schema, and examples for NeuroJSON.

## Roadmap

### Phase 0: Stability and parity (now)
Goal: ensure JS and Python produce consistent results.
Deliverables:
- Validate NeuroJSON schema versioning and validation rules.
- Align inference semantics between JS and Python engines.
- Add minimal parity test vectors shared across JS and Python.
Exit criteria:
- Same inputs yield same outputs within tolerances in both runtimes.

### Phase 1: Docs and packaging (short term)
Goal: make the project usable without reading source code.
Deliverables:
- Keep `neurosym-js/README.md` and root `README.md` aligned.
- Publish or prepare publish steps for the `neurosym` npm package.
- Ensure examples compile and run against the current API.
Exit criteria:
- Quick start works end-to-end from docs without edits.

### Phase 2: Core library hardening
Goal: reliability and maintainability of the JS core.
Deliverables:
- Clear convergence rules for inference iterations.
- Training API stabilization and documented heuristics.
- Additional tests for constraints and argumentation operations.
Exit criteria:
- Test suite covers core logic paths and passes reliably.

### Phase 3: NeuroJSON evolution
Goal: formalize and extend schema safely.
Deliverables:
- A formal schema spec and validation utilities.
- Expand supported operations and constraint types where needed.
- Migration guidance for schema version bumps.
Exit criteria:
- Schema spec is versioned and cross-runtime validators exist.

### Phase 4: NeuroJSON spec repository
Goal: make the spec standalone, testable, and versioned.
Deliverables:
- Spec markdown and a strict JSON Schema for v0.1.
- Example programs with expected behavior.
- Mapping notes for external integrations (kept in separate doc if needed).
Exit criteria:
- Schema validates all examples and rejects invalid programs.

### Phase 5: Transpiler and LLM tools (optional)
Goal: transform NeuroJSON into explanations or code via LLMs.
Deliverables:
- Prompt templates and a reference transpiler module.
- Output formats: natural language, predicate logic, python code.
Exit criteria:
- A minimal end-to-end example works and is documented.

### Phase 6: Service and UI integration (optional)
Goal: expose a service endpoint and demo UI for reasoning.
Deliverables:
- Minimal API endpoint to run inference on stored graphs.
- Microservice packaging pattern for future reuse.
Exit criteria:
- A reference service runs locally and can execute inference.

## Downstream integration guidance
Keep KnowShowGo integration plans in the separate plan document. This plan
should not block core library development.

## Testing strategy
- JS: `npm test`, `npm run typecheck`, `npm run lint`.
- Python: `pytest` for the KnowShowGo integration layers.
- Cross-runtime: parity tests using shared JSON fixtures.

## Risks and mitigations
- Schema divergence: mitigate with shared JSON fixtures and validators.
- Logic drift between JS and Python: enforce parity tests.
- Overreach on optional components: keep phases 5-7 optional.
- Data model mismatch with downstream repositories: document mappings clearly.

## Decision log
When a major decision changes the plan (schema changes, engine semantics, API
breaks), add a short entry here with date and rationale.
