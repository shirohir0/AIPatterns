from __future__ import annotations

import ast
import operator as op
from datetime import date

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool


# --- Инструменты ---


@tool
def calc(expression: str) -> str:
    """Калькулятор: +, -, *, /, (), числа."""
    expr = "".join(ch for ch in expression if ch in "0123456789+-*/(). ").strip()
    if not expr:
        return "Пустое выражение"
    return str(_safe_eval(expr))


@tool
def today() -> str:
    """Сегодняшняя дата."""
    return date.today().isoformat()


@tool
def kb(query: str) -> str:
    """Мини-база знаний."""
    data = {
        "agent": "Агент — система, которая действует для достижения цели.",
        "python": "Python — язык программирования общего назначения.",
    }
    for key, value in data.items():
        if key in query.lower():
            return value
    return "Нет ответа в базе знаний."


# --- Безопасный вычислитель ---


_ALLOWED_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}


def _safe_eval(expr: str) -> float:
    def _eval(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
            return _ALLOWED_OPS[type(node.op)](_eval(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
            return _ALLOWED_OPS[type(node.op)](_eval(node.left), _eval(node.right))
        raise ValueError("Неподдерживаемое выражение")

    parsed = ast.parse(expr, mode="eval")
    return _eval(parsed.body)


# --- Tool-calling helper ---


def run_tool_calling(llm, user_query: str) -> str:
    tools = [calc, today, kb]
    tool_map = {t.name: t for t in tools}

    model = llm.bind_tools(tools)
    messages = [HumanMessage(content=user_query)]

    print("LLM: решаю, нужен ли инструмент...")
    response = model.invoke(messages)

    if not getattr(response, "tool_calls", None):
        print("LLM: инструмент не нужен")
        return response.content or ""

    tool_messages = []
    for call in response.tool_calls:
        tool_name = call["name"]
        tool_args = call.get("args", {})
        print(f"LLM выбрал инструмент: {tool_name} | args={tool_args}")
        tool_result = tool_map[tool_name].invoke(tool_args)
        print(f"Результат инструмента: {tool_result}")
        tool_messages.append(
            ToolMessage(content=str(tool_result), tool_call_id=call["id"])
        )

    final = model.invoke(messages + [response] + tool_messages)
    return final.content or ""
