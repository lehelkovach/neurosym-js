from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, Mapping, Optional

NeuralPredicate = Callable[[Mapping[str, float]], float]


def clamp_probability(value: float) -> float:
    if value < 0:
        return 0.0
    if value > 1:
        return 1.0
    return value


@dataclass
class NeuralPredicateRegistry:
    """Registry for neural predicates used as evidence sources."""

    predicates: Dict[str, NeuralPredicate] = field(default_factory=dict)

    def register(self, name: str, predicate: NeuralPredicate) -> None:
        self.predicates[name] = predicate

    def evaluate(self, name: str, inputs: Mapping[str, float]) -> Optional[float]:
        predicate = self.predicates.get(name)
        if predicate is None:
            return None
        try:
            value = predicate(inputs)
        except Exception:
            return None
        if not isinstance(value, (int, float)):
            return None
        return clamp_probability(float(value))
