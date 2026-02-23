from __future__ import annotations

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


def get_llm() -> ChatOpenAI:
    load_dotenv()
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        raise RuntimeError("DEEPSEEK_API_KEY не найден. Добавь его в .env")

    return ChatOpenAI(
        api_key=key,
        base_url="https://api.deepseek.com",
        model="deepseek-chat",
        temperature=0.2,
    )
