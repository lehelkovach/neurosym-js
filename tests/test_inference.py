from knowshowgo.graph import KnowledgeGraph
from knowshowgo.inference import process_instruction


def test_midnight_trash_event():
    graph = KnowledgeGraph()
    proto, inst = process_instruction(graph, "At midnight, remind me to take out the trash.")

    assert proto.kind == "event"
    assert proto.name == "event"
    assert inst.attributes["time"] == "00:00"
    assert "trash" in inst.attributes["action"].lower()

    # Prototype is reused on subsequent event instructions
    proto2, inst2 = process_instruction(graph, "Remind me at midnight to check the oven.")
    assert proto2.id == proto.id
    assert inst2.attributes["time"] == "00:00"