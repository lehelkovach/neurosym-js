# NeuroSym.js

NeuroSym.js is a zero-dependency JavaScript/TypeScript library for neurosymbolic AI.
It implements Logical Neural Networks (LNN) with a JSON-first "NeuroJSON" schema so
logic can be serialized, versioned, and shared.

Core idea: code as data. Logic lives in JSON, not hardcoded functions.

## Features
- NeuroJSON v0.1 spec and AJV schema validation
- Compiler to an explicit intermediate representation (IR)
- Likelihood-weighted sampler for boolean programs
- Minimal explanations for supporting and inhibiting factors
- Zero runtime dependencies with TypeScript types

## Repository layout
- `neurojson/`: NeuroJSON v0.1 spec repo (schema + examples)
- `neurosym-js/`: primary TypeScript package (core library)
- `neurosym.js-standalone/`: standalone package with docs, examples, and release assets
- `src/knowshowgo/` and `packages/`: optional Python integration and KnowShowGo modules
- `docs/`: design notes and integration guides

## Quick start (JavaScript/TypeScript)
Install from npm (published package name is `neurosym`):
```bash
npm install neurosym
```

Use the main API (v0.1):
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

## Development (core library)
```bash
cd neurosym-js
npm install
npm test
npm run build
npm run lint
npm run typecheck
```

## Documentation
- Core package README: `neurosym-js/README.md`
- Standalone docs: `neurosym.js-standalone/docs/`
- NeuroJSON spec: `neurojson/spec/neurojson.v0.1.md`

## Design docs
- Unified plan (includes design/positioning): `docs/DEVELOPMENT_PLAN.md`
- KnowShowGo plan (separate track): `docs/KNOWSHOWGO_PLAN.md`
