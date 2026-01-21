from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple
import hashlib
import math
import random

from .models import Node

VSA_PAYLOAD_KEY = "vsa_vector"


def _seed_from_symbol(symbol: str, base_seed: int) -> int:
    digest = hashlib.sha256(f"{base_seed}:{symbol}".encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def normalize_vector(vector: List[float]) -> List[float]:
    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return [0.0 for _ in vector]
    return [value / norm for value in vector]


def random_bipolar_vector(dim: int, seed: int) -> List[float]:
    rng = random.Random(seed)
    raw = [1.0 if rng.random() >= 0.5 else -1.0 for _ in range(dim)]
    return normalize_vector(raw)


def bundle(vectors: Iterable[List[float]], weights: Optional[Iterable[float]] = None) -> List[float]:
    vector_list = list(vectors)
    if not vector_list:
        return []
    dim = len(vector_list[0])
    weight_list = list(weights) if weights is not None else [1.0] * len(vector_list)
    if len(weight_list) != len(vector_list):
        raise ValueError("weights must match number of vectors")

    summed = [0.0 for _ in range(dim)]
    for vec, weight in zip(vector_list, weight_list):
        if len(vec) != dim:
            raise ValueError("all vectors must have the same dimension")
        for idx, value in enumerate(vec):
            summed[idx] += value * weight
    return normalize_vector(summed)


def bind(left: List[float], right: List[float]) -> List[float]:
    if len(left) != len(right):
        raise ValueError("vectors must have the same dimension")
    return normalize_vector([l * r for l, r in zip(left, right)])


def unbind(bound: List[float], key: List[float]) -> List[float]:
    return bind(bound, key)


def cosine_similarity(left: List[float], right: List[float]) -> float:
    if len(left) != len(right):
        raise ValueError("vectors must have the same dimension")
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    dot = sum(l * r for l, r in zip(left, right))
    return dot / (left_norm * right_norm)


@dataclass
class VsaEncoder:
    """Deterministic symbol-to-vector encoder."""

    dim: int = 128
    seed: int = 0
    _cache: Dict[str, List[float]] = field(default_factory=dict, init=False)

    def vector(self, symbol: str) -> List[float]:
        if symbol in self._cache:
            return list(self._cache[symbol])
        seed = _seed_from_symbol(symbol, self.seed)
        vec = random_bipolar_vector(self.dim, seed)
        self._cache[symbol] = vec
        return list(vec)


@dataclass
class VsaMemoryIndex:
    """In-memory VSA index for nearest-neighbor recall."""

    encoder: VsaEncoder
    _vectors: Dict[str, List[float]] = field(default_factory=dict, init=False)

    def add(self, item_id: str, vector: List[float]) -> None:
        if len(vector) != self.encoder.dim:
            raise ValueError("vector dimension does not match encoder")
        self._vectors[item_id] = normalize_vector(vector)

    def add_symbol(self, item_id: str, symbol: str) -> List[float]:
        vector = self.encoder.vector(symbol)
        self.add(item_id, vector)
        return vector

    def query(self, vector: List[float], top_k: int = 5) -> List[Tuple[str, float]]:
        if not self._vectors:
            return []
        if len(vector) != self.encoder.dim:
            raise ValueError("vector dimension does not match encoder")
        normalized = normalize_vector(vector)
        scored = [
            (item_id, cosine_similarity(normalized, stored))
            for item_id, stored in self._vectors.items()
        ]
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]


def attach_vsa(node: Node, vector: List[float]) -> None:
    node.payload[VSA_PAYLOAD_KEY] = list(vector)


def get_node_vsa(node: Node) -> Optional[List[float]]:
    raw = node.payload.get(VSA_PAYLOAD_KEY)
    if isinstance(raw, list) and all(isinstance(value, (int, float)) for value in raw):
        return [float(value) for value in raw]
    return None
