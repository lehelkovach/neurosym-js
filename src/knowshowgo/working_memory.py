import networkx as nx


class WorkingMemoryGraph:
    """NetworkX-backed working memory used for selection/retrieval.

    v1: reinforcement only (no decay), with a max cap to avoid runaway growth.
    """

    def __init__(self, reinforce_delta: float = 1.0, max_weight: float = 100.0) -> None:
        self._g = nx.DiGraph()
        self.reinforce_delta = reinforce_delta
        self.max_weight = max_weight

    def _ensure_nodes(self, u: str, v: str) -> None:
        if not self._g.has_node(u):
            self._g.add_node(u)
        if not self._g.has_node(v):
            self._g.add_node(v)

    def link(self, source: str, target: str, seed_weight: float = 0.0) -> float:
        """Create or reinforce an edge; returns updated weight."""
        self._ensure_nodes(source, target)
        if self._g.has_edge(source, target):
            self._g[source][target]["weight"] = min(
                self.max_weight, self._g[source][target]["weight"] + self.reinforce_delta
            )
        else:
            self._g.add_edge(source, target, weight=min(self.max_weight, seed_weight))
        return self._g[source][target]["weight"]

    def access(self, source: str, target: str) -> float | None:
        """Access reinforces the edge if present."""
        if not self._g.has_edge(source, target):
            return None
        self._g[source][target]["weight"] = min(
            self.max_weight, self._g[source][target]["weight"] + self.reinforce_delta
        )
        return self._g[source][target]["weight"]

    def get_weight(self, source: str, target: str) -> float | None:
        edge = self._g.get_edge_data(source, target)
        return None if edge is None else edge.get("weight")
