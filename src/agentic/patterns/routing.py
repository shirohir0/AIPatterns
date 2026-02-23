from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Tuple
import ast
import operator as op

from ..llm_stub import LLMStub
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
    # Извлекаем только допустимые символы, чтобы избежать инъекций.
    expr = "".join(ch for ch in query if ch in "0123456789+-*/(). ")
    expr = expr.strip()
    if not expr:
        return "Математическое выражение не найдено."
    return f"Результат: {_safe_eval(expr)}"


def _code_handler(query: str) -> str:
    # В учебной версии возвращаем фиксированный пример.
    return "Пример кода: def hello():\n    return 'hello'"


def _general_handler(llm: LLMStub, query: str) -> str:
    # Общий режим — просто отдаем запрос модели.
    return llm.complete(system="ОБЩИЙ", user=query)


def _normalize_route(raw: str, query: str) -> str:
    # Нормализуем ответ LLM: он может вернуть не строгое значение.
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


def route_query(llm: LLMStub, query: str) -> Tuple[str, str]:
    """Правило-ориентированный роутер -> обработчик -> ответ."""

    logger.info("Routing | query_len=%s", len(query))
    # Просим LLM выбрать одну из фиксированных меток.
    prompt = (
        "Выбери только один маршрут: math | planning | code | general. "
        "Ответь одним словом из списка."
    )
    raw_route = llm.complete(system="МАРШРУТИЗАТОР", user=f"{prompt}\nЗапрос: {query}")
    route = _normalize_route(raw_route, query)
    logger.debug("Routing decision | raw=%s | normalized=%s", raw_route, route)
    handlers: Dict[str, Callable[[str], str]] = {
        "math": _math_handler,
        "code": _code_handler,
        "planning": lambda q: "Используйте паттерн планирования для этого запроса.",
        "general": lambda q: _general_handler(llm, q),
    }
    # Дефолт на случай непредвиденного ответа.
    handler = handlers.get(route, handlers["general"])
    return route, handler(query)
