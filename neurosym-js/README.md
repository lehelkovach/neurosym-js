# NeuroSym.js

NeuroSym.js is a zero-dependency JavaScript/TypeScript library for NeuroJSON
v0.1. It validates, compiles, and runs boolean neurosymbolic programs with
lightweight probabilistic inference.

Core philosophy: code as data. Logic is serialized as JSON, not hardcoded
functions.

## Features
- NeuroJSON v0.1 validation (AJV) with clear errors
- Compiler to a small intermediate representation (IR)
- Likelihood-weighted sampler for boolean programs
- Minimal explanations for supporting and inhibiting factors
- TypeScript-first types and exports

## Installation
```bash
npm install neurosym
```

## Quick start
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
  queries: ['rain', 'sprinkler', 'wet_grass']
};

const result = infer(program, undefined, { iterations: 5000, seed: 42 });
console.log(result.posteriors);
```

## How it differs from Datalog/Prolog
NeuroJSON is numeric and uncertainty-first:
- NeuroJSON uses weighted factors and probabilistic aggregation.
- Datalog/Prolog use strict logical entailment over discrete facts.

In short: NeuroJSON is practical for uncertain signals; Datalog/Prolog are
best for strict symbolic reasoning.

## NeuroJSON v0.1
Spec and schema live in `neurojson/`:
- Spec: `neurojson/spec/neurojson.v0.1.md`
- Schema: `neurojson/spec/neurojson.schema.json`
- Examples: `neurojson/examples/`

## API
```typescript
import { validateProgram, compileProgram, infer } from 'neurosym';
```

- `validateProgram(program)` -> `{ valid, errors }`
- `compileProgram(program)` -> `ProgramIR`
- `infer(programOrIr, evidence?, opts?)` -> `{ posteriors, explanations, ... }`

## Examples
- `examples/wet-grass.ts`
- `examples/inhibit.ts`
- `examples/conflict.ts`

## Development
```bash
npm install
npm test
npm run lint
npm run typecheck
npm run build
```

## Documentation
- Unified plan and positioning: `docs/DEVELOPMENT_PLAN.md`
- KnowShowGo plan (separate track): `docs/KNOWSHOWGO_PLAN.md`
