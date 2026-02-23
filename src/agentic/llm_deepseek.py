from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI
from dotenv import load_dotenv
from common.logging_utils import get_logger

logger = get_logger(__name__)


@dataclass
class DeepSeekLLM:
    """DeepSeek API client wrapper compatible with the demo patterns."""

    api_key: Optional[str] = None
    model: str = "deepseek-chat"
    base_url: str = "https://api.deepseek.com"

    def _client(self) -> OpenAI:
        # Загружаем переменные окружения из .env, чтобы не хранить ключи в коде.
        load_dotenv()
        key = self.api_key or os.getenv("DEEPSEEK_API_KEY")
        if not key:
            raise RuntimeError("DEEPSEEK_API_KEY is not set.")
        # Используем OpenAI SDK с base_url DeepSeek — это официальный совместимый способ.
        logger.debug("Создаем клиента DeepSeek (model=%s, base_url=%s)", self.model, self.base_url)
        return OpenAI(api_key=key, base_url=self.base_url)

    def complete(self, system: str, user: str, context: Optional[str] = None) -> str:
        # В сообщениях соблюдаем роли (system/assistant/user).
        # context в этом проекте — предыдущий вывод (например, черновик или критика).
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        if context:
            messages.append({"role": "assistant", "content": context})
        messages.append({"role": "user", "content": user})

        client = self._client()
        # Минимальные параметры: модель и температура.
        logger.info("LLM запрос | model=%s | system=%s | user_len=%s", self.model, system, len(user))
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
        )
        # В реальном проекте стоит добавить обработку ошибок и логирование.
        return response.choices[0].message.content or ""
