# Unified Development Plan

This file is the single source of truth for development planning in this
repository. It merges and supersedes all other plan and analysis documents.
Keep other documents for historical context and deep dives, but execute
against this plan.

## Source documents merged
- `docs/NEUROSYM_MASTER_PLAN.md`
- `docs/KSG_INTEGRATION.md`
- `docs/GPT-5.2.txt`
- `docs/claude-opus-4-analysis.txt`
- `docs/gemini-3-pro-preview.txt`
- `docs/salvage-knowshowgo.txt`
- `docs/salvage-osl-agent-prototype.txt`
- `readme-agentic-memory-prototype.md`
- `neurosym-js/README.md`
- `neurosym.js-standalone/README.md`

## Scope and goals
1) Deliver a zero-dependency NeuroSym.js core for neurosymbolic reasoning.
2) Maintain a stable NeuroJSON schema shared across JS and Python.
3) Provide Python parity and KnowShowGo integration.
4) Provide optional working-memory reinforcement and async persistence.
5) Offer clean documentation, examples, and testing guidance.

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
- Working memory is distinct from long-term semantic memory.
- Async persistence is optional and must not block the hot path.

## Architecture summary
- Logic core: t-norms and operators for fuzzy logic and argumentation.
- NeuroGraph: in-memory structure for variables, rules, and constraints.
- NeuroEngine: inference, training, and export surface.
- NeuroJSON: the shared schema that encodes variables, rules, constraints.
- Working memory: reinforcement graph with activation weights (optional layer).
- Replication: async queue for persistence of activation updates (optional layer).

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

### Phase 4: KnowShowGo integration and Python parity
Goal: a consistent story for Python users and graph integration.
Deliverables:
- Update the Python engine to match JS behavior and config defaults.
- Document mapping from KnowShowGo nodes/associations to NeuroJSON.
- Keep `docs/KSG_INTEGRATION.md` accurate and minimal.
Exit criteria:
- Python examples in docs run and match JS outputs.

### Phase 5: Working memory and replication (optional)
Goal: provide cognitive primitives for activation and persistence.
Deliverables:
- WorkingMemoryGraph with reinforcement and optional decay.
- AsyncReplicator for background persistence with a GraphClient protocol.
- Clear guidance for when to keep activation ephemeral vs persisted.
Exit criteria:
- Working memory can be used standalone without storage dependencies.
- Persistence is optional and does not block inference.

### Phase 6: Transpiler and LLM tools (optional)
Goal: transform NeuroJSON into explanations or code via LLMs.
Deliverables:
- Prompt templates and a reference transpiler module.
- Output formats: natural language, predicate logic, python code.
Exit criteria:
- A minimal end-to-end example works and is documented.

### Phase 7: Service and UI integration (optional)
Goal: expose a service endpoint and demo UI for reasoning.
Deliverables:
- Minimal API endpoint to run inference on stored graphs.
- Microservice packaging pattern for future reuse.
Exit criteria:
- A reference service runs locally and can execute inference.

## Downstream integration guidance (osl-agent-prototype)
These items are recommendations only; do not block core library work.
Priority order:
1) WorkingMemoryGraph as activation layer.
2) AsyncReplicator for background persistence.
3) Deterministic parser for offline or low-cost intent detection.
4) Immutable prototype patterns for schema integrity.

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
