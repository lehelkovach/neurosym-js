# KnowShowGo Integration Plan (Separate Track)

This plan covers KnowShowGo-related integration and memory primitives. It is
kept separate from the core NeuroJSON/neurosym.js plan and may be executed on
its own branch or repository as needed.

## Scope
- Integration between NeuroJSON programs and KnowShowGo (KSG) entities.
- Working memory reinforcement as a session-scoped activation layer.
- Optional async replication of activation updates to persistent storage.
- Deterministic parsing utilities for offline or low-cost intent detection.

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

## Integration constraints
- Keep the activation graph session-scoped by default.
- Persistence is optional and should not block the agent loop.
- Avoid hard dependencies on external services in v0.1.

## Exit criteria
- Working memory and async replication are usable standalone.
- Mapping guidance is documented and consistent with the KSG schema.
- Optional integration hooks exist without introducing mandatory runtime deps.
