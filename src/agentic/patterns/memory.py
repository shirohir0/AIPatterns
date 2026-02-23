from __future__ import annotations

from typing import List

from ..memory import SimpleMemory


def memory_demo(mem: SimpleMemory, query: str) -> List[str]:
    results = mem.retrieve(query)
    return [item["content"] for item in results]
