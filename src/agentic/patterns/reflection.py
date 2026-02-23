from __future__ import annotations

from typing import Tuple

from ..llm_stub import LLMStub
from common.logging_utils import get_logger

logger = get_logger(__name__)


def reflect_and_improve(llm: LLMStub, question: str, answer: str) -> Tuple[str, str]:
    logger.info("Reflection | question_len=%s | answer_len=%s", len(question), len(answer))
    # Шаг 1: критик ищет проблемы в текущем ответе.
    critique = llm.complete(system="КРИТИК", user=answer)
    # Шаг 2: улучшитель переписывает ответ с учетом критики.
    improved = llm.complete(system="УЛУЧШИТЕЛЬ", user=answer, context=critique)
    return critique, improved
