# NeuroJSON Homoiconic DSL (proposal)

This document proposes a homoiconic JSON-based DSL that treats logic programs
as data. The intent is to keep a single program representation that can:

- compile to the existing NeuroJSON v0.1 factor format,
- run in deterministic (DAG) or cyclic (fixpoint) modes,
- support explainability traces that stay stable across modes.

This is a proposal for v0.2+ and does not replace the current NeuroJSON v0.1
spec. The goal is to define a clear substrate for "code as data" while keeping
the core library small and predictable.

## 1) Design goals

1) Homoiconic program representation (JSON as code and data).
2) Clear, minimal core forms with stable evaluation rules.
3) A compiler path into the existing NeuroJSON factor model.
4) Explicit support for recursion (cycles) with fixpoint semantics.
5) Explainability trace format that works for DAG and cyclic graphs.

## 2) Program shape (JSON s-expressions)

Programs are JSON objects with a `version`, a `defs` map, and a `main`
expression. Expressions are encoded as JSON arrays ("s-expressions").

```json
{
  "version": "sexpr-0.1",
  "defs": {
    "is_bird": ["and", ["var", "has_feathers"], ["var", "can_fly"]],
    "can_fly": ["if", ["var", "is_penguin"], 0, ["var", "is_bird"]]
  },
  "main": ["is_bird"]
}
```

### Core forms (proposed)

| Form | Meaning |
| --- | --- |
| `["var", name]` | lookup variable |
| `["let", [[name, expr], ...], body]` | local bindings |
| `["if", cond, then, else]` | conditional |
| `["call", name, ...args]` | call a defined procedure |
| `["and", expr, ...]` | fuzzy AND (Lukasiewicz) |
| `["or", expr, ...]` | fuzzy OR (Lukasiewicz) |
| `["not", expr]` | fuzzy NOT |
| `["imply", a, b]` | implication (a supports b) |
| `["attack", a, b]` | argumentation/defeat (a inhibits b) |
| `["collapse", expr, threshold]` | harden fuzzy value to 0/1 |

Notes:
- `["call", name, ...]` and `["var", name]` are separate: `call` invokes a
  procedure; `var` reads a value from state/evidence.
- `imply` and `attack` are syntax sugar that compile into factor edges.
- `collapse` is explicit so "hard" logic remains a projection of the soft model.

## 3) Graph IR (compiler target)

The DSL should compile into an intermediate representation that aligns with
NeuroJSON v0.1 factors and constraints.

```json
{
  "variables": {
    "can_fly": { "type": "boolean", "prior": 0.2 }
  },
  "factors": [
    { "inputs": ["bird"], "output": "can_fly", "op": "IF_THEN", "weight": 0.9, "mode": "support", "id": "f1" }
  ],
  "constraints": [
    { "source": "penguin", "target": "can_fly", "mode": "inhibit", "weight": 1.0, "id": "c1" }
  ]
}
```

Mapping guidance:
- `["imply", a, b]` compiles to a factor (`IF_THEN`) with `mode: support`.
- `["attack", a, b]` compiles to a constraint with `mode: inhibit`.
- `["and", ...]` and `["or", ...]` compile to small factor networks.

## 4) Evaluation semantics

### 4.1 DAG mode (acyclic)

- Topologically sort dependencies.
- Evaluate each node once (no recursion).
- This yields deterministic output and clear explanations.

### 4.2 Cyclic mode (recursion)

To support recursion, allow cycles and define a fixpoint rule:

1) Initialize all variables to priors.
2) Iterate updates until convergence or max iterations.
3) Convergence is defined by an epsilon delta per node.

Recommended defaults:
- `maxIterations = 10`
- `epsilon = 1e-3`
- Optional damping: `new = old * (1 - alpha) + update * alpha`

If convergence fails, return a warning with the final partial trace.

### 4.3 Soft-to-hard collapse

Use the explicit `collapse` form to harden values:

```
collapse(x, 0.5) => x >= 0.5 ? 1 : 0
```

This keeps the same program usable as fuzzy or deterministic logic depending
on the runtime target.

## 5) Explainability trace format

The evaluator should emit a trace of the form:

```json
{
  "iterations": 3,
  "warnings": [],
  "steps": [
    {
      "iteration": 1,
      "node": "can_fly",
      "inputs": ["bird"],
      "op": "IF_THEN",
      "weight": 0.9,
      "prior": 0.2,
      "value_before": 0.2,
      "value_after": 0.86,
      "delta": 0.66
    }
  ],
  "scc_summary": [
    {
      "nodes": ["a", "b"],
      "iterations": 4,
      "converged": true,
      "delta_max": 0.0007
    }
  ]
}
```

Notes:
- The `steps` array is an ordered log of updates.
- For cyclic graphs, compute strongly connected components (SCCs) and include
  a short summary per SCC.
- If convergence fails, set `converged: false` and include the final delta.

## 6) Compatibility with NeuroJSON v0.1

The homoiconic DSL should compile into a strict NeuroJSON v0.1 program when:

- all variables are boolean,
- ops are limited to IF_THEN/AND/OR/NOT,
- recursion is disabled or unrolled to a finite depth.

When recursion is used, the compiler should emit a warning that the output
requires cyclic evaluation (fixpoint semantics).

## 7) Recommended API surface (npm)

```ts
parse(json): Program
validate(program): void
compile(program): NeuroJSONProgram
evaluate(program, options): Result
explain(program, options): Trace
```

The `evaluate` method should accept:

- `mode: "dag" | "cyclic"`
- `maxIterations`, `epsilon`, `damping`
- `collapseThreshold` (optional)

## 8) Open decisions

- Exact mapping of `and`/`or` to factor networks (single factor vs expansion).
- Whether `call` must be pure (no side effects).
- Whether to allow full Turing completeness or keep to logic-only forms.

