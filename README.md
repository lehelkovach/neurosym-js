# NeuroSym.js

NeuroSym.js is a zero-dependency JavaScript/TypeScript library for neurosymbolic AI.
It implements Logical Neural Networks (LNN) with a JSON-first "NeuroJSON" schema so
logic can be serialized, versioned, and shared.

Core idea: code as data. Logic lives in JSON, not hardcoded functions.

## Features
- Lukasiewicz fuzzy logic core and continuous truth values (0.0 to 1.0)
- Graph-based inference with rules and constraints
- Argumentation via attack/support relations
- Heuristic weight training from examples
- Zero runtime dependencies with TypeScript types

## Repository layout
- `neurosym-js/`: primary TypeScript package (core library)
- `neurosym.js-standalone/`: standalone package with docs, examples, and release assets
- `src/knowshowgo/` and `packages/`: optional Python integration and KnowShowGo modules
- `docs/`: design notes and integration guides

## Quick start (JavaScript/TypeScript)
Install from npm (published package name is `neurosym`):
```bash
npm install neurosym
```

Use the main API:
```typescript
import { NeuroEngine } from 'neurosym';

const schema = {
  version: '1.0',
  variables: {
    rain: { type: 'bool', prior: 0.3 },
    wet_ground: { type: 'bool', prior: 0.1 }
  },
  rules: [{
    id: 'rain_wets',
    type: 'IMPLICATION',
    inputs: ['rain'],
    output: 'wet_ground',
    op: 'IDENTITY',
    weight: 0.95
  }],
  constraints: []
};

const engine = new NeuroEngine(schema);
const result = engine.run({ rain: 1.0 });
console.log(result.wet_ground);
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
- Architecture and roadmap: `docs/NEUROSYM_MASTER_PLAN.md`
- Python integration guide: `docs/KSG_INTEGRATION.md`
