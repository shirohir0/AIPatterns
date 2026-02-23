from __future__ import annotations

from typing import Dict
from ..llm_stub import LLMStub
from common.logging_utils import get_logger

logger = get_logger(__name__)


def prompt_chaining(llm: LLMStub, task: str) -> Dict[str, str]:
    """Двухшаговая цепочка: черновик -> улучшение."""

    logger.info("Prompt chaining | task_len=%s", len(task))
    # Шаг 1: модель быстро формирует черновик без лишней точности.
    draft = llm.complete(system="ЧЕРНОВИК", user=task)
    # Шаг 2: тот же запрос, но с контекстом черновика для улучшения.
    refined = llm.complete(system="РЕДАКТОР", user=task, context=draft)

    return {
        "draft": draft,
        "refined": refined,
    }
