from __future__ import annotations

from datetime import date
from typing import Dict, Tuple

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from common.logging_utils import get_logger

logger = get_logger(__name__)


@tool
def calc(expression: str) -> str:
    """Простой калькулятор: поддерживает +, -, *, /, (), числа."""

    allowed = "0123456789+-*/(). "
    cleaned = "".join(ch for ch in expression if ch in allowed)
    if not cleaned.strip():
        return "Нет выражения для вычисления."
    return str(eval(cleaned, {"__builtins__": {}}))


@tool
def today(_: str) -> str:
    """Возвращает сегодняшнюю дату в ISO-формате."""

    return date.today().isoformat()


@tool
def kb(query: str) -> str:
    """Мини-база знаний (учебная)."""

    data = {
        "python": "Python — язык программирования общего назначения.",
        "agent": "Агент — система, которая воспринимает среду и действует для достижения целей.",
    }
    for key, value in data.items():
        if key in query.lower():
            return value
    return "Запись в базе знаний не найдена."


def tool_use_agent(llm: ChatOpenAI, query: str) -> str:
    """
    Мини-агент с tool-calling (LangChain).

    1) LLM выбирает инструмент.
    2) Мы исполняем инструмент.
    3) LLM формирует итоговый ответ, видя результат инструмента.
    """

    tools = [calc, today, kb]
    tool_map = {t.name: t for t in tools}

    model = llm.bind_tools(tools)
    messages = [HumanMessage(content=query)]
    response = model.invoke(messages)

    if not getattr(response, "tool_calls", None):
        return response.content or ""

    tool_messages = []
    for call in response.tool_calls:
        tool_name = call["name"]
        tool_args = call.get("args", {})
        logger.info("LC tool call | tool=%s | args=%s", tool_name, tool_args)
        tool_result = tool_map[tool_name].invoke(tool_args)
        tool_messages.append(
            ToolMessage(content=str(tool_result), tool_call_id=call["id"])
        )

    final = model.invoke(messages + [response] + tool_messages)
    return final.content or ""
