from __future__ import annotations

from typing import List

from common.memory import SimpleMemory
from common.logging_utils import get_logger

logger = get_logger(__name__)


def memory_demo(mem: SimpleMemory, query: str) -> List[str]:
    """
    Учебный пример памяти.

    Пока это кастомная память, но интерфейс можно заменить
    на LangChain memory, когда понадобится хранение истории диалога.
    """

    logger.info("LC memory demo | query=%s", query)
    results = mem.retrieve(query)
    return [item["content"] for item in results]
