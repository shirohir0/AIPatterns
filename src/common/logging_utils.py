from __future__ import annotations

import logging
from typing import Optional


# Простая функция настройки логирования.
# Логирование лучше print, потому что:
# 1) можно менять уровень подробности
# 2) формат всегда одинаковый
# 3) легко писать в файл, если понадобится


def configure_logging(level: str = "INFO") -> None:
    """
    Настраивает базовое логирование.

    level: строка уровня ("DEBUG", "INFO", "WARNING", "ERROR")
    """

    logging.basicConfig(
        level=level.upper(),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Возвращает логгер для модуля.

    name обычно = __name__ — так понятно, откуда пришло сообщение.
    """

    return logging.getLogger(name)
