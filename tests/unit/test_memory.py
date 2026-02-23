from common.memory import SimpleMemory


def test_memory_add_and_retrieve():
    mem = SimpleMemory()
    mem.add("fact", "Agents use tools")
    mem.add("note", "Memory keeps context")

    hits = mem.retrieve("tools context")
    assert len(hits) == 2


def test_memory_recent():
    mem = SimpleMemory()
    mem.add("fact", "one")
    mem.add("fact", "two")
    mem.add("fact", "three")

    recent = mem.recent(2)
    assert [item["content"] for item in recent] == ["two", "three"]
