from __future__ import annotations

import re

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from llm import get_llm
from tools import run_tool_calling


def prompt_chaining(llm, task: str) -> None:
    print("\n== Prompt Chaining ==")
    draft_prompt = ChatPromptTemplate.from_messages(
        [("system", "Ты пишешь быстрый черновик."), ("human", "{task}")]
    )
    refine_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Ты редактор, улучшающий черновик."),
            ("human", "Задача: {task}"),
            ("assistant", "Черновик: {draft}"),
            ("human", "Улучшенная версия:"),
        ]
    )

    draft = (draft_prompt | llm | StrOutputParser()).invoke({"task": task})
    refined = (refine_prompt | llm | StrOutputParser()).invoke(
        {"task": task, "draft": draft}
    )

    print("Черновик:", draft)
    print("Улучшено:", refined)


def route_by_rules(query: str) -> str | None:
    text = query.lower()

    # Явные математические маркеры.
    if any(word in text for word in ("посчитай", "вычисли", "сколько будет", "calc")):
        return "math"
    if re.search(r"\d+\s*[\+\-\*/]\s*\d+", text):
        return "math"

    # Явные запросы на инструменты (дата, мини-БЗ).
    if any(word in text for word in ("сегодня", "дата", "какой день", "agent", "python")):
        return "tools"

    return None


def resolve_route(llm, query: str) -> str:
    rule_route = route_by_rules(query)
    if rule_route:
        print("Маршрут rules:", rule_route)
        return rule_route

    router_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "Ты роутер. Выбери только один маршрут: math | tools | general.\n"
                    "Критерии:\n"
                    "- math: вычисления, арифметика, формулы;\n"
                    "- tools: дата/время или вопрос к мини-базе знаний;\n"
                    "- general: всё остальное.\n"
                    "Верни ровно одно слово без пояснений."
                ),
            ),
            ("human", "Запрос: {query}"),
        ]
    )

    route = (router_prompt | llm | StrOutputParser()).invoke({"query": query})
    route = route.strip().lower().split()[0] if route.strip() else "general"
    if route not in {"math", "tools", "general"}:
        print(f"Маршрут LLM невалиден: {route!r} -> fallback в general")
        return "general"

    print("Маршрут LLM:", route)
    return route


def routing(llm, query: str) -> None:
    print("\n== Routing ==")
    route = resolve_route(llm, query)

    if route == "math":
        print("Маршрут math -> используем tool-calling (calc)")
        result = run_tool_calling(llm, query)
        print("Ответ:", result)
    elif route == "tools":
        print("Маршрут tools -> tool-calling")
        result = run_tool_calling(llm, query)
        print("Ответ:", result)
    else:
        print("Маршрут general -> обычный ответ LLM")
        result = llm.invoke(query)
        print("Ответ:", result.content if hasattr(result, "content") else result)


def planning(llm, goal: str) -> None:
    print("\n== Planning ==")
    plan_prompt = ChatPromptTemplate.from_messages(
        [("system", "Составь план из 3 шагов."), ("human", "Цель: {goal}")]
    )
    plan = (plan_prompt | llm | StrOutputParser()).invoke({"goal": goal})
    print("План:")
    print(plan)

    steps = [line.strip() for line in plan.splitlines() if line.strip()]
    print("\nИсполнение (заглушка):")
    for step in steps:
        print("- Выполнено:", step)


def tool_use(llm, query: str) -> None:
    print("\n== Tool Use ==")
    result = run_tool_calling(llm, query)
    print("Итоговый ответ:", result)


def main() -> None:
    llm = get_llm()

    # prompt_chaining(llm, "Объясни, что такое AI-агент, в одном абзаце.")
    routing(llm, "Посчитай 2 + 2 * 5")
    # tool_use(llm, "Что сегодня за дата?")
    # planning(llm, "Сделать маленькое демо агента")


if __name__ == "__main__":
    main()
