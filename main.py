import argparse
import sys
from pathlib import Path

# pylint: disable=import-outside-toplevel

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def main() -> None:
    from agentic_lc.demo import run_demo

    parser = argparse.ArgumentParser(description="Запуск учебных демо AI-агентов через LangChain")
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Уровень логирования (DEBUG, INFO, WARNING, ERROR)",
    )
    args = parser.parse_args()

    run_demo(log_level=args.log_level)


if __name__ == "__main__":
    main()
