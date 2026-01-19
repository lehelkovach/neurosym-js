from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from .models import Node


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
