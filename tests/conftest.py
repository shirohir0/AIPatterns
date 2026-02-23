import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def pytest_addoption(parser):
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="Run integration tests that call real APIs",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "integration: tests that call real APIs")


def pytest_collection_modifyitems(config, items):
    run_integration = config.getoption("--run-integration")
    has_key = bool(os.getenv("DEEPSEEK_API_KEY"))

    if run_integration and has_key:
        return

    reason = "Set DEEPSEEK_API_KEY and use --run-integration"
    skip_integration = pytest.mark.skipif(True, reason=reason)

    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)
