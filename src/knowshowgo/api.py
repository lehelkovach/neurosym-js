from __future__ import annotations

from typing import Any, Dict, List, Optional

from .models import (
    Association,
    OBJECT_PROPERTY_PROTOTYPE,
    OBJECT_PROTOTYPE,
    TAG_PROTOTYPE,
    SET_PROTOTYPE,
    QUANTITY_PROTOTYPE,
    UNDEFINED_PROTOTYPE,
    Node,
    Prototype,
    seed_core_prototypes,
)
from .arangodb_client import ArangoGraphStore


class KnowShowGoAPI:
    """ORM-like convenience layer over Arango + in-memory models."""

    def __init__(self, store: ArangoGraphStore) -> None:
        self.store = store
        self.prototypes: Dict[str, Prototype] = {}

    def ensure_core_prototypes(self, created_by: Optional[str] = None) -> None:
        seeds = seed_core_prototypes(created_by=created_by)
        for proto in seeds.values():
            self.prototypes.setdefault(proto.name, proto)
            self.store.upsert_prototype(self._proto_doc(proto))

    def create_prototype_version(
        self, name: str, schema_meta: Dict[str, Any], tags: Optional[List[str]], created_by: Optional[str], previous_version_id: Optional[str]
    ) -> Prototype:
        proto = Prototype.base(name=name, schema_meta=schema_meta, tags=tags, created_by=created_by, previous_version_id=previous_version_id)
        self.prototypes[name] = proto
        self.store.upsert_prototype(self._proto_doc(proto))
        return proto

    def create_node(
        self,
        prototype_id: Optional[str],
        payload: Optional[Dict[str, Any]] = None,
        created_by: Optional[str] = None,
        context_ids: Optional[List[str]] = None,
    ) -> Node:
        node = Node.create(prototype_id=prototype_id, payload=payload, created_by=created_by, context_ids=context_ids)
        self.store.upsert_node(self._node_doc(node))
        return node

    def add_association(
        self,
        source_id: str,
        target_id: str,
        relation: str,
        weight: float = 0.0,
        created_by: Optional[str] = None,
        position: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Association:
        assoc = Association.create(
            source_id=source_id,
            target_id=target_id,
            relation=relation,
            weight=weight,
            created_by=created_by,
            position=position,
            metadata=metadata,
        )
        self.store.upsert_association(self._assoc_doc(assoc))
        return assoc

    def add_object_property(self, object_id: str, property_node_id: str, created_by: Optional[str] = None) -> Association:
        return self.add_association(object_id, property_node_id, relation="ELEMENT_OF", weight=0.0, created_by=created_by)

    def add_tag(self, object_id: str, tag_node_id: str, weight: float = 1.0, created_by: Optional[str] = None) -> Association:
        return self.add_association(object_id, tag_node_id, relation="HAS_TAG", weight=weight, created_by=created_by)

    # ---- Helpers to render docs for Arango ----
    @staticmethod
    def _proto_doc(proto: Prototype) -> Dict[str, Any]:
        return {
            "_key": proto.id,
            "name": proto.name,
            "schema_meta": proto.schema_meta,
            "tags": proto.tags,
            "created_at": proto.created_at.isoformat(),
            "created_by": proto.created_by,
            "previous_version_id": proto.previous_version_id,
        }

    @staticmethod
    def _node_doc(node: Node) -> Dict[str, Any]:
        return {
            "_key": node.id,
            "prototype_id": node.prototype_id or UNDEFINED_PROTOTYPE,
            "prototype_ids": node.prototype_ids,
            "payload": node.payload,
            "associations": node.associations,
            "embedding_ref": node.embedding_ref,
            "weight": node.weight,
            "created_at": node.created_at.isoformat(),
            "created_by": node.created_by,
            "context_ids": node.context_ids,
        }

    @staticmethod
    def _assoc_doc(assoc: Association) -> Dict[str, Any]:
        return {
            "_key": assoc.id,
            "source_id": assoc.source_id,
            "target_id": assoc.target_id,
            "relation": assoc.relation,
            "weight": assoc.weight,
            "created_at": assoc.created_at.isoformat(),
            "created_by": assoc.created_by,
            "previous_version_id": assoc.previous_version_id,
            "position": assoc.position,
            "metadata": assoc.metadata,
        }
