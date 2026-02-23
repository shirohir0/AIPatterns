from __future__ import annotations

from datetime import date
from typing import Callable, Dict, Tuple

from ..llm_stub import LLMStub
from common.logging_utils import get_logger

logger = get_logger(__name__)


def tool_calc(expr: str) -> str:
    # Мини-инструмент "калькулятор": только безопасные символы.
    allowed = "0123456789+-*/(). "
    cleaned = "".join(ch for ch in expr if ch in allowed)
    if not cleaned.strip():
        return "Нет выражения для вычисления."
    return str(eval(cleaned, {"__builtins__": {}}))


def tool_today(_: str) -> str:
    # Инструмент "сегодня": возвращает дату в ISO-формате.
    return date.today().isoformat()


def tool_kb(query: str) -> str:
    # Заглушка базы знаний (KB).
    kb = {
        "python": "Python — язык программирования общего назначения.",
        "agent": "Агент — система, которая воспринимает среду и действует для достижения целей.",
    }
    for key, value in kb.items():
        if key in query.lower():
            return value
    return "Запись в базе знаний не найдена."


def choose_tool(query: str) -> Tuple[str, str]:
    # Простейшая логика выбора инструмента.
    q = query.lower()
    if any(ch.isdigit() for ch in q):
        return "calc", query
    if "today" in q or "сегодня" in q:
        return "today", query
    return "kb", query


def tool_use_agent(llm: LLMStub, query: str) -> str:
    # Карта инструментов, доступных агенту.
    tools: Dict[str, Callable[[str], str]] = {
        "calc": tool_calc,
        "today": tool_today,
        "kb": tool_kb,
    }

    # Выбираем инструмент и выполняем его.
    tool_name, tool_input = choose_tool(query)
    logger.info("Tool use | tool=%s", tool_name)
    tool_output = tools[tool_name](tool_input)

    # Модель формирует итоговый ответ с учетом результата инструмента.
    return llm.complete(
        system="ОБЩИЙ",
        user=f"Пользователь спросил: {query}\nИнструмент: {tool_name}\nРезультат: {tool_output}\nОтвет:",
    )
