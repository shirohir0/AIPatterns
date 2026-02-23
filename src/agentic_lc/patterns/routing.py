from __future__ import annotations

import ast
import operator as op
from typing import Callable, Dict, Tuple

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from common.logging_utils import get_logger

logger = get_logger(__name__)


_ALLOWED_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}


def _safe_eval(expr: str) -> float:
    expr = expr.strip()

    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
            return _ALLOWED_OPS[type(node.op)](_eval(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
            return _ALLOWED_OPS[type(node.op)](_eval(node.left), _eval(node.right))
        raise ValueError("Unsupported expression")

    parsed = ast.parse(expr, mode="eval")
    return _eval(parsed.body)


def _math_handler(query: str) -> str:
    # Извлекаем только безопасные символы.
    expr = "".join(ch for ch in query if ch in "0123456789+-*/(). ")
    expr = expr.strip()
    if not expr:
        return "Математическое выражение не найдено."
    return f"Результат: {_safe_eval(expr)}"


def _code_handler(_: str) -> str:
    return "Пример кода: def hello():\n    return 'hello'"


def _planning_handler(_: str) -> str:
    return "Используйте паттерн планирования для этого запроса."


def _general_handler(llm: ChatOpenAI, query: str) -> str:
    prompt = ChatPromptTemplate.from_messages(
        [("system", "Ты полезный помощник."), ("human", "{query}")]
    )
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"query": query})


def _normalize_route(raw: str, query: str) -> str:
    text = (raw or "").strip().lower()
    if text in {"math", "planning", "code", "general"}:
        return text
    if "math" in text or "матем" in text or any(ch.isdigit() for ch in query):
        return "math"
    if "plan" in text or "план" in text or "шаг" in text:
        return "planning"
    if "code" in text or "код" in text or "пример" in text:
        return "code"
    return "general"


def route_query(llm: ChatOpenAI, query: str) -> Tuple[str, str]:
    """LLM-роутинг (LangChain) с fallback-логикой."""

    logger.info("LC routing | query_len=%s", len(query))
    router_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Выбери только один маршрут: math | planning | code | general. "
                "Ответь одним словом из списка.",
            ),
            ("human", "Запрос: {query}"),
        ]
    )
    router_chain = router_prompt | llm | StrOutputParser()
    raw = router_chain.invoke({"query": query})
    route = _normalize_route(raw, query)
    logger.debug("LC routing decision | raw=%s | normalized=%s", raw, route)

    # Простая ветвизация без RunnableBranch для совместимости версий.
    if route == "math":
        response = _math_handler(query)
    elif route == "code":
        response = _code_handler(query)
    elif route == "planning":
        response = _planning_handler(query)
    else:
        response = _general_handler(llm, query)
    return route, response
