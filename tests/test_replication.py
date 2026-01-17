import asyncio
import pytest

from knowshowgo.replication import AsyncReplicator, EdgeUpdate


class FakeGraphClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, float, float]] = []

    async def increment_edge_weight(self, source: str, target: str, delta: float, max_weight: float) -> None:
        self.calls.append((source, target, delta, max_weight))


@pytest.mark.asyncio
async def test_replicator_enqueues_and_flushes_updates():
    client = FakeGraphClient()
    replicator = AsyncReplicator(client)

    await replicator.start()
    await replicator.enqueue(EdgeUpdate(source="a", target="b", delta=0.5, max_weight=10.0))

    await asyncio.wait_for(replicator.queue.join(), timeout=1.0)
    await replicator.stop()

    assert client.calls == [("a", "b", 0.5, 10.0)]
