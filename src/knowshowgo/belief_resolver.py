from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Optional, Protocol

from .models import Association, LogicType, Node, CONTEXT_PROTOTYPE
from .neural_predicates import NeuralPredicateRegistry


class ContextGraphLike(Protocol):
    nodes: Dict[str, Node]
    associations: Dict[str, Association]


class BeliefResolver(Protocol):
    """Resolves priors and evidence without hard-coding node fields."""

    def get_prior(self, node: Node) -> float:
        ...

    def get_evidence(self, node: Node) -> Optional[float]:
        ...

    def is_locked(self, node: Node) -> bool:
        ...


@dataclass
class DefaultBeliefResolver:
    """Default resolver that preserves current behavior."""

    default_prior: float = 0.5
    use_node_prior: bool = True
    use_node_locked: bool = True
    use_node_truth_as_evidence: bool = False

    def get_prior(self, node: Node) -> float:
        if self.use_node_prior:
            return node.prior
        return self.default_prior

    def get_evidence(self, node: Node) -> Optional[float]:
        if self.use_node_truth_as_evidence and node.is_locked:
            return node.truth_value
        return None

    def is_locked(self, node: Node) -> bool:
        if self.use_node_locked:
            return node.is_locked
        return False


@dataclass
class GraphDerivedBeliefResolver(DefaultBeliefResolver):
    """Derives priors/evidence from context and associations (lazy, cached)."""

    context_boost: float = 0.2
    use_context_ids: bool = True
    use_support_edges: bool = True
    treat_context_as_evidence: bool = True
    _prior_by_node: Dict[str, float] = field(default_factory=dict, init=False)
    _evidence_by_node: Dict[str, float] = field(default_factory=dict, init=False)

    def prepare_context(
        self,
        context: ContextGraphLike,
        active_context_ids: Optional[Iterable[str]] = None,
    ) -> None:
        active = set(active_context_ids or [])
        for node in context.nodes.values():
            if node.prototype_id == CONTEXT_PROTOTYPE or node.payload.get("is_context"):
                active.add(node.id)

        support_boosts: Dict[str, float] = {}
        if self.use_support_edges and active:
            for assoc in context.associations.values():
                logic = assoc.logic_meta
                if (
                    logic
                    and logic.type == LogicType.SUPPORTS
                    and assoc.source_id in active
                ):
                    support_boosts[assoc.target_id] = support_boosts.get(assoc.target_id, 0.0) + (
                        logic.weight * self.context_boost
                    )

        self._prior_by_node = {}
        self._evidence_by_node = {}

        for node in context.nodes.values():
            prior = self.get_prior(node)
            if self.use_context_ids and active and node.context_ids:
                if any(ctx_id in active for ctx_id in node.context_ids):
                    prior = min(1.0, prior + self.context_boost)

            prior = min(1.0, prior + support_boosts.get(node.id, 0.0))
            self._prior_by_node[node.id] = prior

            if self.treat_context_as_evidence and node.id in active:
                self._evidence_by_node[node.id] = 1.0

    def get_prior(self, node: Node) -> float:
        if node.id in self._prior_by_node:
            return self._prior_by_node[node.id]
        return super().get_prior(node)

    def get_evidence(self, node: Node) -> Optional[float]:
        if node.id in self._evidence_by_node:
            return self._evidence_by_node[node.id]
        return super().get_evidence(node)

    def is_locked(self, node: Node) -> bool:
        if node.id in self._evidence_by_node:
            return True
        return super().is_locked(node)


@dataclass
class PredicateBeliefResolver(DefaultBeliefResolver):
    """Derives evidence from a neural predicate registry."""

    registry: NeuralPredicateRegistry
    predicate_key: str = "predicate"
    predicate_inputs_key: str = "predicate_inputs"

    def get_evidence(self, node: Node) -> Optional[float]:
        evidence = super().get_evidence(node)
        if evidence is not None:
            return evidence
        predicate_name = node.payload.get(self.predicate_key)
        if not predicate_name:
            return None
        raw_inputs = node.payload.get(self.predicate_inputs_key, {})
        if not isinstance(raw_inputs, dict):
            return None
        inputs = {
            key: float(value)
            for key, value in raw_inputs.items()
            if isinstance(value, (int, float))
        }
        return self.registry.evaluate(str(predicate_name), inputs)
