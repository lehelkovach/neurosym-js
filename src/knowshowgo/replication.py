import asyncio
from dataclasses import dataclass
from typing import Protocol


@dataclass
class EdgeUpdate:
    source: str
    target: str
    delta: float
    max_weight: float


class GraphClient(Protocol):
    async def increment_edge_weight(self, source: str, target: str, delta: float, max_weight: float) -> None: ...


class AsyncReplicator:
    """Background worker to push edge-weight updates to long-term store."""

    def __init__(self, client: GraphClient) -> None:
        self.client = client
        self.queue: asyncio.Queue[EdgeUpdate] = asyncio.Queue()
        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        if self._task is None:
            self._task = asyncio.create_task(self._worker())

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None

    async def enqueue(self, update: EdgeUpdate) -> None:
        await self.queue.put(update)

    async def _worker(self) -> None:
        while True:
            upd = await self.queue.get()
            try:
                await self.client.increment_edge_weight(
                    source=upd.source, target=upd.target, delta=upd.delta, max_weight=upd.max_weight
                )
            finally:
                self.queue.task_done()
