from __future__ import annotations

from typing import Dict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from common.logging_utils import get_logger

logger = get_logger(__name__)


def prompt_chaining(llm: ChatOpenAI, task: str) -> Dict[str, str]:
    """Двухшаговая цепочка: черновик -> улучшение (LangChain)."""

    logger.info("LC prompt chaining | task_len=%s", len(task))
    # Шаг 1: быстрый черновик.
    draft_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Ты пишешь быстрый черновик без идеальной формулировки."),
            ("human", "{task}"),
        ]
    )
    draft_chain = draft_prompt | llm | StrOutputParser()
    draft = draft_chain.invoke({"task": task})

    # Шаг 2: редактор улучшает с учетом черновика.
    refine_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Ты редактор, улучшающий черновик."),
            ("human", "Задача: {task}"),
            ("assistant", "Черновик: {draft}"),
            ("human", "Улучшенная версия:"),
        ]
    )
    refine_chain = refine_prompt | llm | StrOutputParser()
    refined = refine_chain.invoke({"task": task, "draft": draft})

    return {"draft": draft, "refined": refined}
