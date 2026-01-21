# KnowShowGo Integration Plan (Separate Track)

This plan covers KnowShowGo-related integration and memory primitives. It is
kept separate from the core NeuroJSON/neurosym.js plan and may be executed on
its own branch or repository as needed.

## Scope
- Integration between NeuroJSON programs and KnowShowGo (KSG) entities.
- Working memory reinforcement as a session-scoped activation layer.
- Optional async replication of activation updates to persistent storage.
- Deterministic parsing utilities for offline or low-cost intent detection.

## Use cases
- Memory-augmented agents that reinforce frequently used concepts or steps.
- Argumentation graphs for conflicting claims with support/inhibit edges.
- Discourse and dialogue tracking (claims, counterclaims, evidence trails).
- Flowchart-like procedural memory with probabilistic activation.
- Knowledge graphs with soft constraints and traceable updates.

## Beyond a schema
KnowShowGo is not just a schema. It provides:
- A working-memory activation layer (session-scoped reinforcement).
- An async persistence pattern for background updates.
- Deterministic parsing for capture paths without LLMs.
- A mapping strategy to store inference runs and provenance.

These allow modeling code, arguments, discourse, and flowcharts as activations
and relations rather than hard-coded procedural logic.

## Discoverability and packaging
KnowShowGo is a Python-first package and service plan:
- Target distribution: PyPI (`knowshowgo`) and a lightweight service API.
- JS users should consume NeuroJSON via `neurosym` on npm, or a thin KSG client
  can be published later if needed.

## Priorities (ordered)
1) WorkingMemoryGraph as a reinforcement layer.
2) AsyncReplicator for background persistence.
3) Deterministic parser for task/event extraction.
4) Immutable prototype patterns for schema integrity.

## Deliverables
### A) Working memory
- A lightweight `WorkingMemoryGraph` with `link`, `access`, and `get_weight`.
- Optional decay and activation boost utilities.
- Clear separation from long-term semantic memory.

### B) Async replication
- `AsyncReplicator` with a queue-based worker.
- `GraphClient` protocol with `increment_edge_weight`.
- Non-blocking enqueue option for hot paths.

### C) Deterministic parsing
- Rule-based classification for task vs event.
- Regex-based time extraction for basic scheduling.
- Utility entrypoint for quick parsing without LLM.

### D) KSG mapping guidance
- Map NeuroJSON variables to KSG Concepts.
- Map factors to KSG Assertions or Associations.
- Store inference runs as separate entities with provenance.
- Write back posteriors to `Assertion.truth` when appropriate.
- Capture `warnings` and `evidenceStats` in run metadata for traceability.

### E) Procedure modeling convention
- Document procedure/decision modeling using `FOLLOWS` + gate nodes.
- Use weighted `SUPPORTS` from conditions to gates.
- Use `MUTEX` when a winner-take-all branch is required.
- See `docs/KNOWSHOWGO_PROCEDURES.md` for the convention.

### F) VSA (vector symbolic) memory layer
- v0.1: minimal VSA module (bundling/binding + cosine similarity + in-memory index).
- Use VSA vectors as an alternate recall signal in semantic search.
- v0.2+: persistence, role/filler binding, and decoding utilities.

### G) Refactor handoff summary
- Consolidated refactor plan and priorities in `docs/KNOWSHOWGO_HANDOFF.md`.

### H) Lazy belief evaluation + caching
- Add a graph-derived resolver that computes priors/evidence at query time.
- Cache derived priors per context; recompute on context change.
- Document the belief model and reasoning view in `docs/KNOWSHOWGO_MODEL.md`.

### I) Neural predicate hooks
- Provide a predicate registry for model-driven evidence.
- Add a belief resolver that reads predicate outputs from node payload.
- Payload keys: `predicate`, `predicate_inputs`.

## Integration constraints
- Keep the activation graph session-scoped by default.
- Persistence is optional and should not block the agent loop.
- Avoid hard dependencies on external services in v0.1.

## Exit criteria
- Working memory and async replication are usable standalone.
- Mapping guidance is documented and consistent with the KSG schema.
- Optional integration hooks exist without introducing mandatory runtime deps.
