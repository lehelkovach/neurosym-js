from knowshowgo.belief_resolver import PredicateBeliefResolver
from knowshowgo.models import Node
from knowshowgo.neural_predicates import NeuralPredicateRegistry


def test_predicate_registry_clamps() -> None:
    registry = NeuralPredicateRegistry()
    registry.register("hot", lambda _: 1.4)
    assert registry.evaluate("hot", {}) == 1.0
    assert registry.evaluate("missing", {}) is None


def test_predicate_belief_resolver_reads_payload() -> None:
    registry = NeuralPredicateRegistry()
    registry.register("temp_is_high", lambda inputs: inputs.get("temp", 0) / 100.0)

    node = Node.create(
        prototype_id=None,
        payload={"predicate": "temp_is_high", "predicate_inputs": {"temp": 80}},
    )
    resolver = PredicateBeliefResolver(registry=registry)

    assert resolver.get_evidence(node) == 0.8
