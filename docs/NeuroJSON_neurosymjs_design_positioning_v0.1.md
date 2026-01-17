# NeuroJSON + neurosym.js v0.1: Design and Positioning

This document defines the scope, positioning, and design intent for NeuroJSON
and the neurosym.js v0.1 library. It is written to align contributors and
users on what v0.1 is, what it is not, and how it should evolve.

## Positioning
NeuroJSON is a small, versioned, JSON-first language for neurosymbolic logic.
neurosym.js is the reference JavaScript/TypeScript implementation that can
validate, compile, and run NeuroJSON programs.

The core stance is "code as data":
- Logic is expressed as JSON and stored alongside data.
- Programs are portable, inspectable, and versioned.
- Reasoning can be embedded into web apps, services, and tools without
  heavyweight dependencies.

## Design goals (v0.1)
- A strict, minimal schema that is easy to validate.
- Boolean variables only, with weighted support and inhibition.
- A simple compiler to an explicit intermediate representation (IR).
- A deterministic and testable inference engine (likelihood-weighted sampling).
- Clear diagnostics for schema errors and invalid programs.

## Non-goals (v0.1)
- Categorical or continuous variables.
- Complex factor graphs with arbitrary potentials.
- Large-scale optimization or GPU acceleration.
- Full logic programming (Datalog/Prolog) semantics.

## Why NeuroJSON (and not Prolog/Datalog)
NeuroJSON is designed for probabilistic and fuzzy reasoning with uncertainty
as a first-class concern. Datalog and Prolog emphasize deterministic logical
entailment, whereas NeuroJSON is intentionally lightweight and numeric:

- NeuroJSON: weighted factors + probabilistic aggregation.
- Datalog/Prolog: discrete rules + strict logical entailment.

In short: NeuroJSON is pragmatic for uncertainty; Datalog/Prolog are ideal for
strict symbolic reasoning.

## Core model (v0.1)
NeuroJSON v0.1 is a directed graph of variables connected by factors.

- Variables are boolean with optional priors in [0, 1].
- Factors connect inputs to a single output.
- Operations: IF_THEN, AND, OR, NOT.
- Mode: support or inhibit.

The recommended aggregation is noisy-OR for supports and multiplicative
attenuation for inhibition.

## Versioning
- Programs must declare a version string.
- Validation is strict and versioned.
- Breaking changes require a version bump.

## Intended usage patterns
- Store NeuroJSON alongside other knowledge artifacts.
- Compile to a lightweight IR for fast inference.
- Provide posteriors and minimal explanations.
- Add integration layers that map to external systems (e.g., KnowShowGo).

## Roadmap pointers
v0.1 establishes the minimal program shape and inference behavior. v0.2 and
beyond can add categorical variables, loopy inference, richer factors, and
compiler backends for symbolic systems.
