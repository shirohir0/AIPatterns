from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from common.logging_utils import get_logger

logger = get_logger(__name__)

@dataclass
class LLMStub:
    """
    Очень простая заглушка для имитации LLM.

    Намеренно упрощено: помогает увидеть управление
    потоками паттернов без внешних API.
    """

    name: str = "llm-stub"

    def complete(self, system: str, user: str, context: Optional[str] = None) -> str:
        # "system" имитирует системное сообщение (роль/задача модели),
        # "user" — запрос пользователя, "context" — предыдущий вывод.
        sys = system.lower()
        text = user.strip()
        ctx = (context or "").strip()

        logger.debug("LLMStub.complete called | system=%s | user_len=%s", system, len(text))

        # Маршрутизация по "роли" системы: так же делают реальные агенты,
        # подбирая специализированные подсистемы/цепочки под задачу.
        if "router" in sys or "маршрутиз" in sys:
            return self._route(text)
        if "planner" in sys or "план" in sys:
            return self._plan(text)
        if "drafter" in sys or "черновик" in sys:
            return f"Черновик: {self._short_answer(text)}"
        if "refiner" in sys or "редактор" in sys:
            return f"Улучшено: {self._refine(ctx or text)}"
        if "critic" in sys or "критик" in sys:
            return self._critique(text)
        if "reviser" in sys or "улучш" in sys:
            return self._revise(text, ctx)

        # Базовый режим: просто вернуть короткий "ответ".
        return self._short_answer(text)

    def _route(self, text: str) -> str:
        lower = text.lower()
        # Простейшая эвристика: цифры или "посчитай" -> math.
        if any(ch.isdigit() for ch in lower) or "calculate" in lower or "сколько" in lower or "посчитай" in lower:
            return "math"
        # Слова "план" или "шаг" -> planning.
        if any(k in lower for k in ["plan", "steps", "план", "шаг"]):
            return "planning"
        # Намек на код/пример -> code.
        if any(k in lower for k in ["code", "snippet", "пример", "код"]):
            return "code"
        # Иначе общий режим.
        return "general"

    def _plan(self, text: str) -> str:
        # В реальном агенте здесь бы происходило:
        # 1) анализ цели, 2) разбиение на шаги, 3) проверка ограничений.
        return (
            "1. Уточнить цель и ограничения.\n"
            "2. Разбить на 3-4 конкретных шага.\n"
            "3. Выполнить шаги и собрать результаты.\n"
            "4. Свести итог и предложить следующие действия."
        )

    def _critique(self, text: str) -> str:
        # "Критик" имитирует внутреннюю проверку качества ответа.
        return (
            "- Не хватает конкретного примера.\n"
            "- Стоит точнее обозначить входы/выходы.\n"
            "- Добавь короткий пошаговый план."
        )

    def _revise(self, text: str, critique: str) -> str:
        # "Улучшитель" учитывает критику и переписывает ответ.
        return (
            "Улучшенный ответ с примером и шагами. "
            "Входы/выходы уточнены. "
            f"(Критика учтена: {critique.strip()})"
        )

    def _short_answer(self, text: str) -> str:
        # Ограничиваем длину, чтобы имитировать короткий ответ модели.
        if len(text) > 120:
            text = text[:120].rstrip() + "..."
        return f"Ответ на: {text}"

    def _refine(self, text: str) -> str:
        # Упрощенная "правка" — удаляем маркер черновика.
        return (
            text.replace("Draft:", "")
            .replace("Черновик:", "")
            .strip()
            + " (очищено)"
        )
