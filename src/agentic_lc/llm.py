from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from common.logging_utils import get_logger

logger = get_logger(__name__)


def get_llm(
    model: str = "deepseek-chat",
    temperature: float = 0.2,
    base_url: str = "https://api.deepseek.com",
    api_key: Optional[str] = None,
) -> ChatOpenAI:
    """
    Создает LLM-клиент LangChain для DeepSeek (OpenAI-compatible API).

    Ключ берется из аргумента или из переменной окружения DEEPSEEK_API_KEY.
    """

    load_dotenv()
    key = api_key or os.getenv("DEEPSEEK_API_KEY")
    if not key:
        raise RuntimeError("DEEPSEEK_API_KEY is not set.")

    logger.info("LangChain LLM | model=%s | base_url=%s", model, base_url)
    return ChatOpenAI(
        api_key=key,
        base_url=base_url,
        model=model,
        temperature=temperature,
    )
