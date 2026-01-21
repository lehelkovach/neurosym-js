from knowshowgo.models import Node
from knowshowgo.vsa import (
    VsaEncoder,
    VsaMemoryIndex,
    attach_vsa,
    bind,
    bundle,
    cosine_similarity,
    get_node_vsa,
    unbind,
)


def test_vsa_encoder_is_deterministic() -> None:
    encoder = VsaEncoder(dim=16, seed=42)
    first = encoder.vector("apple")
    second = encoder.vector("apple")
    assert first == second
    assert cosine_similarity(first, second) == 1.0


def test_binding_and_unbinding_recovers_signal() -> None:
    encoder = VsaEncoder(dim=32, seed=7)
    key = encoder.vector("key")
    value = encoder.vector("value")
    bound = bind(key, value)
    recovered = unbind(bound, key)
    assert cosine_similarity(recovered, value) > 0.9


def test_bundle_similarity_is_nonzero() -> None:
    encoder = VsaEncoder(dim=32, seed=9)
    a = encoder.vector("a")
    b = encoder.vector("b")
    merged = bundle([a, b])
    assert cosine_similarity(merged, a) > 0
    assert cosine_similarity(merged, b) > 0


def test_vsa_memory_index_returns_best_match() -> None:
    encoder = VsaEncoder(dim=16, seed=1)
    index = VsaMemoryIndex(encoder)
    index.add_symbol("id_a", "alpha")
    index.add_symbol("id_b", "beta")

    query = encoder.vector("alpha")
    results = index.query(query, top_k=1)
    assert results[0][0] == "id_a"


def test_attach_and_get_node_vsa() -> None:
    node = Node.create(prototype_id=None)
    vec = [0.1, 0.2, 0.3]
    attach_vsa(node, vec)
    recovered = get_node_vsa(node)
    assert recovered == vec
