from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict

from common.logging_utils import get_logger

logger = get_logger(__name__)


@dataclass
class SimpleMemory:
    """Простейшее хранилище в памяти с наивным поиском по ключевым словам."""

    items: List[Dict[str, str]] = field(default_factory=list)

    def add(self, kind: str, content: str) -> None:
        # Сохраняем элемент памяти с типом и текстом.
        logger.debug("Memory add | kind=%s | content_len=%s", kind, len(content))
        self.items.append({"kind": kind, "content": content})

    def recent(self, n: int = 5) -> List[Dict[str, str]]:
        # Возвращаем последние N элементов.
        return self.items[-n:]

    def retrieve(self, query: str, k: int = 3) -> List[Dict[str, str]]:
        # Наивное ранжирование по пересечению слов.
        logger.info("Memory retrieve | query=%s | k=%s", query, k)
        q = set(query.lower().split())
        scored = []
        for item in self.items:
            tokens = set(item["content"].lower().split())
            score = len(q & tokens)
            scored.append((score, item))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for score, item in scored[:k] if score > 0]
