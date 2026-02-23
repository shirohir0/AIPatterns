import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from common.logging_utils import configure_logging, get_logger
from agentic.memory import SimpleMemory
from agentic_lc import get_llm
from agentic_lc.patterns import (
    prompt_chaining,
    route_query,
    tool_use_agent,
    plan_and_execute,
    reflect_and_improve,
    memory_demo,
)

logger = get_logger(__name__)


def main() -> None:
    # Включаем логирование, чтобы видеть ход работы паттернов.
    configure_logging("INFO")

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    llm = get_llm()

    logger.info("== LangChain: Цепочка промптов ==")
    chain = prompt_chaining(llm, "Объясни, что такое AI-агент, в одном абзаце.")
    logger.info("Черновик: %s", chain["draft"])
    logger.info("Улучшено: %s", chain["refined"])

    logger.info("== LangChain: Маршрутизация ==")
    route, response = route_query(llm, "Посчитай 2 + 2 * 5")
    logger.info("Маршрут: %s", route)
    logger.info("Ответ: %s", response)

    logger.info("== LangChain: Использование инструментов ==")
    answer = tool_use_agent(llm, "Что такое Python?")
    logger.info("Ответ: %s", answer)

    logger.info("== LangChain: Планирование ==")
    summary, results = plan_and_execute(llm, "Сделать маленькое демо агента")
    logger.info("Результаты: %s", results)
    logger.info("Итог: %s", summary)

    logger.info("== LangChain: Рефлексия ==")
    critique, improved = reflect_and_improve(
        llm,
        "Объясни цепочку промптов",
        "Цепочка промптов — это использование нескольких промптов для решения задачи.",
    )
    logger.info("Критика: %s", critique)
    logger.info("Улучшено: %s", improved)

    logger.info("== LangChain: Память ==")
    mem = SimpleMemory()
    mem.add("fact", "Агенты могут использовать инструменты для действий в мире.")
    mem.add("fact", "Память помогает сохранять контекст во времени.")
    mem.add("note", "Маршрутизация выбирает специализированные обработчики.")
    hits = memory_demo(mem, "инструменты и память")
    logger.info("Найдено: %s", hits)


if __name__ == "__main__":
    main()
