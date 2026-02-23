from __future__ import annotations

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


def routing(llm, query: str) -> None:
    print("\n== Routing ==")
    router_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Выбери маршрут: math | tools | general. Ответь одним словом.",
            ),
            ("human", "Запрос: {query}"),
        ]
    )

    route = (router_prompt | llm | StrOutputParser()).invoke({"query": query})
    route = route.strip().lower()
    print("Маршрут LLM:", route)

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

    prompt_chaining(llm, "Объясни, что такое AI-агент, в одном абзаце.")
    routing(llm, "Посчитай 2 + 2 * 5")
    tool_use(llm, "Что сегодня за дата?")
    planning(llm, "Сделать маленькое демо агента")


if __name__ == "__main__":
    main()
