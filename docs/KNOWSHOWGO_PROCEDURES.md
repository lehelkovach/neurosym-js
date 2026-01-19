# Procedure and Decision Modeling (KSG Convention)

This document defines a minimal, parsimonious convention for representing
procedures, forks, and conditional logic in KnowShowGo.

## Primitives
Use only nodes and associations:
- **Step node**: a procedure step (concept node).
- **Condition node**: a boolean predicate (concept node).
- **Gate node**: an OR/AND decision node (concept node).
- **Context node**: runtime context or situation (concept node).

Use existing association types and weights:
- `FOLLOWS`: directed sequence edge (step ordering).
- `SUPPORTS`: graded support for activating a gate or step.
- `ATTACKS`: graded inhibition (optional).
- `MUTEX`: enforce winner-take-all among options.

## Minimal pattern
1) **Sequence**: link steps with `FOLLOWS`.
2) **Fork**: route through a gate node.
3) **Conditions**: connect condition nodes to the gate with `SUPPORTS`.
4) **Options**: connect gate to option steps with `FOLLOWS` (or `IMPLIES`).
5) **WTA**: add `MUTEX` among option steps.

## Example: sort algorithm (first step)
Nodes:
- `Algorithm:Sort`
- `Step:IterateList`
- `Step:SwapElements`
- `Gate:Step1Options`
- `Cond:ListHasInversions`
- `Cond:ListNearlySorted`

Edges:
- `Algorithm:Sort` → `Gate:Step1Options` (`SUPPORTS`, weight=1.0)
- `Cond:ListHasInversions` → `Gate:Step1Options` (`SUPPORTS`, weight=0.9)
- `Cond:ListNearlySorted` → `Gate:Step1Options` (`SUPPORTS`, weight=0.5)
- `Gate:Step1Options` → `Step:IterateList` (`FOLLOWS`, weight=1.0, position=1)
- `Gate:Step1Options` → `Step:SwapElements` (`FOLLOWS`, weight=0.6, position=1)
- `Step:IterateList` ↔ `Step:SwapElements` (`MUTEX`)

Runtime:
- Set condition nodes as evidence (locked or high truth_value).
- Inference activates the most supported option.
- `FOLLOWS` preserves procedural order after the fork.

## Notes
- This is a **convention**, not a schema change.
- It stays parsimonious: only nodes + weighted associations.
- Gates emulate hyperedges without adding new graph primitives.
