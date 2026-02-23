from __future__ import annotations

from typing import List, Tuple

from ..llm_stub import LLMStub
from common.logging_utils import get_logger

logger = get_logger(__name__)


def plan_and_execute(llm: LLMStub, goal: str) -> Tuple[str, List[str]]:
    """Простое планирование и выполнение со заглушками действий."""

    logger.info("Planning | goal_len=%s", len(goal))
    # Планируем шаги (в реальности сюда можно добавить ограничения/ресурсы).
    plan = llm.complete(system="ПЛАНИРОВЩИК", user=goal)
    # Разбиваем ответ на шаги.
    steps = [line.strip() for line in plan.splitlines() if line.strip()]

    results: List[str] = []
    for step in steps:
        # Исполняем шаги по очереди (в учебной версии это заглушка).
        results.append(_execute_step(step))

    # Итог формируется моделью на основе плана и результатов.
    summary = llm.complete(
        system="ОБЩИЙ",
        user=f"Цель: {goal}\nПлан: {plan}\nРезультаты: {results}\nИтог:",
    )
    return summary, results


def _execute_step(step: str) -> str:
    # Учебная заглушка: превращает шаг в фиктивный результат.
    return f"Сделано: {step}"
