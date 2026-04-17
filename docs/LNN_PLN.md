# LNN and probabilistic logic support

This note clarifies what qualifies as an LNN (Logical Neural Network) or
probabilistic logic network in this repo, what is supported today, and the
current limits.

## 1) LNN support (legacy engine, v1.0 schema)

**Supported (v1.0 engine):**
- Lukasiewicz fuzzy logic operations
- Weighted rules: IMPLICATION, CONJUNCTION, DISJUNCTION, EQUIVALENCE
- Argumentation constraints: ATTACK, SUPPORT, MUTEX
- Deterministic fuzzy inference + optional training

**Not yet supported:**
- Full differentiable constraint training
- Advanced neural predicate learning
- End-to-end backprop across symbolic constraints

### Minimal LNN-style example (TypeScript)
```typescript
import { NeuroEngine } from 'neurosym';

const schema = {
  version: '1.0',
  variables: {
    has_wings: { type: 'bool', prior: 0.5 },
    has_feathers: { type: 'bool', prior: 0.5 },
    is_bird: { type: 'bool', prior: 0.2 }
  },
  rules: [
    {
      id: 'wings_imply_bird',
      type: 'IMPLICATION',
      inputs: ['has_wings'],
      output: 'is_bird',
      op: 'IDENTITY',
      weight: 0.8
    },
    {
      id: 'feathers_imply_bird',
      type: 'IMPLICATION',
      inputs: ['has_feathers'],
      output: 'is_bird',
      op: 'IDENTITY',
      weight: 0.9
    }
  ],
  constraints: [
    {
      id: 'mutex_example',
      type: 'MUTEX',
      source: 'has_wings',
      target: 'has_feathers',
      weight: 1.0
    }
  ]
};

const engine = new NeuroEngine(schema);
const result = engine.run({ has_wings: 1.0, has_feathers: 1.0 });
console.log(result.is_bird);
```

## 2) Probabilistic logic network support (NeuroJSON v0.1)

**Supported (v0.1 sampler):**
- Boolean probabilistic programs with weighted factors
- Evidence clamping (0/1)
- Likelihood-weighted sampling
- Explanations and warnings for unknown evidence/queries

**Not yet supported:**
- Recursion/unification/grounding (ProbLog-style)
- Exact inference or loopy belief propagation
- Neural predicates with learning

### Minimal PLN-style example (NeuroJSON v0.1)
```typescript
import { infer } from 'neurosym';

const program = {
  version: '0.1',
  variables: {
    rain: { type: 'boolean', prior: 0.2 },
    sprinkler: { type: 'boolean', prior: 0.1 },
    wet_grass: { type: 'boolean', prior: 0.05 }
  },
  factors: [
    { inputs: ['rain'], output: 'wet_grass', op: 'IF_THEN', weight: 0.8, mode: 'support' },
    { inputs: ['sprinkler'], output: 'wet_grass', op: 'IF_THEN', weight: 0.6, mode: 'support' }
  ],
  evidence: { wet_grass: 1 },
  queries: ['rain', 'sprinkler']
};

const result = infer(program, undefined, { iterations: 5000, seed: 42 });
console.log(result.posteriors);
```

## 3) KnowShowGo (KSG) and LNN/PLN // pragma: allowlist secret

KSG uses a graph memory and compiles a **reasoning view** into NeuroJSON. This
provides:
- LNN-style fuzzy inference (via the v1.0 engine).
- Probabilistic inference for portable NeuroJSON programs (v0.1 sampler).

Neural predicates and advanced VSA are intentionally minimal for the first
release; see `docs/KNOWSHOWGO_MODEL.md` and `docs/KNOWSHOWGO_PLAN.md` for the // pragma: allowlist secret
roadmap.
