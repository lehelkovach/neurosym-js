# KnowShowGo Refactor & Development Handoff (Consolidated)

This document consolidates the KnowShowGo refactor + development direction
discussed so far into one handoff plan.

## Goals (your stated intent)
- Represent logic conceptions as a **parsimonious graph** of concepts + relations.
- Support **human-like recall**: semantic search → concept → sub-steps.
- Model **procedures** with conditional forks and context gating.
- Keep inference **explainable** with graded support and inhibition.

## Current foundation (already in repo)
### Data model primitives
- **Node** has `prior`, `truth_value`, `is_locked`, `context_ids`, `prototype_ids`.
- **Association** has typed logic metadata with weights.
- **New sequence edge**: `FOLLOWS` for step ordering.

### Reasoning + artifacts
- NeuroService converts KSG subgraphs to NeuroJSON for inference.
- Neuro artifacts store can persist programs + inference runs with provenance.

## Core conventions (parsimonious modeling)
### 1) Procedure + decision modeling
Use only nodes and associations:
- **Step nodes** (concepts)
- **Condition nodes** (boolean predicates)
- **Gate nodes** (OR/AND aggregators)
- **Context nodes** (runtime context)

Edges:
- `FOLLOWS` for sequence
- `SUPPORTS` / `ATTACKS` for graded activation
- `MUTEX` for winner-take-all branches

### 2) Forks via gate nodes (hyperedge emulation)
Represent conditional branches as:
`Condition(s) → Gate → Step options`
This emulates hyperedges without changing storage primitives.

### 3) Context gating
- Context nodes support gates or steps with weighted edges.
- Evaluation time = apply context + evidence, then infer active steps.

## Refactor priorities (most advantageous)
### A) Semantic recall interface
- Add an embedding-based search API (top-K by similarity).
- Apply context gating as a **weighted boost**, not a hard filter.
- Return concept node + ordered steps if present.

### B) Weighted prototype inheritance (JS-like)
- Use `IS_A` edges with weights to represent multiple inheritance.
- Add lazy prototype resolver that merges properties by weight.
- Allow fuzzy prototype matching via embeddings + edge weights.

### C) Decouple NeuroJSON from node priors/truth values
- Introduce a belief resolver interface:
  - `get_prior(node)`
  - `get_evidence(node)`
  - `get_is_locked(node)`
- Default to current fields, but allow alternative policies.
- Add a **graph-derived resolver** that lazily computes priors/evidence at query time
  and caches results per context.

### D) Statistical fuzzy VSA layer (optional but aligned)
- Add a **Vector Symbolic Architecture (VSA)** layer for compositional memory.
- Support **bundling** (superposition) and **binding** (role–filler).
- Use VSA vectors as an alternative retrieval signal alongside embeddings.
- Map VSA traces to prototypes or subgraphs for fast recall.

### E) Artifact + provenance integration
- Store NeuroJSON programs as immutable artifacts.
- Store inference runs with evidence, warnings, and metadata.

## Implementation tasks (checklist)
1) Implement `memory_query` module for embedding search + context boost.
2) Implement `prototype_resolver` module for weighted `IS_A` casting.
3) Add belief resolver policy layer for NeuroJSON mapping.
4) Add tests for:
   - weighted prototype resolution
   - context-boosted retrieval
   - procedure fork routing (gate + MUTEX)
5) Add docs:
   - Procedure modeling convention
   - Semantic recall pipeline
   - Prototype resolution rules

## Notes
- Keep the model parsimonious: nodes + weighted edges only.
- Treat NeuroJSON as the **reasoning view**, not the memory itself.
- Evidence and context drive recall; priors capture baseline belief.
