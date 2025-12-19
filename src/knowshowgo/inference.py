import asyncio
import re
from typing import Dict, Tuple, Optional

from .graph import KnowledgeGraph, Prototype, Instance
from .working_memory import WorkingMemoryGraph
from .replication import AsyncReplicator, EdgeUpdate

EVENT_KEYWORDS = {"remind", "schedule", "event", "meet", "meeting"}


def infer_concept_kind(instruction: str) -> str:
    text = instruction.lower()
    if any(keyword in text for keyword in EVENT_KEYWORDS):
        return "event"
    return "task"


def extract_event_fields(instruction: str) -> Dict[str, str]:
    # Time extraction (very lightweight)
    time_match = re.search(r"\bat\s+(midnight|noon|\d{1,2}(:\d{2})?\s*(am|pm)?)", instruction, re.IGNORECASE)
    time_value = None
    if time_match:
        phrase = time_match.group(1).lower()
        if phrase == "midnight":
            time_value = "00:00"
        elif phrase == "noon":
            time_value = "12:00"
        else:
            time_value = phrase

    # Remove the time phrase and common reminder phrasing to isolate the action
    text = re.sub(r"(?i)\bat\s+(midnight|noon|\d{1,2}(:\d{2})?\s*(am|pm)?)", "", instruction)
    text = re.sub(r"(?i)\b(remind me to|remind me|please)", "", text)
    action = text.strip(" ,.")

    return {"time": time_value or "unspecified", "action": action or instruction.strip()}


def process_instruction(
    graph: KnowledgeGraph,
    instruction: str,
    working_memory: Optional[WorkingMemoryGraph] = None,
    replicator: Optional[AsyncReplicator] = None,
    embedding_similarity: float = 1.0,
) -> Tuple[Prototype, Instance]:
    """Infer concept kind, ensure prototype, and create an instance for the instruction.

    working_memory: optional in-memory selection layer; strengthened per activation.
    replicator: optional async replicator to long-term store (e.g., Arango).
    """
    kind = infer_concept_kind(instruction)
    prototype_name = "event" if kind == "event" else "task"
    prototype = graph.ensure_prototype(prototype_name, kind, attributes={"source": "inferred"})
    attributes = extract_event_fields(instruction) if kind == "event" else {"description": instruction}
    instance = graph.create_instance(prototype, attributes)

    if working_memory:
        weight = working_memory.link(prototype.id, instance.id, seed_weight=embedding_similarity)
        if replicator:
            # Fire-and-forget replication; caller should ensure replicator.start() is running
            asyncio.create_task(
                replicator.enqueue(
                    EdgeUpdate(source=prototype.id, target=instance.id, delta=working_memory.reinforce_delta, max_weight=working_memory.max_weight)
                )
            )
    return prototype, instance
