# NeuroJSON v0.1 Spec Repository

NeuroJSON is a small, versioned JSON format for neurosymbolic programs.
This repo contains the v0.1 spec, the JSON Schema, and runnable examples.

## Contents
- `spec/neurojson.v0.1.md`: spec and semantics
- `spec/neurojson.schema.json`: AJV-compatible JSON Schema
- `examples/`: sample programs for testing and demos
- `docs/mapping-to-ksg.md`: mapping guidance for KSG integrations

## Quick example
```json
{
  "version": "0.1",
  "variables": {
    "rain": { "type": "boolean", "prior": 0.2 },
    "sprinkler": { "type": "boolean", "prior": 0.1 },
    "wet_grass": { "type": "boolean", "prior": 0.05 }
  },
  "factors": [
    { "inputs": ["rain"], "output": "wet_grass", "op": "IF_THEN", "weight": 0.8, "mode": "support" },
    { "inputs": ["sprinkler"], "output": "wet_grass", "op": "IF_THEN", "weight": 0.6, "mode": "support" }
  ],
  "evidence": { "wet_grass": 1 },
  "queries": ["rain", "sprinkler", "wet_grass"]
}
```

## Versioning
This repository tracks NeuroJSON v0.1. New breaking changes require a
version bump and a new schema.
