from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from uuid import uuid4


@dataclass
class Prototype:
    id: str
    name: str
    kind: str
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Instance:
    id: str
    prototype_id: str
    attributes: Dict[str, Any]


class KnowledgeGraph:
    def __init__(self) -> None:
        self._prototypes: Dict[str, Prototype] = {}
        self._instances: Dict[str, Instance] = {}

    def get_prototype(self, name: str) -> Optional[Prototype]:
        return self._prototypes.get(name.lower())

    def ensure_prototype(self, name: str, kind: str, attributes: Optional[Dict[str, Any]] = None) -> Prototype:
        existing = self.get_prototype(name)
        if existing:
            return existing
        prototype = Prototype(id=uuid4().hex, name=name, kind=kind, attributes=attributes or {})
        self._prototypes[name.lower()] = prototype
        return prototype

    def create_instance(self, prototype: Prototype, attributes: Dict[str, Any]) -> Instance:
        instance = Instance(id=uuid4().hex, prototype_id=prototype.id, attributes=attributes)
        self._instances[instance.id] = instance
        return instance