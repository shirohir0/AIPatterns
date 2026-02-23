from __future__ import annotations

from typing import List, Tuple

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from common.logging_utils import get_logger

logger = get_logger(__name__)


def plan_and_execute(llm: ChatOpenAI, goal: str) -> Tuple[str, List[str]]:
    """Планирование и выполнение (LangChain)."""

    logger.info("LC planning | goal_len=%s", len(goal))
    plan_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Составь короткий план из 3-4 шагов."),
            ("human", "Цель: {goal}"),
        ]
    )
    plan_chain = plan_prompt | llm | StrOutputParser()
    plan = plan_chain.invoke({"goal": goal})

    steps = [line.strip() for line in plan.splitlines() if line.strip()]

    results: List[str] = []
    for step in steps:
        results.append(_execute_step(step))

    summary_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Подведи итог, учитывая план и результаты."),
            ("human", "Цель: {goal}\nПлан: {plan}\nРезультаты: {results}"),
        ]
    )
    summary_chain = summary_prompt | llm | StrOutputParser()
    summary = summary_chain.invoke({"goal": goal, "plan": plan, "results": results})

    return summary, results


def _execute_step(step: str) -> str:
    # Учебная заглушка для исполнения шага.
    return f"Сделано: {step}"
