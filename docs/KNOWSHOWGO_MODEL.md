# KnowShowGo model and reasoning view

This document explains **what** the KnowShowGo (KSG) memory model stores,
**how** reasoning is derived from it, and **why** the system keeps belief as a
lazy, computed value instead of a static field.

## 1) Core primitives (what is stored)

### Nodes
`Node` is the atomic memory item. Key fields:
- `id`: stable identifier.
- `prototype_id`: the semantic category (e.g., `concept`, `step`, `context`).
- `payload`: arbitrary metadata (labels, embeddings, provenance, etc.).
- `context_ids`: list of context node IDs that gate activation.
- `prior`: optional baseline belief (can be ignored by a resolver).
- `truth_value`: optional current belief (often left unset).
- `is_locked`: optional hard evidence flag.

### Associations
`Association` connects two nodes. Key fields:
- `source_id` / `target_id`
- `logic_meta`: logic type + weight + operator where applicable.

Common `LogicType` values:
- `SUPPORTS`, `ATTACKS` (graded influence)
- `MUTEX` (winner-take-all)
- `FOLLOWS` (procedure sequencing)

## 2) Structural memory vs reasoning view (how it works)

The **graph** is the stored memory: nodes, edges, and metadata. It is not
inherently a probabilistic program. When we reason, we **compile a view** of
the graph into a NeuroJSON program:
- Nodes become NeuroJSON variables.
- Associations become NeuroJSON factors.
- Evidence is derived from a resolver policy.
- Queries are chosen by the caller (or derived from a target node).

This separation keeps storage flexible and reasoning explicit.

## 3) Belief is computed, not stored (what/why)

**Edge weights are influence strengths, not beliefs.**
They describe how strongly one node pushes or inhibits another. A belief is the
current activation of a node **in a specific context**.

Because context and evidence change per query, belief is computed on demand.
This avoids constantly mutating stored graph state while still allowing the
system to surface a numeric belief when asked.

## 4) Lazy evaluation with caching (how)

KSG uses a `BeliefResolver` abstraction to map graph data into priors and
evidence. The default resolver reads `prior`, `truth_value`, and `is_locked`.

For lazy evaluation, use `GraphDerivedBeliefResolver`:
- `prepare_context(context, active_context_ids)` derives priors/evidence from
  the graph.
- Results are cached in the resolver instance for the current context.
- `get_prior` and `get_evidence` read from that cache during compilation.

### Example
```python
from knowshowgo import GraphDerivedBeliefResolver, NeuroService

resolver = GraphDerivedBeliefResolver(
    default_prior=0.1,
    context_boost=0.4,
    use_node_prior=False,
)
service = NeuroService(belief_resolver=resolver)

context = service.extract_context(nodes, associations, center_node_id)
resolver.prepare_context(context, active_context_ids=[context_id])
program = service.to_neuro_json(context)
result = service.run_inference(context, active_context_ids=[context_id])
```

### Cache behavior
The cache lives in the resolver instance. Instantiate a new resolver (or
re-run `prepare_context`) to refresh cached priors/evidence.

## 5) Context gating (how/why)

Context can influence belief in two ways:
- `context_ids` on a node: if any active context matches, boost its prior.
- `SUPPORTS` edges from a context node: boost the target prior by edge weight.

This is a soft, weighted gating mechanism (not a hard filter) that supports
flexible recall.

## 6) Why this model

- **Separation of concerns**: storage is stable; reasoning is contextual.
- **Pluggable policies**: swap resolvers without changing the graph.
- **Compatibility**: supports fuzzy belief, hard evidence, and WTA constraints.
- **Scalable recall**: cache computed priors for repeated queries.

## 7) Not yet implemented (future work)

The following are planned but not yet available in KSG:
- **VSA (vector symbolic) memory** for bundling/binding.
- **Neural predicates / DeepProbLog-like features**.
- **Recursion / full logic programming semantics**.

See `docs/KNOWSHOWGO_PLAN.md` for the current roadmap.
