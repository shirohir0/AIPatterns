from __future__ import annotations

from typing import Tuple

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from common.logging_utils import get_logger

logger = get_logger(__name__)


def reflect_and_improve(llm: ChatOpenAI, question: str, answer: str) -> Tuple[str, str]:
    """Критика -> улучшение (LangChain)."""

    logger.info("LC reflection | question_len=%s | answer_len=%s", len(question), len(answer))
    critic_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Ты критик. Найди слабые места ответа."),
            ("human", "Ответ: {answer}"),
        ]
    )
    critic_chain = critic_prompt | llm | StrOutputParser()
    critique = critic_chain.invoke({"answer": answer})

    revise_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Ты улучшитель. Учитывай критику."),
            ("human", "Вопрос: {question}"),
            ("assistant", "Исходный ответ: {answer}"),
            ("assistant", "Критика: {critique}"),
            ("human", "Улучшенный ответ:"),
        ]
    )
    revise_chain = revise_prompt | llm | StrOutputParser()
    improved = revise_chain.invoke({"question": question, "answer": answer, "critique": critique})

    return critique, improved
