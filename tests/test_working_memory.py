from knowshowgo.working_memory import WorkingMemoryGraph


def test_link_reinforce_and_cap_weight():
    wm = WorkingMemoryGraph(reinforce_delta=2.0, max_weight=3.0)

    # Seed new edge with provided weight
    first = wm.link("proto", "inst", seed_weight=1.0)
    assert first == 1.0

    # Reinforce should cap at max_weight
    reinforced = wm.link("proto", "inst")
    assert reinforced == 3.0
    assert wm.get_weight("proto", "inst") == 3.0

    # Access reinforces but still respects cap
    accessed = wm.access("proto", "inst")
    assert accessed == 3.0

    # Access on missing edge is a no-op
    assert wm.access("missing", "edge") is None
