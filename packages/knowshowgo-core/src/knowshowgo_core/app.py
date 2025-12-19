from fastapi import FastAPI
from pydantic import BaseModel

from knowshowgo import KnowledgeGraph, WorkingMemoryGraph, process_instruction


class InstructionRequest(BaseModel):
    text: str


class InstructionResponse(BaseModel):
    prototype_id: str
    instance_id: str
    weight: float | None = None


graph = KnowledgeGraph()
working_memory = WorkingMemoryGraph()
app = FastAPI(title="KnowShowGo Core")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/instructions", response_model=InstructionResponse)
async def handle_instruction(body: InstructionRequest) -> InstructionResponse:
    proto, inst = process_instruction(graph, body.text, working_memory=working_memory, replicator=None, embedding_similarity=1.0)
    weight = working_memory.get_weight(proto.id, inst.id)
    return InstructionResponse(prototype_id=proto.id, instance_id=inst.id, weight=weight)
