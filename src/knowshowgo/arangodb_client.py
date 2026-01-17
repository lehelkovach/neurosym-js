from typing import Any, Dict, Optional

try:
    from arango import ArangoClient  # type: ignore
except ImportError:  # pragma: no cover - python-arango may not be installed in all environments
    ArangoClient = None  # type: ignore


class ArangoGraphStore:
    """Thin wrapper around Arango for nodes/associations/prototypes and embeddings.

    This is intentionally minimal and can be fleshed out with concrete collection names and auth config.
    """

    def __init__(
        self,
        db_name: str = "knowshowgo",
        *,
        username: Optional[str] = None,
        password: Optional[str] = None,
        hosts: Optional[str] = None,
        client: Any = None,
    ) -> None:
        if client:
            self._client = client
        elif ArangoClient:
            self._client = ArangoClient(hosts=hosts or "http://localhost:8529")
        else:
            self._client = None

        self._db = None
        if self._client:
            self._db = self._client.db(db_name, username=username, password=password)

        # Defaults; override as needed.
        self.nodes_col = "nodes"
        self.prototypes_col = "prototypes"
        self.associations_col = "associations"
        self.embeddings_col = "embeddings"

    # ---- Prototypes / Nodes / Associations ----
    def upsert_prototype(self, proto: Dict[str, Any]) -> None:
        if not self._db:
            return
        col = self._db.collection(self.prototypes_col)
        col.insert(proto, overwrite=True)

    def upsert_node(self, node: Dict[str, Any]) -> None:
        if not self._db:
            return
        # duplicate into nodes collection
        col = self._db.collection(self.nodes_col)
        col.insert(node, overwrite=True)

    def upsert_association(self, assoc: Dict[str, Any]) -> None:
        if not self._db:
            return
        col = self._db.collection(self.associations_col)
        col.insert(assoc, overwrite=True)

    # ---- Embeddings (versioned) ----
    def upsert_embedding_version(self, embedding: Dict[str, Any]) -> str:
        """Stores a new embedding version and returns its key."""
        if not self._db:
            return ""
        col = self._db.collection(self.embeddings_col)
        meta = col.insert(embedding, overwrite=False)
        return meta.get("_key", "")

    # ---- Weights ----
    async def increment_edge_weight(self, source: str, target: str, delta: float, max_weight: float) -> None:
        """Increment edge weight with cap. Concrete AQL update should be added here."""
        if not self._db:
            return
        # Placeholder: a real impl would use afox or AQL update on associations_col
        return
